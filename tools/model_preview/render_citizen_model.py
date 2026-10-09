#!/usr/bin/env python3
"""
Tiny software renderer for MineColonies citizen models (Blockbench Java exports).

It parses the ``createMesh()`` method of a model class (the
``PartDefinition x = parent.addOrReplaceChild("name", CubeListBuilder..., PartPose...)``
statements), rebuilds the part hierarchy and renders textured orthographic views
of the model, using the same cube/UV conventions as ``net.minecraft.client.model.geom.ModelPart.Cube``:

* box UV layout  : [top][bottom] on the first row, [right(-X)][front(-Z)][left(+X)][back(+Z)] below
* CubeDeformation: inflates the box by ``g`` on every side
* mirror()       : swaps the X extents (mirrors every face horizontally)
* PartPose       : translate(pivot) then rotate Z, Y, X (JOML ``rotationZYX``)

No OpenGL / Minecraft needed – only Pillow and numpy.

Example::

    python3 tools/model_preview/render_citizen_model.py \
        --java src/main/java/com/minecolonies/core/client/model/FemaleBuilderModel.java \
        --texture src/main/resources/assets/minecolonies/textures/entity/citizen/default/builderfemale1_a.png \
        --out /tmp/builder_female.png --views front,back,left,right,iso

    # idle citizen (work gear hidden):
    python3 tools/model_preview/render_citizen_model.py ... --hide toolbag,HardHat
"""
from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

# ----------------------------------------------------------------------------
# Parsing
# ----------------------------------------------------------------------------

NUM = r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?[fFdD]?"


def _f(s: str) -> float:
    return float(s.rstrip("fFdD"))


@dataclass
class Cube:
    u: int
    v: int
    x: float
    y: float
    z: float
    w: float
    h: float
    d: float
    g: float          # growX (kept for display)
    mirror: bool
    gy: float = None  # growY / growZ when a 3-axis CubeDeformation is used
    gz: float = None

    def grow(self):
        return self.g, (self.g if self.gy is None else self.gy), (self.g if self.gz is None else self.gz)


@dataclass
class Part:
    name: str
    var: str
    parent_var: Optional[str]
    pivot: Tuple[float, float, float]
    rot: Tuple[float, float, float]
    cubes: List[Cube] = field(default_factory=list)
    children: List["Part"] = field(default_factory=list)


class Model:
    def __init__(self, root_parts: List[Part], tex_w: int, tex_h: int, by_name: Dict[str, Part]):
        self.roots = root_parts
        self.tex_w = tex_w
        self.tex_h = tex_h
        self.by_name = by_name


def _strip_comments(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"//[^\n]*", "", src)
    return src


def parse_cube_list(s: str) -> List[Cube]:
    """Parse ``CubeListBuilder.create().texOffs(..).mirror().addBox(..)...``."""
    cubes: List[Cube] = []
    u = v = 0
    mirror = False
    # tokens: .texOffs(a,b) | .mirror() | .mirror(bool) | .addBox(...)
    token_re = re.compile(r"\.(texOffs|mirror|addBox)\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
    for m in token_re.finditer(s):
        kind, args = m.group(1), m.group(2)
        if kind == "texOffs":
            a, b = [int(_f(t)) for t in re.findall(NUM, args)]
            u, v = a, b
        elif kind == "mirror":
            mirror = "false" not in args
        else:  # addBox
            nums = [_f(t) for t in re.findall(NUM, args)]
            x, y, z, w, h, d = nums[:6]
            g, gy, gz = 0.0, None, None
            gm = re.search(r"CubeDeformation\(([^()]*)\)", args)
            if gm:
                gs = [_f(t) for t in re.findall(NUM, gm.group(1))]
                if len(gs) >= 3:
                    g, gy, gz = gs[0], gs[1], gs[2]
                elif gs:
                    g = gs[0]
            cubes.append(Cube(u, v, x, y, z, w, h, d, g, mirror, gy, gz))
    return cubes


def parse_pose(s: str) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    nums = [_f(t) for t in re.findall(NUM, s)]
    if "offsetAndRotation" in s:
        return (nums[0], nums[1], nums[2]), (nums[3], nums[4], nums[5])
    if "PartPose.offset" in s:
        return (nums[0], nums[1], nums[2]), (0.0, 0.0, 0.0)
    if "PartPose.rotation" in s:
        return (0.0, 0.0, 0.0), (nums[0], nums[1], nums[2])
    return (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)


def _resolve_constants(src: str, body: str, extra_sources: Tuple[str, ...] = ()) -> str:
    """Inline ``static final`` String / numeric / CubeDeformation constants used inside createMesh().

    Constants may come from the model class itself or from ``extra_sources`` (e.g. the
    ``CitizenModel`` base class). ``NAME.extend(g)`` on a known CubeDeformation constant is evaluated.
    """
    consts = {}
    for text in extra_sources + (src,):
        for cm in re.finditer(r"static\s+final\s+(String|float|double|int|CubeDeformation)\s+(\w+)\s*=\s*([^;]+);", text):
            typ, name, value = cm.groups()
            value = " ".join(value.split())
            if typ == "String":
                if not re.fullmatch(r"\"[^\"]*\"", value):
                    continue
            elif typ == "CubeDeformation":
                em = re.fullmatch(r"(\w+)\.extend\(\s*(" + NUM + r")\s*\)", value)
                if em and em.group(1) in consts:
                    base = [_f(t) for t in re.findall(NUM, consts[em.group(1)])]
                    if len(base) == 1:
                        base = base * 3
                    e = _f(em.group(2))
                    value = "new CubeDeformation(%sF, %sF, %sF)" % (base[0] + e, base[1] + e, base[2] + e)
                elif not re.fullmatch(r"new\s+CubeDeformation\([^()]*\)", value):
                    continue
            elif not re.fullmatch(NUM, value):
                continue
            consts[name] = value
    for name, value in consts.items():
        body = re.sub(r"(?<![\w.])" + re.escape(name) + r"\b", value, body)
        body = re.sub(r"\bCitizenModel\." + re.escape(name) + r"\b", value, body)
    return body


def parse_model(java_path: str, constants_from: Tuple[str, ...] = ()) -> Model:
    src = _strip_comments(open(java_path, encoding="utf-8").read())
    extra = tuple(_strip_comments(open(f, encoding="utf-8").read()) for f in constants_from)
    m = re.search(r"createMesh\s*\([^)]*\)\s*\{(.*?)return\s+LayerDefinition\.create\(\s*\w+\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", src, re.S)
    if not m:
        sys.exit("createMesh() not found in " + java_path)
    body, tex_w, tex_h = m.group(1), int(m.group(2)), int(m.group(3))
    body = " ".join(body.split())
    body = _resolve_constants(src, body, extra)
    root_var = None
    rm = re.search(r"PartDefinition\s+(\w+)\s*=\s*\w+\.getRoot\(\)", body)
    if rm:
        root_var = rm.group(1)
    parts: Dict[str, Part] = {}
    order: List[Part] = []
    stmt_re = re.compile(
        r"PartDefinition\s+(\w+)\s*=\s*(\w+)\.addOrReplaceChild\(\s*\"([^\"]+)\"\s*,\s*(CubeListBuilder\.create\(\).*?)\s*,\s*(PartPose\.\w+(?:\([^;]*?\))?)\s*\)\s*;"
    )
    for sm in stmt_re.finditer(body):
        var, parent_var, name, cubes_s, pose_s = sm.groups()
        pivot, rot = parse_pose(pose_s)
        p = Part(name=name, var=var, parent_var=parent_var, pivot=pivot, rot=rot, cubes=parse_cube_list(cubes_s))
        parts[var] = p
        order.append(p)
    roots: List[Part] = []
    for p in order:
        if p.parent_var in parts:
            parts[p.parent_var].children.append(p)
        elif p.parent_var == root_var or root_var is None:
            roots.append(p)  # child of the mesh root
        else:
            print(f"WARNING: part '{p.name}' has unknown parent variable '{p.parent_var}', attached to the root", file=sys.stderr)
            roots.append(p)
    by_name = {p.name: p for p in order}
    return Model(roots, tex_w, tex_h, by_name)


# ----------------------------------------------------------------------------
# Geometry
# ----------------------------------------------------------------------------

def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float)


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float)


def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def part_matrix(p: Part, zero_rot: bool) -> np.ndarray:
    """4x4 local matrix: translate(pivot) * Rz * Ry * Rx (Minecraft ``translateAndRotate``)."""
    rx, ry, rz = (0.0, 0.0, 0.0) if zero_rot else p.rot
    r = rot_z(rz) @ rot_y(ry) @ rot_x(rx)
    m = np.eye(4)
    m[:3, :3] = r
    m[:3, 3] = p.pivot
    return m


# Faces, in the same order/vertex convention as ModelPart.Cube
#   vertex7=(x0,y0,z0) vertex=(x1,y0,z0) vertex1=(x1,y1,z0) vertex2=(x0,y1,z0)
#   vertex3=(x0,y0,z1) vertex4=(x1,y0,z1) vertex5=(x1,y1,z1) vertex6=(x0,y1,z1)
def cube_quads(c: Cube):
    gx, gy, gz = c.grow()
    x0, x1 = c.x - gx, c.x + c.w + gx
    if c.mirror:
        x0, x1 = x1, x0
    y0, y1 = c.y - gy, c.y + c.h + gy
    z0, z1 = c.z - gz, c.z + c.d + gz
    v7 = (x0, y0, z0); v_ = (x1, y0, z0); v1 = (x1, y1, z0); v2 = (x0, y1, z0)
    v3 = (x0, y0, z1); v4 = (x1, y0, z1); v5 = (x1, y1, z1); v6 = (x0, y1, z1)
    u, v, w, h, d = c.u, c.v, c.w, c.h, c.d
    f4, f5, f6, f7, f8, f9 = u, u + d, u + d + w, u + d + w + w, u + d + w + d, u + d + w + d + w
    f10, f11, f12 = v, v + d, v + d + h
    quads = [
        # (vertices, u1, v1, u2, v2, label)
        ([v4, v3, v7, v_], f5, f10, f6, f11, "top"),      # DOWN polygon (model -Y) = top in world
        ([v1, v2, v6, v5], f6, f11, f7, f10, "bottom"),   # UP polygon   (model +Y) = bottom in world
        ([v7, v3, v6, v2], f4, f11, f5, f12, "right"),    # WEST  (-X) = character's right
        ([v_, v7, v2, v1], f5, f11, f6, f12, "front"),    # NORTH (-Z) = face
        ([v4, v_, v1, v5], f6, f11, f8, f12, "left"),     # EAST  (+X)
        ([v3, v4, v5, v6], f8, f11, f9, f12, "back"),     # SOUTH (+Z)
    ]
    out = []
    for verts, u1, v1_, u2, v2_, label in quads:
        uvs = [(u2, v1_), (u1, v1_), (u1, v2_), (u2, v2_)]  # Polygon(...) remap order
        out.append((np.array(verts, dtype=float), np.array(uvs, dtype=float), label))
    return out


def collect_triangles(model: Model, hidden: set, zero_rot_parts: set):
    """Return list of (xyz[3,3] in model space, uv[3,2], part_name, face_label)."""
    tris = []

    def walk(p: Part, parent_m: np.ndarray):
        if p.name in hidden:
            return
        m = parent_m @ part_matrix(p, p.name in zero_rot_parts)
        for c in p.cubes:
            for verts, uvs, label in cube_quads(c):
                hv = np.c_[verts, np.ones(4)] @ m.T
                w = hv[:, :3]
                tris.append((w[[0, 1, 2]], uvs[[0, 1, 2]], p.name, label))
                tris.append((w[[0, 2, 3]], uvs[[0, 2, 3]], p.name, label))
        for ch in p.children:
            walk(ch, m)

    for r in model.roots:
        walk(r, np.eye(4))
    return tris


# ----------------------------------------------------------------------------
# Rasterisation
# ----------------------------------------------------------------------------

def model_to_world(xyz: np.ndarray) -> np.ndarray:
    """Model space (Y down, face toward -Z) -> world (Y up, face toward +Z) as the entity renderer does."""
    return np.c_[xyz[:, 0], -xyz[:, 1], -xyz[:, 2]]


def camera_basis(yaw_deg: float, pitch_deg: float):
    """Camera orbiting the model. yaw=0 looks at the face (from +Z), pitch>0 looks from above."""
    yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
    # camera position direction (unit vector from origin to camera)
    cx = math.sin(yaw) * math.cos(pitch)
    cy = math.sin(pitch)
    cz = math.cos(yaw) * math.cos(pitch)
    cam = np.array([cx, cy, cz])
    fwd = -cam
    up0 = np.array([0.0, 1.0, 0.0])
    right = np.cross(fwd, up0)
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return right, up, fwd


VIEWS = {
    "front": (0, 0),
    "back": (180, 0),
    "left": (90, 0),    # looks at the character's left side
    "right": (-90, 0),  # looks at the character's right side
    "iso": (35, 22),
    "iso_back": (215, 22),
    "top": (0, 89),
}


def render_view(tris, tex: np.ndarray, yaw: float, pitch: float, scale: float, pad: int = 6,
                light_dir=(0.35, 0.8, 0.5)) -> Image.Image:
    right, up, fwd = camera_basis(yaw, pitch)
    L = np.array(light_dir, dtype=float)
    L /= np.linalg.norm(L)
    # project everything first to find bounds
    proj = []
    for xyz, uv, pname, label in tris:
        w = model_to_world(xyz)
        sx = w @ right
        sy = w @ up
        depth = -(w @ fwd)  # larger = closer to camera
        n = np.cross(w[1] - w[0], w[2] - w[0])
        nn = np.linalg.norm(n)
        shade = 1.0
        if nn > 1e-9:
            n /= nn
            shade = 0.55 + 0.45 * abs(float(n @ L))  # two-sided (no-cull render type)
        proj.append((sx, sy, depth, uv, shade))
    all_x = np.concatenate([p[0] for p in proj])
    all_y = np.concatenate([p[1] for p in proj])
    minx, maxx, miny, maxy = all_x.min(), all_x.max(), all_y.min(), all_y.max()
    W = int(math.ceil((maxx - minx) * scale)) + 2 * pad
    H = int(math.ceil((maxy - miny) * scale)) + 2 * pad
    color = np.zeros((H, W, 4), dtype=np.uint8)
    zbuf = np.full((H, W), -1e9, dtype=float)
    th, tw = tex.shape[0], tex.shape[1]

    for sx, sy, depth, uv, shade in proj:
        px = (sx - minx) * scale + pad
        py = (maxy - sy) * scale + pad
        x0, x1 = int(math.floor(px.min())), int(math.ceil(px.max()))
        y0, y1 = int(math.floor(py.min())), int(math.ceil(py.max()))
        if x1 <= x0 or y1 <= y0:
            continue
        xs = np.arange(x0, x1) + 0.5
        ys = np.arange(y0, y1) + 0.5
        gx, gy = np.meshgrid(xs, ys)
        (xa, ya), (xb, yb), (xc, yc) = (px[0], py[0]), (px[1], py[1]), (px[2], py[2])
        det = (yb - yc) * (xa - xc) + (xc - xb) * (ya - yc)
        if abs(det) < 1e-9:
            continue
        l0 = ((yb - yc) * (gx - xc) + (xc - xb) * (gy - yc)) / det
        l1 = ((yc - ya) * (gx - xc) + (xa - xc) * (gy - yc)) / det
        l2 = 1.0 - l0 - l1
        eps = -1e-6
        inside = (l0 >= eps) & (l1 >= eps) & (l2 >= eps)
        if not inside.any():
            continue
        z = l0 * depth[0] + l1 * depth[1] + l2 * depth[2]
        u = l0 * uv[0, 0] + l1 * uv[1, 0] + l2 * uv[2, 0]
        v = l0 * uv[0, 1] + l1 * uv[1, 1] + l2 * uv[2, 1]
        umin, umax = uv[:, 0].min(), uv[:, 0].max()
        vmin, vmax = uv[:, 1].min(), uv[:, 1].max()
        ui = np.clip(np.floor(np.clip(u, umin, umax - 1e-3)), 0, tw - 1).astype(int)
        vi = np.clip(np.floor(np.clip(v, vmin, vmax - 1e-3)), 0, th - 1).astype(int)
        texel = tex[vi, ui]
        opaque = texel[..., 3] > 25  # cutout
        sub_z = zbuf[y0:y1, x0:x1]
        write = inside & opaque & (z > sub_z)
        if not write.any():
            continue
        rgb = (texel[..., :3].astype(float) * shade).clip(0, 255).astype(np.uint8)
        sub_c = color[y0:y1, x0:x1]
        sub_c[write, :3] = rgb[write]
        sub_c[write, 3] = 255
        sub_z[write] = z[write]
    return Image.fromarray(color, "RGBA")


def render(model: Model, tex_path: str, views: List[str], hidden: set, scale: float,
           zero_rot_parts: set, bg=(70, 70, 70, 255), gap: int = 16) -> Image.Image:
    tex_img = Image.open(tex_path).convert("RGBA")
    if tex_img.size != (model.tex_w, model.tex_h):
        print(f"WARNING: texture is {tex_img.size}, model expects {(model.tex_w, model.tex_h)}", file=sys.stderr)
    tex = np.array(tex_img)
    tris = collect_triangles(model, hidden, zero_rot_parts)
    imgs = []
    for vname in views:
        yaw, pitch = VIEWS[vname] if vname in VIEWS else tuple(float(t) for t in vname.split(":"))
        imgs.append(render_view(tris, tex, yaw, pitch, scale))
    W = sum(i.width for i in imgs) + gap * (len(imgs) + 1)
    H = max(i.height for i in imgs) + 2 * gap
    out = Image.new("RGBA", (W, H), bg)
    x = gap
    for im in imgs:
        out.alpha_composite(im, (x, H - gap - im.height))
        x += im.width + gap
    return out


# ----------------------------------------------------------------------------
# UV sanity checks
# ----------------------------------------------------------------------------

def uv_rects(model: Model):
    """Yield (part, cube, (u0,v0,u1,v1)) texture rectangles used by every cube."""
    def walk(p: Part):
        for c in p.cubes:
            yield p, c, (c.u, c.v, c.u + 2 * c.d + 2 * c.w, c.v + c.d + c.h)
        for ch in p.children:
            yield from walk(ch)
    for r in model.roots:
        yield from walk(r)


def check_uvs(model: Model, tex_path: Optional[str]) -> int:
    problems = 0
    tex = None
    if tex_path:
        tex = np.array(Image.open(tex_path).convert("RGBA"))
    for p, c, (u0, v0, u1, v1) in uv_rects(model):
        if u1 > model.tex_w or v1 > model.tex_h or u0 < 0 or v0 < 0:
            print(f"  OUT OF BOUNDS: part '{p.name}' cube texOffs({c.u},{c.v}) size {c.w}x{c.h}x{c.d} -> rect {u0},{v0}-{u1},{v1}")
            problems += 1
        elif tex is not None:
            # faces of a box in the standard layout (skip the empty corners)
            d, w, h = int(c.d), int(c.w), int(c.h)
            faces = [
                (c.u + d, c.v, c.u + d + w, c.v + d),          # top
                (c.u + d + w, c.v, c.u + d + 2 * w, c.v + d),  # bottom
                (c.u, c.v + d, c.u + 2 * d + 2 * w, c.v + d + h),  # side strip
            ]
            for (a, b, cc, dd) in faces:
                if cc <= a or dd <= b:
                    continue
                region = tex[int(b):int(dd), int(a):int(cc), 3]
                if region.size and (region > 25).mean() < 0.05:
                    print(f"  (almost) fully transparent face: part '{p.name}' texOffs({c.u},{c.v}) rect {a},{b}-{cc},{dd}")
    return problems


# ----------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--java", required=True, help="Model .java file (Blockbench export)")
    ap.add_argument("--texture", required=True, help="PNG texture matching the model")
    ap.add_argument("--out", required=True, help="output PNG")
    ap.add_argument("--views", default="front,back,left,right,iso", help="comma list of %s or yaw:pitch" % ",".join(VIEWS))
    ap.add_argument("--hide", default="", help="comma list of part names to hide (e.g. toolbag,Cap)")
    ap.add_argument("--scale", type=float, default=12.0, help="pixels per model unit (1/16 block)")
    ap.add_argument("--keep-pose", action="store_true",
                    help="keep the PartPose rotation of head/body/arms/legs (by default they are zeroed, like setupAnim() does when the citizen stands still)")
    ap.add_argument("--constants-from", action="append", default=[], metavar="FILE.java",
                    help="extra Java source(s) whose static final constants may be referenced by the model (e.g. CitizenModel.java)")
    ap.add_argument("--pivot", action="append", default=[], metavar="NAME=X,Y,Z",
                    help="override the pivot of a part (what setupAnim() may do at runtime), e.g. hairback2_r1=0.1,-2.5,5.9")
    ap.add_argument("--list", action="store_true", help="print the part tree and exit")
    ap.add_argument("--check", action="store_true", help="validate UV rectangles against the texture")
    a = ap.parse_args(argv)

    model = parse_model(a.java, tuple(a.constants_from))
    for spec in a.pivot:
        name, _, xyz = spec.partition("=")
        if name not in model.by_name:
            sys.exit(f"--pivot: unknown part '{name}'")
        model.by_name[name].pivot = tuple(float(t) for t in xyz.split(","))
    if a.list:
        def dump(p: Part, depth=0):
            print("  " * depth + f"{p.name}  pivot={p.pivot} rot={tuple(round(r, 4) for r in p.rot)} cubes={len(p.cubes)}")
            for c in p.cubes:
                print("  " * (depth + 1) + f"- texOffs({c.u},{c.v}) box({c.x},{c.y},{c.z} {c.w}x{c.h}x{c.d}) g={c.grow() if c.gy is not None else c.g}{' mirror' if c.mirror else ''}")
            for ch in p.children:
                dump(ch, depth + 1)
        for r in model.roots:
            dump(r)
        return 0
    if a.check:
        print(f"Texture size declared by the model: {model.tex_w}x{model.tex_h}")
        n = check_uvs(model, a.texture)
        print("UV check:", "OK" if n == 0 else f"{n} problem(s)")
    hidden = {s.strip() for s in a.hide.split(",") if s.strip()}
    zero = set() if a.keep_pose else {"head", "hat", "body", "right_arm", "left_arm", "right_leg", "left_leg"}
    views = [v.strip() for v in a.views.split(",") if v.strip()]
    img = render(model, a.texture, views, hidden, a.scale, zero)
    img.save(a.out)
    print("wrote", a.out, img.size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
