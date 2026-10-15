"""CG band for the frozen baseline: aft limit from static margin, forward limit from
up-elevon authority. AERO seat, CE-AERO-01 (proposed).

Everything is computed with the twin (twin/perf.py) on cad/params.json. Nothing here
writes to params.json or changes the frozen record.

Limits
- Aft (stability): SM >= 5.5% design floor (Constitution Art V.6). CG_aft = NP - 0.055*MAC.
- Forward (control authority, PROPOSED criterion): trim at 1.3 Vs needs no more than
  AUTH_FRAC of the minimum up-throw (elevon_up_deg). The rest is the reserve for flare,
  gusts and pull-up. AUTH_FRAC = 2/3 is an AERO engineering-judgement value, labelled
  PROVISIONAL until MBSE approves a criterion.
- The forward limit depends on flap_knockdown (CRITICAL, UNCALIBRATED in twin/perf.py),
  so it is reported across a knockdown band, not as one number.

Usage: python scripts/cg_band.py [--json out.json]
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "twin"))
import perf  # noqa: E402

SM_FLOOR_DESIGN = 0.055     # Constitution Art V.6 (design floor)
SM_FLOOR_ABS = 0.050        # Constitution Art V.6 (absolute floor)
AUTH_FRAC = 2.0 / 3.0       # PROVISIONAL (AERO): share of up-throw usable for trim at 1.3 Vs
KNOCKDOWNS = (0.80, 0.75, 0.70, 0.60)   # 0.7-0.8 = perf.py's cited band; 0.60 = pessimistic stress case
UP_THROWS = (12.0, 14.0, 15.0)          # 12 = DR-02 frozen; 14/15 = candidate linkage change


def _twin(x_cg_mm=None, knockdown=None):
    """Build a Twin with temporary overrides of the CG and flap knockdown."""
    saved = dict(perf.ASSUMPTIONS)
    try:
        if x_cg_mm is not None:
            perf.ASSUMPTIONS["x_cg_mm"] = (x_cg_mm,) + saved["x_cg_mm"][1:]
        if knockdown is not None:
            perf.ASSUMPTIONS["flap_knockdown"] = (knockdown,) + saved["flap_knockdown"][1:]
        return perf.Twin()
    finally:
        perf.ASSUMPTIONS.clear(); perf.ASSUMPTIONS.update(saved)


def trim_elevon_13vs(x_cg_mm, knockdown):
    t = _twin(x_cg_mm, knockdown)
    return t.trim(1.3 * t.vstall())["elevon"]


def forward_limit(knockdown, up_throw_deg, frac=AUTH_FRAC, lo=100.0, hi=None):
    """Most-forward CG (mm) at which |trim elevon at 1.3 Vs| <= frac * up_throw.
    Trim elevon is linear in CG, so two evaluations solve it exactly."""
    target = -frac * up_throw_deg
    if hi is None:
        hi = perf.A("x_cg_mm")
    d_lo, d_hi = trim_elevon_13vs(lo, knockdown), trim_elevon_13vs(hi, knockdown)
    return lo + (target - d_lo) * (hi - lo) / (d_hi - d_lo)


def band():
    base = _twin()
    np_mm, mac = base.d["x_np_mm"], base.w.cref
    mac_mm = mac * 1000 if mac < 1 else mac
    sm = lambda x: (np_mm - x) / mac_mm
    out = dict(
        design_hash=base.hash, np_mm=np_mm, mac_mm=mac_mm,
        frozen_cg_mm=base.x_cg_mm, frozen_sm=base.SM, vstall=base.vstall(),
        aft_limit_design_mm=np_mm - SM_FLOOR_DESIGN * mac_mm,
        aft_limit_abs_mm=np_mm - SM_FLOOR_ABS * mac_mm,
        auth_frac=AUTH_FRAC, labels={
            "np_mm": "modelled (VLM, notched wing)",
            "frozen_cg_mm": "modelled (CE-01 roll-up; weigh-as-built replaces it)",
            "aft_limit": "modelled, from rule SM >= 5.5%",
            "forward_limit": "modelled, PROVISIONAL criterion, depends on uncalibrated flap_knockdown",
        },
        forward=[], frozen_trim=[],
    )
    for k in KNOCKDOWNS:
        out["frozen_trim"].append(dict(knockdown=k,
                                       de_13vs=trim_elevon_13vs(base.x_cg_mm, k)))
        for up in UP_THROWS:
            xf = forward_limit(k, up)
            out["forward"].append(dict(knockdown=k, up_throw_deg=up, fwd_limit_mm=xf,
                                       sm_at_fwd=sm(xf),
                                       window_mm=out["aft_limit_design_mm"] - xf))
    return out


def report(b):
    print(f"hash {b['design_hash']}  NP {b['np_mm']:.2f} mm  MAC {b['mac_mm']:.0f} mm  "
          f"Vs {b['vstall']:.2f} m/s")
    print(f"frozen CG {b['frozen_cg_mm']:.2f} mm  SM {100*b['frozen_sm']:.2f}%")
    print(f"AFT limit (SM 5.5%): {b['aft_limit_design_mm']:.2f} mm   "
          f"(SM 5.0% absolute: {b['aft_limit_abs_mm']:.2f} mm)")
    print(f"FORWARD limit: trim at 1.3 Vs <= {b['auth_frac']:.3f} x up-throw")
    print(" knockdown  up-throw  fwd limit   SM@fwd   window to aft limit")
    for r in b["forward"]:
        flag = "" if r["window_mm"] > 0 else "  <-- NO WINDOW"
        print(f"   {r['knockdown']:.2f}     {r['up_throw_deg']:4.1f}   {r['fwd_limit_mm']:7.2f} mm"
              f"  {100*r['sm_at_fwd']:5.2f}%   {r['window_mm']:6.2f} mm{flag}")
    print(" trim elevon at 1.3 Vs, frozen CG:")
    for r in b["frozen_trim"]:
        print(f"   knockdown {r['knockdown']:.2f}: {r['de_13vs']:.2f} deg")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    a = ap.parse_args()
    b = band(); report(b)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(b, f, indent=2, default=float)
