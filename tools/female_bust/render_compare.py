#!/usr/bin/env python3
"""Render side-by-side comparisons of the female models, before and after.

    python3 tools/female_bust/render_compare.py --models FemaleCitizenModel,FemaleBuilderModel \
        --before 75a3c0a --style default --scale 16 --out /tmp/cmp.png

``--before`` is any git revision: the model file, its ``CitizenModel`` base class and
the matching texture are read from there with ``git show``, so the left column shows
what that revision really rendered, without touching the working tree.  Use
``--before HEAD`` to compare against the previous state of this fork, and
``--mid <rev>`` to insert a third column (used for the intermediate, still flat
version of the bust).
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_DIR = "src/main/java/com/minecolonies/core/client/model"
BASE_MODEL = "src/main/java/com/minecolonies/api/client/render/modeltype/CitizenModel.java"
TEX_DIR = "src/main/resources/assets/minecolonies/textures/entity/citizen"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
RENDERER = os.path.join(ROOT, "tools/model_preview/render_citizen_model.py")


def job_of(model: str) -> str:
    name = model.replace("Female", "").replace("Model", "")
    return {"Apiary": "beekeeper", "ChickenHerder": "chickenfarmer", "CowHerder": "cowfarmer",
            "SwineHerder": "pigfarmer", "Fisher": "fisherman", "Shepherd": "sheepfarmer",
            "NobleModle": "noble"}.get(name, name[0].lower() + name[1:]).lower()


def git_show(ref: str, path: str, dest: str) -> str:
    data = subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{path}"],
                          check=True, capture_output=True).stdout
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as fh:
        fh.write(data)
    return dest


def render(model: str, ref: str | None, style: str, variant: str, views, scale, workdir, tag):
    """Returns (png path, texture path used)."""
    job = job_of(model)
    tex_name = f"{job}female1_{variant}.png"
    if ref:
        java = git_show(ref, f"{MODEL_DIR}/{model}.java", os.path.join(workdir, tag, f"{model}.java"))
        base = git_show(ref, BASE_MODEL, os.path.join(workdir, tag, "CitizenModel.java"))
        tex = git_show(ref, f"{TEX_DIR}/{style}/{tex_name}", os.path.join(workdir, tag, tex_name))
    else:
        java = os.path.join(ROOT, MODEL_DIR, f"{model}.java")
        base = os.path.join(ROOT, BASE_MODEL)
        tex = os.path.join(ROOT, TEX_DIR, style, tex_name)
    out = os.path.join(workdir, tag, f"{model}_{style}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([sys.executable, RENDERER, "--java", java, "--texture", tex, "--out", out,
                    "--views", ",".join(views), "--scale", str(scale), "--constants-from", base],
                   check=True, capture_output=True)
    return out, tex


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="FemaleCitizenModel")
    ap.add_argument("--before", default="HEAD", help="git rev of the 'avant' column ('' = working tree only)")
    ap.add_argument("--mid", default="", help="optional extra column (git rev)")
    ap.add_argument("--style", default="default")
    ap.add_argument("--variant", default="a")
    ap.add_argument("--views", default="front,left,iso")
    ap.add_argument("--scale", type=int, default=16)
    ap.add_argument("--out", required=True)
    ap.add_argument("--labels", default="")
    args = ap.parse_args()
    views = args.views.split(",")
    models = args.models.split(",")
    workdir = tempfile.mkdtemp(prefix="bustcmp")
    refs = [r for r in (args.before, args.mid, "") if r is not None]
    labels = args.labels.split(",") if args.labels else (
        ["ORIGINAL", "PLAT", "ARRONDI"] if args.mid else ["AVANT", "APRÈS"])
    font = ImageFont.truetype(FONT, 16)

    tiles, texes = [], []
    for m in models:
        row = []
        for i, ref in enumerate(refs):
            png, tex = render(m, ref or None, args.style, args.variant, views, args.scale, workdir, f"r{i}")
            row.append((png, tex))
        tiles.append(row)
    # grid: one block per model, columns = view x ref
    blocks = []
    for mi, row in enumerate(tiles):
        imgs = []
        for ri, (png, _tex) in enumerate(row):
            im = Image.open(png).convert("RGBA")
            w = im.width // len(views)
            for v in range(len(views)):
                imgs.append((f"{labels[ri] if ri < len(labels) else ''} {views[v]}", im.crop((v * w, 0, (v + 1) * w, im.height))))
        pw = max(i.width for _l, i in imgs)
        ph = max(i.height for _l, i in imgs)
        gap = 8
        blk = Image.new("RGBA", (len(imgs) * (pw + gap) + gap, ph + 26 + gap), (246, 246, 246, 255))
        d = ImageDraw.Draw(blk)
        for k, (lab, im) in enumerate(imgs):
            x = gap + k * (pw + gap)
            blk.alpha_composite(im, (x, 26))
            d.text((x + 2, 6), lab, fill=(20, 20, 20), font=font)
        blocks.append(blk)
    W = max(b.width for b in blocks)
    H = sum(b.height for b in blocks)
    out = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    y = 0
    for b in blocks:
        out.alpha_composite(b, (0, y))
        y += b.height
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    out.save(args.out)
    print(f"wrote {args.out} {out.size}  (models={len(models)} cols={len(refs) * len(views)})")
    print("textures used:", ", ".join(sorted({os.path.relpath(t[1], workdir) for r in tiles for t in r})))


if __name__ == "__main__":
    main()
