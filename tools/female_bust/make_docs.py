#!/usr/bin/env python3
"""Build the PNGs of documentation/female_models_bust/ from the current models.

Everything is rendered with tools/model_preview/render_citizen_model.py.  The "before"
panels are rendered straight out of a git revision (``git show``), so they show what that
revision really drew rather than a re-creation: ``--before`` is the untouched MineColonies
import, ``--prev`` the previous (still flat) state of this fork.

    python3 tools/female_bust/make_docs.py [--scale 11] [--only avant_apres,textures]
"""
from __future__ import annotations

import argparse
import io
import os
import re
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_compare as RC  # noqa: E402
import bust_paint as P  # noqa: E402

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
VIEWS = ("front", "left", "iso")
BEFORE = "75a3c0a"
PREVIOUS = "HEAD"
OUTDIR = os.path.join(ROOT, "documentation/female_models_bust")
WORKDIR = tempfile.mkdtemp(prefix="bustdocs")


# --------------------------------------------------------------------------- rendering
def _source(rev: str | None, path: str, tag: str) -> str:
    """Working tree file, or the same file as of ``rev`` (extracted to the scratch dir)."""
    if rev is None:
        return os.path.join(ROOT, path)
    dest = os.path.join(WORKDIR, tag, os.path.basename(path))
    return RC.git_show(rev, path, dest)


def panels(model: str, scale: int, tag: str, rev: str | None = None, style: str = "default",
           variant: str = "a", views=VIEWS, base_override: str | None = None,
           texture_override: str | None = None) -> list[Image.Image]:
    """Render one model, return the panels in the requested view order."""
    job = RC.job_of(model)
    tex = f"{RC.TEX_DIR}/{style}/{job}female1_{variant}.png"
    java = _source(rev, f"{RC.MODEL_DIR}/{model}.java", tag)
    base = base_override or _source(rev, RC.BASE_MODEL, tag)
    texture = texture_override or _source(rev, tex, tag)
    out = os.path.join(WORKDIR, tag, f"{model}_{abs(hash((rev, scale, views)))}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run([sys.executable, RC.RENDERER, "--java", java, "--texture", texture, "--out", out,
                    "--views", ",".join(views), "--scale", str(scale), "--constants-from", base],
                   check=True, capture_output=True)
    im = Image.open(out).convert("RGBA")
    w = im.width // len(views)
    return [im.crop((i * w, 0, (i + 1) * w, im.height)) for i in range(len(views))]


def const_variant(value: str, name: str) -> str:
    """A copy of CitizenModel.java whose BREAST_DEFORMATION has another value."""
    src = open(os.path.join(ROOT, RC.BASE_MODEL)).read()
    pat = r"public static final CubeDeformation BREAST_DEFORMATION = [^;]*;"
    if not re.search(pat, src):
        raise SystemExit("BREAST_DEFORMATION not found in CitizenModel.java")
    out = re.sub(pat, f"public static final CubeDeformation BREAST_DEFORMATION = new CubeDeformation({value});",
                 src, count=1)
    path = os.path.join(WORKDIR, f"consts_{name}.java")
    os.makedirs(WORKDIR, exist_ok=True)
    open(path, "w").write(out)
    return path


# --------------------------------------------------------------------------- composing
def spacer(ref: Image.Image) -> Image.Image:
    return Image.new("RGBA", ref.size, (255, 255, 255, 0))


def row(items: list[tuple[Image.Image, str]], gap: int = 8, head: int = 24) -> Image.Image:
    """A row of panels; each entry carries the caption to draw above it ("" = none)."""
    font = ImageFont.truetype(FONT, 15)
    pw = max(im.width for im, _ in items)
    ph = max(im.height for im, _ in items)
    out = Image.new("RGBA", (len(items) * (pw + gap) + gap, ph + head + gap), (246, 246, 246, 255))
    d = ImageDraw.Draw(out)
    for k, (im, lab) in enumerate(items):
        x = gap + k * (pw + gap)
        if im.size != (pw, ph):
            im = im.resize((pw, ph))
        out.alpha_composite(im, (x, head))
        if lab:
            d.text((x + 2, 5), lab, fill=(18, 18, 18), font=font)
    return out


def with_title(img: Image.Image, text: str, size: int = 19, height: int = 32) -> Image.Image:
    out = Image.new("RGBA", (img.width, img.height + height), (255, 255, 255, 255))
    ImageDraw.Draw(out).text((10, 7), text, fill=(12, 12, 12), font=ImageFont.truetype(FONT, size))
    out.alpha_composite(img, (0, height))
    return out


def save(img: Image.Image, name: str, title: str | None = None) -> None:
    if title:
        img = with_title(img, title)
    path = os.path.join(OUTDIR, name)
    os.makedirs(OUTDIR, exist_ok=True)
    img.save(path)
    print(f"{os.path.relpath(path, ROOT):52s} {img.size}")


# --------------------------------------------------------------------------- the images
def image_before_after(scale: int) -> None:
    """One line per job: the upstream model, then the fork's model."""
    models = [("FemaleCitizenModel", "Citoyenne"), ("FemaleBuilderModel", "Buildeuse"),
              ("FemaleFarmerModel", "Fermiere"), ("FemaleNobleModle", "Noble"),
              ("FemaleCookModel", "Cuisiniere"), ("FemaleKnightModel", "Chevaliere")]
    rows = []
    for model, fr in models:
        before = panels(model, scale, "before", rev=BEFORE)
        after = panels(model, scale, "after")
        rows.append(row(list(zip(before, [fr + " : AVANT", "", ""])) + [(spacer(before[0]), "")]
                        + list(zip(after, ["APRES", "", ""]))))
    save(row_to_image(rows), "avant_apres.png",
         "Buste des modeles feminins adultes : a gauche l'original de MineColonies, a droite la version du fork")


def row_to_image(rows: list[Image.Image]) -> Image.Image:
    W = max(r.width for r in rows)
    out = Image.new("RGBA", (W, sum(r.height for r in rows) + 8 * (len(rows) - 1)), (255, 255, 255, 255))
    y = 0
    for r in rows:
        out.alpha_composite(r, (0, y))
        y += r.height + 8
    return out


def image_three_states(scale: int) -> None:
    """Upstream, the first (flat) attempt of this fork, and the current result."""
    rows = []
    for model, fr in [("FemaleCitizenModel", "Citoyenne"), ("FemaleBuilderModel", "Buildeuse")]:
        ups = panels(model, scale, "s0", rev=BEFORE)
        flat = panels(model, scale, "s1", rev=PREVIOUS)
        new = panels(model, scale, "s2")
        rows.append(row(list(zip(ups, [fr + " : original", "", ""])) + [(spacer(ups[0]), "")]
                        + list(zip(flat, ["1er essai : cube unique etire", "", ""])) + [(spacer(ups[0]), "")]
                        + list(zip(new, ["actuel : 8 bandes + texture repeinte", "", ""]))))
    save(row_to_image(rows), "trois_etats.png",
         "Le cube etire laissait une face plate et une coquille de tissu par-dessus : remplace par des bandes")


def image_sizes(scale: int) -> None:
    """The tuning knob: same shape, four sizes."""
    variants = [("0.0F, 0.0F, 0.0F", "0 : forme seule"), ("0.2F, 0.3F, 0.6F", "discret"),
                ("0.35F, 0.6F, 1.25F", "valeur retenue"), ("0.5F, 0.8F, 1.7F", "limite avant le cou")]
    rows = []
    for model, fr in [("FemaleCitizenModel", "Citoyenne"), ("FemaleBuilderModel", "Buildeuse")]:
        items: list[tuple[Image.Image, str]] = []
        for i, (value, lab) in enumerate(variants):
            base = const_variant(value, f"{re.sub(r'[^0-9.]', '', value)}_{model}")
            p = panels(model, scale, f"size{i}_{model}", base_override=base)
            items += list(zip(p, [f"{fr} {lab}" if i == 0 else lab, "", ""]))
            if i < len(variants) - 1:
                items.append((spacer(p[0]), ""))
        rows.append(row(items))
    save(row_to_image(rows), "comparatif_tailles.png",
         "Tout le reglage tient dans BREAST_DEFORMATION (CitizenModel.java) : une ligne pour les 40 modeles")


def image_textures() -> None:
    """The chest rectangle of the texture itself, repainted or not."""
    zoom, box0, box1 = 6, (62, 44), (90, 64)
    rows = []
    for job in ["citizen", "builder", "farmer", "noble", "smelter", "healer"]:
        cell = []
        for rev in (BEFORE, None):
            if rev:
                raw = subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{RC.TEX_DIR}/default/{job}female1_a.png"],
                                     check=True, capture_output=True).stdout
                im = Image.open(io.BytesIO(raw)).convert("RGBA")
            else:
                im = Image.open(os.path.join(ROOT, RC.TEX_DIR, "default", f"{job}female1_a.png")).convert("RGBA")
            s = P.scale_of(im.size[0])
            big = im.resize((im.width * zoom, im.height * zoom), Image.NEAREST)
            cell.append(big.crop((box0[0] * zoom, box0[1] * zoom, box1[0] * zoom, box1[1] * zoom)))
        pad = 20
        box = Image.new("RGBA", (cell[0].width * 2 + 28, cell[0].height + pad + 26), (246, 246, 246, 255))
        d = ImageDraw.Draw(box)
        d.text((4, 4), job, fill=(18, 18, 18), font=ImageFont.truetype(FONT, 15))
        d.text((6, cell[0].height + pad + 2), "zone echantillonnee par le buste : avant", fill=(90, 90, 90),
               font=ImageFont.truetype(FONT, 13))
        d.text((cell[0].width + 24, cell[0].height + pad + 2), "repeinte : une couleur par ligne", fill=(120, 0, 0),
               font=ImageFont.truetype(FONT, 13))
        box.alpha_composite(cell[0], (4, pad))
        box.alpha_composite(cell[1], (cell[0].width + 20, pad))
        rows.append(box)
    save(row_to_image(rows), "textures.png",
         "La zone du buste est uniformisee ligne par ligne : aucune couture possible entre les 8 bandes")


def image_all_models() -> None:
    models = sorted(m[:-5] for m in os.listdir(os.path.join(ROOT, RC.MODEL_DIR))
                    if m.startswith("Female") and m.endswith(".java") and "Child" not in m)
    cells = []
    for m in models:
        p = panels(m, 6, f"sheet_{m}", views=("front", "iso"))
        c = Image.new("RGBA", (p[0].width + p[1].width + 12, p[0].height + 18), (246, 246, 246, 255))
        c.alpha_composite(p[0], (4, 18))
        c.alpha_composite(p[1], (p[0].width + 8, 18))
        ImageDraw.Draw(c).text((6, 2), RC.job_of(m), fill=(20, 20, 20), font=ImageFont.truetype(FONT, 13))
        cells.append(c)
    ncol = 5
    cw, ch = max(c.width for c in cells), max(c.height for c in cells)
    nrow = (len(cells) + ncol - 1) // ncol
    sheet = Image.new("RGBA", (ncol * (cw + 8) + 8, nrow * (ch + 8) + 8), (255, 255, 255, 255))
    for i, c in enumerate(cells):
        sheet.alpha_composite(c, (8 + (i % ncol) * (cw + 8), 8 + (i // ncol) * (ch + 8)))
    save(sheet, "planche_40_modeles.png",
         "Les 40 modeles feminins adultes modifies : face et 3/4, chacun avec la texture de son metier")


IMAGES = {"avant_apres": lambda s: image_before_after(s),
          "trois_etats": lambda s: image_three_states(s),
          "comparatif_tailles": lambda s: image_sizes(s),
          "textures": lambda s: image_textures(),
          "planche_40_modeles": lambda s: image_all_models()}


def main():
    global BEFORE, PREVIOUS, OUTDIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", default=BEFORE, help="git rev of the untouched MineColonies import")
    ap.add_argument("--prev", default=PREVIOUS, help="git rev of the previous flat version")
    ap.add_argument("--out", default="documentation/female_models_bust")
    ap.add_argument("--scale", type=int, default=11)
    ap.add_argument("--only", default="", help="comma separated names: " + ", ".join(IMAGES))
    args = ap.parse_args()
    BEFORE, PREVIOUS = args.before, args.prev
    OUTDIR = os.path.join(ROOT, args.out)
    todo = [t.strip() for t in args.only.split(",") if t.strip()] or list(IMAGES)
    for name in todo:
        IMAGES[name](args.scale)


if __name__ == "__main__":
    main()
