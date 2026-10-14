"""Export the twin state to twin/twin_bundle.json for the viewer page."""
import os, sys, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import perf  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def f(x):
    if isinstance(x, (np.floating, np.integer)): return float(x)
    if isinstance(x, np.bool_): return bool(x)
    return x


def main():
    T = perf.Twin(); s = T.summary(); P = T.design; W = T.w
    # planform outline + ribs + elevons (mm, x aft of root LE, y span)
    half = P["span"] / 2
    ys = np.linspace(-half, half, 41)
    le = [[float(y), float(W.xle(y / 1000) * 1000)] for y in ys]
    te = [[float(y), float((W.xle(y / 1000) + W.chord(y / 1000)) * 1000)] for y in ys]
    ribs = [[y, float(W.xle(y / 1000) * 1000), float((W.xle(y / 1000) + W.chord(y / 1000)) * 1000)] for y in T.raw["derived"]["rib_stations_y"]]
    elev = []
    for sgn in (-1, 1):
        y0, y1 = sgn * P["elevon_y0"], sgn * P["elevon_y1"]
        pts = []
        for y in (y0, y1):
            xl = W.xle(y / 1000) * 1000; c = W.chord(y / 1000) * 1000
            pts.append([y, xl + P["hinge_x_frac"] * c, xl + c])
        elev.append(pts)
    sweep = []
    for V in np.arange(5.0, 14.01, 0.25):
        t = T.trim(float(V)); E = perf.A("pack_wh") * perf.A("usable_frac") * 3600
        sweep.append({k: f(v) for k, v in t.items()} | {"endurance_min": E / t["P_batt"] / 60, "range_km": E / t["P_batt"] * V / 1000})
    fly_res = json.load(open(f"{HERE}/fly_results.json"))
    mis = json.load(open(f"{HERE}/mission_results.json"))
    ledger = [{"key": k, "value": v[0] if not isinstance(v[0], list) else "MH60 table", "status": v[1], "source": v[2]}
              for k, v in perf.ASSUMPTIONS.items()]
    d = s["derivatives"]
    baseline = {"x_np_mm": 144.98, "x_cg_mm": 128.5, "SM_pct": 8.26, "elevon_deg": -4.60, "range_km": 31.86, "endurance_min": 75.8}
    checks = [
        {"name": "Neutral point", "twin": d["x_np_mm"], "base": 144.98, "unit": "mm", "tol": "±5 mm", "ok": abs(d["x_np_mm"] - 144.98) <= 5},
        {"name": "Static margin", "twin": 100 * s["SM"], "base": 8.26, "unit": "% MAC", "tol": "±2.5 pt", "ok": abs(100 * s["SM"] - 8.26) <= 2.5},
        {"name": "Trim elevon", "twin": f(s["best_range"]["elevon"]), "base": -4.60, "unit": "deg", "tol": "±1 deg", "ok": abs(s["best_range"]["elevon"] + 4.60) <= 1},
        {"name": "Range (6-DOF)", "twin": mis["result"]["range_km"], "base": 31.86, "unit": "km", "tol": "±10%", "ok": abs(mis["result"]["range_km"] / 31.86 - 1) <= 0.10},
        {"name": "Endurance (6-DOF)", "twin": mis["result"]["flight_time_min"], "base": 75.8, "unit": "min", "tol": "±10%", "ok": abs(mis["result"]["flight_time_min"] / 75.8 - 1) <= 0.10},
    ]
    bundle = dict(hash=T.hash, design={k: P[k] for k in ("span", "chord", "taper", "sweep_deg", "washout_deg", "n_ribs", "airfoil_dat", "hinge_x_frac", "elevon_y0", "elevon_y1", "battery_mass_g")},
                  planform=dict(le=le, te=te, ribs=ribs, elevons=elev, np=d["x_np_mm"], cg=s["x_cg_mm"]),
                  derivs={k: f(v) for k, v in d.items()} | {"SM": f(s["SM"]), "vstall": f(s["vstall"]), "Cm0_cg": f(s["Cm0_cg"]), "Cma_cg": f(s["Cma_cg"]), "Cmde_cg": f(s["Cmde_cg"]), "CLde": f(s["CLde"])},
                  mass_g=s["mass_g"], sweep=sweep, fly=fly_res["result"], pitch=[[r["Time"], r["q-rad_sec"] * 57.3] for r in fly_res["pitch"]],
                  roll=[[r["Time"], r["phi-deg"]] for r in fly_res["roll"]],
                  mission=mis["result"], trace=[[o["t"] / 60, o["h"], o["E_wh"], o["V"], o["x"] / 1000] for o in mis["trace"]],
                  ledger=ledger, checks=checks, baseline=baseline,
                  findings=[
                      "Committed zb_wing.xml did not load: engine/thruster files missing from repo.",
                      "Its placeholder fuel tank added 50 g, so simulated AUW was 254.3 g (over the cap).",
                      "Its aero axes returned raw coefficients instead of forces and moments.",
                      "Unnamed locations put the aero reference point and empty-weight CG at x = 0 (CG 77 mm, intended 116 mm).",
                      "Pitch trim was not wired to the elevon.",
                      "Its CL slope (0.109/deg) is 2-D-like; the params-driven VLM gives 0.063/deg.",
                      "Drag keyed on alpha ignored elevon lift and over-counted induced drag (0.13 m/s cruise sink). Fixed: drag keyed on actual CL.",
                      "Range/endurance read 5–8% above baseline: VLM Oswald e = 0.90 vs 0.78 in drag.py (CE-01).",
                  ])
    json.dump(bundle, open(f"{HERE}/twin_bundle.json", "w"), default=f)
    print("ok", len(json.dumps(bundle, default=f)), "bytes")


if __name__ == "__main__":
    main()
