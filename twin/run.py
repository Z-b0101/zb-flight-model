import subprocess, csv, math, sys, os
JSB = "/home/claude/tools/jsbsim/build/src/JSBSim"; ROOT = "/home/claude/twin"
def sim(V, alpha, elev_deg, thr, T=30.0, extra="", name="run", ail=0.0):
    a = math.radians(alpha)
    open(f"{ROOT}/aircraft/zb_wing/{name}_ic.xml","w").write(f'''<?xml version="1.0"?>
<initialize name="{name}_ic"><ubody unit="M/SEC">{V*math.cos(a)}</ubody><wbody unit="M/SEC">{V*math.sin(a)}</wbody>
<altitude unit="M">100</altitude><latitude unit="DEG">37</latitude><longitude unit="DEG">-122</longitude>
<psi unit="DEG">0</psi><theta unit="DEG">{alpha}</theta><phi unit="DEG">0</phi></initialize>''')
    open(f"{ROOT}/scripts/{name}.xml","w").write(f'''<?xml version="1.0"?>
<runscript name="{name}"><use aircraft="zb_wing" initialize="{name}_ic"/>
<run start="0" end="{T}" dt="0.002">
 <property value="{thr}">fcs/throttle-cmd-norm</property>
 <property value="{elev_deg/20.0}">fcs/elevator-cmd-norm</property>
 <property value="{ail}">fcs/aileron-cmd-norm</property>{extra}
</run>
<output name="{name}.csv" type="CSV" rate="20">
 <property>velocities/vt-fps</property><property>position/h-sl-ft</property><property>aero/alpha-deg</property>
 <property>attitude/theta-deg</property><property>attitude/phi-deg</property><property>attitude/psi-deg</property>
 <property>position/lat-gc-deg</property><property>position/long-gc-deg</property><property>velocities/q-rad_sec</property>
 <property>fcs/elevon-sym-deg</property><property>fcs/throttle-pos-norm</property>
</output></runscript>''')
    r = subprocess.run(cwd=ROOT, args=[JSB, f"--root={ROOT}", f"--script=scripts/{name}.xml"], capture_output=True, text=True)
    rows = list(csv.reader(open(f"{ROOT}/{name}.csv")))
    hdr = [h.split("/")[-1] for h in rows[0]]
    return hdr, [list(map(float, r)) for r in rows[1:]]
if __name__ == "__main__":
    sys.path.insert(0, ROOT); from twin.aero import Model
    M = Model(); t = M.trim(7.0); print(t)
    h, d = sim(7.0, t["alpha"], t["elevon"], t["throttle"], T=30)
    for row in d[::100]: print(f"t={row[0]:5.1f} V={row[1]*0.3048:5.2f} h={row[2]*0.3048:6.1f} a={row[3]:5.2f} th={row[4]:5.2f}")
