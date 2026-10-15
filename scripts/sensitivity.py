"""D-32 decision-sensitivity sweep: does any PROVISIONAL input, at the pessimistic or
optimistic end of its band, flip a program decision or claim?

Decisions / claims checked (frozen CE-01 baseline, 233.0 g, CG 130.32 mm):
  C1 range at 7 m/s >= 26 km      (investor deck "26-29 km")
  C2 endurance at 7 m/s >= 59 min  (deck "62-70 min"; 59 = old headline floor)
  C3 static margin >= 5.5 %        (program rule)
  C4 all-up mass <= 250 g          (regulatory cap)
  C5 static thrust at THR_MAX >= 1.6 N (bench acceptance; requirement >= 1.1 N)
  C6 Cn_beta >= 0.001 /deg at CL 0.17 (DR-01 yaw stability)
  C7 elevon trim at 1.3 Vs within -12 deg up throw (DR-02), with 2 deg control reserve

Bands and sources: program/PROVISIONAL_VALUES.md. Usage: python3 scripts/sensitivity.py [--json out]
"""
import argparse, json, math, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin")); sys.path.insert(0, os.path.join(REPO, "scripts"))
import perf, lateral, vlm, motor_trade as mt  # noqa: E402

M0, X0 = 233.0, 130.32
_, DESIGN, _ = vlm.load()

# id: (name, low, best, high, unit)
BANDS = {
    "P-01": ("propulsion efficiency eta (overall)", 0.36, 0.42, 0.45, "-"),
    "P-02": ("hotel (electronics) power", 1.7, 1.0, 0.8, "W"),          # low = pessimistic
    "P-03": ("usable battery fraction", 0.75, 0.80, 0.85, "-"),
    "P-04": ("misc drag cd_misc", 0.018, 0.012, 0.008, "-"),
    "P-05": ("plain-flap knockdown", 0.65, 0.75, 0.85, "-"),
    "P-06": ("fin endplate factor", 1.30, 1.55, 1.80, "-"),
    "P-07": ("fin sidewash factor", 0.80, 1.00, 1.20, "-"),
    "P-08": ("aft-mass growth (motor/prop/adapter/fins vs estimate)", +4.0, 0.0, -1.0, "g at ~200 mm"),
    "P-09": ("motor Io and Rm vs vendor", 1.25, 1.00, 0.85, "x"),
}


def perf_case(eta=None, hotel=None, usable=None, cdm=None, knock=None, dm_aft=0.0):
    saved = {k: perf.ASSUMPTIONS[k] for k in ("eta_provisional", "p_hotel_w", "usable_frac", "cd_misc", "flap_knockdown")}
    try:
        for k, v in (("eta_provisional", eta), ("p_hotel_w", hotel), ("usable_frac", usable), ("cd_misc", cdm), ("flap_knockdown", knock)):
            if v is not None:
                perf.ASSUMPTIONS[k] = (v,) + perf.ASSUMPTIONS[k][1:]
        T = perf.Twin()
        if dm_aft:
            m = M0 + dm_aft; x = (M0 * X0 + dm_aft * 200.0) / m
            T.m, T.x_cg_mm = m / 1000, x
        T.p_hotel = perf.A("p_hotel_w")
        E = perf.A("pack_wh") * perf.A("usable_frac") * 3600
        t = T.trim(7.0)
        rng = E / t["P_batt"] * 7.0 / 1000; end = E / t["P_batt"] / 60
        sm = (T.d["x_np_mm"] - T.x_cg_mm) / 200
        vs = T.vstall(); tt = T.trim(1.3 * vs)
        return dict(range_km=rng, endur_min=end, sm=sm, auw=T.m * 1000, trim_slow=tt["elevon"])
    finally:
        perf.ASSUMPTIONS.update(saved)


def thrust_case(k=1.0):
    m = dict(mt.MOTORS["Suppo 2204/14 1400kv"]); m["Io"] *= k; m["Rm"] *= k
    return mt.full_throttle(m, mt.PROPS["APC 8x6SF"], 0.0, 12.6 * 0.65)["T"]


def cn_case(endplate=None, sidewash=None):
    saved = dict(lateral.ASSUMED)
    try:
        if endplate: lateral.ASSUMED["fin_endplate_factor"] = endplate
        if sidewash: lateral.ASSUMED["fin_eta_sidewash"] = sidewash
        T = perf.Twin()
        return float(lateral.derive(DESIGN, T.x_cg_mm, T.d["x_np_mm"], 0.17)["cn_beta_per_deg"])
    finally:
        lateral.ASSUMED.clear(); lateral.ASSUMED.update(saved)


def checks(r):
    out = {}
    if "range_km" in r:
        out["C1"] = r["range_km"] >= 26.0; out["C2"] = r["endur_min"] >= 59.0
        out["C3"] = r["sm"] >= 0.055; out["C4"] = r["auw"] <= 250.0; out["C7"] = r["trim_slow"] >= -10.0
    if "thrust" in r: out["C5"] = r["thrust"] >= 1.6
    if "cn" in r: out["C6"] = r["cn"] >= 0.001
    return out


def run():
    rows = []
    for pid, (name, lo, best, hi, unit) in BANDS.items():
        for tag, v in (("low", lo), ("best", best), ("high", hi)):
            if pid == "P-01": r = perf_case(eta=v)
            elif pid == "P-02": r = perf_case(hotel=v)
            elif pid == "P-03": r = perf_case(usable=v)
            elif pid == "P-04": r = perf_case(cdm=v)
            elif pid == "P-05": r = perf_case(knock=v)
            elif pid == "P-06": r = dict(cn=cn_case(endplate=v))
            elif pid == "P-07": r = dict(cn=cn_case(sidewash=v))
            elif pid == "P-08": r = perf_case(dm_aft=v)
            elif pid == "P-09": r = dict(thrust=thrust_case(v))
            c = checks(r)
            rows.append(dict(id=pid, name=name, case=tag, value=v, unit=unit, **{k: (round(x, 4) if isinstance(x, float) else x) for k, x in r.items()},
                             fails=[k for k, ok in c.items() if not ok]))
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--json")
    a = ap.parse_args(); rows = run()
    for r in rows:
        vals = {k: r[k] for k in ("range_km", "endur_min", "sm", "auw", "trim_slow", "thrust", "cn") if k in r}
        print(f"{r['id']} {r['case']:4s} {r['value']:>7} {r['unit']:12s} {vals}  FAILS={r['fails']}")
    if a.json: json.dump(rows, open(a.json, "w"), indent=1, default=float)
