"""Lateral-directional derivatives derived from geometry (replaces typed-in values; DR-01).

Cn_beta = wing-alone (USAF DATCOM sweep/CL^2 term) + tip fins (lift-slope x volume).
Every constant that is assumed is named here and listed in ASSUMED; the twin ledger
(twin/perf.py ASSUMPTIONS) points at this module.
"""
import math

ASSUMED = dict(
    fin_endplate_factor=1.55,   # effective AR = factor x geometric AR (wing acts as an endplate); 1.5-2 typical
    fin_eta_sidewash=1.0,       # eta_v (1 + d sigma/d beta) at the tips; no fuselage, tips in near-freestream
)


def lift_slope(ar):
    """Helmbold low-AR lift slope, per rad."""
    return 2 * math.pi * ar / (2 + math.sqrt(ar * ar + 4))


def cn_beta_wing(design, x_cg_mm, x_np_mm, CL):
    """DATCOM wing-alone yaw stability, per rad (positive = stable)."""
    b, c = design["span"] / 1000, design["chord"] / 1000
    A = b * b / (b * c); L = math.radians(design["sweep_deg"])
    xbar = (x_np_mm - x_cg_mm) / design["chord"]
    return CL ** 2 * (1 / (4 * math.pi * A) - math.tan(L) / (math.pi * A * (A + 4 * math.cos(L)))
                      * (math.cos(L) - A / 2 - A ** 2 / (8 * math.cos(L)) + 6 * xbar * math.sin(L) / A))


def fin_geometry(design):
    h, cf = design.get("fin_height", 0.0), design.get("fin_chord", 0.0)
    if h <= 0 or cf <= 0:
        return None
    x_tip_le = (design["span"] / 2) * math.tan(math.radians(design["sweep_deg"]))
    x_fin_le = x_tip_le + design["fin_x_frac"] * design["chord"]
    x_ac = x_fin_le + 0.25 * cf
    ar_g = h / cf
    return dict(h=h, cf=cf, area_mm2=h * cf, ar_geom=ar_g, ar_eff=ASSUMED["fin_endplate_factor"] * ar_g,
                x_le_mm=x_fin_le, x_ac_mm=x_ac, z_ac_mm=0.45 * h)


def cn_beta_fins(design, x_cg_mm):
    g = fin_geometry(design)
    if g is None:
        return 0.0, None
    b, S = design["span"] / 1000, design["span"] * design["chord"] / 1e6
    a = lift_slope(g["ar_eff"])
    lv = (g["x_ac_mm"] - x_cg_mm) / 1000
    cn = 2 * a * ASSUMED["fin_eta_sidewash"] * (g["area_mm2"] / 1e6 / S) * (lv / b)
    g.update(lift_slope_per_rad=a, arm_m=lv)
    return cn, g


def derive(design, x_cg_mm, x_np_mm, CL):
    w = cn_beta_wing(design, x_cg_mm, x_np_mm, CL)
    f, g = cn_beta_fins(design, x_cg_mm)
    d = math.pi / 180
    return dict(CL=CL, cn_beta_wing_per_deg=w * d, cn_beta_fins_per_deg=f * d, cn_beta_per_deg=(w + f) * d, fin=g)


if __name__ == "__main__":
    import json, os
    P = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cad", "params.json")))["design"]
    for CL in (0.17, 0.37, 0.6):
        print(json.dumps(derive(P, 130.9, 142.6, CL), default=lambda v: round(v, 6)))
