"""Fly the generated twin in JSBSim (6-DOF): trim check, elevon step, roll step.

JSBSim executable path via env JSBSIM (built from source, v1.2.1).
"""
import os, sys, math, csv, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_jsbsim  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
JSB = os.environ.get("JSBSIM", "/home/claude/tools/jsbsim/build/src/JSBSim")
PROPS = ["velocities/vt-fps", "position/h-sl-ft", "aero/alpha-deg", "attitude/theta-deg",
         "attitude/phi-deg", "attitude/psi-deg", "position/distance-from-start-mag-mt",
         "velocities/q-rad_sec", "velocities/p-rad_sec", "fcs/elevon-sym-deg", "fcs/elevon-diff-deg"]


def sim(name, V, alpha, elev_deg, thr, T=60.0, events=""):
    a = math.radians(alpha)
    os.makedirs(f"{HERE}/scripts", exist_ok=True)
    open(f"{HERE}/aircraft/zb_twin/{name}_ic.xml", "w").write(f'''<?xml version="1.0"?>
<initialize name="{name}_ic"><ubody unit="M/SEC">{V*math.cos(a)}</ubody><wbody unit="M/SEC">{V*math.sin(a)}</wbody>
<altitude unit="M">120</altitude><latitude unit="DEG">37</latitude><longitude unit="DEG">-122</longitude>
<psi unit="DEG">0</psi><theta unit="DEG">{alpha}</theta><phi unit="DEG">0</phi></initialize>''')
    out = "\n".join(f"  <property>{p}</property>" for p in PROPS)
    open(f"{HERE}/scripts/{name}.xml", "w").write(f'''<?xml version="1.0"?>
<runscript name="{name}"><use aircraft="zb_twin" initialize="{name}_ic"/>
<run start="0" end="{T}" dt="0.002">
 <property value="{thr}">fcs/throttle-cmd-norm</property>
 <property value="{elev_deg/8.0}">fcs/elevator-cmd-norm</property>{events}
</run>
<output name="out_{name}.csv" type="CSV" rate="10">
{out}
</output></runscript>''')
    r = subprocess.run([JSB, f"--root={HERE}", f"--script=scripts/{name}.xml"], cwd=HERE, capture_output=True, text=True)
    path = f"{HERE}/out_{name}.csv"
    if not os.path.exists(path):
        raise RuntimeError(r.stdout[-2000:] + r.stderr[-2000:])
    rows = list(csv.reader(open(path)))
    hdr = [h.split("/")[-1] for h in rows[0]]
    data = [dict(zip(hdr, map(float, x))) for x in rows[1:]]
    os.remove(path)
    return data


def step(t0, prop, val, name):
    return f'''
 <event name="{name}"><condition>simulation/sim-time-sec ge {t0}</condition>
  <set name="{prop}" value="{val}"/></event>'''


def main():
    T = gen_jsbsim.build()
    best_r, best_e, _ = T.mission()
    V = float(best_r["V"]); tr = T.trim(V)
    thr = tr["D"] / 1.5
    res = {"hash": T.hash, "V_trim": V, "alpha_trim": float(tr["alpha"]), "elevon_trim": float(tr["elevon"]), "throttle": thr}
    cruise = sim("cruise", V, tr["alpha"], tr["elevon"], thr, T=90)
    last = cruise[-1]
    res["cruise_90s"] = dict(V_end=last["vt-fps"] * 0.3048, dh_m=(last["h-sl-ft"] - cruise[0]["h-sl-ft"]) * 0.3048,
                             alpha_end=last["alpha-deg"], dist_m=last["distance-from-start-mag-mt"])
    pitch = sim("pitchstep", V, tr["alpha"], tr["elevon"], thr, T=20,
                events=step(2.0, "fcs/elevator-cmd-norm", (tr["elevon"] - 1.0) / 8.0, "de_step"))
    roll = sim("rollstep", V, tr["alpha"], tr["elevon"], thr, T=6,
               events=step(1.0, "fcs/aileron-cmd-norm", 0.5, "ail_on") + step(2.0, "fcs/aileron-cmd-norm", 0.0, "ail_off"))
    res["pitch_step_peak_q_dps"] = max(abs(r["q-rad_sec"]) for r in pitch) * 57.3
    res["roll_step_max_p_dps"] = max(abs(r["p-rad_sec"]) for r in roll) * 57.3
    res["roll_step_phi_at_2s"] = [r["phi-deg"] for r in roll if abs(r["Time"] - 2.0) < 0.05][0]
    json.dump({"result": res, "cruise": cruise[::5], "pitch": pitch, "roll": roll},
              open(f"{HERE}/fly_results.json", "w"))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
