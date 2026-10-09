#!/usr/bin/env python3
"""Geometry of the bust of the adult female citizen models: two balls, each built as a
stack of bands, every band built as a set of concentric rings.

A single ``addBox`` is a brick; a sphere is what you get when you stack bricks whose
size follows a circle.  Two profiles are therefore needed:

* **vertically** the lobe is cut into ``nbands`` bands of ``band_h`` (they overlap a
  little so that no two faces are ever coplanar, which is what makes z-fighting), and
  the band at the vertical distance ``t`` from the centre is multiplied by
  ``V(t) = sqrt(1 - (t/Rv)^2)`` -- that rounds the silhouette seen from the side;
* **in depth** every band is a set of nested rings, ring *k* ``W[k]`` wide and
  ``P[k]`` in front of the original chest plane -- that rounds the silhouette seen from
  above, and it is also what makes the front view read as a volume: every ring samples
  its own row of the painted texture, so the tip comes out lighter than the base.

The two lobes are separate boxes from the start, ``cleavage`` apart, which is what the
single upstream cube could never do.

Everything is expressed in the frame of the ``"breast"`` part, relative to the original
Blockbench cube (``cx``/``cy`` its centre, ``front0`` the plane of its front face), so a
per-model quirk -- the courier sits a bit lower -- is handled by the same code.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Bust:
    """Parameters of one bust.  All numbers are 1/16 of a block, part space.

    ``rings`` is ``(width, protrusion)`` from the ring glued to the torso to the ring at
    the tip of the ball.  The first ring is the only one narrow enough to stay inside the
    width of the torso -- it is also the only one whose box reaches back into the chest,
    so it is the only one that could cut through the arm that hangs there.  The rings in
    front of it may be wider: they sit at ``z`` well in front of the arms, so they only
    hide them, which is what a bust that is wider than the body is supposed to do.
    """

    rings: tuple = ((3.10, 1.50), (4.60, 2.90), (5.40, 4.90),
                    (5.20, 6.90), (4.10, 8.60), (2.20, 9.90))
    nbands: int = 5
    band_h: float = 1.20      # height of a band
    band_step: float = 1.12   # ... and the pitch, so bands overlap by band_h - band_step
    radius_v: float = 2.75    # vertical radius of a lobe: how fast it rounds off
    cleavage: float = 1.10    # gap between the two lobes
    cleavage_step: float = 0.05   # opened up ring by ring, to keep inner faces non coplanar
    back: float = 2.2         # how deep the base ring is buried in the torso
    ring_eps: float = 0.14    # a ring overlaps the one behind it by that much (no coplanar faces)
    tilt: float = -0.14       # rad, pitch of the whole piece (negative = pointing up)
    u: int = 64               # the texture rectangle every box samples
    v: int = 49

    # ---------------------------------------------------------------- profile
    def v_factor(self, i: int) -> float:
        """Vertical roundness of band ``i``: 1.0 in the middle, smaller near the neck."""
        t = (i - (self.nbands - 1) / 2.0) * self.band_step
        s = 1.0 - (t / self.radius_v) ** 2
        return math.sqrt(s) if s > 0.0 else 0.0

    def stack_height(self) -> float:
        return self.band_step * (self.nbands - 1) + self.band_h

    # ---------------------------------------------------------------- geometry
    def cells(self, cx: float, cy: float, front0: float):
        """Yield every box as ``(x, y, z, w, h, d)``, left lobe then right lobe, ring by ring."""
        total = self.stack_height()
        y0 = cy - total / 2.0
        out = []
        for i in range(self.nbands):
            v = max(0.18, self.v_factor(i))
            y = y0 + i * self.band_step
            prev_p = -self.back                 # protrusion of the plane the base ring is buried in
            for k, (w_r, p_r) in enumerate(self.rings):
                w = round(w_r * v, 3)
                p = round(p_r * v, 3)
                z = round(front0 - p, 3)
                d = round(p - prev_p + self.ring_eps, 3)
                gap = self.cleavage + self.cleavage_step * k
                for sgn in (-1.0, 1.0):
                    bx = round(cx + sgn * (w / 2.0 + gap / 2.0) - w / 2.0, 3)
                    out.append((bx, round(y, 3), z, w, self.band_h, d))
                prev_p = p
        return out

    # ---------------------------------------------------------------- texture
    def uv_need(self, cx: float, front0: float):
        """How much of the texture rectangle the whole design really samples.

        ``du`` is the widest ``2 * depth + 2 * width`` of a box (the strip of its four side
        faces), ``dv`` the lowest row it reaches (``depth + band height``); the repaint
        covers ``U/V/UW/VH`` of bust_paint, and ``verify_bust.py`` checks the two agree.
        """
        du = dv = 0.0
        for (x, y, z, w, h, d) in self.cells(cx, 0.0, front0):
            du = max(du, 2 * d + 2 * w)
            dv = max(dv, d + h)
        return round(du, 2), round(dv, 2)
