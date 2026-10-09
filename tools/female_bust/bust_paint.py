#!/usr/bin/env python3
"""Repaint helpers for the chest area of the female citizen textures.

The bust cubes all sample ``texOffs(64, 49)`` of a 128x64 citizen texture, i.e. the
rectangle ``x 64..85, y 49..54`` (times two on the 256x128 textures some styles ship).
In that rectangle the original Blockbench layout uses:

* rows 49..51 for the faces looking up/down (``x 67..82``),
* rows 52..54 for the four side faces, the one the player sees being ``x 67..74``.

The eight bands the bust is now built from are 1 px tall with depth 2..5, so a band
samples exactly *one* row of that rectangle (row ``49 + depth``), at a different x
offset per band.  Repainting each row as a single colour, spread over the whole width,
is therefore what makes seams impossible while still showing the shading the original
texture had on the chest.  A gentle extra ramp adds the roundness cue.
"""
from __future__ import annotations

import numpy as np

U, V, UW, VH = 64, 49, 22, 6       # the rectangle sampled by an 8x3x3 cube
OVERLAY_DV = 6                     # the old clothing cube used the same layout, 6 rows lower
BOX_D, BOX_W = 3, 8                # its depth and width, which is where its faces sit

# Extra brightness applied to rows 49..54 (top light, bottom in shadow).
RAMP = [1.06, 1.03, 1.00, 1.00, 0.95, 0.88]


def scale_of(w: int) -> int:
    """Texture scale (MineColonies ships 1x and 2x citizen textures)."""
    if w == 128:
        return 1
    if w == 256:
        return 2
    raise ValueError(f"unexpected citizen texture width {w}")


def _row_colors(region: np.ndarray, s: int) -> np.ndarray:
    """Median colour of the chest-facing columns of every row of the rectangle."""
    x0, x1 = BOX_D * s, (BOX_D + BOX_W) * s
    out = np.zeros((6, 3))
    for r in range(6):
        rows = region[r * s:(r + 1) * s, x0:x1]
        solid = rows[rows[..., 3] > 25]
        if solid.size:
            out[r] = np.median(solid[..., :3], axis=0)
        else:                                    # nothing painted there (rare): reuse the row below/above
            out[r] = out[r - 1] if r else np.array([170.0, 140.0, 140.0])
    for r in range(1, 6):                          # fill gaps left by unpainted rows
        if not region[r * s:(r + 1) * s].any():
            out[r] = out[r - 1]
    return np.clip(out, 0, 255)


def merge_overlay(a: np.ndarray, s: int) -> int:
    """Fold the old clothing cube into the chest rectangle (it is drawn on top of it).

    Only when that layer really is painted -- for most jobs it holds nothing but a
    couple of stray pixels, which is exactly what used to show up as specks on the
    chest.  Returns the number of pixels taken over.
    """
    base = a[V * s: V * s + VH * s, U * s: U * s + UW * s]
    over = a[(V + OVERLAY_DV) * s: (V + OVERLAY_DV) * s + VH * s, U * s: U * s + UW * s]
    mask = over[..., 3] > 25
    if mask.sum() < 12 * s * s:
        return 0
    before = base.copy()
    base[mask] = over[mask]
    return int((base[..., :3] != before[..., :3]).any(-1).sum())


def repaint(a: np.ndarray, s: int) -> np.ndarray:
    """Repaint the chest rectangle of ``a`` in place, return the 6 colours used."""
    region = a[V * s: V * s + VH * s, U * s: U * s + UW * s]
    colors = _row_colors(region, s) * np.array(RAMP, dtype=float)[:, None]
    colors = np.clip(colors, 0, 255).astype(np.uint8)
    for r in range(6):
        region[r * s:(r + 1) * s, :, :3] = colors[r]
        region[r * s:(r + 1) * s, :, 3] = 255
    return colors
