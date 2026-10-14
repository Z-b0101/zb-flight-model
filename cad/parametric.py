#!/usr/bin/env python3
"""Parametric core for the Z!B PoC CAD (shared by airframe + systems builders).

Single source of geometry truth. ALL spatial definitions (ribs, spar, skins,
elevons, LRU placements, wire routes) derive from these functions, so a
twist/washout/sweep/taper/airfoil change propagates everywhere with one
regeneration.

Parameter schema (params.json) — the optimizer stream returns THIS schema:
  span, chord (root chord), taper, sweep_deg, washout_deg,
  twist_stations (optional [[yfrac, deg],...] overriding washout_deg),
  spar_x_frac, spar_dia, spar_slot_dia, rib_t, skin_t,
  hinge_x_frac, hinge_gap, elevon_y0, elevon_y1,
  airfoil_dat, n_ribs, hole_*
  lru: {name: {dims, mass_g, source, estimated, place: {...}}}
  wires: [{name, r, pts: [["sec", uf, vf, y], ...] or ["xyz", x, y, z], connectors}]

Coordinate frames (documented consumption contract for the twin):
  CAD : x = aft (+ toward trailing edge), y = spanwise (0 = wing centre,
        + = right wing), z = up. Units = millimetres.
  Root leading edge is at x = -0.25*chord (quarter-chord sweep puts the
  quarter-chord line through x=0 at y=0).
  x_aft_of_root_LE = x_cad + 0.25*chord_root.
"""
import json
import math
import numpy as np

import os
OUT = os.path.dirname(os.path.abspath(__file__))  # cad/ in the repo (was an absolute workspace path)

DEFAULTS = dict(
    span=900.0,
    chord=200.0,          # root chord, mm
    taper=1.0,            # tip chord / root chord
    sweep_deg=25.0,       # quarter-chord sweep (A2 winner)
    washout_deg=6.0,      # linear root->tip washout (deg at tip); ignored if twist_stations set (A2 winner)
    twist_stations=None,  # e.g. [[0.0,0.0],[0.5,-1.0],[1.0,-2.0]] (yfrac, deg)
    spar_x_frac=0.30,
    spar_dia=4.0,
    spar_slot_dia=4.2,
    rib_t=3.0,
    skin_t=3.0,
    hinge_x_frac=0.75,
    hinge_gap=0.5,
    elevon_y0=112.5,
    elevon_y1=405.0,
    airfoil_dat="mh60.dat",
    n_ribs=8,
    hole_x_fracs=(0.15, 0.42, 0.56, 0.68),
    hole_dia_frac=0.55,
    hole_min_dia=6.0,
    hole_min_wall=2.0,
    # -- battery (CG-critical LRU: placement is a design parameter) --
    battery_u=0.205,             # section fraction of pack centre (spanwise pack)
    battery_y=0.0,               # spanwise centre (0 = centreline)
    battery_orientation="spanwise",  # "spanwise" (64 mm along y) or "chordwise"
    battery_mass_g=62.0,
    battery_dims=(28.0, 64.0, 20.0),  # [dx, dy, dz] mm box (GNB 3S 650mAh)
    # -- battery hatch H1 (bottom aperture + tray + lid) --
    hatch_margin_x=3.0,          # aperture clearance around pack, chordwise (mm/side)
    hatch_margin_y=4.0,          # aperture clearance around pack, spanwise (mm/side)
    hatch_top_clearance=2.0,     # pack top to wing interior (mm, sets battery zc)
)

# Authoritative hand-edited design parameters (MBSE §4.2 "design" section).
# Everything else in params.json is "derived" (recomputed, never hand-edited).
DESIGN_KEYS = [
    "span", "chord", "taper", "sweep_deg", "washout_deg", "twist_stations",
    "airfoil_dat",
    "spar_x_frac", "spar_dia", "spar_slot_dia",
    "rib_t", "n_ribs",
    "hole_x_fracs", "hole_dia_frac", "hole_min_dia", "hole_min_wall",
    "skin_t",
    "hinge_x_frac", "hinge_gap", "elevon_y0", "elevon_y1",
    "battery_u", "battery_y", "battery_orientation", "battery_mass_g",
    "battery_dims",
    "hatch_margin_x", "hatch_margin_y", "hatch_top_clearance",
    # DR-01 tip fins (upright, aft part of the tip chord) and DR-02 elevon throw (CE-01 proposal, 2026-10-14)
    "fin_height", "fin_chord", "fin_x_frac", "fin_t", "fin_mass_g",
    "elevon_up_deg", "elevon_down_deg",
    # DR-14 pusher-prop trailing-edge notch + prop diameter (CE-01 freeze, CEO decision 2026-10-14)
    "prop_dia_in", "prop_notch_x", "prop_notch_halfspan",
]

# ----------------------------------------------------------------------------
from collections import defaultdict


def make_consistent(tris):
    """Orient every triangle of a closed manifold mesh consistently (shared
    edges traversed in opposite directions) and outward (positive volume).
    BFS over faces; handles multiple disjoint components."""
    t = np.asarray(tris, dtype=np.float64).reshape(-1, 3, 3).copy()
    n = len(t)
    vk = np.round(t, 6)
    und = defaultdict(list)
    for fi in range(n):
        for k in range(3):
            a = tuple(vk[fi, k])
            b = tuple(vk[fi, (k + 1) % 3])
            und[tuple(sorted((a, b)))].append((fi, a, b))
    seen = np.zeros(n, bool)
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        stack = [s]
        while stack:
            fi = stack.pop()
            for k in range(3):
                a = tuple(vk[fi, k])
                b = tuple(vk[fi, (k + 1) % 3])
                for (fj, fa, fb) in und[tuple(sorted((a, b)))]:
                    if fj == fi or seen[fj]:
                        continue
                    if (fa, fb) == (a, b):      # same direction -> flip
                        vk[fj] = vk[fj][::-1]
                        t[fj] = t[fj][::-1]
                    seen[fj] = True
                    stack.append(fj)
    v = t.reshape(-1, 3, 3)
    if float(np.einsum('ij,ij->i', v[:, 0], np.cross(v[:, 1], v[:, 2])).sum()) < 0:
        t = t[:, ::-1, :]
    return t
def load_params(path=None):
    """Load parameters from a file.

    Accepts TWO formats (backward compatible):
      - split format (MBSE §4.2): {"meta":..., "design": {...}, "derived": {...}}.
        Only the "design" section is used; "derived" is recomputed, never read.
      - flat format: legacy params.json OR optimizer variant files
        (aero_opt loop --params pattern: flat overrides over DEFAULTS).
        Variant files keep working unchanged.
    """
    P = dict(DEFAULTS)
    if path:
        with open(path) as f:
            ov = json.load(f)
        if isinstance(ov, dict) and isinstance(ov.get("design"), dict):
            P.update(ov["design"])
        else:
            P.update(ov)
    if isinstance(P.get("hole_x_fracs"), list):
        P["hole_x_fracs"] = tuple(P["hole_x_fracs"])
    if isinstance(P.get("battery_dims"), tuple):
        P["battery_dims"] = list(P["battery_dims"])
    return P


def hole_layout(P, af):
    """Lightening-hole (u, v, dia) in root-chord mm. Pure computation;
    build_cad.py asserts the wall/spar clearances on top."""
    CH = P["chord"]
    holes = []
    for fx in P["hole_x_fracs"]:
        u = fx * CH
        d = max(P["hole_min_dia"], P["hole_dia_frac"] * af.thick(fx) * CH)
        v = af.mid(fx) * CH
        holes.append((u, v, d))
    return holes


def compute_derived(P):
    """Recompute EVERYTHING in the params.json "derived" section from design.

    Single source used by build_cad.py, build_systems.py, and verify_params.py.
    A mismatch between this output and the file's "derived" section is a defect.
    """
    W = WingParam(P)
    CH = P["chord"]
    af = W.af
    ST = W.rib_stations()
    holes = hole_layout(P, af)

    # -- battery placement (spanwise pack; zc from the top-clearance rule) --
    # The pack is an axis-aligned box on a SWEPT wing: its corners sample
    # different sections, so the clearance rule uses the corners' GLOBAL
    # (x, y) -> local section, not the centre section.
    bu, by = P["battery_u"], P["battery_y"]
    bdx, bdy, bdz = P["battery_dims"]
    if P["battery_orientation"] == "spanwise":
        hdu, hdw = bdx / 2, bdy / 2      # chordwise / spanwise half-extents
    else:
        hdu, hdw = bdy / 2, bdx / 2
    cx = W.xle_at(0.0) + bu * CH
    corners_xy = [(cx + hdu, by + hdw), (cx + hdu, by - hdw),
                  (cx - hdu, by + hdw), (cx - hdu, by - hdw)]
    def _ztop(x, y):
        uf = (x - W.xle_at(y)) / W.chord_at(y)
        return W.section_to_global(uf, af.top(uf), y)[2]
    ztop_min = min(_ztop(x, y) for (x, y) in corners_xy)
    zc = ztop_min - bdz / 2 - P["hatch_top_clearance"]

    # -- hatch H1 aperture rect (section space; builders use union grids,
    #    so no snapping is needed for vertex coincidence) --
    mx, my = P["hatch_margin_x"], P["hatch_margin_y"]
    hatch = {"u0": bu - (bdx / 2 + mx) / CH, "u1": bu + (bdx / 2 + mx) / CH,
             "y0": by - (bdy / 2 + my), "y1": by + (bdy / 2 + my)}

    return {
        "rib_stations_y": [round(s, 4) for s in ST],
        "spar_centre_uv": [round(W.u_spar * CH, 4), round(W.v_spar * CH, 4)],
        "holes_uvd": [[round(u, 4), round(v, 4), round(d, 4)] for (u, v, d) in holes],
        "hatch_rect": {k: round(v, 4) for k, v in hatch.items()},
        "battery_zc_mm": round(zc, 3),
        "battery_box": {
            "dims": [bdx, bdy, bdz],
            "center_sec": [bu, round(zc / CH, 5), by],
            "orientation": P["battery_orientation"],
        },
    }


class Airfoil:
    def __init__(self, dat_path):
        pts, name = [], None
        with open(dat_path) as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                if i == 0 and not line[0].replace('.', '', 1).replace('-', '', 1).isdigit():
                    name = line
                    continue
                x, y = line.split()[:2]
                pts.append((float(x), float(y)))   # unit chord
        self.name = name
        self.pts = np.array(pts)
        ile = int(np.argmin(self.pts[:, 0]))
        self.upper = self.pts[:ile + 1][::-1]      # LE -> TE
        self.lower = self.pts[ile:]               # LE -> TE

    def top(self, uf):
        return float(np.interp(uf, self.upper[:, 0], self.upper[:, 1]))

    def bot(self, uf):
        return float(np.interp(uf, self.lower[:, 0], self.lower[:, 1]))

    def thick(self, uf):
        return self.top(uf) - self.bot(uf)

    def mid(self, uf):
        return 0.5 * (self.top(uf) + self.bot(uf))


class WingParam:
    """Parametric wing: every geometric query derives from P."""

    def __init__(self, P, dat_dir=OUT):
        self.P = P
        self.af = Airfoil(f"{dat_dir}/{P['airfoil_dat']}")
        self.sw = math.tan(math.radians(P["sweep_deg"]))
        # twist axis (spar centre) in section fractions
        self.u_spar = P["spar_x_frac"]
        self.v_spar = self.af.mid(self.u_spar)

    # -- planform -----------------------------------------------------------
    def chord_at(self, y):
        return self.P["chord"] * (1.0 - (1.0 - self.P["taper"]) * abs(y) / (self.P["span"] / 2))

    def xqc_at(self, y):
        """Quarter-chord x (global CAD) at station y."""
        return abs(y) * self.sw

    def xle_at(self, y):
        return self.xqc_at(y) - 0.25 * self.chord_at(y)

    def twist_at(self, y):
        """Radians, + = nose-down (washout direction) about the spar axis."""
        yf = abs(y) / (self.P["span"] / 2)
        ts = self.P.get("twist_stations")
        if ts:
            ys = [p[0] for p in ts]
            ds = [p[1] for p in ts]
            deg = float(np.interp(yf, ys, ds))
        else:
            deg = self.P["washout_deg"] * yf
        return math.radians(deg)

    # -- section -> global ---------------------------------------------------
    def section_to_global(self, uf, vf, y):
        """Unit-chord section fractions -> global (x, y, z) mm."""
        c = self.chord_at(y)
        u, v = uf * c, vf * c
        us, vs = self.u_spar * c, self.v_spar * c
        th = self.twist_at(y)
        co, si = math.cos(th), math.sin(th)
        ur = us + (u - us) * co - (v - vs) * si
        vr = vs + (u - us) * si + (v - vs) * co
        return (self.xle_at(y) + ur, y, vr)

    def spar_point(self, y):
        x, yy, z = self.section_to_global(self.u_spar, self.v_spar, y)
        return np.array([x, yy, z])

    def rib_stations(self):
        bay = self.P["span"] / self.P["n_ribs"]
        return sorted([s * ((k + 0.5) * bay)
                       for s in (1, -1) for k in range(self.P["n_ribs"] // 2)])

    def x_aft_root_le(self, x_cad):
        return x_cad + 0.25 * self.P["chord"]
