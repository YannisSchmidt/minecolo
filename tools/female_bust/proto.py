#!/usr/bin/env python3
"""Prototype candidate bust geometries for the female citizen models.

For every candidate the ``"breast"`` statement of a copy of FemaleCitizenModel.java is
rewritten, then rendered (front / left / 3-4) with a repainted texture so that only the
shape and the shading of the new boxes are judged.  Results are stacked in a contact
sheet, with the silhouette extremes measured in model space (y = 0 is the neck line,
-z is forward).

    python3 tools/female_bust/proto.py [--scale 22] [--out /tmp/.../sheet.png]
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

MODEL_DIR = os.path.join(ROOT, "src/main/java/com/minecolonies/core/client/model")
CONSTS = os.path.join(ROOT, "src/main/java/com/minecolonies/api/client/render/modeltype/CitizenModel.java")
TEX = os.path.join(ROOT, "src/main/resources/assets/minecolonies/textures/entity/citizen/default/citizenfemale1_a.png")
CITIZEN = os.path.join(MODEL_DIR, "FemaleCitizenModel.java")

# Original Blockbench values of the "breast" cube, in the part's own frame.
CX = 1.0            # centre of the original 8-wide box (x from -3 to 5)
CY = 1.8938 + 1.5   # its vertical centre
BACK = -5.716 + 3.0  # its back face, inside the torso (= -2.716)

GROW = "BREAST_DEFORMATION"


def box(x, y, z, w, h, d, grow=GROW, mirror=False, tex=(64, 49)):
    g = grow if isinstance(grow, str) else f"new CubeDeformation({grow[0]}F, {grow[1]}F, {grow[2]}F)"
    m = ".mirror()" if mirror else ""
    return f".texOffs({tex[0]}, {tex[1]}){m}.addBox({x}F, {y}F, {z}F, {w}F, {h}F, {d}F, {g})"


def stmt(boxes, tilt_deg=-30.0, yshift=0.0, pivot=(-1.0, 3.0, 4.0)):
    body = "\n          ".join(boxes)
    rot = round(np.radians(tilt_deg), 4)
    return (
        '        PartDefinition breast = bipedBody.addOrReplaceChild("breast", CubeListBuilder.create()\n'
        f"          {body},\n"
        f"          PartPose.offsetAndRotation({pivot[0]}F, {pivot[1] + yshift}F, {pivot[2]}F, {rot}F, 0.0F, 0.0F));"
    )


def single(grow):
    gx, gy, gz = grow
    return [box(-3.0, 1.8938, -5.716, 8.0, 3.0, 3.0,
               grow=f"new CubeDeformation({gx}F, {gy}F, {gz}F)")]



FRONT0 = -5.716          # front plane of the original chest cube
BACK0 = FRONT0 + 3.0     # its back plane, inside the torso


def bust(grow, bands=((3.0, 2, 0.7), (4.0, 3, 0.0), (3.0, 4, 0.5)), gap=0.5,
         split=True, h=1.0, tilt_deg=-30.0, yshift=0.0, mirror=True, tex=(64, 49)):
    """Rounded chest: a stack of horizontal bands, one per side.

    Each band is ``(width, depth, recess)``: *depth* only picks which row of the
    painted ramp the front face samples (bigger depth = darker = lower on the curve),
    *recess* pulls the band back from the front plane, which is what makes the
    silhouette round.  Bands are 1 px tall so the whole stack keeps the original
    vertical span and never reaches the neck.
    """
    out = []
    total = h * len(bands)
    y = CY - total / 2.0
    for (w, d, rec) in bands:
        z = round(FRONT0 + rec, 3)
        if split and gap:
            bw = round(w - gap / 2.0, 3)
            for sgn in (-1, 1):
                x = round(CX + sgn * (w / 2.0 + gap / 2.0) - bw / 2.0, 3)
                out.append(box(x, round(y, 3), z, bw, h, d, grow=grow, tex=tex,
                               mirror=mirror and sgn > 0))
        else:
            out.append(box(round(CX - w / 2.0, 3), round(y, 3), z, w, h, d, grow=grow, tex=tex))
        y += h
    return out



def measure(java_path):
    m = R.parse_model(java_path, constants_from=(CONSTS,))
    part = m.by_name.get("breast")
    mat = R.part_matrix(m.by_name["body"], False) @ R.part_matrix(part, False)
    pts = []
    for c in part.cubes:
        for verts, _uv, _l in R.cube_quads(c):
            pts.append(np.c_[verts, np.ones(4)] @ mat.T)
    pts = np.concatenate(pts)[:, :3]
    return dict(
        top_y=round(float(pts[:, 1].min()), 2),        # 0 = neck line
        front=round(float(-pts[:, 2].min()), 2),       # z of the most forward point
        width=round(float(pts[:, 0].max() - pts[:, 0].min()), 2),
        height=round(float(pts[:, 1].max() - pts[:, 1].min()), 2),
        n=len(part.cubes),
    )


def patched_texture(path_out, grow=None):
    """Copy of the job texture with the chest rectangle repainted (bust_paint)."""
    a = np.array(Image.open(path_out).convert("RGBA"))
    s = P.scale_of(a.shape[1])
    P.merge_overlay(a, s)
    P.repaint(a, s)
    out = os.path.join(tempfile.gettempdir(), "bust_proto", "painted.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    Image.fromarray(a).save(out)
    return out


BANDS = ((3.4, 2, 0.6), (3.8, 3, -0.5), (3.8, 4, -1.4), (3.0, 5, -0.2))
ONE = ((6.5, 2, 0.6), (7.6, 3, -0.5), (7.6, 4, -1.4), (6.0, 5, -0.2))

CANDIDATES = {
    # None means "whatever the model file in the working tree does right now"
    "actuel (8 bandes)": None,
    "upstream (cube, pas de gonflement)": ((0.0, 0.0, 0.0), {"flat": True}),
    "1er essai (cube etire)": ((0.25, 1.0, 1.0), {"flat": True}),
    "bandes, taille discrete": ((0.2, 0.3, 0.6), {"bands": BANDS, "h": 1.05, "tilt_deg": -25.0}),
    "bandes, plus grand": ((0.5, 0.8, 1.7), {"bands": BANDS, "h": 1.05, "tilt_deg": -25.0}),
    "une seule piece (pas de sillon)": ((0.35, 0.6, 1.25), dict(
        bands=ONE, h=1.05, tilt_deg=-25.0, split=False, gap=0.0)),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=int, default=22)
    ap.add_argument("--java-model", default=CITIZEN)
    ap.add_argument("--texture", default=TEX)
    ap.add_argument("--out", default=os.path.join(tempfile.gettempdir(), "bust_proto", "sheet.png"))
    args = ap.parse_args()
    outdir = os.path.dirname(args.out)
    os.makedirs(outdir, exist_ok=True)
    src = open(args.java_model).read()
    tex = patched_texture(args.texture)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    rows = []
    for name, spec in CANDIDATES.items():
        if spec is None:      # the state of the repo right now
            kw, boxes = {}, None
        else:
            grow, kw = spec
            g = f"new CubeDeformation({grow[0]}F, {grow[1]}F, {grow[2]}F)"
            kw = {k: v for k, v in kw.items() if k != "flat"}
            boxes = single(grow) if spec[1].get("flat") else bust(grow=g, **kw)
        j = os.path.join(outdir, re.sub(r"[^a-z0-9]+", "_", name.lower()) + ".java")
        if boxes is None:
            open(j, "w").write(src)
        else:
            i = src.find('addOrReplaceChild("breast"')
            i = src.rfind("PartDefinition", 0, i)
            k = src.find(");", src.find("offsetAndRotation", i)) + 2
            open(j, "w").write(src[:i] + stmt(boxes, **{k2: v for k2, v in kw.items()
                                                        if k2 in ("tilt_deg", "yshift")}) + src[k:])
        info = measure(j)
        png = j.replace(".java", ".png")
        subprocess.run([sys.executable, os.path.join(ROOT, "tools/model_preview/render_citizen_model.py"),
                        "--java", j, "--texture", tex, "--out", png, "--views", "front,left,iso",
                        "--scale", str(args.scale)], check=True, capture_output=True)
        print(f'{name:38s} {info}')
        im = Image.open(png).convert("RGBA")
        W, Hh = im.size
        pw = W // 3
        row = Image.new("RGBA", (pw * 3 + 12, Hh + 26), (246, 246, 246, 255))
        for i in range(3):
            row.alpha_composite(im.crop((i * pw, 0, (i + 1) * pw, Hh)), (i * pw + 4, 26))
        ImageDraw.Draw(row).text(
            (6, 5), f"{name}   n={info['n']} top_y={info['top_y']} front={info['front']} w={info['width']} h={info['height']}",
            fill=(20, 20, 20), font=font)
        rows.append(row)
    W = max(r.width for r in rows)
    sheet = Image.new("RGBA", (W, sum(r.height for r in rows)), (255, 255, 255, 255))
    y = 0
    for r in rows:
        sheet.alpha_composite(r, (0, y))
        y += r.height
    sheet.save(args.out)
    print("wrote", args.out, sheet.size)


if __name__ == "__main__":
    main()
