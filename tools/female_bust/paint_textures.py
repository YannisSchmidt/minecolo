#!/usr/bin/env python3
"""Repaint the chest area of every female citizen texture.

The bust cube (and now its eight bands) samples ``texOffs(64, 49)``, i.e. the rectangle
``x 64..85, y 49..54`` of a 128x64 citizen texture.  Two things are done to it:

* the "clothing" layer that used to live at ``texOffs(64, 55)`` is folded into it
  (that second cube is gone from the models: it drew a hard shell 0.25 proud of the
  chest and showed stray pixels of the texture on the bust);
* the whole rectangle is then filled with a single smooth vertical ramp built from
  the colours the file already had there, uniform along x.

The second point is what keeps the result clean: every band of the bust samples the
same rows, so no seam can appear between the boxes, and the light-to-dark ramp is
what makes the shape read as a rounded volume rather than as a stretched flat patch.

    python3 tools/female_bust/paint_textures.py [--only default] [--dry-run] [--check]
"""
from __future__ import annotations

import argparse
import glob
import io
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bust_paint as P  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEX_DIR = os.path.join(ROOT, "src/main/resources/assets/minecolonies/textures/entity/citizen")


def texture_files(styles=None, genders=("female",)):
    out = []
    for p in sorted(glob.glob(os.path.join(TEX_DIR, "*", "*.png"))):
        name = os.path.basename(p)
        if not any(g in name for g in genders):
            continue
        style = os.path.basename(os.path.dirname(p))
        if styles and style not in styles:
            continue
        out.append(p)
    return out


def paint_file(path: str, dry: bool = False):
    """Returns (merged_pixels, changed, colors) for one texture."""
    im = Image.open(path)
    size = im.size
    a = np.array(im.convert("RGBA"))
    s = P.scale_of(size[0])
    merged = P.merge_overlay(a, s)
    before = a.copy()
    colors = P.repaint(a, s)
    changed = bool((a != before).any())
    if changed and not dry:
        # Palette ("P") files simply become RGBA: the ramp needs more colours than their
        # palette holds, and Minecraft loads both the same way.
        out = Image.fromarray(a, "RGBA")
        buf = io.BytesIO()
        out.save(buf, "PNG", optimize=True)
        with open(path, "wb") as fh:
            fh.write(buf.getvalue())
    return merged, changed, colors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma separated style folders to process")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    files = texture_files(tuple(args.only.split(",")) if args.only else None)
    n_merged = n_changed = 0
    merged_files = 0
    for p in files:
        merged, changed, colors = paint_file(p, args.dry_run)
        n_merged += merged
        n_changed += changed
        merged_files += bool(merged)
        print(f"{os.path.relpath(p, ROOT):64s} {'paint' if changed else 'same ':5s} overlay px={merged}")
    print(f"\n{len(files)} textures, {n_changed} modified, {merged_files} had a clothing layer folded in "
          f"({n_merged} pixels)")


if __name__ == "__main__":
    main()
