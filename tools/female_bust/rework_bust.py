#!/usr/bin/env python3
"""Rewrite the ``"breast"`` cube of every adult female citizen model.

Upstream that cube is a single flat 8x3x3 box inflated with a ``CubeDeformation``: a
plank with no cleft, whose "clothing" copy (a second box, 0.25 thicker) drew a hard
shell edge around the chest and leaked stray texture pixels.  This script replaces that
pair with two balls -- each built out of a stack of bands, every band out of concentric
rings -- and leaves the size of the whole thing to ``CitizenModel.BREAST_DEFORMATION``
plus the numbers in ``bust_shape.Bust``.  See ``bust_shape.py`` for the profiles.

The script is idempotent and recovers the frame of the chest piece (centre and front
plane of the original Blockbench box) from the file itself, so per-model quirks -- the
courier sits 0.4 px lower, the alchemist's statement is split over several lines -- are
preserved, and re-running it after a tweak to ``Bust`` rewrites the same files.

    python3 tools/female_bust/rework_bust.py [--check-only] [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bust_shape import Bust  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_DIR = os.path.join(ROOT, "src/main/java/com/minecolonies/core/client/model")
CITIZEN_MODEL = os.path.join(ROOT, "src/main/java/com/minecolonies/api/client/render/modeltype/CitizenModel.java")

BUST = Bust()

STMT_RE = re.compile(
    r'(?P<indent>[ ]*)PartDefinition (?P<var>\w+)\s*=\s*(?P<parent>\w+)\.addOrReplaceChild\(\s*"breast",'
    r'.*?PartPose\.offsetAndRotation\((?P<pose>[^)]*)\)\s*\);',
    re.S,
)
NUM = r"-?\d+(?:\.\d+)?F?"


def _f(x) -> float:
    return round(float(str(x).rstrip("Ff")), 4)


def fmt(v: float) -> str:
    """Java float literal, e.g. 3.0 -> "3.0F", -0.5 -> "-0.5F", 1.3938 -> "1.3938F"."""
    s = f"{round(float(v), 4):.4f}".rstrip("0")
    return (s + "0" if s.endswith(".") else s) + "F"


def model_files():
    out = []
    for f in sorted(glob.glob(os.path.join(MODEL_DIR, "Female*.java"))):
        if "Child" in os.path.basename(f):
            continue
        out.append(f)
    return out


def build_boxes(bust: Bust, cx: float, cy: float, front0: float):
    """Every box of the bust as ``(x, y, z, w, h, d)``, in the frame of the part."""
    return bust.cells(cx, cy, front0)


def original_geometry(src: str, bust: Bust = BUST):
    """The canonical frame of the chest piece: ``(cx, cy, front0, pose, already_done)``.

    ``cx``/``cy`` are the centre of the original Blockbench box and ``front0`` the plane
    of its front face; every band is laid out relative to those three numbers, which is
    what keeps the per-model quirks (the courier sits 0.4 px lower, the alchemist's
    statement is split over three lines).

    The frame is *inverted* out of whatever the file currently holds, which makes this
    script idempotent and lets it upgrade a file written by an older layout of itself:
    ``LAY_V1`` is the eight-band bust of the first revision of this fork.  The first box
    of the statement is enough in every case, because the boxes are laid out from the
    centre of the stack outwards.
    """
    m = STMT_RE.search(src)
    if not m:
        raise SystemExit("no breast statement found")
    raw = re.findall(r"addBox\(([^)]*)\)", m.group(0))
    if not raw:
        raise SystemExit("no addBox inside the breast statement")
    boxes = [[_f(v) for v in a.split(",")[:6]] for a in raw]
    pose = [_f(v) for v in m.group("pose").split(",")]
    offs = re.findall(r"texOffs\((-?\d+),\s*(-?\d+)\)", m.group(0))
    x, y, z, w, h, d = boxes[0]                          # left lobe, top band, ring glued to the chest

    n_here = 2 * bust.nbands * len(bust.rings)
    if len(boxes) == n_here and all(o == (str(bust.u), str(bust.v)) for o in offs):
        v0 = max(0.18, bust.v_factor(0))
        cx = x + w + bust.cleavage / 2.0                 # invert bx = cx - w - gap/2, w = W0*v0 already applied
        cy = y + bust.stack_height() / 2.0
        front0 = z + bust.rings[0][1] * v0                # invert z = front0 - P0*v0
        return round(cx, 4), round(cy, 4), round(front0, 4), pose, True
    if len(boxes) == LAY_V1[0] and all(o == ("64", "49") for o in offs):
        nb, step, hgt, gap, rec0 = LAY_V1[1:]
        cx = x + w + gap / 2.0
        cy = y + (step * (nb - 1) + hgt) / 2.0
        front0 = z - rec0                                 # that layout pushed band 0 *back* by rec0
        return round(cx, 4), round(cy, 4), round(front0, 4), pose, True
    return x + w / 2.0, y + h / 2.0, z, pose, False


# (boxes per side... ) the eight-band layout of the first revision: n boxes, bands,
# band step, band height, cleavage, recess of the top band (positive = pushed back).
LAY_V1 = (8, 4, 1.0, 1.05, 0.5, 0.6)


def build_statement(cx, cy, front0, pose, bust: Bust = BUST, grow="BREAST_DEFORMATION",
                     var="breast", parent="bipedBody", indent="        "):
    """The whole bust, as one Java statement."""
    lines = []
    for (x, y, z, w, h, d) in build_boxes(bust, cx, cy, front0):
        lines.append(f".texOffs({bust.u}, {bust.v}).addBox({fmt(x)}, {fmt(y)}, {fmt(z)}, "
                     f"{fmt(w)}, {fmt(h)}, {fmt(d)}, {grow})")
    px, py, pz = pose[0], pose[1], pose[2]
    body = ("\n" + indent + "  ").join(lines)
    return (
        f"{indent}PartDefinition {var} = {parent}.addOrReplaceChild(\"breast\", CubeListBuilder.create()\n"
        f"{indent}  {body},\n"
        f"{indent}  PartPose.offsetAndRotation({fmt(px)}, {fmt(py)}, {fmt(pz)}, "
        f"{fmt(bust.tilt)}, 0.0F, 0.0F));\n"
    )


def patch_file(path: str, dry: bool, bust: Bust = BUST) -> str:
    src = open(path).read()
    cx, cy, front0, pose, done = original_geometry(src, bust)
    m = STMT_RE.search(src)
    head = src[:m.start("indent")]
    tail = src[m.end():]
    new = build_statement(cx, cy, front0, pose, bust, "BREAST_DEFORMATION",
                          m.group("var"), m.group("parent"), m.group("indent"))
    if tail.startswith("\n"):
        tail = tail[1:]
    out = head + new + tail
    if not dry:
        open(path, "w").write(out)
    return out


CONST_BLOCK = '''    /**
     * Inflation (in 1/16 of a block, per axis x / y / z of a cube) applied to every box of the bust of the adult
     * female citizen models. The Blockbench exports put a single flat 8x3x3 cube here with
     * {@code new CubeDeformation(0.0F)}; the models of this fork build the chest out of two balls, each of them a
     * stack of bands and every band a set of concentric rings (see
     * {@link com.minecolonies.core.client.model.FemaleCitizenModel}), and all of them use this constant, so this
     * single line still sets how far the bust sticks out. Growing a box along z only pushes its faces forward, it
     * stretches no texture, so that is the axis to grow on: 0.0F keeps the shape exactly as the bands describe it,
     * 1.0F adds two thirds of a block to the projection. The other two axes have to stay at 0: the arms hang at
     * |x| = 4 and would cut through a box grown along x, and the top band of a lobe already ends 2 px under the
     * collar.
     */
    public static final CubeDeformation BREAST_DEFORMATION = new CubeDeformation(0.0F, 0.0F, 0.35F);
'''


def patch_constants(dry: bool) -> bool:
    """Replace the BREAST_DEFORMATION declaration (javadoc included) by the new one."""
    src = open(CITIZEN_MODEL).read()
    decl = "public static final CubeDeformation BREAST_DEFORMATION"
    i = src.find(decl)
    if i < 0:
        raise SystemExit("could not find the BREAST_DEFORMATION declaration in CitizenModel.java")
    start = src.rindex("/**", 0, i)                      # start of its javadoc
    start = src.rindex("\n", 0, start) + 1               # start of the line
    end = src.index(";", i) + 1
    end = src.index("\n", end) + 1
    out = src[:start] + CONST_BLOCK + src[end:]
    changed = out != src
    if changed and not dry:
        open(CITIZEN_MODEL, "w").write(out)
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--check-only", action="store_true", help="only report what the models contain")
    args = ap.parse_args()

    if not args.check_only:
        if patch_constants(args.dry_run):
            print(" CitizenModel.java: constants updated" if not args.dry_run else " CitizenModel.java: would update constants")

    n = 0
    for f in model_files():
        src = open(f).read()
        cx, cy, front0, pose, done = original_geometry(src)
        new = patch_file(f, args.dry_run or args.check_only)
        nb = new.count(f".texOffs({BUST.u}, {BUST.v}).addBox")
        uses_const = "BREAST_DEFORMATION)" in new
        if args.check_only:
            flag = "[deja reecrit]" if done else ""
            print(f"{os.path.basename(f):32s} centre=({cx}, {cy}) front={front0} pose={pose[:3]} "
                  f"rot={pose[3]} {flag}")
            continue
        n += 1
        again = "  (reecrit a l'identique)" if done else ""
        print(f"{os.path.basename(f):32s} {nb:2d} boxes  constants={'ok' if uses_const else 'MISSING'}{again}")
    if not args.check_only:
        print(f"patched {n} model files")


if __name__ == "__main__":
    main()
