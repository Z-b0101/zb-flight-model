"""As-built CG tolerance for the CE-01 frozen configuration (SCM/MFG seat, 2026-10-14).

Question: how much build error (grams, in which place) can the frozen design absorb before the
static margin drops below the 5.5 % rule or the 5.0 % floor, and what trim range does the build have?

Inputs come only from the controlled sources:
  - frozen stack from scripts/mass_rollup.py with the CE-01 freeze arguments (233.0 g, CG 130.32 mm, NP 141.64 mm)
  - battery box and hatch aperture from cad/params.json (design + derived blocks)
Everything here is MODELLED (no part has been weighed yet).
Usage: python3 mfg/tools/cg_tolerance.py [--json]
"""
import json, os, sys, argparse
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "scripts")); sys.path.insert(0, os.path.join(REPO, "twin"))
import mass_rollup, prop_notch

SM_RULE, SM_FLOOR, CAP_G = 0.055, 0.050, 250.0

def frozen():
    r = prop_notch.run(dia_in=8.0)
    notch = dict(mass_removed_g=r["mass_removed_g"], x_centroid_mm=r["x_centroid_mm"], closure_g=0.5,
                 x_notch_mm=r["x_notch_mm"], dnp_mm=r["dnp_mm"])
    np_mm, rows = mass_rollup.rollup(20.0, 9.0, 95.0, prop_g=7.1, adapter_g=5.1, notch=notch, fc_fwd_mm=5.0)
    last = rows[-1]
    return np_mm, last["mass_g"], last["cg_mm"]

def sm(np_mm, m, cg, chord): return (np_mm - cg) / chord

def add(m, cg, dm, x):
    m2 = m + dm
    return m2, (m * cg + dm * x) / m2

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true"); a = ap.parse_args()
    P = json.load(open(os.path.join(REPO, "cad", "params.json")))
    D, H = P["design"], P["derived"]["hatch_rect"]
    c = D["chord"]
    np_mm, m0, cg0 = frozen()
    sm0 = sm(np_mm, m0, cg0, c)
    out = dict(frozen=dict(mass_g=round(m0, 1), cg_mm=round(cg0, 2), np_mm=round(np_mm, 2), sm_pct=round(100 * sm0, 2)))

    # 1. CG budget: how far aft the as-built CG may sit
    out["cg_aft_allow_mm"] = dict(to_rule_5p5=round((sm0 - SM_RULE) * c, 2), to_floor_5p0=round((sm0 - SM_FLOOR) * c, 2))

    # 2. Grams of unplanned mass at each station that use up the margin (station x from the CAD / roll-up)
    stations = {
        "prop + adapter (x 200-206)": 203.0,
        "motor (x 192)": 192.0,
        "fins / tip trailing edge (x ~350)": 350.0,
        "wing structure average (x ~128)": 128.5,
        "FC / receiver tray (x ~90)": 90.0,
        "nose / battery area (x ~32)": 32.0,
    }
    rows = []
    for name, x in stations.items():
        res = {"station": name, "x_mm": x, "dSM_pt_per_g": None, "g_to_rule": None, "g_to_floor": None, "g_to_cap": round(CAP_G - m0, 1)}
        m1, cg1 = add(m0, cg0, 1.0, x)
        d = 100 * (sm(np_mm, m1, cg1, c) - sm0)
        res["dSM_pt_per_g"] = round(d, 3)
        for key, lim in (("g_to_rule", SM_RULE), ("g_to_floor", SM_FLOOR)):
            if d >= 0:
                res[key] = "never (moves CG forward)"
                continue
            g = 0.0
            while g < 200:
                g += 0.1
                mm, cc = add(m0, cg0, g, x)
                if sm(np_mm, mm, cc, c) < lim: break
            res[key] = round(g, 1)
        rows.append(res)
    out["unplanned_mass"] = rows

    # 3. Built-in trim range: battery fore/aft travel inside the hatch aperture
    u0, u1 = H["u0"], H["u1"]
    bx = D["battery_dims"][0]                       # 28 mm chordwise (spanwise orientation)
    bc = D["battery_u"] * c
    fwd_room = (bc - bx / 2) - (u0 * c + D["hatch_margin_x"])
    aft_room = (u1 * c - D["hatch_margin_x"]) - (bc + bx / 2)
    out["battery_trim_mm"] = dict(aperture_x_mm=[round(u0 * c, 1), round(u1 * c, 1)],
                                  battery_x_mm=[round(bc - bx / 2, 1), round(bc + bx / 2, 1)],
                                  forward_room=round(fwd_room, 1), aft_room=round(aft_room, 1),
                                  note="battery is the CEO's chosen trim weight (R-15, D-31 option 1), but the frozen tray leaves this much travel")
    per_mm = 100 * D["battery_mass_g"] / m0 / c     # SM points per mm of battery travel
    out["battery_sm_pt_per_mm"] = round(per_mm, 3)

    # 4. Nose ballast effectiveness (last resort)
    xb = 5.0
    m1, cg1 = add(m0, cg0, 1.0, xb)
    out["nose_ballast_sm_pt_per_g_at_x5"] = round(100 * (sm(np_mm, m1, cg1, c) - sm0), 3)

    # 5. Plausible first-build deltas (MODELLED scenario, to be replaced by the as-built sheet)
    scen = [("wiring above the 3.0 g CAD allowance (connectors, leads)", 5.0, 100.0),
            ("glue above the roll-up allowance", 3.0, 128.5),
            ("printed motor mount above estimate", 2.0, 188.0),
            ("Depron density at the top of its 84-120 g/m2 band (skins +7 g)", 7.0, 128.5)]
    m, cg, srows = m0, cg0, []
    for name, dm, x in scen:
        m, cg = add(m, cg, dm, x)
        srows.append(dict(item=name, dm_g=dm, x_mm=x, mass_g=round(m, 1), cg_mm=round(cg, 2), sm_pct=round(100 * sm(np_mm, m, cg, c), 2)))
    out["scenario_first_build"] = srows
    need = 0.0
    while sm(np_mm, *add(m, cg, need, xb), c) < SM_RULE and need < 50: need += 0.1
    out["scenario_ballast_g_at_x5_to_restore_rule"] = round(need, 1)
    out["scenario_auw_with_ballast_g"] = round(m + need, 1)

    if a.json:
        print(json.dumps(out, indent=1)); return
    f = out["frozen"]
    print(f"Frozen: {f['mass_g']} g, CG {f['cg_mm']} mm, NP {f['np_mm']} mm, SM {f['sm_pct']}%")
    print(f"CG may move aft by {out['cg_aft_allow_mm']['to_rule_5p5']} mm (5.5% rule) / {out['cg_aft_allow_mm']['to_floor_5p0']} mm (5.0% floor)\n")
    print("| Unplanned mass at | dSM per g (pt) | g to 5.5% rule | g to 5.0% floor |")
    print("|---|---|---|---|")
    for r in rows: print(f"| {r['station']} | {r['dSM_pt_per_g']:+.3f} | {r['g_to_rule']} | {r['g_to_floor']} |")
    b = out["battery_trim_mm"]
    print(f"\nBattery trim travel in the frozen hatch: forward {b['forward_room']} mm, aft {b['aft_room']} mm "
          f"(aperture x {b['aperture_x_mm']}, pack x {b['battery_x_mm']}); {out['battery_sm_pt_per_mm']} pt per mm")
    print(f"Nose ballast at x = 5 mm: {out['nose_ballast_sm_pt_per_g_at_x5']:+.3f} pt per g\n")
    print("| First-build scenario (modelled) | +g | at x | AUW | CG | SM |")
    print("|---|---|---|---|---|---|")
    for r in srows: print(f"| {r['item']} | {r['dm_g']} | {r['x_mm']} | {r['mass_g']} | {r['cg_mm']} | {r['sm_pct']}% |")
    print(f"\nTo restore 5.5%: {out['scenario_ballast_g_at_x5_to_restore_rule']} g nose ballast -> AUW {out['scenario_auw_with_ballast_g']} g")

if __name__ == "__main__":
    main()
