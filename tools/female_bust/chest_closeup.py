#!/usr/bin/env python3
"""Close-up of the chest of job models, for the artefact hunt.

    python3 tools/female_bust/chest_closeup.py [--jobs baker,druid] [--scale 26]

For every job it renders the front / left / iso views of the model with its real (already
repainted) texture and crops them around the *bust*, so an intersection between a piece of
job gear and one of the balls is visible instead of being lost in a full-body thumbnail.
"""
from __future__ import annotations

import argparse
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "model_preview"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render_citizen_model as R  # noqa: E402

MODEL_DIR = os.path.join(ROOT, "src/main/java/com/minecolonies/core/client/model")
TEX_DIR = os.path.join(ROOT, "src/main/resources/assets/minecolonies/textures/entity/citizen")
CITIZEN_MODEL = os.path.join(ROOT, "src/main/java/com/minecolonies/api/client/render/modeltype/CitizenModel.java")
ZERO = {"head", "hat", "body", "right_arm", "left_arm", "right_leg", "left_leg"}
PAD = 6


def jobs():
    out = []
    for f in sorted(os.listdir(MODEL_DIR)):
        if f.startswith("Female") and f.endswith("Model.java") and "Child" not in f:
            out.append(f[len("Female"):-len("Model.java")].lower())
    return out


def model_java(job):
    for cand in (f"Female{job.capitalize()}Model.java", f"Female{job.capitalize()}Modle.java"):
        p = os.path.join(MODEL_DIR, cand)
        if os.path.exists(p):
            return p
    return None


def texture_for(job, style="default", variant="w"):
    for v in (variant, "d", "a", "b"):
        p = os.path.join(TEX_DIR, style, f"{job}female1_{v}.png")
        if os.path.exists(p):
            return p
    return None


def bust_crop(model, tex_path, view, scale, margin=0.35):
    """Render one view and crop it around the projected bounding box of the bust."""
    tris = R.collect_triangles(model, set(), ZERO)
    yaw, pitch = R.VIEWS[view] if view in R.VIEWS else tuple(float(t) for t in view.split(":"))
    right, up, fwd = R.camera_basis(yaw, pitch)
    allp, bustp = [], []
    for xyz, uv, pname, label in tris:
        w = R.model_to_world(xyz)
        allp.append(np.c_[w @ right, w @ up])
        if pname == "breast":
            bustp.append(np.c_[w @ right, w @ up])
    allp = np.concatenate(allp)
    bustp = np.concatenate(bustp)
    minx, maxx, miny, maxy = allp[:, 0].min(), allp[:, 0].max(), allp[:, 1].min(), allp[:, 1].max()
    img = R.render_view(tris, np.array(Image.open(tex_path).convert("RGBA")), yaw, pitch, scale, PAD)
    a = np.array(img)
    x0, x1 = bustp[:, 0].min(), bustp[:, 0].max()
    y0, y1 = bustp[:, 1].min(), bustp[:, 1].max()
    dx, dy = (x1 - x0) * margin, (y1 - y0) * margin
    px = lambda v: int(round((v - minx) * scale + PAD))
    py = lambda v: int(round((maxy - v) * scale + PAD))
    box = (max(0, px(x0 - dx)), max(0, py(y1 + dy)), min(img.width, px(x1 + dx)), min(img.height, py(y0 - dy)))
    return Image.fromarray(a[box[1]:box[3], box[0]:box[2]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", default="")
    ap.add_argument("--style", default="default")
    ap.add_argument("--variant", default="w")
    ap.add_argument("--scale", type=int, default=22)
    ap.add_argument("--views", default="front,left,iso")
    ap.add_argument("--out", default="/tmp/chest_closeup.png")
    a = ap.parse_args()
    jl = a.jobs.split(",") if a.jobs else jobs()
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    rows = []
    for job in jl:
        mj, tx = model_java(job), texture_for(job, a.style, a.variant)
        if not (mj and tx):
            print("skip", job)
            continue
        model = R.parse_model(mj, constants_from=(CITIZEN_MODEL,))
        if "breast" not in model.by_name:
            continue
        cells = [bust_crop(model, tx, v, a.scale) for v in a.views.split(",")]
        w = sum(c.width for c in cells) + 8 * (len(cells) + 1)
        h = max(c.height for c in cells)
        row = Image.new("RGBA", (w, h + 16), (248, 248, 248, 255))
        x = 8
        for c in cells:
            row.alpha_composite(c, (x, 16))
            x += c.width + 8
        ImageDraw.Draw(row).text((4, 1), f"{job}  [{os.path.basename(tx)}]", fill=(0, 0, 0), font=font)
        rows.append(row)
    W = max(r.width for r in rows)
    out = Image.new("RGBA", (W, sum(r.height for r in rows)), (255, 255, 255, 255))
    y = 0
    for r in rows:
        out.alpha_composite(r, (0, y))
        y += r.height
    out.save(a.out)
    print("wrote", a.out, out.size)


if __name__ == "__main__":
    main()
