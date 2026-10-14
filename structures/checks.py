"""Z!B structural checks beyond the flight load cases (analysis.py):

  A. Spar-alone root bending (skins assumed buckled: the conservative design basis)
  B. Curved top-skin panel buckling (raises the flat-plate value used in analysis.py)
  C. Landing impact: centre-body pulse, wing dynamic bending (modal), battery/hatch, motor
  D. Hand launch: battery longitudinal load, grip crush on the centre section
  E. Motor mount (pusher): thrust, torque, landing inertia -> bond area required
  F. Root joiner (V-joint at 2 x 25 deg sweep): socket bearing, block bending, PLA orientation
  G. Glue joints: spar-rib (torque transfer, with and without the hinge-line web), rib-skin peel
  H. Carbon cap strips as an option (spar + caps alone)

Every input that is an assumption is named ASSUMED in the output so the coupon / bench data
can replace it. Reserve factor RF = allowable / (FOS x limit stress); RF >= 1 passes.

Run: python3 structures/checks.py -> structures/checks.json
"""
import os, sys, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "twin"))
from structures import model as SM  # noqa: E402
from structures import materials as MAT  # noqa: E402
from structures import analysis as AN  # noqa: E402

GEO = SM.Geometry()
FOS = MAT.FOS
D = MAT.DEPRON; PLA = MAT.PLA
G0 = SM.G0
BATT_KG = GEO.design["battery_mass_g"] / 1000

ASSUMED = dict(
    landing_sink_ms=1.5, landing_sink_abuse_ms=2.5, crush_stroke_m=0.003,
    inverted_impact_g=10.0,
    launch_speed_ms=9.0, launch_stroke_m=0.7, grip_force_N=20.0, grip_area_m2=2 * 15e-3 * 15e-3,
    motor_prop_kg=0.0322,   # CE-01 frozen: Suppo 2204/14 20 g + APC 8x6SF 7.1 g + adapter 5.1 g (was 0.025)
     thrust_max_N=6.0, shaft_power_W=120.0, rpm_max=15000.0,
    adhesive_tau_cf_pla_Pa=3.0e6,  # CA on lightly sanded pultruded carbon to PLA, conservative
    joiner_socket_L_m=0.040, joiner_block_mm=(12.0, 12.0),
    cap=dict(w=3e-3, t=0.5e-3, E=120e9, sigma_allow_c=500e6),
)


def rf(allow, limit):
    return allow / (FOS * limit) if limit > 0 else float("inf")


def gust_case(spar, web):
    c = [c for c in AN.cases() if c["id"] == "C4"][0]
    return AN.run_case(c, spar=spar, web=web), c


# ------------------------------------------------------------------ A. spar alone
def spar_alone():
    out = []
    sec = SM.section(GEO)
    I_t = sec["I_t"]; r = GEO.od / 2
    for cid in ("C3", "C4"):
        c = [c for c in AN.cases() if c["id"] == cid][0]
        M = AN.run_case(c, spar="nominal", web=True)["root"]["M"]   # root moment is grade-independent (statically determinate)
        sig = M * r / I_t
        for g, S in MAT.SPAR_GRADES.items():
            out.append(dict(case=cid, n=c["n"], grade=g, M_limit=M, sigma_limit_MPa=sig / 1e6, allow_MPa=S["sigma_allow"] / 1e6,
                            RF=rf(S["sigma_allow"], sig)))
    return out


# ------------------------------------------------------------------ B. curved panel buckling
def circle_radius(p1, p2, p3):
    a = np.linalg.norm(p2 - p1); b = np.linalg.norm(p3 - p2); c = np.linalg.norm(p3 - p1)
    A = 0.5 * abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1]))
    return a * b * c / (4 * A)


def curved_panel():
    c = GEO.c
    u0, u1 = GEO.u_spar, GEO.u_h; um = 0.5 * (u0 + u1)
    P = [np.array([u * c, GEO.af.top(u) * c]) for u in (u0, um, u1)]
    R = circle_radius(*P)
    b = (u1 - u0) * c
    flat = SM.skin_buckling_stress(GEO)
    flat_midweb = SM.skin_buckling_stress(GEO, width_frac=(u1 - u0) / 2)
    # curved panel, axial compression: knocked-down cylinder term (0.3 E t / R; classical 0.605, knockdown ~0.5)
    curved = 0.3 * D["E"] * D["t"] / R
    scr = max(flat, curved)
    Z = b**2 / (R * D["t"]) * math.sqrt(1 - D["nu"]**2)
    res = dict(R_mm=R * 1000, b_mm=b * 1000, Z=Z, flat_kPa=flat / 1e3, curved_kPa=curved / 1e3, used_kPa=scr / 1e3,
               midweb_kPa=flat_midweb / 1e3, crush_kPa=D["sigma_c"] / 1e3, cases=[])
    for cid in ("C3", "C4"):
        cc = [x for x in AN.cases() if x["id"] == cid][0]
        st = AN.run_case(cc, spar="nominal", web=True)["root"]
        res["cases"].append(dict(case=cid, skin="top (compression)", sig_kPa=st["sig_top"] / 1e3, RF_buckling=rf(scr, st["sig_top"]),
                                 RF_buckling_midweb=rf(flat_midweb, st["sig_top"]), RF_crush=rf(D["sigma_c"], st["sig_top"])))
    # landing: the wing bends DOWN, the bottom skin is in compression (scale the gust bottom stress by the moment ratio)
    st = AN.run_case([x for x in AN.cases() if x["id"] == "C4"][0], spar="nominal", web=True)["root"]
    Ml = landing_dynamic("nominal", True, ASSUMED["landing_sink_ms"])["M_root"]
    sb = st["sig_bot"] * Ml / st["M"]
    res["cases"].append(dict(case="landing 1.5 m/s", skin="bottom (compression)", sig_kPa=sb / 1e3, RF_buckling=rf(scr, sb),
                             RF_buckling_midweb=rf(flat_midweb, sb), RF_crush=rf(D["sigma_c"], sb)))
    return res


# ------------------------------------------------------------------ C. landing
def landing_dynamic(spar="nominal", web=True, sink=1.5):
    """Base-stop transient: the centre body stops in the crush stroke; the wings keep moving.
    Modal superposition (first 6 uncoupled-mass modes), peak root moment by SRSS of the
    modal maxima amp_i = Gamma_i * v / omega_i (impulse limit; the pulse is short vs the
    wing period) -- conservative versus the half-sine shock spectrum."""
    fe, ys, sec = SM.build(GEO, spar=spar, web=web)
    Mg = SM.mass_matrix(GEO, fe, ys)
    f = fe.free
    from scipy.linalg import eigh
    w2, phi = eigh(fe.K[np.ix_(f, f)], Mg[np.ix_(f, f)] + 1e-12 * np.eye(len(f)))
    rvec = np.zeros(6 * fe.n); rvec[2::6] = 1.0
    t_pulse = 2 * ASSUMED["crush_stroke_m"] / sink
    Ms, Ts = [], []
    for i in range(6):
        v = np.zeros(6 * fe.n); v[f] = phi[:, i]
        Gam = v @ Mg @ rvec
        om = math.sqrt(w2[i])
        # half-sine base pulse DLF on the impulse: shock-spectrum factor <= 1 for short pulses, use 1
        amp = Gam * sink / om
        ef = fe.element_forces(v * amp)[0]
        Ms.append(abs(ef["My"])); Ts.append(abs(ef["T"]))
    M = math.sqrt(sum(m**2 for m in Ms)); T = math.sqrt(sum(t**2 for t in Ts))
    n_body = sink**2 / (2 * ASSUMED["crush_stroke_m"]) / G0
    return dict(spar=spar, web=web, sink=sink, pulse_ms=1000 * t_pulse, n_body=n_body, M_root=M, T_root=T,
                f1_hz=math.sqrt(w2[0]) / (2 * math.pi))


def landing():
    sink = ASSUMED["landing_sink_ms"]
    n_body = sink**2 / (2 * ASSUMED["crush_stroke_m"]) / G0
    F_batt_down = BATT_KG * G0 * n_body                       # into the hatch, which is on the ground: compression
    F_batt_out = BATT_KG * G0 * ASSUMED["inverted_impact_g"]  # cartwheel / inverted: pulls the hatch off
    req_retention = FOS * F_batt_out
    dyn = [landing_dynamic(s, True, v) for s in ("low", "nominal", "premium") for v in (sink, ASSUMED["landing_sink_abuse_ms"])]
    r = GEO.od / 2; I_t = SM.section(GEO)["I_t"]
    for d in dyn:
        d["sigma_spar_alone_MPa"] = d["M_root"] * r / I_t / 1e6
        d["RF_spar_alone"] = rf(MAT.SPAR_GRADES[d["spar"]]["sigma_allow"], d["M_root"] * r / I_t)
    F_motor = ASSUMED["motor_prop_kg"] * G0 * n_body
    return dict(n_body=n_body, F_battery_into_hatch_N=F_batt_down, F_battery_inverted_N=F_batt_out,
                hatch_retention_required_N=req_retention, F_motor_landing_N=F_motor, wing_dynamic=dyn)


# ------------------------------------------------------------------ D. hand launch
def launch():
    v = ASSUMED["launch_speed_ms"]; s = ASSUMED["launch_stroke_m"]
    a = v**2 / (2 * s); n_x = a / G0
    F_batt = BATT_KG * a
    p_grip = ASSUMED["grip_force_N"] / ASSUMED["grip_area_m2"]
    return dict(n_x=n_x, F_battery_aft_N=F_batt, grip_pressure_kPa=p_grip / 1e3,
                RF_grip_crush=rf(D["sigma_c"], p_grip))


# ------------------------------------------------------------------ E. motor mount
def motor_mount():
    T = ASSUMED["thrust_max_N"]
    Q = ASSUMED["shaft_power_W"] / (ASSUMED["rpm_max"] * 2 * math.pi / 60)
    n_body = ASSUMED["landing_sink_ms"]**2 / (2 * ASSUMED["crush_stroke_m"]) / G0
    F_land = ASSUMED["motor_prop_kg"] * G0 * n_body
    F_design = max(T, F_land)
    A_foam = FOS * F_design / D["tau"]                       # bonded to Depron only
    A_pla = FOS * F_design / ASSUMED["adhesive_tau_cf_pla_Pa"]  # bonded/screwed into the PLA centre section
    return dict(thrust_N=T, torque_Nm=Q, F_landing_N=F_land, F_design_N=F_design,
                bond_area_min_foam_mm2=A_foam * 1e6, bond_area_min_pla_mm2=A_pla * 1e6,
                note="foam-only bond area is a shear minimum; peel on a cantilevered mount needs ~4x that. Tie the mount into the printed centre section.")


# ------------------------------------------------------------------ F. root joiner
def joiner():
    r4, _ = gust_case("nominal", True)
    M = r4["root"]["M"]; T = r4["root"]["T"]
    Meq = math.hypot(M, T)                     # at the V apex, one arm's torsion becomes the other's bending
    Mu = FOS * Meq
    L = ASSUMED["joiner_socket_L_m"]; d = GEO.od
    p_bear = 6 * Mu / (d * L**2)               # linear bearing distribution along the socket, peak
    bw, bh = (x / 1000 for x in ASSUMED["joiner_block_mm"])
    dh = GEO.design["spar_slot_dia"] / 1000
    I_blk = bw * bh**3 / 12 - math.pi * dh**4 / 64
    sig_blk = Mu * (bh / 2) / I_blk
    depth = (GEO.af.top(GEO.u_spar) - GEO.af.bot(GEO.u_spar)) * GEO.c
    return dict(M_limit=M, T_limit=T, M_equiv_limit=Meq, M_ult=Mu, socket_L_mm=L * 1000, bearing_peak_MPa=p_bear / 1e6,
                block_mm=ASSUMED["joiner_block_mm"], block_sigma_ult_MPa=sig_blk / 1e6,
                RF_block_inlayer=PLA["sigma_xy"] / sig_blk, RF_block_interlayer=PLA["sigma_z"] / sig_blk,
                RF_bearing=PLA["sigma_xy"] / p_bear, airfoil_depth_at_spar_mm=depth * 1000)


# ------------------------------------------------------------------ G. glue joints
def bonds():
    out = []
    for web in (False, True):
        r4, _ = gust_case("nominal", web)
        sec = r4["sec"]
        T_sp = r4["root"]["T"] * sec["GJ_spar"] / sec["GJ"]
        # spar torque fed in through the 4 rib slots per side; worst rib takes ~half (root bay)
        T_rib = 0.5 * T_sp
        A = math.pi * GEO.od * MAT_rib_t()
        tau = T_rib / (A * GEO.od / 2)
        out.append(dict(web=web, T_spar_limit=T_sp, tau_spar_rib_kPa=tau / 1e3,
                        RF=rf(ASSUMED["adhesive_tau_cf_pla_Pa"], tau)))
    # rib-skin peel under top-surface suction: peak suction ~3x mean at gust
    n = [c for c in AN.cases() if c["id"] == "C4"][0]["n"]
    W = SM.MASS["total_g"] / 1000 * G0
    p_peak = 3 * n * W / GEO.wing.S
    spacing = GEO.rib_y[1] - GEO.rib_y[0]
    line = p_peak * spacing                      # N/m along each rib (both sides of the rib share it)
    peel = line / (GEO.design["rib_t"] / 1000)
    return dict(spar_rib=out, rib_skin=dict(p_peak_Pa=p_peak, rib_spacing_mm=spacing * 1000, line_load_N_per_m=line,
                                            peel_kPa=peel / 1e3, RF_vs_depron_tension=rf(D["sigma_t"], peel)))


def MAT_rib_t():
    return GEO.design["rib_t"] / 1000


# ------------------------------------------------------------------ H. caps option
def caps_option():
    cap = ASSUMED["cap"]
    zt = GEO.af.top(GEO.u_spar) * GEO.c - D["t"] - cap["t"] / 2; zb = GEO.af.bot(GEO.u_spar) * GEO.c + D["t"] + cap["t"] / 2
    zs = GEO.af.mid(GEO.u_spar) * GEO.c
    A = cap["w"] * cap["t"]
    out = []
    for g, S in MAT.SPAR_GRADES.items():
        sec = SM.section(GEO, spar=g)
        EI_t = S["E"] * sec["I_t"]
        # neutral axis of tube + 2 caps
        EA = S["E"] * sec["A_t"] + 2 * cap["E"] * A
        zn = (S["E"] * sec["A_t"] * zs + cap["E"] * A * (zt + zb)) / EA
        EI = EI_t + S["E"] * sec["A_t"] * (zs - zn)**2 + cap["E"] * A * ((zt - zn)**2 + (zb - zn)**2)
        M = gust_case(g, True)[0]["root"]["M"]
        k = M / EI
        s_cap = cap["E"] * k * max(zt - zn, zn - zb)
        s_tube = S["E"] * k * (abs(zs - zn) + GEO.od / 2)
        # cap stability: between ribs it is a column on the spar-line web (elastic foundation k = E_foam t_web / h)
        h = zt - zb; k_f = D["E"] * D["t"] / h; I_c = cap["w"] * cap["t"]**3 / 12
        s_cr = 2 * math.sqrt(k_f * cap["E"] * I_c) / A
        s_cr_noweb = math.pi**2 * cap["E"] * I_c / (GEO.rib_y[1] - GEO.rib_y[0])**2 / A
        out.append(dict(grade=g, EI_tube=EI_t, EI_with_caps=EI, RF_tube=rf(S["sigma_allow"], s_tube),
                        RF_cap=rf(cap["sigma_allow_c"], s_cap), cap_sigma_limit_MPa=s_cap / 1e6,
                        cap_buckle_on_web_MPa=s_cr / 1e6, RF_cap_buckle_on_web=rf(s_cr, s_cap),
                        cap_buckle_no_web_MPa=s_cr_noweb / 1e6, RF_cap_buckle_no_web=rf(s_cr_noweb, s_cap),
                        cap_arm_mm=1000 * (zt - zn)))
    mass_full = 2 * A * GEO.b / math.cos(GEO.lam) * 1600 * 1000
    return dict(per_grade=out, mass_full_span_g=mass_full, mass_inboard_60pct_g=0.6 * mass_full,
                note="caps need a shear connection to the tube (filler or full-depth web at the spar line); fallback only")


def main():
    out = dict(hash=GEO.hash, fos=FOS, assumed=ASSUMED,
               A_spar_alone=spar_alone(), B_curved_panel=curved_panel(), C_landing=landing(),
               D_launch=launch(), E_motor_mount=motor_mount(), F_joiner=joiner(), G_bonds=bonds(), H_caps=caps_option())
    json.dump(out, open(os.path.join(HERE, "checks.json"), "w"), default=float, indent=1)
    return out


if __name__ == "__main__":
    o = main()
    print(json.dumps({k: v for k, v in o.items() if k != "assumed"}, default=lambda x: round(float(x), 3), indent=1))
