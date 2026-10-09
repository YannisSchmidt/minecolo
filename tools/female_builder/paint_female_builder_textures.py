#!/usr/bin/env python3
"""
Paint the texture areas used by the new parts of ``FemaleBuilderModel`` (minecolo fork):

* the yellow construction hard hat  (parts shell / dome / ridge / brim / peak)
* the leather tool belt             (part toolBelt)
* the rolled-up blueprint           (part blueprintRoll)

The female builder textures are 128x64. The left 64x64 is the regular humanoid skin,
the right half holds the extra parts (hair, bag, hammer, rulers, ...). The new parts
only use texture space that was fully transparent in every style/skin variant, plus the
rectangle (64,28)-(88,34) that belonged to the removed flat cap.

UV rectangles (texOffs + box size => occupied rectangle, Minecraft box layout):

    part            texOffs   box        rectangle (x0,y0)-(x1,y1)
    brim            (88, 0)   10x1x10    (88, 0)-(128,11)
    shell           (64,11)    8x4x8     (64,11)-( 96,23)
    dome            (96,11)    6x2x6     (96,11)-(120,19)
    ridge           (96,19)    2x1x8     (96,19)-(116,28)
    peak            (64,23)    8x1x2     (64,23)-( 84,26)
    blueprintRoll  (120,11)    2x10x2   (120,11)-(128,23)
    toolBelt        (64,28)    8x2x4     (64,28)-( 88,34)   <- old cap area

The script is idempotent: running it twice gives the same result.

Usage (from the repository root)::

    python3 tools/female_builder/paint_female_builder_textures.py            # paint all 32 textures
    python3 tools/female_builder/paint_female_builder_textures.py --only default
    python3 tools/female_builder/paint_female_builder_textures.py --layout-png /tmp/uv_layout.png
"""
from __future__ import annotations

import argparse
import glob
import os
import random
import sys
from typing import Dict, Tuple

from PIL import Image, ImageDraw

RGB = Tuple[int, int, int]

DEFAULT_TEXTURE_DIR = os.path.join("src", "main", "resources", "assets", "minecolonies", "textures", "entity", "citizen")
TEXTURE_GLOB = os.path.join("*", "builderfemale1_*.png")
TEX_W, TEX_H = 128, 64

# ----------------------------------------------------------------------------- palette
# hard hat (safety yellow)
Y_HIGHLIGHT: RGB = (255, 232, 120)
Y_LIGHT: RGB = (253, 214, 64)
Y_BASE: RGB = (240, 190, 38)
Y_SHADE: RGB = (214, 160, 28)
Y_DARK: RGB = (168, 118, 22)
Y_EDGE: RGB = (140, 96, 16)
# leather belt
B_LIGHT: RGB = (96, 64, 40)
B_BASE: RGB = (74, 48, 30)
B_DARK: RGB = (50, 32, 20)
BRASS_LIGHT: RGB = (226, 192, 104)
BRASS: RGB = (201, 164, 72)
BRASS_DARK: RGB = (136, 104, 40)
# blueprint roll
PAPER: RGB = (234, 223, 196)
PAPER_SHADE: RGB = (208, 194, 162)
PAPER_DARK: RGB = (166, 150, 120)
BLUE_LINE: RGB = (86, 122, 186)
STRING: RGB = (122, 88, 54)


def box_faces(u: int, v: int, w: int, h: int, d: int) -> Dict[str, Tuple[int, int, int, int]]:
    """Face rectangles (x0, y0, x1, y1), exclusive end, of a w*h*d box at texOffs(u, v)."""
    return {
        "top": (u + d, v, u + d + w, v + d),
        "bottom": (u + d + w, v, u + d + 2 * w, v + d),
        "right": (u, v + d, u + d, v + d + h),
        "front": (u + d, v + d, u + d + w, v + d + h),
        "left": (u + d + w, v + d, u + 2 * d + w, v + d + h),
        "back": (u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h),
    }


def bounds(u: int, v: int, w: int, h: int, d: int) -> Tuple[int, int, int, int]:
    return u, v, u + 2 * d + 2 * w, v + d + h


# part name -> (texOffs u, v, w, h, d)
PARTS = {
    "brim": (88, 0, 10, 1, 10),
    "shell": (64, 11, 8, 4, 8),
    "dome": (96, 11, 6, 2, 6),
    "ridge": (96, 19, 2, 1, 8),
    "peak": (64, 23, 8, 1, 2),
    "blueprintRoll": (120, 11, 2, 10, 2),
    "toolBelt": (64, 28, 8, 2, 4),
}


class Painter:
    def __init__(self, img: Image.Image, seed: int = 1399):
        self.px = img.load()
        self.rng = random.Random(seed)  # deterministic => identical result for all 32 textures

    def fill(self, rect, color: RGB, jitter: int = 0):
        x0, y0, x1, y1 = rect
        for y in range(y0, y1):
            for x in range(x0, x1):
                c = color
                if jitter:
                    j = self.rng.randint(-jitter, jitter)
                    c = tuple(max(0, min(255, ch + j)) for ch in color)
                self.px[x, y] = (c[0], c[1], c[2], 255)

    def set(self, x: int, y: int, color: RGB):
        self.px[x, y] = (color[0], color[1], color[2], 255)

    def row(self, x0: int, x1: int, y: int, color: RGB):
        for x in range(x0, x1):
            self.set(x, y, color)

    def col(self, x: int, y0: int, y1: int, color: RGB):
        for y in range(y0, y1):
            self.set(x, y, color)

    def border(self, rect, color: RGB):
        x0, y0, x1, y1 = rect
        self.row(x0, x1, y0, color)
        self.row(x0, x1, y1 - 1, color)
        self.col(x0, y0, y1, color)
        self.col(x1 - 1, y0, y1, color)


def clear(img: Image.Image, rect):
    x0, y0, x1, y1 = rect
    px = img.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            px[x, y] = (0, 0, 0, 0)


# ----------------------------------------------------------------------------- painting

def paint_hard_hat(p: Painter):
    # --- shell: 8x4x8, the big part wrapping the top of the head
    f = box_faces(*PARTS["shell"])
    p.fill(f["top"], Y_BASE, jitter=4)
    p.border(f["top"], Y_LIGHT)
    p.fill(f["bottom"], Y_DARK)
    for face in ("right", "front", "left", "back"):
        x0, y0, x1, y1 = f[face]
        p.fill((x0, y0, x1, y1), Y_BASE, jitter=4)
        p.row(x0, x1, y0, Y_LIGHT)          # upper row catches the light
        p.row(x0, x1, y1 - 1, Y_SHADE)      # lower row = slightly darker band

    # --- dome: 6x2x6 on top of the shell
    f = box_faces(*PARTS["dome"])
    p.fill(f["top"], Y_LIGHT, jitter=3)
    tx0, ty0, tx1, ty1 = f["top"]
    p.fill((tx0 + 1, ty0 + 1, tx0 + 3, ty0 + 3), Y_HIGHLIGHT)  # specular blob, front-left
    p.fill(f["bottom"], Y_DARK)
    for face in ("right", "front", "left", "back"):
        x0, y0, x1, y1 = f[face]
        p.row(x0, x1, y0, Y_LIGHT)
        p.row(x0, x1, y1 - 1, Y_BASE)

    # --- ridge: 2x1x8 reinforcement running front to back
    f = box_faces(*PARTS["ridge"])
    p.fill(f["top"], Y_HIGHLIGHT)
    p.fill(f["bottom"], Y_DARK)
    for face in ("right", "front", "left", "back"):
        p.fill(f[face], Y_LIGHT)

    # --- brim: 10x1x10 all around the bottom edge
    f = box_faces(*PARTS["brim"])
    p.fill(f["top"], Y_BASE, jitter=3)
    p.border(f["top"], Y_LIGHT)
    p.fill(f["bottom"], Y_DARK)          # underside, in shadow
    for face in ("right", "front", "left", "back"):
        p.fill(f[face], Y_SHADE)         # 1px thick edge

    # --- peak: 8x1x2 small visor at the front
    f = box_faces(*PARTS["peak"])
    p.fill(f["top"], Y_BASE, jitter=3)
    tx0, ty0, tx1, ty1 = f["top"]
    p.row(tx0, tx1, ty0, Y_LIGHT)        # leading edge
    p.fill(f["bottom"], Y_DARK)
    for face in ("right", "front", "left", "back"):
        p.fill(f[face], Y_SHADE)


def paint_tool_belt(p: Painter):
    f = box_faces(*PARTS["toolBelt"])
    p.fill(f["top"], B_LIGHT)
    p.fill(f["bottom"], B_DARK)
    for face in ("right", "front", "left", "back"):
        x0, y0, x1, y1 = f[face]
        p.fill((x0, y0, x1, y1), B_BASE, jitter=5)
        p.row(x0, x1, y0, B_LIGHT)       # top edge highlight
    # buckle in the middle of the front face (2x2 brass)
    fx0, fy0, fx1, fy1 = f["front"]
    bx = fx0 + (fx1 - fx0) // 2 - 1
    p.set(bx, fy0, BRASS_LIGHT)
    p.set(bx + 1, fy0, BRASS)
    p.set(bx, fy0 + 1, BRASS)
    p.set(bx + 1, fy0 + 1, BRASS_DARK)
    # belt loops / stitching: a dark column on each side face and at the back
    rx0, ry0, rx1, ry1 = f["right"]
    p.col(rx0 + 1, ry0, ry1, B_DARK)
    lx0, ly0, lx1, ly1 = f["left"]
    p.col(lx1 - 2, ly0, ly1, B_DARK)
    kx0, ky0, kx1, ky1 = f["back"]
    p.col(kx0 + 2, ky0, ky1, B_DARK)
    p.col(kx1 - 3, ky0, ky1, B_DARK)


def paint_blueprint_roll(p: Painter):
    f = box_faces(*PARTS["blueprintRoll"])
    # end caps (2x2): rolled paper spiral
    for cap in ("top", "bottom"):
        x0, y0, x1, y1 = f[cap]
        p.set(x0, y0, PAPER)
        p.set(x0 + 1, y0, PAPER_SHADE)
        p.set(x0, y0 + 1, PAPER_DARK)
        p.set(x0 + 1, y0 + 1, PAPER)
    # long sides (2x10): paper, a string tied near each end, a few blueprint lines
    for face, shade in (("right", PAPER), ("front", PAPER_SHADE), ("left", PAPER_SHADE), ("back", PAPER)):
        x0, y0, x1, y1 = f[face]
        p.fill((x0, y0, x1, y1), shade, jitter=3)
        p.row(x0, x1, y0 + 1, STRING)      # string near one end
        p.row(x0, x1, y1 - 2, STRING)      # string near the other end
    # drawing lines only on the two faces that are visible (top of the roll / outside)
    for face in ("right", "back"):
        x0, y0, x1, y1 = f[face]
        p.row(x0, x1, y0 + 4, BLUE_LINE)
        p.set(x0, y0 + 6, BLUE_LINE)
        p.set(x0 + 1, y0 + 7, BLUE_LINE)


def paint(img: Image.Image) -> Image.Image:
    if img.size != (TEX_W, TEX_H):
        raise ValueError(f"unexpected texture size {img.size}, expected {(TEX_W, TEX_H)}")
    img = img.convert("RGBA")
    for part in PARTS.values():
        clear(img, bounds(*part))  # start from a clean, fully transparent rectangle (idempotent)
    p = Painter(img)
    paint_hard_hat(p)
    paint_tool_belt(p)
    paint_blueprint_roll(p)
    return img


# ----------------------------------------------------------------------------- debug layout

def layout_png(texture_path: str, out_path: str, scale: int = 8):
    img = Image.open(texture_path).convert("RGBA")
    bg = Image.new("RGBA", img.size, (60, 60, 60, 255))
    bg.alpha_composite(img)
    big = bg.resize((img.width * scale, img.height * scale), Image.NEAREST)
    d = ImageDraw.Draw(big)
    colors = {"brim": (255, 0, 0), "shell": (0, 255, 0), "dome": (0, 160, 255), "ridge": (255, 0, 255),
              "peak": (255, 160, 0), "blueprintRoll": (0, 255, 255), "toolBelt": (255, 255, 0)}
    for name, part in PARTS.items():
        x0, y0, x1, y1 = bounds(*part)
        d.rectangle((x0 * scale, y0 * scale, x1 * scale - 1, y1 * scale - 1), outline=colors[name], width=2)
        d.text((x0 * scale + 3, y0 * scale + 2), name, fill=colors[name])
    big.save(out_path)
    print("wrote", out_path)


# ----------------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--textures-dir", default=DEFAULT_TEXTURE_DIR, help="textures/entity/citizen directory")
    ap.add_argument("--only", default=None, help="restrict to one style folder (e.g. 'default')")
    ap.add_argument("--dry-run", action="store_true", help="list the files but do not write")
    ap.add_argument("--layout-png", default=None, help="write an upscaled debug image of <style default>/builderfemale1_a.png with the UV rectangles")
    a = ap.parse_args(argv)

    pattern = os.path.join(a.textures_dir, a.only or "*", "builderfemale1_*.png")
    files = sorted(glob.glob(pattern))
    if not files:
        print("no texture found with pattern", pattern, file=sys.stderr)
        return 1
    for f in files:
        if a.dry_run:
            print("would paint", f)
            continue
        img = Image.open(f)
        out = paint(img)
        out.save(f, optimize=True)
        print("painted", f)
    if a.layout_png:
        ref = os.path.join(a.textures_dir, "default", "builderfemale1_a.png")
        layout_png(ref, a.layout_png)
    return 0


if __name__ == "__main__":
    sys.exit(main())
