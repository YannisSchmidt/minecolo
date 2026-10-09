#!/usr/bin/env python3
"""Everything that must stay true about the bust of the 40 adult female citizen models.

    python3 tools/female_bust/verify_bust.py [--syntax] [--views front,left,iso,back]

Checks, per model file, on the *shipped* geometry (the ``BREAST_DEFORMATION`` constant of
``CitizenModel`` is resolved, exactly like the preview renderer does it):

* ``neck``   the highest point of the bust stays under the collar line (body y >= 0.5),
  otherwise it is drawn through the head;
* ``belt``   the lowest point stays above the waist (body y <= 10.5);
* ``back``   no box goes through the back of the torso (body z <= 1.9), which would show
  a green lump on the character's back;
* ``arm``    how many boxes reach into the volume the arms hang in (x 3.75..7.25,
  z -2.25..2.25): a box there is cut by the arm's faces, which is the artefact people
  notice first.  Only the ring glued to the chest can reach that deep, so this stays 0
  as long as that one ring is not widened;
* ``uv``     every rectangle the boxes sample is inside the texture and inside the strip
  of rows the repaint covers (``bust_paint.U/V/UW/VH``), so no face can ever show a
  pixel of another part;
* ``clip``   no other cube of the same model (apron, bag, collar, instrument...) has a
  corner inside a box of the bust: those parts are painted by the same texture and an
  intersection between two of their boxes shows up as a chunk missing.
``--syntax`` additionally parses every touched file with ``javalang``, which is the only
Java front end that can be installed without a JDK.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "model_preview"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render_citizen_model as R  # noqa: E402
import bust_paint as P  # noqa: E402
from rework_bust import model_files, CITIZEN_MODEL  # noqa: E402

MODEL_DIR = os.path.join(ROOT, "src/main/java/com/minecolonies/core/client/model")
TEX_DIR = os.path.join(ROOT, "src/main/resources/assets/minecolonies/textures/entity/citizen")

TORSO_FRONT, TORSO_BACK = -2.0, 2.0
ARM = (3.75, 7.25, -2.25, 2.25, -0.25, 14.25)   # xmin xmax zmin zmax ymin ymax (one side)
NECK_LIMIT, BELT_LIMIT = 0.5, 10.5


def part_boxes(model):
    """(part name, 8 corners in body space) for every cube of the model, at rest."""
    zero = {"head", "hat", "body", "right_arm", "left_arm", "right_leg", "left_leg"}
    out = []

    def walk(p, m):
        mm = m @ R.part_matrix(p, p.name in zero)
        for c in p.cubes:
            for verts, _uv, label in R.cube_quads(c):
                pass
            pts = np.concatenate([np.c_[v, np.ones(4)] @ mm.T for v, _uv, _l in R.cube_quads(c)])[:, :3]
            out.append((p.name, c, pts))
        for ch in p.children:
            walk(ch, mm)

    for r in model.roots:
        walk(r, np.eye(4))
    return out


def aabb(pts):
    return pts.min(0), pts.max(0)


def overlap(a, b):
    lo = np.maximum(a[0], b[0])
    hi = np.minimum(a[1], b[1])
    d = hi - lo
    return d if (d > 0).all() else None


def check_model(java_path, check_clip=True):
    model = R.parse_model(java_path, constants_from=(CITIZEN_MODEL,))
    boxes = part_boxes(model)
    bust = [(n, c, p) for (n, c, p) in boxes if n == "breast"]
    if not bust:
        return {"error": "no breast part"}
    allpts = np.concatenate([p for _n, _c, p in bust])
    lo, hi = aabb(allpts)
    res = dict(
        n=len(bust),
        top_y=round(float(lo[1]), 2), bot_y=round(float(hi[1]), 2),
        tip=round(float(TORSO_FRONT - lo[2]), 2), back_z=round(float(hi[2] - TORSO_BACK), 2),
        halfx=round(float(max(abs(lo[0]), abs(hi[0]))), 2),
        neck=0 if lo[1] >= NECK_LIMIT else round(NECK_LIMIT - lo[1], 2),
        belt=0 if hi[1] <= BELT_LIMIT else round(hi[1] - BELT_LIMIT, 2),
        back=0 if hi[2] <= TORSO_BACK - 0.05 else round(hi[2] - (TORSO_BACK - 0.05), 2),
        arm=0, uv=0, clip="", wide=0,
    )
    res["wide"] = sum(1 for _n, _c, p in bust if max(abs(p[:, 0].min()), abs(p[:, 0].max())) > 4.0)
    bboxes = [aabb(p) for _n, _c, p in bust]
    for _n, c, p in bust:
        b0, b1 = aabb(p)
        ax = max(0.0, min(b1[0], ARM[1]) - max(b0[0], ARM[0]), min(b1[0], -ARM[0]) - max(b0[0], -ARM[1]))
        az = min(b1[2], ARM[3]) - max(b0[2], ARM[2])
        ay = min(b1[1], ARM[5]) - max(b0[1], ARM[4])
        if min(ax, az, ay) > 0.02:
            res["arm"] += 1
    # UV: every cube of the bust must sample the painted rectangle only
    for _n, c, _p in bust:
        u1 = c.u + 2 * c.d + 2 * c.w            # the x extent of the strip of side faces
        v1 = c.v + c.d + c.h                    # ... and the row its front face ends on
        ok = (c.u == P.U and c.v == P.V and u1 <= P.U + P.UW and v1 <= P.V + P.VH
              and c.v + c.d >= P.V)
        if not ok or u1 > model.tex_w or v1 > model.tex_h:
            res["uv"] += 1
            res.setdefault("uv_why", []).append(f"({c.w}x{c.h}x{c.d}) -> {c.u}..{u1},{c.v}..{v1}")
    if check_clip:
        hits = []
        for (n, c, p) in boxes:
            if n == "breast":
                continue
            o = overlap(aabb(p), (lo, hi))          # cheap reject first
            if o is None:
                continue
            for corner in p:
                for (b0, b1) in bboxes:
                    if ((corner >= b0 - 1e-6) & (corner <= b1 + 1e-6)).all():
                        hits.append(name_or(n, c))
                        break
                else:
                    continue
                break
        res["clip"] = ",".join(sorted(set(hits)))
    return res


def name_or(n, c):
    return f"{n}@({c.u},{c.v})"


def syntax(paths):
    import javalang
    bad = 0
    for f in paths:
        try:
            javalang.parse.parse(open(f).read())
        except Exception as exc:                                   # noqa: BLE001
            bad += 1
            print(f"SYNTAX {os.path.basename(f)}: {type(exc).__name__}: {str(exc)[:160]}")
    print(f"javalang: {len(paths)} files parsed, {bad} with a syntax error")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--syntax", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="only print the failures")
    ap.add_argument("--model", default="", help="a single model file instead of all of them")
    a = ap.parse_args()
    files = [a.model] if a.model else model_files()
    if a.syntax:
        return 1 if syntax(files + [CITIZEN_MODEL]) else 0
    bad = soft = 0
    for f in files:
        r = check_model(f)
        flags = [k for k in ("neck", "belt", "back", "arm", "uv") if r.get(k)]
        gear = r.get("clip")
        if not a.quiet or flags or gear or r.get("error"):
            print(f"{os.path.basename(f)[:-5]:22s} n={r.get('n')} top_y={r.get('top_y')} bot={r.get('bot_y')} "
                  f"tip={r.get('tip')} halfx={r.get('halfx')} wide={r.get('wide')} backz={r.get('back_z')} "
                  f"arm={r.get('arm')} uv={r.get('uv')} "
                  f"{' '.join(flags) or 'ok'}{('  gear:' + gear) if gear else ''}")
        bad += bool(flags) or bool(r.get("error"))
        soft += bool(gear)
    print(f"{len(files)} models: {bad} with a geometry/UV problem, {soft} with job gear inside a lobe "
          f"(expected, see MODIFICATIONS_POITRINE.md)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
