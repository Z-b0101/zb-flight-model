"""R-07 / DR-14: pusher-propeller clearance and the trailing-edge prop notch.

Finding (GM, 2026-10-14): with the prop plane 5.6 mm aft of the root trailing edge
(cad/build_systems.py prop pos u=1.028), the 25 deg sweep puts the trailing edge aft of
the prop plane for |y| > ~12 mm, so any 5-8 inch blade sweeps through the wing. The CAD
clash check skips the prop (build_systems.py skip list), which is why this was not caught.

This script (1) re-derives the intersection from the CAD WingParam, (2) sizes a rectangular
TE notch (cut aft of x_n for |y| <= r_n), and (3) re-runs the twin VLM with the notched chord
distribution to get the neutral-point shift. Usage:
  python3 scripts/prop_notch.py [--dia-in 8] [--xn 195] [--gap 5]
"""
import argparse, json, math, os, sys
import numpy as np
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin")); sys.path.insert(0, os.path.join(REPO, "cad"))
import vlm  # noqa: E402

PROP_PLANE_MM = 205.6       # aft of root LE, cad/build_systems.py LRU "prop" pos u=1.028 x 200
DEPRON_SANDWICH_G_PER_MM2 = 2 * 3.0 * 40e-9 * 1e3   # two 3 mm Depron skins at 40 kg/m^3 -> g/mm^2 (ASSUMED density)


def intersection(W, dia_in, xp=PROP_PLANE_MM):
    r = dia_in * 25.4 / 2; xle0 = W.xle_at(0.0); hits = []
    for th in np.linspace(0, 2 * math.pi, 721):
        for rr in np.linspace(0.15 * r, r, 40):
            y, z = rr * math.cos(th), rr * math.sin(th)
            uf = (xle0 + xp - W.xle_at(y)) / W.chord_at(y)
            if not 0 <= uf <= 1: continue
            _, _, zt = W.section_to_global(uf, W.af.top(uf), y); _, _, zb = W.section_to_global(uf, W.af.bot(uf), y)
            if zb - 3 <= z <= zt + 3: hits.append(abs(y))
    return (min(hits), max(hits)) if hits else None


# The notched-wing VLM now lives in twin/vlm.py (Wing reads prop_notch_x / prop_notch_halfspan
# from the controlled design; CE-01 freeze). This script compares it with the un-notched wing.


def run(dia_in=None, xn=None, gap=5.0, ns=80):
    """Defaults come from the controlled design (prop_dia_in, prop_notch_x, prop_notch_halfspan)."""
    raw, design, _ = vlm.load()
    dia_in = design.get("prop_dia_in", 8.0) if dia_in is None else dia_in
    xn = design.get("prop_notch_x", 195.0) if xn is None else xn
    d_un = dict(design); d_un["prop_notch_halfspan"] = 0.0
    base = vlm.Wing(d_un, ns=ns); d0 = base.derivatives()
    rn = dia_in * 25.4 / 2 + gap
    if "prop_notch_halfspan" in design and dia_in == design.get("prop_dia_in"):
        rn = design["prop_notch_halfspan"]
    d_n = dict(design); d_n["prop_notch_x"] = xn; d_n["prop_notch_halfspan"] = rn
    nw = vlm.Wing(d_n, ns=ns); d1 = nw.derivatives()
    sw = math.tan(math.radians(design["sweep_deg"])); c = design["chord"]
    # removed planform (both sides): integral of (TE(y) - xn) over |y| <= rn
    ys = np.linspace(0, rn, 2001); cut = np.maximum(c + ys * sw - xn, 0)
    area = 2 * np.trapezoid(cut, ys)
    xc = 2 * np.trapezoid(cut * (xn + 0.5 * cut), ys) / area
    hinge_cut_from = (xn - design["hinge_x_frac"] * c) / sw    # |y| beyond which the R2 web is inside the notch
    return dict(dia_in=dia_in, r_notch_mm=rn, x_notch_mm=xn, area_mm2=area, area_pct=100 * area / (base.S * 1e6),
                x_centroid_mm=xc, mass_removed_g=area * DEPRON_SANDWICH_G_PER_MM2,
                np_base_mm=d0["x_np_mm"], np_notch_mm=d1["x_np_mm"], dnp_mm=d1["x_np_mm"] - d0["x_np_mm"],
                CLa_base=d0["CLa_per_deg"], CLa_notch=d1["CLa_per_deg"],
                Cmde_base=d0["Cmde_rootLE_per_deg"], Cmde_notch=d1["Cmde_rootLE_per_deg"],
                elevon_root_gap_mm=design["elevon_y0"] - rn,
                r2_web_cut_for_abs_y_gt_mm=hinge_cut_from if hinge_cut_from < rn else None,
                intersection_unnotched=intersection(base.W, dia_in))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dia-in", type=float, default=None); ap.add_argument("--xn", type=float, default=None)
    ap.add_argument("--gap", type=float, default=5.0)
    a = ap.parse_args()
    for k, v in run(a.dia_in, a.xn, a.gap).items():
        print(f"{k:28s} {v if not isinstance(v, float) else round(v, 4)}")
