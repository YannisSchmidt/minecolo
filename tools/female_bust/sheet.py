#!/usr/bin/env python3
"""Contact sheet of candidate bust shapes (balls built out of rings x bands).

    python3 tools/female_bust/sheet.py [--scale 20] [--views front,left,iso,back] [--out /tmp/sheet.png]

The candidates live in ``CANDIDATES`` below; every one of them is turned into a real
``"breast"`` statement, measured in body space (top_y = distance to the neck line, tip =
how far the ball sticks out past the torso, halfx = how close it gets to the arms, and
``arm`` = how many of its corners actually land inside the volume swept by the arms,
which is the number that must stay 0) and rendered with a repainted texture, so shape
and shading are judged together.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "model_preview"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render_citizen_model as R  # noqa: E402
import bust_paint as P  # noqa: E402
from bust_shape import Bust  # noqa: E402
from rework_bust import build_boxes, fmt  # noqa: E402

MODEL_DIR = os.path.join(ROOT, "src/main/java/com/minecolonies/core/client/model")
CONSTS = os.path.join(ROOT, "src/main/java/com/minecolonies/api/client/render/modeltype/CitizenModel.java")
CITIZEN = os.path.join(MODEL_DIR, "FemaleCitizenModel.java")
TEX_DIR = os.path.join(ROOT, "src/main/resources/assets/minecolonies/textures/entity/citizen")

CX, CY, FRONT0 = 1.0, 3.3938, -5.716      # original Blockbench frame of the chest cube
ARM_IN = 4.0           # the arms start there (|x| = 4, torso ends at 4 as well)
TORSO_FRONT = -2.0     # body-space z of the front face of the torso

# The torso cube texOffs(16,16) 8x12x4: its front face is x 20..28, y 20..32, and the
# copy for the clothing layer texOffs(16,32) the same at y 36..48.  The middle column of
# that face is the middle of the chest, i.e. exactly the valley between the two lobes.
BODY_FRONT = (20, 20, 28, 32)
OVERLAY_DY = 16


def statement(bust: Bust, deform=None, var="breast", parent="bipedBody", indent="        "):
    grow = "BREAST_DEFORMATION" if deform is None else \
        f"new CubeDeformation({fmt(deform[0])}F, {fmt(deform[1])}F, {fmt(deform[2])}F)"
    lines = []
    for (x, y, z, w, h, d) in build_boxes(bust, CX, CY, FRONT0):
        lines.append(f".texOffs({bust.u}, {bust.v}).addBox({fmt(x)}, {fmt(y)}, {fmt(z)}, "
                     f"{fmt(w)}, {fmt(h)}, {fmt(d)}, {grow})")
    body = ("\n" + indent + "  ").join(lines)
    return (f'{indent}PartDefinition {var} = {parent}.addOrReplaceChild("breast", CubeListBuilder.create()\n'
            f"{indent}  {body},\n"
            f"{indent}  PartPose.offsetAndRotation(-1.0F, 3.0F, 4.0F, {fmt(bust.tilt)}, 0.0F, 0.0F));\n")


def measure(java_path):
    """Body-space bounds of the bust + how much of it lands inside the volume of the arms.

    The arms are boxes x 4..7 (0.25 wider for their clothing layer), y 0..14, z -2..2.
    A bust box that reaches into that volume is cut by the arm's own faces: that is the
    one kind of artefact a viewer notices, so it is counted per box and reported.
    """
    m = R.parse_model(java_path, constants_from=(CONSTS,))
    part = m.by_name["breast"]
    mat = R.part_matrix(m.by_name["body"], False) @ R.part_matrix(part, False)
    pts = []
    for c in part.cubes:
        for verts, _uv, _l in R.cube_quads(c):
            pts.append(np.c_[verts, np.ones(4)] @ mat.T)
    pts = np.concatenate(pts)[:, :3]
    lo, hi = pts.min(0), pts.max(0)
    bad = 0
    deepest = 0.0
    for c in part.cubes:
        q = np.concatenate([np.c_[v, np.ones(4)] @ mat.T for v, _uv, _l in R.cube_quads(c)])[:, :3]
        a0, a1 = q.min(0), q.max(0)
        ov_x = min(a1[0], 7.25) - max(a0[0], 3.75)
        ov_x = max(ov_x, min(a1[0], -3.75) - max(a0[0], -7.25))
        ov_z = min(a1[2], 2.25) - max(a0[2], -2.25)
        ov_y = min(a1[1], 14.25) - max(a0[1], -0.25)
        if min(ov_x, ov_y, ov_z) > 0.02:
            bad += 1
            deepest = max(deepest, ov_x)
    in_arm = bad
    return dict(top_y=round(float(lo[1]), 2), bot_y=round(float(hi[1]), 2),
                tip=round(float(TORSO_FRONT - lo[2]), 2), back=round(float(hi[2]), 2),
                halfx=round(float(max(abs(lo[0]), abs(hi[0]))), 2), arm=int(in_arm),
                armd=round(deepest, 2), n=len(part.cubes))


def painted_texture(ramp, flat=True, cleft=0.0, path=None):
    """A copy of the default texture, repainted the way the real textures will be."""
    path = path or os.path.join(TEX_DIR, "default", "citizenfemale1_a.png")
    a = np.array(Image.open(path).convert("RGBA"))
    s = P.scale_of(a.shape[1])
    P.merge_overlay(a, s)
    colors = P.repaint(a, s, ramp=ramp, flat=flat)
    if cleft:
        cleft_shadow(a, s, cleft, y0=2.0, y1=9.5)
    out = os.path.join(tempfile.gettempdir(), "bust_sheet", "painted.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.fromarray(a).save(out)
    return out


def cleft_shadow(a, s, k=0.28, y0=2.0, y1=9.5, half=2.0):
    """Darken the middle of the chest on the torso's own front face: the valley."""
    u0, v0, u1, v1 = BODY_FRONT
    cx = (u0 + u1) / 2.0
    for dy in (0, OVERLAY_DY):
        for x in range(int(round((cx - half) * s)), int(round((cx + half) * s)) + 1):
            t = abs(x / s + 0.5 * (1 if s == 1 else 0) - cx) / half       # 0 in the middle
            f = 1.0 - k * max(0.0, 1.0 - t * t)
            for y in range(int(round((v0 + y0 + dy) * s)), int(round((v0 + y1 + dy) * s))):
                a[y, x, :3] = np.clip(a[y, x, :3].astype(float) * f, 0, 255)


def sheet(cands, out, scale=20, views="front,left,iso,back"):
    src = open(CITIZEN).read()
    i = src.find('addOrReplaceChild("breast"')
    i = src.rfind("PartDefinition", 0, i)
    k = src.find(");", src.find("offsetAndRotation", i)) + 2
    d = os.path.join(tempfile.gettempdir(), "bust_sheet")
    os.makedirs(d, exist_ok=True)
    rows = []
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    for name, spec in cands.items():
        bust, ramp, deform, kw = spec
        tex = painted_texture(ramp, **(kw or {}))
        j = os.path.join(d, re.sub(r"[^a-z0-9]+", "_", name.lower()) + ".java")
        open(j, "w").write(open(CITIZEN).read() if bust is None else src[:i] + statement(bust, deform) + src[k:])
        info = measure(j)
        png = j.replace(".java", ".png")
        subprocess.run([sys.executable, os.path.join(ROOT, "tools/model_preview/render_citizen_model.py"),
                        "--java", j, "--texture", tex, "--out", png, "--views", views,
                        "--scale", str(scale)], check=True, capture_output=True)
        print(f"{name:26s} {info}")
        im = Image.open(png).convert("RGBA")
        n = len(views.split(","))
        pw = im.width // n
        row = Image.new("RGBA", (pw * n + 12, im.height + 26), (244, 244, 244, 255))
        for q in range(n):
            row.alpha_composite(im.crop((q * pw, 0, (q + 1) * pw, im.height)), (q * pw + 4, 26))
        ImageDraw.Draw(row).text((6, 5), f"{name}   n={info['n']} top_y={info['top_y']} tip={info['tip']} "
                                 f"halfx={info['halfx']} arm={info['arm']}/{info['armd']} back={info['back']} bot={info['bot_y']}",
                                 fill=(20, 20, 20), font=font)
        rows.append(row)
    W = max(r.width for r in rows)
    sh = Image.new("RGBA", (W, sum(r.height for r in rows)), (255, 255, 255, 255))
    y = 0
    for r in rows:
        sh.alpha_composite(r, (0, y))
        y += r.height
    sh.save(out)
    print("wrote", out, sh.size)


FLAT = (1.0,) * 6
SOFT = (1.10, 1.05, 1.00, 0.94, 0.88, 0.80)


def rings(a, b, n, base=1.1):
    """Ellipse profile: n rings of a ball half as wide as ``2a`` and ``b`` deep."""
    out = []
    for k in range(n):
        th = (k + 0.5) / n * (np.pi / 2)
        p = base + b * np.sin(th)
        w = min(2 * a * np.cos(th), 2 * a)
        out.append((round(float(w), 2), round(float(p), 2)))
    return tuple(out)


def scaled(f_w, f_p):
    return tuple((round(w * f_w, 2), round(p_ * f_p, 2)) for (w, p_) in Bust().rings)


def prof(fp, fw=1.0):
    return tuple((round(w * fw, 2), round(p_ * fp, 2)) for (w, p_) in Bust().rings)


W1 = ((3.10, 1.50), (4.60, 2.70), (5.40, 4.60), (5.20, 6.40), (4.20, 8.00), (2.40, 9.20))
CANDIDATES = {
    "W0 retenu": (Bust(), SOFT, None, {"cleft": 0.28}),
    "W1 large": (Bust(rings=W1), SOFT, None, {"cleft": 0.28}),
    "W2 large+1,1": (Bust(rings=prof(1.1, 1.0) and tuple((round(w * 1.22, 2), round(p_ * 1.1, 2))
                                                           for (w, p_) in W1)), SOFT, None, {"cleft": 0.28}),
    "W3 6 bandes": (Bust(rings=W1, nbands=6, band_step=1.1, band_h=1.18, radius_v=3.15), SOFT, None, {"cleft": 0.28}),
    "W4 pointe": (Bust(rings=((3.10, 1.50), (4.60, 2.80), (5.40, 4.80), (5.00, 7.00), (3.40, 9.00), (1.40, 10.6))),
                  SOFT, None, {"cleft": 0.28}),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=int, default=20)
    ap.add_argument("--views", default="front,left,iso,back")
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=os.path.join(tempfile.gettempdir(), "bust_sheet", "sheet.png"))
    a = ap.parse_args()
    cands = {k: v for k, v in CANDIDATES.items() if not a.only or re.search(a.only, k)}
    sheet(cands, a.out, a.scale, a.views)


if __name__ == "__main__":
    main()
