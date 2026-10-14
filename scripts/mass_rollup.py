"""Stacked mass / CG / static-margin roll-up for the CE-01 freeze (MBSE flag 2, 2026-10-14).

Baseline (locked, proposed): planning mass 211.9 g at CG 128.5 mm aft of root LE
(CAD rollup 209.0 + V-spar tube overage 0.8 + root joiner 2.1). Adds the SA-01 structural
changes from params.json "structure", the tip fins from the design block, and a motor delta.
NP from the twin VLM (mass-independent). Usage:
  python3 scripts/mass_rollup.py [--motor-g 17] [--battery-fwd-mm 0] [--esc-to-mm 185]
"""
import argparse, json, math, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_G, BASE_X = 211.9, 128.5
MOTOR_BASE_G, MOTOR_X = 10.0, 192.0
ESC_G, ESC_X = 3.5, 185.0
PROP_BASE_G, PROP_X = 7.9, 205.6      # Gemfan 7040-3 at the prop plane (cad/build_systems.py)
ADAPTER_X = 200.0                     # prop adapter between motor bell and prop hub
BATT_G = 62.0
FC_G = 23.0                           # SpeedyBee F405 WING stack (WEIGHT_BUDGET)
SM_FLOOR = 0.05


def rollup(motor_g=MOTOR_BASE_G, battery_fwd_mm=0.0, esc_to_mm=ESC_X, np_mm=None,
           prop_g=PROP_BASE_G, adapter_g=0.0, notch=None, fc_fwd_mm=0.0):
    """notch: dict(mass_removed_g, x_centroid_mm, closure_g, dnp_mm) from scripts/prop_notch.py (R-07/DR-14)."""
    raw = json.load(open(os.path.join(REPO, "cad", "params.json")))
    D, S = raw["design"], raw.get("structure", {})
    sweep = math.tan(math.radians(D["sweep_deg"])); c = D["chord"]; semi = D["span"] / 2
    xmid = lambda u: u * c + (semi / 2) * sweep   # mid-semispan chordwise station
    if np_mm is None:
        import vlm
        np_mm = vlm.Wing(D).derivatives()["x_np_mm"]
    rows = [("Planning baseline (locked)", BASE_G, BASE_X)]
    if "R2_hinge_web" in S: rows.append(("R2 hinge-line web", S["R2_hinge_web"]["mass_g"], xmid(S["R2_hinge_web"]["x_frac"])))
    if "R3_midchord_web" in S: rows.append(("R3 mid-chord web", S["R3_midchord_web"]["mass_g"], xmid(S["R3_midchord_web"]["x_frac"])))
    if "web_glue_mass_g" in S: rows.append(("Web glue", S["web_glue_mass_g"], 232.0))
    if "R4_hatch" in S: rows.append(("R4 hatch frame/tray/lid (net)", S["R4_hatch"]["net_mass_g"], 41.0))
    if "R5_centre_section" in S: rows.append(("R5 centre section (net)", S["R5_centre_section"]["net_mass_g"], 80.0))
    if D.get("fin_height", 0) > 0:
        xf = semi * sweep + D["fin_x_frac"] * c + 0.5 * D["fin_chord"]
        rows.append(("DR-01 tip fins", 2 * D["fin_mass_g"], xf))
    if notch:
        if not D.get("prop_notch_halfspan"):     # VLM NP already includes the notch once it is in params
            np_mm += notch["dnp_mm"]
        rows.append(("DR-14 prop notch: foam removed", -notch["mass_removed_g"], notch["x_centroid_mm"]))
        rows.append(("DR-14 prop notch: edge closure", notch["closure_g"], notch["x_notch_mm"]))
    if prop_g != PROP_BASE_G: rows.append((f"Prop delta ({prop_g:g} g vs {PROP_BASE_G:g} g)", prop_g - PROP_BASE_G, PROP_X))
    if adapter_g: rows.append((f"Prop adapter ({adapter_g:g} g)", adapter_g, ADAPTER_X))
    if motor_g != MOTOR_BASE_G: rows.append((f"Motor delta ({motor_g:g} g vs {MOTOR_BASE_G:g} g)", motor_g - MOTOR_BASE_G, MOTOR_X))
    if battery_fwd_mm: rows.append((f"Battery {battery_fwd_mm:g} mm forward", 0.0, -BATT_G * battery_fwd_mm))   # moment-only
    if fc_fwd_mm: rows.append((f"FC {fc_fwd_mm:g} mm forward", 0.0, -FC_G * fc_fwd_mm))   # moment-only
    if esc_to_mm != ESC_X: rows.append((f"ESC moved to {esc_to_mm:g} mm", 0.0, ESC_G * (esc_to_mm - ESC_X)))
    m, mx, out = 0.0, 0.0, []
    for name, dm, x in rows:
        if dm == 0.0:
            mx += x          # pure moment shift
        else:
            m += dm; mx += dm * x
        cg = mx / m
        out.append(dict(item=name, d_mass_g=dm, mass_g=m, cg_mm=cg, sm=(np_mm - cg) / c))
    return np_mm, out


def table(out):
    lines = ["| Step | Mass (g) | CG (mm) | SM |", "| --- | --- | --- | --- |"]
    for r in out:
        flag = " **below 5% floor**" if r["sm"] < SM_FLOOR else ""
        lines.append(f"| {r['item']} | {r['mass_g']:.1f} | {r['cg_mm']:.2f} | {100*r['sm']:.2f}%{flag} |")
    return "\n".join(lines)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--motor-g", type=float, default=17.0)
    ap.add_argument("--battery-fwd-mm", type=float, default=0.0)
    ap.add_argument("--esc-to-mm", type=float, default=ESC_X)
    ap.add_argument("--fc-fwd-mm", type=float, default=0.0)
    ap.add_argument("--prop-g", type=float, default=PROP_BASE_G)
    ap.add_argument("--adapter-g", type=float, default=0.0)
    ap.add_argument("--notch-dia-in", type=float, default=0.0, help="apply the DR-14 TE notch for this prop diameter")
    a = ap.parse_args()
    notch = None
    if a.notch_dia_in:
        import prop_notch
        r = prop_notch.run(dia_in=a.notch_dia_in)
        notch = dict(mass_removed_g=r["mass_removed_g"], x_centroid_mm=r["x_centroid_mm"], closure_g=0.5,
                     x_notch_mm=r["x_notch_mm"], dnp_mm=r["dnp_mm"])
    np_mm, out = rollup(a.motor_g, a.battery_fwd_mm, a.esc_to_mm, prop_g=a.prop_g, adapter_g=a.adapter_g, notch=notch, fc_fwd_mm=a.fc_fwd_mm)
    print(f"NP {np_mm:.1f} mm (twin VLM)\n"); print(table(out))
