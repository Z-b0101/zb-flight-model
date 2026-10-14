"""6-DOF mission flight in JSBSim with battery energy accounting.

Profile: climb at fixed throttle until +60 m, then cruise at best-range trim
until the usable battery energy is spent. Battery power each sample =
T*V/eta(P_shaft) + P_hotel (assumption ledger; all UNCALIBRATED).
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fly, perf  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def run(p_hotel=None, tag="mission"):
    T = perf.Twin()
    if p_hotel is not None: T.p_hotel = p_hotel
    ph = T.p_hotel
    best_r, _, _ = T.mission()
    V = float(best_r["V"]); tr = T.trim(V)
    thr_cruise = tr["D"] / 1.5
    thr_climb = 0.45
    E_usable = perf.A("pack_wh") * perf.A("usable_frac") * 3600.0
    # estimate cruise duration from analytic power, then fly a bit longer and cut at depletion
    T_end = E_usable / tr["P_batt"] * 1.15 + 120
    ev = fly.step(0.0, "fcs/throttle-cmd-norm", thr_climb, "climb")
    ev += f'''
 <event name="level"><condition>position/h-sl-ft ge {(120+60)/0.3048:.1f}</condition>
  <set name="fcs/throttle-cmd-norm" value="{thr_cruise}"/></event>'''
    fly.PROPS[:] = list(dict.fromkeys(fly.PROPS + ["fcs/throttle-pos-norm"]))
    data = fly.sim("mission", V, tr["alpha"], tr["elevon"], thr_climb, T=T_end, events=ev)
    E = 0.0; t_prev = 0.0; out = []; depleted = None
    for r in data:
        dt = r["Time"] - t_prev; t_prev = r["Time"]
        v = r["vt-fps"] * 0.3048
        Tn = 1.5 * r["throttle-pos-norm"]
        ps = Tn * v                      # shaft (air) power, program definition
        pb = ps / perf.eta(ps) + ph
        E += pb * dt
        out.append(dict(t=r["Time"], V=v, h=r["h-sl-ft"] * 0.3048, x=r["distance-from-start-mag-mt"],
                        alpha=r["alpha-deg"], theta=r["theta-deg"], phi=r["phi-deg"], P=pb, E_wh=E / 3600))
        if depleted is None and E >= E_usable:
            depleted = out[-1]; break
    res = dict(V_cruise=V, throttle_cruise=thr_cruise, E_usable_wh=E_usable / 3600,
               flight_time_min=(depleted or out[-1])["t"] / 60, range_km=(depleted or out[-1])["x"] / 1000,
               depleted=depleted is not None, h_min=min(o["h"] for o in out), h_max=max(o["h"] for o in out),
               analytic_range_km=float(best_r["range_km"]), analytic_endurance_min=float(best_r["endurance_min"]))
    res["p_hotel_w"] = ph
    json.dump({"result": res, "trace": out[::30]}, open(f"{HERE}/{tag}_results.json", "w"))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    run(0.0, "mission_a2basis")
    run(None, "mission")
