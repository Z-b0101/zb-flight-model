"""One-minute takeoff-to-landing flight of the Z!B twin in JSBSim (6-DOF).

Profile: hand launch -> climb to 20 m -> level -> right 180 deg turn -> downwind ->
right 180 deg descending turn, power off -> glide approach -> flare -> belly landing and slide-out.

The aircraft is the generated twin (aircraft/zb_twin/zb_twin.xml, from cad/params.json)
plus a SIMPLE SCRIPTED CONTROLLER added here (pitch-attitude hold and bank hold, in a
JSBSim <system>). It stands in for the ArduPlane autopilot, which is not in the loop yet
(SITL is roadmap Phase 0 work). The thrust model is the UNCALIBRATED 1.5 N placeholder (R-07).
Output: twin/takeoff_landing.json (30 Hz trace for the viewer).
"""
import os, sys, math, csv, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_jsbsim  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
JSB = os.environ.get("JSBSIM", "/home/claude/tools/jsbsim/build/src/JSBSim")
NAME = "zb_twin_tl"

AUTOPILOT = """
 <system name="scripted_controller">
  <!-- Stand-in for the autopilot: pitch-attitude hold and bank hold. Not ArduPlane. -->
  <property value="0">ap/theta-cmd-deg</property>
  <property value="0">ap/phi-cmd-deg</property>
  <property value="-0.22">ap/elev-trim-norm</property>
  <property value="0">ap/phase</property>
  <property value="0.9">fcs/throttle-cmd-norm</property>
  <channel name="pitch">
   <fcs_function name="ap/theta-err-deg"><function><difference>
     <property>ap/theta-cmd-deg</property><property>attitude/theta-deg</property></difference></function></fcs_function>
   <pid name="ap/theta-pi"><input>ap/theta-err-deg</input><kp>0.15</kp><ki>0.06</ki><kd>0.0</kd>
     <clipto><min>-0.6</min><max>0.6</max></clipto></pid>
   <fcs_function name="fcs/elevator-cmd-norm"><function><sum>
     <property>ap/elev-trim-norm</property>
     <product><property>ap/theta-pi</property><value>-1</value></product>
     <product><property>velocities/q-rad_sec</property><value>2.0</value></product></sum></function>
     <clipto><min>-1</min><max>1</max></clipto></fcs_function>
  </channel>
  <channel name="roll">
   <fcs_function name="fcs/aileron-cmd-norm"><function><sum>
     <product><difference><property>ap/phi-cmd-deg</property><property>attitude/phi-deg</property></difference><value>0.03</value></product>
     <product><property>velocities/p-rad_sec</property><value>-0.25</value></product></sum></function>
     <clipto><min>-1</min><max>1</max></clipto></fcs_function>
  </channel>
 </system>
"""


def ev(name, cond, sets):
    s = "".join(f'<set name="{p}" value="{v}"/>' for p, v in sets)
    tests = "\n    ".join(cond.split(" AND "))
    return f'\n <event name="{name}"><condition logic="AND">\n    {tests}\n  </condition>{s}</event>'


def build_aircraft():
    gen_jsbsim.build()
    src = open(f"{HERE}/aircraft/zb_twin/zb_twin.xml").read()
    src = src.replace('name="zb_twin"', f'name="{NAME}"', 1)
    src = src.replace("</fdm_config>", AUTOPILOT + "</fdm_config>")
    os.makedirs(f"{HERE}/aircraft/{NAME}", exist_ok=True)
    open(f"{HERE}/aircraft/{NAME}/{NAME}.xml", "w").write(src)


def run(T=62.0):
    build_aircraft()
    open(f"{HERE}/aircraft/{NAME}/launch_ic.xml", "w").write('''<?xml version="1.0"?>
<initialize name="launch_ic"><ubody unit="M/SEC">9.0</ubody><wbody unit="M/SEC">0.3</wbody>
<altitude unit="M">1.8</altitude><latitude unit="DEG">37</latitude><longitude unit="DEG">-122</longitude>
<psi unit="DEG">0</psi><theta unit="DEG">6</theta><phi unit="DEG">0</phi></initialize>''')
    events = "".join([
        ev("launch", "simulation/sim-time-sec ge 0", [("fcs/throttle-cmd-norm", 0.9), ("ap/theta-cmd-deg", 18.4), ("ap/phase", 1)]),
        ev("level", "position/h-agl-ft ge 66 AND ap/phase == 1", [("fcs/throttle-cmd-norm", 0.25), ("ap/theta-cmd-deg", 6.9), ("ap/phase", 2)]),
        ev("turn1", "simulation/sim-time-sec ge 10 AND ap/phase == 2", [("ap/phi-cmd-deg", 30), ("ap/theta-cmd-deg", 8.4), ("fcs/throttle-cmd-norm", 0.32), ("ap/phase", 3)]),
        ev("downwind", "attitude/psi-deg ge 172 AND attitude/psi-deg le 200 AND ap/phase == 3", [("ap/phi-cmd-deg", 0), ("ap/theta-cmd-deg", 6.9), ("fcs/throttle-cmd-norm", 0.25), ("ap/phase", 4)]),
        ev("turn2", "simulation/sim-time-sec ge 26 AND ap/phase == 4", [("ap/phi-cmd-deg", 30), ("ap/theta-cmd-deg", 2.9), ("fcs/throttle-cmd-norm", 0.0), ("ap/phase", 5)]),
        ev("final", "attitude/psi-deg ge 352 AND attitude/psi-deg le 359.99 AND ap/phase == 5",
           [("ap/phi-cmd-deg", 0), ("fcs/throttle-cmd-norm", 0.0), ("ap/theta-cmd-deg", -0.1), ("ap/phase", 6)]),
        ev("flare", "position/h-agl-ft le 5 AND ap/phase == 6", [("ap/theta-cmd-deg", 7.9), ("ap/phase", 7)]),
        ev("touchdown", "position/h-agl-ft le 0.6 AND ap/phase == 7", [("ap/phase", 8)]),
    ])
    props = ["position/lat-geod-deg", "position/long-gc-deg", "position/h-agl-ft", "attitude/phi-deg",
             "attitude/theta-deg", "attitude/psi-deg", "velocities/vt-fps", "velocities/vc-kts",
             "fcs/throttle-pos-norm", "fcs/elevon-sym-deg", "fcs/elevon-diff-deg", "ap/phase", "aero/alpha-deg",
             "velocities/h-dot-fps"]
    out = "\n".join(f"  <property>{p}</property>" for p in props)
    os.makedirs(f"{HERE}/scripts", exist_ok=True)
    open(f"{HERE}/scripts/takeoff_landing.xml", "w").write(f'''<?xml version="1.0"?>
<runscript name="takeoff_landing"><use aircraft="{NAME}" initialize="launch_ic"/>
<run start="0" end="{T}" dt="0.002">
 <property value="0.9">fcs/throttle-cmd-norm</property>{events}
</run>
<output name="out_tl.csv" type="CSV" rate="30">
{out}
</output></runscript>''')
    r = subprocess.run([JSB, f"--root={HERE}", "--script=scripts/takeoff_landing.xml"], cwd=HERE, capture_output=True, text=True)
    path = f"{HERE}/out_tl.csv"
    if not os.path.exists(path):
        raise RuntimeError(r.stdout[-3000:] + r.stderr[-3000:])
    rows = list(csv.reader(open(path)))
    hdr = [h.split("/")[-1] for h in rows[0]]
    data = [dict(zip(hdr, map(float, x))) for x in rows[1:]]
    os.remove(path)
    lat0, lon0 = data[0]["lat-geod-deg"], data[0]["long-gc-deg"]
    R = 6371000.0
    trace = []
    for d in data:
        n = math.radians(d["lat-geod-deg"] - lat0) * R
        e = math.radians(d["long-gc-deg"] - lon0) * R * math.cos(math.radians(lat0))
        trace.append(dict(t=round(d["Time"], 3), n=round(n, 2), e=round(e, 2), h=round(d["h-agl-ft"] * 0.3048, 3),
                          phi=round(d["phi-deg"], 2), theta=round(d["theta-deg"], 2), psi=round(d["psi-deg"], 2),
                          V=round(d["vt-fps"] * 0.3048, 2), thr=round(d["throttle-pos-norm"], 3),
                          de=round(d["elevon-sym-deg"], 2), da=round(d["elevon-diff-deg"], 2),
                          alpha=round(d["alpha-deg"], 2), vs=round(d["h-dot-fps"] * 0.3048, 2), phase=int(d["phase"])))
    # end the trace once the aircraft has stopped on the ground (sim contact model is crude after that)
    for i, p in enumerate(trace):
        if p["phase"] == 8 and (p["V"] < 3.0 or abs(p["theta"]) > 5 or abs(p["phi"]) > 15):
            return trace[:i + 1]
    return trace


PHASES = ["", "Hand launch and climb", "Level off", "Turn 1 (180 deg right)", "Downwind",
          "Turn 2 (180 deg right), power off", "Final glide approach", "Flare", "Touchdown and slide-out"]


def summarize(tr):
    first = {}
    for p in tr:
        first.setdefault(p["phase"], p["t"])
    td = next((p for p in tr if p["phase"] == 8), None)
    stop = next((p for p in tr if p["phase"] == 8 and p["V"] < 0.5), tr[-1])
    air = [p for p in tr if p["h"] > 0.05]
    return dict(duration_s=tr[-1]["t"], max_alt_m=max(p["h"] for p in tr), max_bank_deg=max(abs(p["phi"]) for p in tr),
                launch_speed_ms=tr[0]["V"], min_air_speed_ms=min(p["V"] for p in air),
                touchdown_t=td and td["t"], touchdown_speed_ms=td and td["V"], touchdown_sink_ms=td and td["vs"],
                stop_t=stop["t"], phase_start={PHASES[k]: v for k, v in sorted(first.items()) if k},
                landing_from_launch_m=round(math.hypot(stop["n"], stop["e"]), 1))


if __name__ == "__main__":
    tr = run()
    s = summarize(tr)
    json.dump({"summary": s, "phases": PHASES, "trace": tr,
               "basis": "Generated twin (params hash 7be168427b4d) + scripted pitch/bank controller (not ArduPlane); thrust placeholder 1.5 N (R-07, uncalibrated)"},
              open(f"{HERE}/takeoff_landing.json", "w"))
    print(json.dumps(s, indent=1))
