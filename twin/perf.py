"""Z!B twin — trim + mission performance from the params-driven VLM.

Every constant not in params.json comes from zb_model/data/assumptions.yaml or
the controlled baseline record and is tagged in ASSUMPTIONS with its status.
"""
import math, os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlm  # noqa: E402

RHO, G = 1.225, 9.80665

# value, status, source  (status: measured | derived | assumed | baseline-record)
ASSUMPTIONS = {
    "mass_kg":        (0.2330, "baseline-record", "CE-01 FROZEN stacked roll-up 233.0 g (2026-10-14): planning 211.9 g + SA-01 R2-R5 + DR-01 fins + DR-14 notch + R-07 power train (Suppo 2204/14 20 g, APC 8x6SF 7.1 g, adapter 5.1 g). Source: scripts/mass_rollup.py --motor-g 20 --prop-g 7.1 --adapter-g 5.1 --notch-dia-in 8 --battery-fwd-mm 9 --esc-to-mm 95 --fc-fwd-mm 5. Weigh-as-built replaces it (B-12)"),
    "x_cg_mm":        (130.32, "baseline-record", "CE-01 FROZEN stacked CG, same roll-up (FC 5 mm fwd, battery_u 0.160, ESC at 95 mm). Was 128.5 (DESIGN_CLOSURE ITEM 2, pre-change baseline)"),
    "record_mass_kg": (0.2119, "baseline-record", "design-team record basis (A2 loop / five checks): planning 211.9 g + fins (added by mass_props); used ONLY for like-for-like twin-vs-record checks"),
    "record_x_cg_mm": (128.5, "baseline-record", "design-team record CG basis (DESIGN_CLOSURE ITEM 2), like-for-like checks only"),
    "mass_basis_includes_fins": (True, "baseline-record", "the CE-01 frozen roll-up already contains the DR-01 fins; mass_props() must not add them again"),
    "cd_misc":        (0.012,  "assumed",  "zb_model/drag.py flat placeholder; Hoerner buildup TODO"),
    "cd_profile_tab": ([(0.40, .0155), (0.50, .0155), (0.60, .0157), (0.70, .0163)], "measured", "MH60 XFoil Re100k Ncrit9 (airfoiltools)"),
    "clmax_section":  (1.16,   "measured", "MH60 polar"),
    "flap_knockdown": (0.75,   "assumed",  "CRITICAL, UNCALIBRATED (MBSE steelman 2026-10-14): inviscid VLM overpredicts plain-flap effectiveness; typical 0.7-0.8. Sets Cm_de (~-0.008/deg) shared with the design loop, so twin/design trim agreement is internal consistency only. Closed by bench throw + flight trim-vs-speed"),
    "pack_wh":        (7.215,  "derived",  "3S 650 mAh nominal"),
    "usable_frac":    (0.80,   "assumed",  "battery derate; bench test pending (UNCALIBRATED)"),
    "p_hotel_w":      (1.0,    "assumed",  "hotel load placeholder; bench test pending (UNCALIBRATED)"),
    "eta":            ("min(0.55, 0.20+0.0875*P_shaft)", "assumed", "propulsion derate fit; wattmeter pending (UNCALIBRATED)"),
    "v_floor_ms":     (7.0,    "derived",  "max(1.5*Vstall, 7.0) AIRFOIL_TRADE §3"),
    "cm0_section":    (-0.022, "measured", "MH60 XFoil Re100k Ncrit9 at CL~0.5 (AIRFOIL_TRADE.md; zb_model/trim.py CM0_AIRFOIL); -0.037 at CL 0"),
}


def thin_airfoil_cm(wing, n=4001):
    """Thin-airfoil Cm_ac of the mean line the VLM uses (inviscid). The VLM's section
    pitching moment is this value; the viscous section value comes from XFoil."""
    th = np.linspace(1e-4, math.pi - 1e-4, n); x = 0.5 * (1 - np.cos(th))
    s = np.array([wing.camber_slope(u) for u in x])
    return 0.5 * np.trapezoid(s * (np.cos(2 * th) - np.cos(th)), th)

def A(k): return ASSUMPTIONS[k][0]

def cd_profile(cl):
    t = A("cd_profile_tab")
    if cl <= t[0][0]: return t[0][1]
    for (c0, d0), (c1, d1) in zip(t, t[1:]):
        if c0 <= cl <= c1: return d0 + (cl - c0) / (c1 - c0) * (d1 - d0)
    (c0, d0), (c1, d1) = t[-2], t[-1]
    return d1 + (cl - c1) * (d1 - d0) / (c1 - c0)

def eta(p_shaft): return min(0.55, 0.20 + 0.0875 * p_shaft)

def mass_props(design, basis="frozen"):
    """Mass + CG. basis="frozen": the CE-01 frozen stacked roll-up (fins included).
    basis="record": the design-team record basis (211.9 g, 128.5 mm) plus the fins, for
    like-for-like twin-vs-record checks only."""
    import lateral
    if basis == "record":
        m, x, add_fins = A("record_mass_kg") * 1000, A("record_x_cg_mm"), True
    else:
        m, x, add_fins = A("mass_kg") * 1000, A("x_cg_mm"), not A("mass_basis_includes_fins")
    g = lateral.fin_geometry(design)
    if g is not None and add_fins:
        mf = 2 * design["fin_mass_g"]; xf = g["x_le_mm"] + 0.5 * g["cf"]
        x = (m * x + mf * xf) / (m + mf); m += mf
    return m / 1000, x


class Twin:
    def __init__(self, params_path=None, mass_basis="frozen"):
        self.raw, self.design, self.hash = vlm.load(params_path)
        self.w = vlm.Wing(self.design)
        self.d = self.w.derivatives()
        d, c = self.d, self.w.cref
        self.m, self.x_cg_mm = mass_props(self.design, mass_basis)
        xcg = self.x_cg_mm / 1000
        k = A("flap_knockdown")
        self.CLa, self.CL0 = d["CLa_per_deg"], d["CL0"]
        self.CLde = d["CLde_per_deg"] * k
        # transfer root-LE moments to CG
        self.Cm0 = d["Cm0_rootLE"] + d["CL0"] * xcg / c
        # viscous section-moment correction (2026-10-14, CE-01 trim reconciliation): the
        # inviscid mean line of the reflexed MH60 gives cm_ac ~ +0.006; XFoil gives -0.022.
        # A uniform section increment on the rectangular planform adds the same wing Cm0.
        self.cm_thin = thin_airfoil_cm(self.w)
        self.dCm_visc = A("cm0_section") - self.cm_thin
        self.Cm0 += self.dCm_visc
        self.Cma = -(d["x_np_mm"] / 1000 - xcg) / c * d["CLa_per_deg"]
        self.Cmde = (d["Cmde_rootLE_per_deg"] + d["CLde_per_deg"] * xcg / c) * k
        self.SM = (d["x_np_mm"] / 1000 - xcg) / c
        self.p_hotel = A("p_hotel_w")
        self.S = self.w.S; self.AR = self.w.AR; self.e = d["oswald_e"]

    def trim(self, V):
        CLreq = self.m * G / (0.5 * RHO * V * V * self.S)
        # Cm: Cm0 + Cma a + Cmde de = 0 ; CL: CL0 + CLa a + CLde de = CLreq
        M = np.array([[self.CLa, self.CLde], [self.Cma, self.Cmde]])
        a, de = np.linalg.solve(M, [CLreq - self.CL0, -self.Cm0])
        CL = CLreq
        CDi = CL * CL / (math.pi * self.AR * self.e)
        CDp = cd_profile(CL) + A("cd_misc")
        CDtrim = 1.3e-4 * de * de
        CD = CDi + CDp + CDtrim
        D = 0.5 * RHO * V * V * self.S * CD
        Pair = D * V
        # program definition (zb_model/mission.py): eta is evaluated at P_shaft = D*V,
        # and electrical propulsion power = P_shaft / eta
        ps = Pair
        p_prop = Pair / eta(Pair)
        stalled = CL > 0.9 * A("clmax_section")  # wing CLmax ~ 0.9 section (assumed)
        return dict(V=V, alpha=a, elevon=de, CL=CL, CD=CD, LD=CL / CD, D=D, P_air=Pair,
                    P_shaft=ps, eta=eta(ps), P_batt=p_prop + self.p_hotel, stalled=stalled)

    def vstall(self):
        CLmax = 0.9 * A("clmax_section")
        return math.sqrt(self.m * G / (0.5 * RHO * self.S * CLmax))

    def mission(self):
        E = A("pack_wh") * A("usable_frac") * 3600
        best_r, best_e, sweep = None, None, []
        for V in np.arange(max(self.vstall() * 1.3, 5.0), 16.01, 0.1):
            t = self.trim(V)
            t["endurance_min"] = E / t["P_batt"] / 60
            t["range_km"] = E / t["P_batt"] * V / 1000
            sweep.append(t)
        flyable = [t for t in sweep if t["V"] >= A("v_floor_ms")]
        best_r = max(flyable, key=lambda t: t["range_km"])
        best_e = max(flyable, key=lambda t: t["endurance_min"])
        return best_r, best_e, sweep

    def summary(self):
        r, e, sweep = self.mission()
        return dict(design_hash=self.hash, derivatives=self.d, SM=self.SM, x_cg_mm=self.x_cg_mm,
                    mass_g=self.m * 1000, vstall=self.vstall(), best_range=r, best_endurance=e,
                    Cm0_cg=self.Cm0, Cma_cg=self.Cma, CLde=self.CLde, Cmde_cg=self.Cmde)

if __name__ == "__main__":
    T = Twin(); s = T.summary()
    print("hash", s["design_hash"], " mass", s["mass_g"], "g  CG", s["x_cg_mm"], "mm")
    print(f"NP {s['derivatives']['x_np_mm']:.1f} mm  SM {100*s['SM']:.2f}%  Vstall {s['vstall']:.2f}")
    print(f"Cm0_cg {s['Cm0_cg']:.4f} Cma_cg {s['Cma_cg']:.5f}/deg CLde {s['CLde']:.4f} Cmde_cg {s['Cmde_cg']:.5f}/deg e {s['derivatives']['oswald_e']:.3f}")
    for k in ("best_range", "best_endurance"):
        t = s[k]; print(k, {kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in t.items()})
    for V in (6, 7, 8, 9, 10, 12):
        t = T.trim(V); print(V, f"a={t['alpha']:.2f} de={t['elevon']:.2f} L/D={t['LD']:.2f} Pb={t['P_batt']:.2f}")
