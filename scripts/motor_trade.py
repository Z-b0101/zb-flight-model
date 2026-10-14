"""R-07 motor / ESC / propeller trade (GM, 2026-10-14).

Physics, not the twin's lumped derate:
  * Propeller: measured CT(J), CP(J) from the UIUC Propeller Data Site, vol. 1
    (Brandt & Selig, low-Re wind tunnel, ~4000 rpm runs + static runs). File names
    are cited per prop so a reviewer can re-pull them.
  * Motor: Drela three-constant brushless DC model (Kv, Rm, Io):
        Q = (I - Io) / Kv_rad ;  V_m = omega / Kv_rad + I * Rm
  * ESC: 0.95 efficiency (ASSUMED); wiring/connector 0.02 ohm (ASSUMED).
  * Battery: 3S, 11.1 V nominal cruise basis, 0.06 ohm pack (ASSUMED, GNB 650 80C class);
    full-throttle cases at 12.6 V (fresh) and 11.1 V.
For every flight point the twin uses, the script solves the rpm that gives T = D (or
the climb thrust), then the motor current, electrical power and overall efficiency, and
compares that efficiency with the twin's ASSUMED derate eta = min(0.55, 0.20 + 0.0875*P).

Usage: python3 scripts/motor_trade.py [--json out.json]
"""
import argparse, json, math, os, sys
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin"))
RHO, G = 1.225, 9.80665
IN = 0.0254

# ------------------------------------------------------------------ propellers (UIUC vol 1)
# static: (rpm, CT, CP) rows; perf: (J, CT, CP) rows at ~4000 rpm.
PROPS = {
    "APC 8x4E": dict(D=8 * IN, mass_g=13.0, rpm_limit=145000 / 8, src="UIUC apce_8x4_static_2791rd / apce_8x4_2792rd_4001",
        static=[(3037, .0892, .0392), (4090, .0921, .0393), (5128, .0941, .0398), (6197, .0961, .0401), (6989, .0978, .0401)],
        perf=[(.172, .0745, .0382), (.223, .0647, .0357), (.266, .0595, .0343), (.309, .0543, .0333), (.368, .0469, .0311),
              (.408, .0413, .0294), (.459, .0343, .0268), (.497, .0288, .0244), (.549, .0201, .0200), (.594, .0124, .0163),
              (.644, .0039, .0121)]),
    "APC 8x6E": dict(D=8 * IN, mass_g=13.9, rpm_limit=145000 / 8, src="UIUC apce_8x6_static_2797rd / apce_8x6_2798rd_4009",
        static=[(2534, .1083, .0745), (3631, .1108, .0740), (4754, .1128, .0742), (5882, .1147, .0759), (6700, .1181, .0760)],
        perf=[(.171, .1098, .0695), (.221, .1097, .0682), (.269, .1057, .0673), (.309, .1031, .0675), (.353, .0992, .0668),
              (.406, .0943, .0673), (.452, .0885, .0670), (.496, .0759, .0619), (.538, .0664, .0571), (.594, .0563, .0516),
              (.634, .0501, .0483), (.681, .0431, .0441), (.727, .0360, .0399), (.776, .0288, .0353), (.806, .0229, .0313),
              (.864, .0129, .0239), (.905, .0052, .0189)]),
    "APC 8x3.8SF": dict(D=8 * IN, mass_g=8.5, rpm_limit=65000 / 8, src="UIUC apcsf_8x3.8_static_2777rd / apcsf_8x3.8_2778rd_4007",
        static=[(3030, .0951, .0415), (4093, .0994, .0424), (5132, .1035, .0441), (6212, .1087, .0464), (7015, .1143, .0481)],
        perf=[(.174, .0828, .0409), (.218, .0771, .0401), (.263, .0705, .0387), (.307, .0644, .0375), (.355, .0568, .0357),
              (.405, .0483, .0338), (.458, .0387, .0316), (.497, .0309, .0294), (.548, .0195, .0260), (.596, .0094, .0230),
              (.631, .0015, .0205)]),
    "APC 8x6SF": dict(D=8 * IN, mass_g=7.1, rpm_limit=65000 / 8, src="UIUC apcsf_8x6_static_2783rd / apcsf_8x6_2784rd_4010",
        static=[(2485, .1412, .0806), (3070, .1412, .0796), (3581, .1449, .0822), (4152, .1469, .0825), (4685, .1482, .0841),
                (5240, .1499, .0864), (5783, .1517, .0885), (6336, .1544, .0909), (6611, .1570, .0923)],
        perf=[(.171, .1373, .0808), (.218, .1321, .0800), (.262, .1271, .0794), (.310, .1207, .0783), (.353, .1135, .0763),
              (.403, .1058, .0743), (.454, .0968, .0713), (.493, .0895, .0685), (.547, .0816, .0656), (.586, .0747, .0626),
              (.637, .0657, .0583), (.676, .0596, .0553), (.726, .0496, .0501), (.771, .0409, .0450), (.816, .0311, .0399),
              (.863, .0211, .0340), (.911, .0080, .0267)]),
}
# prop masses (vendor listings, 2026-10-14): ReadyMadeRC 8x4E 13.0 g, 8x6E 13.9 g, 8x6SF 7.1 g (Motion RC 7.08 g);
# 8x3.8SF ~8.5 g (estimate). WEIGH AT RECEIPT. APC SF props have a 65,000/D(in) rpm limit (8125 rpm for 8 in).


def prop_coeffs(p, J, rpm):
    st = np.array(p["static"]); pf = np.array(p["perf"])
    ct0 = np.interp(rpm, st[:, 0], st[:, 1]); cp0 = np.interp(rpm, st[:, 0], st[:, 2])
    if J <= 0: return ct0, cp0
    Js = np.concatenate([[0.0], pf[:, 0]]); CT = np.concatenate([[ct0], pf[:, 1]]); CP = np.concatenate([[cp0], pf[:, 2]])
    if J > Js[-1]: return -1.0, CP[-1]
    return float(np.interp(J, Js, CT)), float(np.interp(J, Js, CP))


def prop_point(p, V, T_req):
    """rpm, shaft power, torque for thrust T_req at airspeed V."""
    D = p["D"]
    lo, hi = 500.0, 30000.0
    for _ in range(80):
        rpm = 0.5 * (lo + hi); n = rpm / 60
        ct, cp = prop_coeffs(p, V / (n * D), rpm)
        if ct * RHO * n * n * D ** 4 < T_req: lo = rpm
        else: hi = rpm
    n = rpm / 60; J = V / (n * D); ct, cp = prop_coeffs(p, J, rpm)
    P = cp * RHO * n ** 3 * D ** 5
    return dict(rpm=rpm, J=J, P_shaft=P, Q=P / (2 * math.pi * n), eta_p=T_req * V / P if P > 0 else 0)


# ------------------------------------------------------------------ motors (vendor constants)
MOTORS = {
    "Suppo 2204/14 1400kv": dict(Kv=1400, Rm=0.550, Io=0.30, Io_V=10, mass_g=20.0, I_max=7.5, P_max=83, shaft_mm=3.0,
        src="altitudehobbies.com (Suppo 2204/14 1400kv, Park 300 equiv.), checked 2026-10-14: 20 g, 7.5 A/60 s, 83 W, Rm 0.550, Io 0.3 A @10 V, 2-3S, props 8x3.8SF/8x4E/GWS 8060"),
    "HobbyStar 2204-27 1200KV (ref., 30 g)": dict(Kv=1200, Rm=0.368, Io=0.40, Io_V=10, mass_g=30.0, I_max=11, P_max=140, shaft_mm=3.0,
        src="rcjuice.com HobbyStar 2204 (2822), 2026-10-14 (sold out; reference only: over the 20 g cap)"),
}
R_WIRE, ETA_ESC, R_PACK = 0.02, 0.95, 0.06


def motor_point(m, rpm, Q, io_speed_scaled=False):
    kv = m["Kv"] * 2 * math.pi / 60          # rad/s per V
    w = rpm * 2 * math.pi / 60
    Io = m["Io"]
    if io_speed_scaled:                      # Io measured at Io_V no-load speed; scale ~ sqrt(speed)
        Io *= math.sqrt(max(w / (kv * m["Io_V"]), 0.05))
    I = Q * kv + Io
    Vm = w / kv + I * (m["Rm"] + R_WIRE)
    Pin = Vm * I / ETA_ESC
    return dict(I=I, Vm=Vm, P_elec=Pin, eta_m=Q * w / (Vm * I))


def full_throttle(m, p, V, Vbatt):
    """Throttle 100%: rpm where motor torque = prop torque at airspeed V."""
    kv = m["Kv"] * 2 * math.pi / 60; D = p["D"]
    lo, hi = 300.0, m["Kv"] * Vbatt
    for _ in range(80):
        rpm = 0.5 * (lo + hi); n = rpm / 60; w = rpm * 2 * math.pi / 60
        ct, cp = prop_coeffs(p, V / (n * D), rpm)
        Qp = cp * RHO * n ** 3 * D ** 5 / (2 * math.pi * n)
        # motor current available at this speed with the pack sagging: Vbatt - I*R_PACK = w/kv + I*(Rm+R_WIRE)
        I = (Vbatt - w / kv) / (m["Rm"] + R_WIRE + R_PACK)
        Qm = (I - m["Io"]) / kv
        if Qm > Qp: lo = rpm
        else: hi = rpm
    n = rpm / 60; ct, cp = prop_coeffs(p, V / (n * D), rpm)
    w = rpm * 2 * math.pi / 60
    I = (Vbatt - w / kv) / (m["Rm"] + R_WIRE + R_PACK)
    return dict(rpm=rpm, T=ct * RHO * n * n * D ** 4, I=I, P_batt=Vbatt * I, P_shaft=cp * RHO * n ** 3 * D ** 5)


def twin_eta(p_air): return min(0.55, 0.20 + 0.0875 * p_air)


def run():
    import perf
    T = perf.Twin(); W = T.m * G
    r, e, _ = T.mission()
    pts = [("A2 endurance cruise", float(e["V"]), float(e["D"])),
           ("A2 range cruise", float(r["V"]), float(r["D"])),
           ("Fast cruise 14 m/s", 14.0, float(T.trim(14.0)["P_shaft"]) / 14.0)]
    # climb: 2.0 m/s at 10 m/s airspeed
    Vc, ROC = 10.0, 2.0
    Dc = float(T.trim(Vc)["P_shaft"]) / Vc
    pts.append(("Climb 2 m/s at 10 m/s", Vc, Dc + W * ROC / Vc))
    out = dict(W_N=W, mass_kg=T.m, points=[], full_throttle=[])
    for mn, m in MOTORS.items():
        for pn, p in PROPS.items():
            for name, V, Treq in pts:
                pp = prop_point(p, V, Treq)
                mp = motor_point(m, pp["rpm"], pp["Q"])
                mps = motor_point(m, pp["rpm"], pp["Q"], io_speed_scaled=True)
                eta = Treq * V / mp["P_elec"]; eta_s = Treq * V / mps["P_elec"]
                out["points"].append(dict(motor=mn, prop=pn, point=name, V=V, T=Treq, **{k: pp[k] for k in ("rpm", "J", "P_shaft", "eta_p")},
                    I=mp["I"], P_elec=mp["P_elec"], eta_m=mp["eta_m"], eta_total=eta, eta_total_Io_scaled=eta_s,
                    throttle=mp["Vm"] / 11.1, twin_eta=twin_eta(Treq * V)))
            for Vb in (12.6, 11.1):
                for V in (0.0, 10.0):
                    ft = full_throttle(m, p, V, Vb)
                    out["full_throttle"].append(dict(motor=mn, prop=pn, Vbatt=Vb, V=V, **ft,
                        T_over_W=ft["T"] / W, I_over_rating=ft["I"] / m["I_max"]))
    return out


def report(o):
    L = [f"Mass {o['mass_kg']*1000:.1f} g, weight {o['W_N']:.3f} N\n",
         "| Motor | Prop | Point | V | T (N) | rpm | J | eta_prop | I (A) | P_elec (W) | eta_motor | eta_total (Io const / Io~sqrt(rpm)) | twin eta | throttle |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for p in o["points"]:
        L.append(f"| {p['motor']} | {p['prop']} | {p['point']} | {p['V']:.2f} | {p['T']:.3f} | {p['rpm']:.0f} | {p['J']:.2f} | {p['eta_p']:.2f} | {p['I']:.2f} | {p['P_elec']:.2f} | {p['eta_m']:.2f} | {p['eta_total']:.2f} / {p['eta_total_Io_scaled']:.2f} | {p['twin_eta']:.2f} | {100*p['throttle']:.0f}% |")
    L += ["", "| Motor | Prop | Vbatt | V (m/s) | rpm | Thrust (N) | T/W | I (A) | I / rating | P_batt (W) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for f in o["full_throttle"]:
        L.append(f"| {f['motor']} | {f['prop']} | {f['Vbatt']} | {f['V']:.0f} | {f['rpm']:.0f} | {f['T']:.2f} | {f['T_over_W']:.2f} | {f['I']:.2f} | {f['I_over_rating']:.2f} | {f['P_batt']:.1f} |")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--json")
    a = ap.parse_args(); o = run(); print(report(o))
    if a.json: json.dump(o, open(a.json, "w"), indent=1, default=float)
