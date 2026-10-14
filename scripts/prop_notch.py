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


class NotchedWing(vlm.Wing):
    """Twin VLM with the TE notch. Strip edges are snapped to +/- r_n so no strip straddles
    the notch edge (a straddling strip gives a sheared panel row and a near-singular AIC)."""
    def __init__(self, design, xn_mm, rn_mm, **kw):
        self.xn, self.rn = xn_mm / 1000, rn_mm / 1000
        super().__init__(design, **kw)
        yb = self.yb.copy()
        for s in (-1, 1):
            yb[np.argmin(abs(yb - s * self.rn))] = s * self.rn
        self.yb = np.sort(yb)
        self.S = sum((self.yb[i + 1] - self.yb[i]) * self._c(0.5 * (self.yb[i] + self.yb[i + 1]), self._cut(i))
                     for i in range(2 * self.ns))
        self.AR = self.b ** 2 / self.S
    def _cut(self, i): return abs(0.5 * (self.yb[i] + self.yb[i + 1])) < self.rn
    def _c(self, y, cut):
        c = vlm.Wing.chord(self, y)
        return min(c, self.xn - self.xle(y)) if cut else c
    def _panels(self, elevon_deg=0.0, aileron_deg=0.0):
        P = self.P; nc = self.nc
        A, B, C, N = [], [], [], []
        hinge = P["hinge_x_frac"]; ey0, ey1 = P["elevon_y0"] / 1000, P["elevon_y1"] / 1000
        for i in range(2 * self.ns):
            ya, yb = self.yb[i], self.yb[i + 1]; ym = 0.5 * (ya + yb); cut = self._cut(i)
            for k in range(nc):
                u0 = k / nc
                def pt(y, u): return np.array([self.xle(y) + u * self._c(y, cut), y, 0.0])
                A.append(pt(ya, u0 + 0.25 / nc)); B.append(pt(yb, u0 + 0.25 / nc))
                C.append(pt(ym, u0 + 0.75 / nc))
                uc = u0 + 0.75 / nc
                # camber of the truncated section: local fraction of the ORIGINAL chord
                uf_orig = uc * self._c(ym, cut) / vlm.Wing.chord(self, ym)
                slope = self.camber_slope(uf_orig) + math.tan(self.twist(ym))
                if uc > hinge and ey0 <= abs(ym) <= ey1 and not cut:
                    d = elevon_deg + (aileron_deg if ym < 0 else -aileron_deg)
                    slope -= math.tan(math.radians(d))
                n = np.array([-slope, 0.0, 1.0]); N.append(n / np.linalg.norm(n))
        return np.array(A), np.array(B), np.array(C), np.array(N)


def run(dia_in=8.0, xn=195.0, gap=5.0, ns=80):
    raw, design, _ = vlm.load()
    base = vlm.Wing(design, ns=ns); d0 = base.derivatives()
    rn = dia_in * 25.4 / 2 + gap
    nw = NotchedWing(design, xn, rn, ns=ns); d1 = nw.derivatives()
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
    ap.add_argument("--dia-in", type=float, default=8.0); ap.add_argument("--xn", type=float, default=195.0)
    ap.add_argument("--gap", type=float, default=5.0)
    a = ap.parse_args()
    for k, v in run(a.dia_in, a.xn, a.gap).items():
        print(f"{k:28s} {v if not isinstance(v, float) else round(v, 4)}")
