#!/usr/bin/env python3
"""Rewrite the ``"breast"`` cube of every adult female citizen model.

Before this script a female chest was a single 8x3x3 box, inflated with a
``CubeDeformation``: it looked like a plank and its "clothing" copy (the second box,
0.25 thicker) drew a hard shell edge around it, occasionally showing stray pixels of
the texture.  This script replaces that pair of boxes with eight thin bands that build
two rounded lobes, and tilts the piece a little less (``-0.4363`` rad instead of
``-0.5236``) so the bust points forward instead of up.

Per band, top to bottom:

    (width, depth, recess)  depth picks which row of the painted texture ramp the front
                             face samples (higher row index = darker), recess pulls the
                             band back from the original front plane, which is what
                             rounds the silhouette.

The band heights add up to the original 3 px, so the bust never reaches the neck.
Everything still samples ``texOffs(64, 49)`` and ``BREAST_DEFORMATION``, i.e. the size
stays a single knob and no UV rectangle moves (see ``paint_textures.py``, which
repaints that rectangle so the flat colour stretches cleanly).

    python3 tools/female_bust/rework_bust.py [--check-only] [--dry-run]
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_DIR = os.path.join(ROOT, "src/main/java/com/minecolonies/core/client/model")
CITIZEN_MODEL = os.path.join(ROOT, "src/main/java/com/minecolonies/api/client/render/modeltype/CitizenModel.java")

# Bands of one side, top -> bottom: (width, texture-depth, recess in front of the original plane)
BANDS = [
    (3.4, 2, 0.6),
    (3.8, 3, -0.5),
    (3.8, 4, -1.4),
    (3.0, 5, -0.2),
]
BAND_H = 1.05         # height of a band...
BAND_STEP = 1.0       # ...and how far the next one starts: the 0.05 they overlap by is what
                      # keeps two faces of neighbouring bands from ever being exactly coplanar
                      # (coplanar = z-fighting = a shimmering line inside the cleft)
CLEAVAGE = 0.5        # gap between the two lobes, in 1/16 blocks
GAP_STEP = 0.1        # ... opened up band by band, same reason: coplanar inner faces blink
TILT = -0.4363        # rad, was -0.5236 (-30 deg) in the Blockbench export

STMT_RE = re.compile(
    r'(?P<indent>[ ]*)PartDefinition (?P<var>\w+)\s*=\s*(?P<parent>\w+)\.addOrReplaceChild\(\s*"breast",'
    r'.*?PartPose\.offsetAndRotation\((?P<pose>[^)]*)\)\s*\);',
    re.S,
)
NUM = r"-?\d+(?:\.\d+)?F?"


def _f(x) -> float:
    return round(float(str(x).rstrip("Ff")), 4)


def _fmt(v: float) -> str:
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


def stack_height() -> float:
    """Vertical span of the stack of bands (they overlap by BAND_H - BAND_STEP)."""
    return BAND_STEP * (len(BANDS) - 1) + BAND_H


def original_geometry(src: str):
    """The canonical frame of the chest piece: ``(cx, cy, front0, pose, already_done)``.

    ``cx``/``cy`` are the centre of the original Blockbench box and ``front0`` the plane of
    its front face; every band is laid out relative to those three numbers, which is what
    keeps the per-model quirks (the courier sits 0.4 px lower, the alchemist's statement is
    split over three lines).  When the file has already been rewritten by this script the
    same three numbers are recovered by inverting the first band, so re-running it after a
    tweak to ``BANDS`` gives the same file.
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
    if len(boxes) == 2 * len(BANDS) and all(o == ("64", "49") for o in offs):
        x, y, z, w, h, d = boxes[0]                      # left box of the top band
        cx = x + w + (CLEAVAGE + GAP_STEP * 0) / 2.0
        cy = y + stack_height() / 2.0
        front0 = z - BANDS[0][2]
        return cx, cy, front0, pose, True
    x, y, z, w, h, d = boxes[0]
    return x + w / 2.0, y + h / 2.0, z, pose, False


def build_statement(cx, cy, front0, pose, var="breast", parent="bipedBody", indent="        "):
    """The eight bands of the bust, as a Java statement."""
    total = stack_height()
    y = cy - total / 2.0
    lines = []
    for i, (w, d, recess) in enumerate(BANDS):
        z = front0 + recess
        gap = CLEAVAGE + GAP_STEP * i
        for sgn in (-1.0, 1.0):
            bx = cx + sgn * (w / 2.0 + gap / 2.0) - w / 2.0
            lines.append(
                f".texOffs(64, 49).addBox({_fmt(bx)}, {_fmt(y)}, {_fmt(z)}, "
                f"{_fmt(w)}, {_fmt(BAND_H)}, {_fmt(d)}, BREAST_DEFORMATION)"
            )
        y += BAND_STEP
    px, py, pz = pose[0], pose[1], pose[2]
    body = ("\n" + indent + "  ").join(lines)
    return (
        f"{indent}PartDefinition {var} = {parent}.addOrReplaceChild(\"breast\", CubeListBuilder.create()\n"
        f"{indent}  {body},\n"
        f"{indent}  PartPose.offsetAndRotation({_fmt(px)}, {_fmt(py)}, {_fmt(pz)}, "
        f"{_fmt(TILT)}, 0.0F, 0.0F));\n"
    )


def patch_file(path: str, dry: bool) -> str:
    src = open(path).read()
    cx, cy, front0, pose, done = original_geometry(src)
    m = STMT_RE.search(src)
    head = src[:m.start("indent")]
    tail = src[m.end():]
    new = build_statement(cx, cy, front0, pose, m.group("var"), m.group("parent"), m.group("indent"))
    # keep whatever followed the statement (a newline is included in `new`)
    if tail.startswith("\n"):
        tail = tail[1:]
    out = head + new + tail
    if not dry:
        open(path, "w").write(out)
    return out


CONST_BLOCK = '''    /**
     * Inflation (in 1/16 of a block, per axis x / y / z of a cube) applied to every band of the bust of the adult
     * female citizen models. The Blockbench exports put a single flat 8x3x3 cube here with
     * {@code new CubeDeformation(0.0F)}; the models in this fork build the chest out of eight thin bands (two
     * rounded lobes of four bands, see {@link com.minecolonies.core.client.model.FemaleCitizenModel}) and all of
     * them use this constant, so this single line sets the bust size of every female citizen. The x axis stays
     * small so the arms do not clip into the shape. The four bands of a lobe are 1.05 tall and step by 1.0 (they
     * overlap a little so no two faces are ever coplanar), which spans 4.05 px instead of the original 3 px, so y
     * should stay at or below ~1.0 before the top band starts to poke out of the collar.
     * {@code new CubeDeformation(0.0F)} shrinks the bust down to the untouched shape and size of the bands.
     */
    public static final CubeDeformation BREAST_DEFORMATION = new CubeDeformation(0.35F, 0.6F, 1.25F);
'''


def patch_constants(dry: bool) -> bool:
    """Replace the two BREAST_* constants (javadoc included) by the new single one."""
    src = open(CITIZEN_MODEL).read()
    decl = "public static final CubeDeformation BREAST_DEFORMATION"
    i = src.find(decl)
    if i < 0:
        raise SystemExit("could not find the BREAST_DEFORMATION declaration in CitizenModel.java")
    start = src.rindex("/**", 0, i)                      # start of its javadoc
    start = src.rindex("\n", 0, start) + 1               # start of the line
    j = src.find("public static final CubeDeformation BREAST_OVERLAY_DEFORMATION", i)
    end = src.index(";", j if j > 0 else i) + 1
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
        nb = new.count(".texOffs(64, 49).addBox")
        uses_const = "BREAST_DEFORMATION)" in new
        if args.check_only:
            flag = "[deja reecrit]" if done else ""
            print(f"{os.path.basename(f):32s} centre=({cx}, {cy}) front={front0} pose={pose[:3]} "
                  f"rot={pose[3]} {flag}")
            continue
        n += 1
        again = "  (reecrit a l'identique)" if done else ""
        print(f"{os.path.basename(f):32s} {nb:2d} bands  constants={'ok' if uses_const else 'MISSING'}{again}")
    if not args.check_only:
        print(f"patched {n} model files")


if __name__ == "__main__":
    main()
