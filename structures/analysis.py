"""Z!B structural analysis: load cases, FE solution, margins, design options.

Run: python3 structures/analysis.py  -> structures/results.json (+ printed tables)
"""
import os, sys, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "twin"))
from structures import model as SM  # noqa: E402
from structures import materials as MAT  # noqa: E402
import perf  # noqa: E402

GEO = SM.Geometry()
TWIN = perf.Twin()
W = SM.MASS["total_g"] / 1000 * SM.G0
S = GEO.wing.S
CLA_RAD = TWIN.CLa * 180 / math.pi
CLMAX_WING = 0.9 * perf.A("clmax_section")


def gust_n(V, Ude=7.6):
    """FAR 23.341 gust load factor with alleviation, capped at the stall-limited load factor."""
    mu = 2 * (W / S) / (SM.RHO * GEO.c * CLA_RAD * SM.G0)
    Kg = 0.88 * mu / (5.3 + mu)
    dn = SM.RHO * V * CLA_RAD * Kg * Ude / (2 * W / S)
    n_stall = 0.5 * SM.RHO * V**2 * S * CLMAX_WING / W
    return min(1 + dn, n_stall), dict(mu=mu, Kg=Kg, dn=dn, n_stall=n_stall)


def cases():
    ng, info = gust_n(12.0)
    return [
        dict(id="C1", name="1 g cruise", V=10.5, n=1.0),
        dict(id="C2", name="2.5 g pull-up", V=12.0, n=2.5),
        dict(id="C3", name="4 g manoeuvre", V=15.0, n=4.0),
        dict(id="C4", name=f"Gust 7.6 m/s at 12 m/s (n = {ng:.1f}, stall-capped)", V=12.0, n=ng, gust=info),
        dict(id="C5", name="High-speed dive, 1 g at 25 m/s", V=25.0, n=1.0),
    ]


def run_case(case, spar="nominal", web=False, **seckw):
    fe, ys, sec = SM.build(GEO, spar=spar, web=web, **seckw)
    de = TWIN.trim(case["V"])["elevon"]
    F, info = SM.nodal_loads(GEO, fe, ys, case["V"], case["n"], elevon_deg=de)
    u = fe.solve(F)
    ef = fe.element_forces(u)
    st = SM.stresses(sec, ef[0])
    twist = SM.streamwise_twist(fe, u)
    return dict(case=case["id"], spar=spar, web=web, root=st, tip_defl_mm=1000 * SM.tip_deflection(u),
                tip_twist_deg=math.degrees(twist[-1]), alpha=info["alpha"], elevon=de,
                half_lift=info["wing_lift_half"], sec=dict(EI=sec["EI_flap"], GJ=sec["GJ"], GJ_skin=sec["GJ_skin"], GJ_spar=sec["GJ_spar"]))


def margins(r, spar):
    a = MAT.SPAR_GRADES[spar]["sigma_allow"]; D = MAT.DEPRON
    st = r["root"]; buck = SM.skin_buckling_stress(GEO)
    return dict(
        spar_factor=a / st["sig_spar"],
        top_skin_vs_crush=D["sigma_c"] / st["sig_top"],
        top_skin_vs_buckling=buck / st["sig_top"],
        bot_skin_vs_tension=D["sigma_t"] / st["sig_bot"],
        skin_shear=D["tau"] / max(st["tau_skin"], 1e-9),
    )


def main():
    out = dict(hash=GEO.hash, fos=MAT.FOS, cases=[], materials=dict(spar=MAT.SPAR_GRADES, depron=MAT.DEPRON, pla=MAT.PLA))
    print(f"design hash {GEO.hash}; W={W:.3f} N; S={S:.3f} m2; CLa={CLA_RAD:.2f}/rad; buckling stress (flat) {SM.skin_buckling_stress(GEO)/1e3:.1f} kPa")
    for c in cases():
        for spar in ("low", "nominal", "premium"):
            for web in (False, True):
                r = run_case(c, spar=spar, web=web)
                r["margins"] = margins(r, spar)
                r["name"] = c["name"]; r["V"] = c["V"]; r["n"] = c["n"]
                out["cases"].append(r)
                m = r["margins"]; st = r["root"]
                print(f"{c['id']} n={c['n']:.2f} V={c['V']:4.1f} spar={spar:8s} web={str(web):5s} | M={st['M']:.3f} T={st['T']:.4f} N.m | "
                      f"spar {st['sig_spar']/1e6:6.1f} MPa (x{m['spar_factor']:.2f}) | top {st['sig_top']/1e3:6.1f} kPa (crush x{m['top_skin_vs_crush']:.2f}, buckle x{m['top_skin_vs_buckling']:.2f}) | "
                      f"bot {st['sig_bot']/1e3:6.1f} kPa (x{m['bot_skin_vs_tension']:.2f}) | tip {r['tip_defl_mm']:5.1f} mm, twist {r['tip_twist_deg']:+.2f} deg")
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), default=float, indent=1)


if __name__ == "__main__":
    main()
