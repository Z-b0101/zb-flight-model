#!/usr/bin/env python3
"""Z!B PoC systems CAD — LRUs, wiring, sub-assemblies.

Usage: build_systems.py [--params params.json] [--outdir DIR]

Every placement is defined RELATIVE to the parametric wing (section
fractions via WingParam.section_to_global / spar_point), never hardcoded
global coordinates, so twist/washout/sweep/taper changes propagate.

Sub-assemblies: propulsion, avionics, power, wiring (+ wing_structure from
build_cad.py). Writes parts/<subasm>/<part>.stl, <subasm>.stl combos,
assembly_full.stl, model_tree.json, cg_report.json, clash_report.json.
"""
import argparse
import math
import numpy as np
from stl import mesh as stl_mesh
import cadquery as cq
from parametric import OUT, WingParam, load_params, make_consistent, compute_derived

ap = argparse.ArgumentParser()
ap.add_argument("--params", default=None)
ap.add_argument("--outdir", default=OUT)
a = ap.parse_args()
P = load_params(a.params)
W = WingParam(P)
Dd = compute_derived(P)          # derived: hatch rect, battery zc, ...
HR = Dd["hatch_rect"]            # aperture rect in section space
ZC = Dd["battery_zc_mm"]          # battery centre z from the top-clearance rule
D = a.outdir
CH = P["chord"]
XLE0 = W.xle_at(0.0)
U_SPAR0 = W.u_spar * CH
V_SPAR0 = W.v_spar * CH

import os
for s in ("propulsion", "avionics", "power", "wiring"):
    os.makedirs(f"{D}/parts/{s}", exist_ok=True)

# ---------------------------------------------------------------- LRU definitions
# dims: [dx, dy, dz] mm box (CAD frame) or ["cyl", r, h, axis] / ["prop3", R, hub];
# pos: section-relative {"sec": [uf, vf, y]} or absolute {"xyz": [x, y, z]}.
# source: dimension provenance. est=True -> flagged ESTIMATED in BOM.
LRU = {
    "motor": dict(sub="propulsion", shape=["cyl", 19.13 / 2, 12.25, "x"],
                  mass=10.0, pos={"sec": [0.96, 0.0, 0.0]},
                  src="hglrc.com Specter 1404 4800KV: dia 19.13 x 12.25 mm, 10 g incl wire",
                  est=False),
    "prop": dict(sub="propulsion", shape=["prop3", 178.43 / 2, 7.5],
                 mass=7.9, pos={"sec": [1.028, 0.0, 0.0]},
                 src="getfpv/phaserfpv Flash 7040-3: dia 178.43 mm, hub 7.5 mm, 7.9 g; blade planform ESTIMATED (max width 18.24 mm known)",
                 est=True),
    "motor_mount": dict(sub="propulsion", shape=["box", [30, 26, 4]],
                        mass=0.0, pos={"sec": [0.94, -0.012, 0.0]},
                        src="custom printed mount (plate + ESC shelf) — ESTIMATED; mass in airframe misc",
                        est=True),
    "esc": dict(sub="propulsion", shape=["box", [20, 12, 6]],
                mass=3.5, pos={"xyz": [XLE0 + 185, 0.0, -12.0]},
                src="EMAX USA FAQ: board 11.9x19.6 mm, 3.5 g w/o wires; 6 mm height incl shrink ESTIMATED; external pod mount",
                est=True),
    "fc": dict(sub="avionics", shape=["box", [37, 26, 14]],
               mass=23.0, pos={"sec": [0.475, 0.0175, 0.0]},
               src="SpeedyBee manual: 37x26x14 mm, 19 g w/ USB extender; 23 g per WEIGHT_BUDGET (oga.global teardown)",
               est=False),
    "gps": dict(sub="avionics", shape=["box", [21, 21, 8.02]],
                mass=7.7, pos={"xyz": [XLE0 + 60, 0.0, 43.0]},
                src="rotorama/n-factory: 21x21x8.02 mm, 7.73 g",
                est=False),
    "gps_mast": dict(sub="avionics", shape=["box", [8, 8, 25]],
                     mass=0.0, pos={"xyz": [XLE0 + 60, 0.0, 26.5]},
                     src="printed mast per WEIGHT_BUDGET S-2 — ESTIMATED; mass in airframe misc",
                     est=True),
    "servo_L": dict(sub="avionics", shape=["box", [19.74, 23.25, 8.34]],
                    mass=4.3, pos={"sec": [0.60, 0.0125, 250.0]},
                    src="buzzardmodels/xyzhobby ES9051: 19.74x8.34x23.25 mm, 4.3 g; mounted flat (8.34 vertical)",
                    est=False),
    "servo_R": dict(sub="avionics", shape=["box", [19.74, 23.25, 8.34]],
                    mass=4.3, pos={"sec": [0.60, 0.0125, -250.0]},
                    src="buzzardmodels/xyzhobby ES9051: 19.74x8.34x23.25 mm, 4.3 g; mounted flat (8.34 vertical)",
                    est=False),
    "rx": dict(sub="avionics", shape=["box", [32, 18, 13]],
               mass=5.0, pos={"sec": [0.475, 0.0125, 24.0]},
               src="HotRC F-04A (manuals.plus/picclick): 32x18x13 mm, 5 g",
               est=False),
    "encoder": dict(sub="avionics", shape=["box", [21, 21, 8]],
                    mass=3.0, pos={"sec": [0.475, 0.0125, -24.0]},
                    src="JHEMCU SPP-S: 21x21 mm (jhemcu.com); height 8 mm ESTIMATED; mass 3 g (budget RX+encoder=8)",
                    est=True),
    "battery": dict(sub="power", shape=["box", P["battery_dims"]],
                    mass=P["battery_mass_g"],
                    pos={"sec": [P["battery_u"], ZC / P["chord"], P["battery_y"]]},
                    src="hobbyrc.co.uk GNB 3S 650mAh 80C: 64x28x20 mm, 62 g; "
                        "SPANWISE (64 along y) at u=0.205 — clears the spar tube "
                        "(fwd surface), sits in hatch H1 tray; zc from 2 mm top-clearance rule",
                    est=False),
}

# ---------------------------------------------------------------- geometry builders
def resolve_pos(pos):
    if "sec" in pos:
        uf, vf, y = pos["sec"]
        return np.array(W.section_to_global(uf, vf, y))
    return np.array(pos["xyz"], float)

def solid_of(name, spec):
    c = resolve_pos(spec["pos"])
    sh = spec["shape"]
    if sh[0] == "box":
        dx, dy, dz = sh[1]
        return cq.Solid.makeBox(dx, dy, dz, cq.Vector(c[0] - dx / 2, c[1] - dy / 2, c[2] - dz / 2))
    if sh[0] == "cyl":
        r, h, ax = sh[1], sh[2], sh[3]
        d = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[ax]
        p0 = c - np.array(d) * h / 2
        return cq.Solid.makeCylinder(r, h, cq.Vector(*p0), cq.Vector(*d))
    if sh[0] == "prop3":
        R, hub_h = sh[1], sh[2]
        hub = cq.Solid.makeCylinder(7.0, hub_h, cq.Vector(c[0] - hub_h / 2, c[1], c[2]),
                                    cq.Vector(1, 0, 0))
        parts = [hub]
        for k in range(3):
            # blade root buried 5 mm into the hub: clean intersection, no tangent faces
            bl = cq.Solid.makeBox(2.0, R - 2.0, 15.0,
                                  cq.Vector(c[0] - 1.0, c[1] + 2.0, c[2] - 7.5))
            bl = bl.rotate(cq.Vector(*c), cq.Vector(1, 0, 0), k * 120.0)
            parts.append(bl)
        return parts[0].fuse(*parts[1:])
    raise ValueError(sh[0])

lru_mesh = {}
for name, spec in LRU.items():
    s = solid_of(name, spec)
    path = f"{D}/parts/{spec['sub']}/{name}.stl"
    cq.exporters.export(s, path)
    lru_mesh[name] = stl_mesh.Mesh.from_file(path).vectors
    print(f"LRU {name}: {spec['shape'][0]} @ {np.round(resolve_pos(spec['pos']),1)}")

# ---------------------------------------------------------------- hatch H1 hardware
# Bottom aperture (derived hatch_rect) + printed tray + Depron lid.
# Retention: fwd tape hinge + 2 aft snap-latches (positive, field-swappable).
_hx0 = XLE0 + HR["u0"] * CH
_hx1 = XLE0 + HR["u1"] * CH
_hy0, _hy1 = HR["y0"], HR["y1"]
_xb = XLE0 + P["battery_u"] * CH
_z_skin = W.section_to_global(P["battery_u"], W.af.bot(P["battery_u"]), 0.0)[2] \
    - P["skin_t"]
_z_lid_top = ZC - P["battery_dims"][2] / 2 - 1.5
_h_tray = _z_skin - _z_lid_top
_z_mid = (_z_skin + _z_lid_top) / 2
_WT = 1.2  # printed wall thickness
# walls overlap volumetrically at corners (no coincident faces -> watertight)
HATCH = {
    "tray_fwd": dict(shape=["box", [_WT, (_hy1 + _WT) - (_hy0 - _WT), _h_tray]], mass=0.0,
                     pos={"xyz": [_hx0 - _WT / 2, 0.0, _z_mid]},
                     src="printed tray fwd wall (vase-mode PETG); mass in hatch_tray",
                     est=True),
    "tray_aft": dict(shape=["box", [_WT, (_hy1 + _WT) - (_hy0 - _WT), _h_tray]], mass=0.0,
                     pos={"xyz": [_hx1 + _WT / 2, 0.0, _z_mid]},
                     src="printed tray aft wall; mass in hatch_tray", est=True),
    "tray_port": dict(shape=["box", [(_hx1 + 0.5) - (_hx0 - 0.5), _WT, _h_tray]], mass=0.0,
                      pos={"xyz": [(_hx0 + _hx1) / 2, _hy0 - _WT / 2, _z_mid]},
                      src="printed tray port wall (0.5 overlap into fwd/aft); mass in hatch_tray",
                      est=True),
    "tray_stbd": dict(shape=["box", [(_hx1 + 0.5) - (_hx0 - 0.5), _WT, _h_tray]], mass=0.0,
                      pos={"xyz": [(_hx0 + _hx1) / 2, _hy1 + _WT / 2, _z_mid]},
                      src="printed tray stbd wall (0.5 overlap into fwd/aft); mass in hatch_tray",
                      est=True),
    "lid": dict(shape=["box", [44.0, 82.0, 3.0]], mass=0.0,
                pos={"xyz": [_xb, 0.0, _z_lid_top - 1.5]},
                src="Depron 3mm lid panel (44x82); mass in hatch_lid", est=True),
    "latch_1": dict(shape=["box", [10.0, 8.0, 5.0]], mass=0.0,
                    pos={"xyz": [_hx1 - 4.0, 20.0, _z_lid_top + 2.3]},
                    src="printed aft snap-latch (embedded 0.2 in lid); mass in hatch_lid",
                    est=True),
    "latch_2": dict(shape=["box", [10.0, 8.0, 5.0]], mass=0.0,
                    pos={"xyz": [_hx1 - 4.0, -20.0, _z_lid_top + 2.3]},
                    src="printed aft snap-latch (embedded 0.2 in lid); mass in hatch_lid",
                    est=True),
    "hinge": dict(shape=["box", [40.0, 8.0, 1.0]], mass=0.0,
                  pos={"xyz": [_hx0 + 2.0, 0.0, _z_lid_top + 0.3]},
                  src="fiber-tape hinge strip, fwd edge (embedded 0.2 in lid); mass in hatch_lid",
                  est=True),
}
os.makedirs(f"{D}/parts/hatch", exist_ok=True)
hatch_mesh = {}
for name, spec in HATCH.items():
    s = solid_of(name, {"shape": spec["shape"], "pos": spec["pos"]})
    path = f"{D}/parts/hatch/{name}.stl"
    cq.exporters.export(s, path)
    hatch_mesh[name] = stl_mesh.Mesh.from_file(path).vectors
    print(f"hatch {name}: box @ {np.round(resolve_pos(spec['pos']),1)}")
print(f"hatch install: aperture x=[{_hx0:.1f},{_hx1:.1f}] y=[{_hy0:.1f},{_hy1:.1f}], "
      f"tray z=[{_z_lid_top:.1f},{_z_skin:.1f}], battery zc={ZC:.2f}")

# ---------------------------------------------------------------- wiring
def rounded_path(pts, radius=6.0, arc_n=5):
    """Fillet polyline corners with quadratic-bezier arcs (bend radius >= `radius`
    unless a segment is too short, in which case the achieved radius shrinks)."""
    pts = [np.array(p, float) for p in pts]
    out = [pts[0]]
    min_r = 1e9
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = pts[i - 1], pts[i], pts[i + 1]
        v1, v2 = p1 - p0, p2 - p1
        l1, l2 = np.linalg.norm(v1), np.linalg.norm(v2)
        if l1 < 1e-9 or l2 < 1e-9:
            continue
        u1, u2 = v1 / l1, v2 / l2
        ang = math.acos(np.clip(np.dot(u1, u2), -1, 1))
        if ang < 1e-3:
            out.append(p1)
            continue
        t = min(radius * math.tan(ang / 2), l1 / 2.01, l2 / 2.01)
        r_eff = t / math.tan(ang / 2)
        min_r = min(min_r, r_eff)
        a, b = p1 - u1 * t, p1 + u2 * t
        for k in range(arc_n + 1):
            f = k / arc_n
            out.append((1 - f) ** 2 * a + 2 * (1 - f) * f * p1 + f ** 2 * b)
    out.append(pts[-1])
    return np.array(out), min_r

def swept_tube(pts, r, n=10):
    pts = np.array(pts, float)
    tang = np.gradient(pts, axis=0)
    tang /= (np.linalg.norm(tang, axis=1)[:, None] + 1e-12)
    ref = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(ref, tang[0])) > 0.9:
        ref = np.array([0.0, 1.0, 0.0])
    nrm = ref - tang[0] * np.dot(ref, tang[0])
    nrm /= np.linalg.norm(nrm)
    rings = []
    for k, t in enumerate(tang):
        nrm = nrm - t * np.dot(nrm, t)
        nrm /= (np.linalg.norm(nrm) + 1e-12)
        binm = np.cross(t, nrm)
        rings.append(np.array([pts[k] + r * (math.cos(a) * nrm + math.sin(a) * binm)
                               for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]))
    tris = []
    for i in range(len(rings) - 1):
        a, b = rings[i], rings[i + 1]
        for j in range(n):
            j2 = (j + 1) % n
            tris += [[a[j], b[j], b[j2]], [a[j], b[j2], a[j2]]]
    c0, c1 = rings[0].mean(axis=0), rings[-1].mean(axis=0)
    for j in range(n):
        j2 = (j + 1) % n
        tris.append([c0, rings[0][j2], rings[0][j]])
        tris.append([c1, rings[-1][j], rings[-1][j2]])
    return np.array(tris)

def to_stl(tris, path):
    t = make_consistent(tris)
    m = stl_mesh.Mesh(np.zeros(len(t), dtype=stl_mesh.Mesh.dtype))
    m.vectors = t
    m.save(path)

def wp_sec(uf, vf, y):
    return np.array(W.section_to_global(uf, vf, y))

midf = lambda uf: W.af.mid(uf)

# documented skin penetration zones (wire pass-throughs needing a physical hole)
PENETRATIONS = [
    {"name": "W3 bottom-skin entry", "center": [XLE0 + 168, 0.0, -4.0], "r": 10.0},
    {"name": "W5/mast top-skin exit", "center": [XLE0 + 64, 0.0, 15.0], "r": 8.0},
]

WIRES = [
    dict(name="w1a", r=1.0, sub="wiring", dy=-3.0,
         route=[["xyz", XLE0 + 186, None, -6], ["xyz", XLE0 + 178, None, -9],
                ["xyz", XLE0 + 175, None, -9.5]],
         desc="motor phase A lead to ESC (external pod run)"),
    dict(name="w1b", r=1.0, sub="wiring", dy=0.0,
         route=[["xyz", XLE0 + 186, None, -6], ["xyz", XLE0 + 178, None, -9],
                ["xyz", XLE0 + 175, None, -9.5]],
         desc="motor phase B lead to ESC (external pod run)"),
    dict(name="w1c", r=1.0, sub="wiring", dy=3.0,
         route=[["xyz", XLE0 + 186, None, -6], ["xyz", XLE0 + 178, None, -9],
                ["xyz", XLE0 + 175, None, -9.5]],
         desc="motor phase C lead to ESC (external pod run)"),
    dict(name="w3a_power", r=1.8, sub="wiring",
         route=[["xyz", XLE0 + 175, 2, -9], ["xyz", XLE0 + 173, 2, -4],
                ["sec", 0.80, -0.01, 2], ["sec", 0.68, 0.01, 4], ["sec", 0.60, 0.02, 6]],
         desc="ESC->FC power (via documented bottom-skin penetration)"),
    dict(name="w3b_signal", r=1.0, sub="wiring",
         route=[["xyz", XLE0 + 175, -2, -9], ["xyz", XLE0 + 173, -2, -4],
                ["sec", 0.80, -0.015, -2], ["sec", 0.68, 0.005, -2], ["sec", 0.60, 0.015, -6]],
         desc="ESC->FC signal+ground"),
    dict(name="w2_batt_fc", r=2.0, sub="wiring",
         route=[["sec", 0.4825, 0.04, -8], ["sec", 0.45, 0.035, 4],
                ["sec", 0.38, 0.03, 16], ["sec", 0.28, 0.02, 28],
                ["sec", P["battery_u"], ZC / P["chord"], 37.0]],
         conn="xt30",
         desc="FC PDB -> battery XT30 pigtail (pack +y end, just outside tray wall; "
              "stays inside wing, no skin breach)"),
    dict(name="w4_servo_L", r=1.2, sub="wiring",
         route=[["sec", 0.5675, 0.03, 10], ["sec", 0.42, midf(0.42), 56.25],
                ["sec", 0.42, midf(0.42), 168.75], ["sec", 0.50, 0.03, 240],
                ["sec", 0.585, 0.02, 250]],
         conn="jr", desc="FC -> left servo lead via 0.42 lightening holes"),
    dict(name="w4_servo_R", r=1.2, sub="wiring",
         route=[["sec", 0.5675, 0.03, -10], ["sec", 0.42, midf(0.42), -56.25],
                ["sec", 0.42, midf(0.42), -168.75], ["sec", 0.50, 0.03, -240],
                ["sec", 0.585, 0.02, -250]],
         conn="jr", desc="FC -> right servo lead via 0.42 lightening holes"),
    dict(name="w5_gps", r=1.0, sub="wiring",
         route=[["sec", 0.50, 0.053, 0], ["sec", 0.30, 0.055, 0],
                ["xyz", XLE0 + 60, 0, 40]],
         conn="sh1_0", desc="FC -> GPS through printed mast wire channel (top-skin penetration at mast base)"),
    dict(name="w6_rx_enc", r=1.0, sub="wiring",
         route=[["sec", 0.45, 0.03, 18], ["sec", 0.45, 0.03, 0], ["sec", 0.45, 0.03, -18]],
         desc="RX -> encoder jumper (corridor fwd of FC, aft of battery)"),
    dict(name="w6_enc_fc", r=1.0, sub="wiring",
         route=[["sec", 0.475, 0.03, -18], ["sec", 0.50, 0.03, -10]],
         desc="encoder -> FC SBUS"),
]

CONN = {  # all ESTIMATED dims
    "xt30":  dict(dims=[16, 8, 7], desc="XT30 male on battery pigtail"),
    "jr":    dict(dims=[10, 6, 5], desc="JR/Futaba servo plug"),
    "sh1_0": dict(dims=[8, 5, 3.5], desc="SH1.0 6-pin GPS plug"),
}

def resolve_route(route, dy=None):
    pts = []
    for wpt in route:
        if wpt[0] == "sec":
            pts.append(wp_sec(wpt[1], wpt[2], wpt[3]))
        else:
            pts.append(np.array([wpt[1], wpt[2] if wpt[2] is not None else dy, wpt[3]], float))
    return pts

wire_mesh, wire_paths, wire_bend = {}, {}, {}
for w in WIRES:
    raw = resolve_route(w["route"], w.get("dy"))
    path, min_r = rounded_path(raw, radius=6.0)
    wire_bend[w["name"]] = min_r
    bend_txt = "straight" if min_r > 1e8 else f"{min_r:.1f}mm"
    tris = [swept_tube(path, w["r"])]
    if w.get("conn"):
        cd = CONN[w["conn"]]["dims"]
        end = path[-1]
        cb = cq.Solid.makeBox(*cd, cq.Vector(end[0] - cd[0] / 2, end[1] - cd[1] / 2,
                                             end[2] - cd[2] / 2))
        cq.exporters.export(cb, "/tmp/_conn.stl")
        tris.append(stl_mesh.Mesh.from_file("/tmp/_conn.stl").vectors)
    tris = np.vstack(tris)
    to_stl(tris, f"{D}/parts/wiring/{w['name']}.stl")
    wire_mesh[w["name"]] = tris
    wire_paths[w["name"]] = path
    print(f"wire {w['name']}: r={w['r']} min_bend={bend_txt} "
          f"{'BEND-OK' if min_r >= 4.0 else 'BEND-TIGHT'}")

# ---------------------------------------------------------------- sub-assembly combos + full assembly
def combine(names_files, out):
    parts = [stl_mesh.Mesh.from_file(f).vectors for f in names_files]
    to_stl(np.vstack(parts), out)

import glob
for sub in ("wing_structure", "propulsion", "avionics", "power", "wiring", "hatch"):
    files = sorted(glob.glob(f"{D}/parts/{sub}/*.stl"))
    files = [f for f in files if not f.endswith(f"{sub}.stl")]
    if files:
        combine(files, f"{D}/parts/{sub}/{sub}.stl")
        print(f"{sub}.stl <- {len(files)} parts")
all_parts = [f for f in sorted(glob.glob(f"{D}/parts/*/*.stl"))
             if not any(f.endswith(f"/{s}/{s}.stl") for s in
                        ("wing_structure", "propulsion", "avionics", "power", "wiring", "hatch"))]
combine(all_parts, f"{D}/assembly_full.stl")
print(f"assembly_full.stl <- {len(all_parts)} parts")

# ---------------------------------------------------------------- CG rollup (masses: WEIGHT_BUDGET.md)
import trimesh
MASSES = {"airframe": 73.6, "battery": 62.0, "motor": 10.0, "esc": 3.5,
          "fc": 23.0, "gps": 7.7, "servo_L": 4.3, "servo_R": 4.3,
          "rx": 5.0, "encoder": 3.0, "prop": 7.9, "wiring": 3.0}
# airframe CG from mesh volumes (ribs x8 placed via parametric transform)
num = np.zeros(3)
den = 0.0
for part, n in (("rib", 8), ("spar", 1), ("skin_top", 1), ("skin_bottom", 1),
                ("elevon_left", 1), ("elevon_right", 1)):
    m = trimesh.load(f"{D}/parts/wing_structure/{part}.stl")
    v = abs(float(m.volume))
    c = np.array(m.centroid, float)
    if part == "rib":
        cs = []
        for y in W.rib_stations():
            s = W.chord_at(y) / CH
            cs.append([W.xle_at(y) + U_SPAR0 + (c[0] - U_SPAR0) * s, y,
                       V_SPAR0 + (c[1] - V_SPAR0) * s])
        c = np.mean(cs, axis=0)
        v *= 8
    num += v * c
    den += v
cg_air = num / den
rows = [{"part": "airframe", "mass_g": 73.6,
         "x_aft_rootLE_mm": round(float(W.x_aft_root_le(cg_air[0])), 1),
         "y_mm": round(float(cg_air[1]), 1), "z_mm": round(float(cg_air[2]), 1),
         "basis": "volume-weighted mesh centroids (mount+mast mass in misc)"}]
for name, spec in LRU.items():
    m = MASSES.get(name, 0.0)
    if m > 0:
        c = resolve_pos(spec["pos"])
        basis = {"battery": "WEIGHT_BUDGET.md", "motor": "WEIGHT_BUDGET.md",
                 "esc": "WEIGHT_BUDGET.md", "fc": "WEIGHT_BUDGET.md (23 g teardown)",
                 "gps": "WEIGHT_BUDGET.md", "prop": "WEIGHT_BUDGET.md",
                 "servo_L": "WEIGHT_BUDGET.md", "servo_R": "WEIGHT_BUDGET.md",
                 "rx": "WEIGHT_BUDGET.md (RX+encoder=8 split 5+3)",
                 "encoder": "WEIGHT_BUDGET.md (RX+encoder=8 split 5+3)"}[name]
        rows.append({"part": name, "mass_g": m,
                     "x_aft_rootLE_mm": round(float(W.x_aft_root_le(c[0])), 1),
                     "y_mm": round(float(c[1]), 1), "z_mm": round(float(c[2]), 1),
                     "basis": basis})
wpts = np.vstack(list(wire_paths.values()))
rows.append({"part": "wiring", "mass_g": 3.0,
             "x_aft_rootLE_mm": round(float(W.x_aft_root_le(wpts[:, 0].mean())), 1),
             "y_mm": round(float(wpts[:, 1].mean()), 1),
             "z_mm": round(float(wpts[:, 2].mean()), 1), "basis": "ESTIMATED"})
# hatch H1 installation (printed tray + Depron lid/latch/hinge) — ESTIMATED
_xb_att = float(W.x_aft_root_le(_xb))
rows.append({"part": "hatch_tray", "mass_g": 1.0,
             "x_aft_rootLE_mm": round(_xb_att, 1), "y_mm": 0.0,
             "z_mm": round(float((_z_skin + _z_lid_top) / 2), 1),
             "basis": "ESTIMATED (printed tray walls)"})
rows.append({"part": "hatch_lid", "mass_g": 0.7,
             "x_aft_rootLE_mm": round(_xb_att, 1), "y_mm": 0.0,
             "z_mm": round(float(_z_lid_top - 1.5), 1),
             "basis": "ESTIMATED (Depron lid + latch + hinge)"})
M = sum(r["mass_g"] for r in rows)
cgx = sum(r["mass_g"] * r["x_aft_rootLE_mm"] for r in rows) / M
cgy = sum(r["mass_g"] * r["y_mm"] for r in rows) / M
cgz = sum(r["mass_g"] * r["z_mm"] for r in rows) / M
cg = {"total_mass_g": round(M, 1), "margin_to_250g": round(250 - M, 1),
      "cg_x_aft_rootLE_mm": round(cgx, 1), "cg_y_mm": round(cgy, 1),
      "cg_z_mm": round(cgz, 1), "target_x_mm": 116.0,
      "delta_to_target_mm": round(cgx - 116.0, 1), "rows": rows}
import json
json.dump(cg, open(f"{D}/cg_report.json", "w"), indent=1)
print(f"CG: x={cgx:.1f} mm aft of root LE (target 116, delta {cgx-116:+.1f}); "
      f"mass {M:.1f} g, margin {250-M:.1f} g")

# ---------------------------------------------------------------- clash check
def min_dist(A, B, n=1200, seed=0):
    A = A[np.random.RandomState(seed).choice(len(A), min(n, len(A)), replace=False)]
    B = B[np.random.RandomState(seed + 1).choice(len(B), min(n, len(B)), replace=False)]
    return float(np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(-1).min()))

def wing_status(p, r):
    """inside / above / below / outside relative to wing interior (offset r)."""
    x, y, z = p
    if abs(y) > P["span"] / 2:
        return "outside"
    uf = (x - W.xle_at(y)) / W.chord_at(y)
    if uf < -0.02 or uf > 1.02:
        return "outside"
    uf = min(max(uf, 0.0), 1.0)
    _, _, zt = W.section_to_global(uf, W.af.top(uf), y)
    _, _, zb = W.section_to_global(uf, W.af.bot(uf), y)
    if z > zt + r:
        return "above"
    if z < zb - r:
        return "below"
    return "inside"

def near_penetration(p):
    for pen in PENETRATIONS:
        if np.linalg.norm(p - np.array(pen["center"])) < pen["r"]:
            return pen["name"]
    return None

clashes = []
struct = {k: stl_mesh.Mesh.from_file(f"{D}/parts/wing_structure/{k}.stl").vectors.reshape(-1, 3)
          for k in ("skin_top", "skin_bottom")}
lru_pts = {n: v.reshape(-1, 3) for n, v in lru_mesh.items()}

# 1) LRU vs LRU
pairs = [(a, b) for a in lru_pts for b in lru_pts if a < b]
skip = {tuple(sorted(p)) for p in [("motor", "motor_mount"), ("motor", "prop"),
                                   ("motor", "esc"), ("esc", "motor_mount"),
                                   ("prop", "motor_mount"), ("gps", "gps_mast")]}
for a, b in pairs:
    if (a, b) in skip:
        continue
    d = min_dist(lru_pts[a], lru_pts[b])
    if d < 1.0:
        clashes.append({"type": "LRU-LRU", "a": a, "b": b,
                        "clearance_mm": round(d, 2),
                        "verdict": "CLASH" if d < 0.2 else "TIGHT"})
# 2) internal LRU vs skins: all corners must be inside (no breach).
#    Battery exception (hatch H1): corners BELOW the skin are allowed inside the
#    documented aperture rect (the pack drops through it into the tray).
#    Hatch install parts (tray/lid/latch/hinge) are bonded structure -> skipped.
def in_hatch_xy(p, grow=1.0):
    x0 = XLE0 + HR["u0"] * CH - grow
    x1 = XLE0 + HR["u1"] * CH + grow
    return (x0 <= p[0] <= x1) and (HR["y0"] - grow <= p[1] <= HR["y1"] + grow)

for name in ("battery", "fc", "rx", "encoder", "servo_L", "servo_R"):
    pts = lru_pts[name]
    d = min(min_dist(pts, struct["skin_top"]), min_dist(pts, struct["skin_bottom"]))
    box = np.array([pts.min(axis=0), pts.max(axis=0)])
    corners = np.array(np.meshgrid(*[[box[0][i], box[1][i]] for i in range(3)])).T.reshape(-1, 3)
    stat = [wing_status(c, 0.0) for c in corners]
    if name == "battery":
        bad = [c for c, s in zip(corners, stat)
               if s == "above" or (s == "below" and not in_hatch_xy(c))]
        verdict = "CLASH" if bad else ("TIGHT" if d < 1.0 else "OK")
    else:
        verdict = "CLASH" if ("above" in stat or "below" in stat) else \
                  ("TIGHT" if d < 1.0 else "OK")
    clashes.append({"type": "LRU-skin", "part": name, "clearance_mm": round(d, 2),
                    "corner_status": {s: stat.count(s) for s in ("inside", "above", "below", "outside")},
                    "verdict": verdict})
# 3) LRU vs spar tube — ANALYTIC segment-vs-box. (The old vertex-sampling
#    check had a false negative: a tube through a box interior has no close
#    VERTICES. This caught the battery-vs-spar interference on 2026-10-13.)
_seg_a = W.spar_point(0.0)
_seg_b = W.spar_point(P["span"] / 2 + 0.5)
_seg_c = W.spar_point(-P["span"] / 2 - 0.5)
_spar_r = P["spar_dia"] / 2
def _seg_box_clearance(p0, p1, bmin, bmax):
    n = max(int(np.linalg.norm(p1 - p0) / 1.0) + 1, 2)
    pts = p0[None, :] + np.linspace(0, 1, n)[:, None] * (p1 - p0)[None, :]
    dd = np.maximum(np.maximum(bmin - pts, pts - bmax), 0.0)
    return float(np.linalg.norm(dd, axis=1).min())
def _box_box_dist(a0, a1, b0, b1):
    dd = np.maximum(np.maximum(a0 - b1, b0 - a1), 0.0)
    return float(np.linalg.norm(dd))
for name in ("battery", "fc", "rx", "encoder", "servo_L", "servo_R",
             "motor_mount", "esc"):
    pts = lru_pts[name]
    bmin, bmax = pts.min(axis=0), pts.max(axis=0)
    dc = min(_seg_box_clearance(_seg_a, _seg_b, bmin, bmax),
             _seg_box_clearance(_seg_a, _seg_c, bmin, bmax)) - _spar_r
    clashes.append({"type": "LRU-spar", "part": name,
                    "clearance_mm": round(dc, 2),
                    "verdict": "CLASH" if dc < 0.5 else ("TIGHT" if dc < 2.0 else "OK")})
# 3b) hatch installation fit: battery vs tray walls / lid; w2 vs tray walls
_batt = lru_mesh["battery"].reshape(-1, 3)
_bbmin, _bbmax = _batt.min(axis=0), _batt.max(axis=0)
for hn in ("tray_fwd", "tray_aft", "tray_port", "tray_stbd"):
    hp = hatch_mesh[hn].reshape(-1, 3)
    dbb = _box_box_dist(_bbmin, _bbmax, hp.min(axis=0), hp.max(axis=0))
    clashes.append({"type": "hatch-fit", "part": hn,
                    "clearance_mm": round(dbb, 2),
                    "verdict": "CLASH" if dbb < 0.5 else ("TIGHT" if dbb < 1.0 else "OK")})
_lid = hatch_mesh["lid"].reshape(-1, 3)
_dlb = float(_lid[:, 2].max() - _bbmin[2])   # lid top vs battery bottom (want <= -1.0)
clashes.append({"type": "hatch-fit", "part": "lid-vs-battery",
                "clearance_mm": round(-_dlb, 2),
                "verdict": "CLASH" if _dlb > -1.0 else "OK"})
_w2m = wire_mesh["w2_batt_fc"].reshape(-1, 3)
for hn in ("tray_fwd", "tray_aft", "tray_port", "tray_stbd", "lid"):
    hp = hatch_mesh[hn].reshape(-1, 3)
    dw = _box_box_dist(_w2m.min(axis=0), _w2m.max(axis=0),
                       hp.min(axis=0), hp.max(axis=0))
    clashes.append({"type": "wire-hatch", "wire": "w2_batt_fc", "part": hn,
                    "clearance_mm": round(dw, 2),
                    "verdict": "CLASH" if dw < 0.5 else ("TIGHT" if dw < 1.5 else "OK")})
# 4) wires: flag inside<->above/below transitions (skin crossings) outside
#    documented penetration zones. The crossing point is interpolated between
#    samples so the zone test hits the true penetration location.
WR = {w["name"]: w["r"] for w in WIRES}
def skin_z(p, r, side):
    x, y, z = p
    uf = min(max((x - W.xle_at(y)) / W.chord_at(y), 0.0), 1.0)
    _, _, zt = W.section_to_global(uf, W.af.top(uf), y)
    _, _, zb = W.section_to_global(uf, W.af.bot(uf), y)
    return (zt + r) if side == "above" else (zb - r)
for wname, path in wire_paths.items():
    r = WR[wname]
    prev = None
    for i, p in enumerate(path[::3]):
        st = wing_status(p, r)
        pair = (prev, st)
        if pair in (("inside", "above"), ("above", "inside"),
                    ("inside", "below"), ("below", "inside")):
            q = path[max(0, 3 * i - 3)]
            side = "above" if "above" in pair else "below"
            # bisect the crossing between q and p
            a, b = q, p
            for _ in range(24):
                m_ = 0.5 * (a + b)
                sa = wing_status(a, r)
                sm = wing_status(m_, r)
                if (sa == "inside") == (sm == "inside"):
                    a = m_
                else:
                    b = m_
            cross = 0.5 * (a + b)
            if not near_penetration(cross):
                clashes.append({"type": "wire-breach", "wire": wname,
                                "at_mm": [round(float(v), 1) for v in cross],
                                "transition": f"{prev}->{st}", "verdict": "CLASH"})
                break
        prev = st
# 5) servo leads vs rib material (must thread the 0.42 lightening holes)
ribs = stl_mesh.Mesh.from_file(f"{D}/parts/wing_structure/rib.stl").vectors.reshape(-1, 3)[:, :2]
for wname in ("w4_servo_L", "w4_servo_R"):
    dmin = 1e9
    for p in wire_paths[wname]:
        ay = abs(p[1])
        if min(abs(ay - s) for s in (56.25, 168.75, 281.25)) < 6:
            y = p[1]
            s = W.chord_at(y) / CH
            us_l, vs_l = U_SPAR0 * s, V_SPAR0 * s
            th = W.twist_at(y)
            co, si = math.cos(th), math.sin(th)
            dx, dz = (p[0] - W.xle_at(y)) - us_l, p[2] - vs_l
            u0 = U_SPAR0 + (dx * co + dz * si) / s
            v0 = V_SPAR0 + (-dx * si + dz * co) / s
            dmin = min(dmin, float(np.linalg.norm(ribs - np.array([u0, v0]), axis=1).min()))
    clashes.append({"type": "wire-rib", "wire": wname,
                    "min_dist_to_rib_material_mm": round(dmin, 2),
                    "verdict": "OK" if dmin > 1.5 else "CLASH"})

n_clash = sum(1 for c in clashes if c["verdict"] == "CLASH")
n_tight = sum(1 for c in clashes if c["verdict"] == "TIGHT")
json.dump({"penetration_zones": PENETRATIONS, "clashes": clashes,
           "n_clash": n_clash, "n_tight": n_tight},
          open(f"{D}/clash_report.json", "w"), indent=1)
print(f"clash check: {n_clash} CLASH, {n_tight} TIGHT")
for c in clashes:
    if c["verdict"] != "OK":
        print("  ", c["verdict"], {k: v for k, v in c.items() if k != "verdict"})

# ---------------------------------------------------------------- model tree
tree = {}
for name, spec in LRU.items():
    tree[name] = {"sub_assembly": spec["sub"],
                  "file": f"parts/{spec['sub']}/{name}.stl",
                  "shape": spec["shape"], "mass_g": spec["mass"],
                  "source": spec["src"], "ESTIMATED": spec["est"],
                  "pos_cad_xyz_mm": [round(float(v), 1) for v in resolve_pos(spec["pos"])]}
for w in WIRES:
    e = {"sub_assembly": "wiring", "file": f"parts/wiring/{w['name']}.stl",
         "wire_r_mm": w["r"], "min_bend_radius_mm": round(wire_bend[w["name"]], 1),
         "desc": w["desc"], "ESTIMATED": False}
    if w.get("conn"):
        e["connector"] = {w["conn"]: CONN[w["conn"]], "ESTIMATED_dims": True}
    tree[w["name"]] = e
for name, spec in HATCH.items():
    tree[name] = {"sub_assembly": "hatch",
                  "file": f"parts/hatch/{name}.stl",
                  "shape": spec["shape"], "mass_g": spec["mass"],
                  "source": spec["src"], "ESTIMATED": spec["est"],
                  "pos_cad_xyz_mm": [round(float(v), 1) for v in resolve_pos(spec["pos"])]}
tree["_wire_penetrations"] = PENETRATIONS
tree["_hatch_H1"] = {"aperture_rect_section": HR,
                     "battery_zc_mm": ZC,
                     "retention": "fwd tape hinge + 2 aft snap-latches (positive)",
                     "desc": "battery hatch: bottom-skin aperture + printed tray + Depron lid"}
json.dump(tree, open(f"{D}/model_tree.json", "w"), indent=1)
print("wrote model_tree.json")
