#!/usr/bin/env python3
"""Z!B PoC CAD — one-command full regeneration + sim/twin exports.

Usage:
  build_all.py [--params params.json] [--outdir DIR]

Runs build_cad.py + build_systems.py, then:
  - mesh quality checks (watertightness, aspect ratio, counts) -> mesh_quality.json
  - twin exports: twin/model.obj (groups, CAD axes, mm),
    twin/model.glb (glTF, mapped axes), twin/manifest.json
"""
import argparse
import glob
import json
import math
import os
import subprocess
import sys

import numpy as np
import trimesh
from stl import mesh as stl_mesh

ap = argparse.ArgumentParser()
ap.add_argument("--params", default=None)
HERE = os.path.dirname(os.path.abspath(__file__))   # cad/ in the repo (was /home/hatch/workspace/uav-sub250g/cad)
ap.add_argument("--outdir", default=HERE)
a = ap.parse_args()
D = a.outdir
PY = os.environ.get("ZIB_CAD_PYTHON", sys.executable)   # interpreter with cadquery (was a hard-coded venv)

for script in ("build_cad.py", "build_systems.py"):
    cmd = [PY, os.path.join(HERE, script), "--outdir", D]
    if a.params:
        cmd += ["--params", a.params]
    print("+", " ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stdout.write(r.stderr)
        sys.exit(f"{script} FAILED")

# ---------------------------------------------------------------- mesh quality
def watertight(tris):
    t = np.asarray(tris, dtype=np.float64).reshape(-1, 3, 3)
    e = np.vstack([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]])
    e = np.sort(e, axis=1)
    key = np.round(e.reshape(-1, 6), 4)
    _, c = np.unique(key, axis=0, return_counts=True)
    return bool((c == 2).all()), int((c != 2).sum())

def aspect_stats(tris):
    t = np.asarray(tris, dtype=np.float64).reshape(-1, 3, 3)
    a = t[:, 1] - t[:, 0]
    b = t[:, 2] - t[:, 1]
    c = t[:, 0] - t[:, 2]
    la, lb, lc = (np.linalg.norm(v, axis=1) for v in (a, b, c))
    s = 0.5 * (la + lb + lc)
    area = np.sqrt(np.maximum(s * (s - la) * (s - lb) * (s - lc), 1e-18))
    inr = area / np.maximum(s, 1e-12)
    ar = np.maximum(np.maximum(la, lb), lc) / np.maximum(2 * inr, 1e-12)
    return {"max": round(float(ar.max()), 2), "mean": round(float(ar.mean()), 2),
            "pct_gt_10": round(float((ar > 10).mean() * 100), 2)}

GROUPS = {  # sim function groups -> part files (under parts/)
    "wing_upper": ["wing_structure/skin_top"],
    "wing_lower": ["wing_structure/skin_bottom"],
    "elevon_R": ["wing_structure/elevon_right"],
    "elevon_L": ["wing_structure/elevon_left"],
    "structure": ["wing_structure/rib", "wing_structure/spar", "wing_structure/te_centre", "wing_structure/te_tip_right", "wing_structure/te_tip_left"],
    "propulsion": ["propulsion/motor", "propulsion/prop", "propulsion/motor_mount",
                   "propulsion/esc"],
    "avionics": ["avionics/fc", "avionics/gps", "avionics/gps_mast",
                 "avionics/servo_L", "avionics/servo_R", "avionics/rx",
                 "avionics/encoder"],
    "power": ["power/battery"],
    "hatch": ["hatch/tray_fwd", "hatch/tray_aft", "hatch/tray_port", "hatch/tray_stbd",
              "hatch/lid", "hatch/latch_1", "hatch/latch_2", "hatch/hinge"],
    "wiring": [],
}
wfiles = [f for f in sorted(glob.glob(f"{D}/parts/wiring/w*.stl"))
         if os.path.basename(f) != "wiring.stl"]
GROUPS["wiring"] = ["wiring/" + os.path.splitext(os.path.basename(f))[0] for f in wfiles]

quality = {}
for g, parts in GROUPS.items():
    tris = []
    for p in parts:
        m = stl_mesh.Mesh.from_file(f"{D}/parts/{p}.stl")
        tris.append(m.vectors)
    tris = np.vstack(tris)
    wt, bad_edges = watertight(tris)
    quality[g] = {"parts": parts, "triangles": int(len(tris)),
                  "vertices": int(np.unique(np.round(tris.reshape(-1, 3), 4), axis=0).shape[0]),
                  "watertight": wt, "bad_edges": bad_edges,
                  **aspect_stats(tris)}
    print(f"quality {g:12s}: tris={quality[g]['triangles']:6d} "
          f"watertight={wt} ar_max={quality[g]['max']}")
json.dump(quality, open(f"{D}/mesh_quality.json", "w"), indent=1)

# ---------------------------------------------------------------- twin exports
os.makedirs(f"{D}/twin", exist_ok=True)

# OBJ with groups (CAD axes, mm)
with open(f"{D}/twin/model.obj", "w") as f:
    f.write("# Z!B PoC — CAD axes: x=aft, y=span(+right), z=up; units mm\n")
    vo = 1
    for g, parts in GROUPS.items():
        f.write(f"\ng {g}\n")
        for p in parts:
            m = stl_mesh.Mesh.from_file(f"{D}/parts/{p}.stl")
            v = m.vectors.reshape(-1, 3)
            for pt in v:
                f.write(f"v {pt[0]:.4f} {pt[1]:.4f} {pt[2]:.4f}\n")
            nv = len(v)
            for i in range(0, nv, 3):
                f.write(f"f {vo+i} {vo+i+1} {vo+i+2}\n")
            vo += nv
print("wrote twin/model.obj")

# glTF: axis map CAD(x=aft,y=span,z=up) -> glTF(x=right,y=up,z=aft)
# glb = (cad_y, cad_z, cad_x), a proper rotation (det +1)
scene = trimesh.Scene()
for g, parts in GROUPS.items():
    for p in parts:
        m = stl_mesh.Mesh.from_file(f"{D}/parts/{p}.stl")
        v = m.vectors.reshape(-1, 3)
        vg = np.column_stack([v[:, 1], v[:, 2], v[:, 0]])
        tm = trimesh.Trimesh(vertices=np.unique(np.round(vg, 4), axis=0),
                             faces=[], process=False)
        # rebuild faces via index map
        key = np.round(vg, 4)
        uniq, inv = np.unique(key, axis=0, return_inverse=True)
        tm = trimesh.Trimesh(vertices=uniq, faces=inv.reshape(-1, 3), process=False)
        scene.add_geometry(tm, geom_name=f"{g}/{p.split('/')[-1]}")
scene.export(f"{D}/twin/model.glb")
# fresh-viewer check: reload the glb independently
chk = trimesh.load(f"{D}/twin/model.glb", force="scene")
ngeom = len(chk.geometry) if hasattr(chk, "geometry") else 1
print(f"wrote twin/model.glb; fresh-load check: {ngeom} geometries present")

manifest = {
    "program": "Z!B PoC sub-250g flying wing",
    "units": "mm",
    "cad_axes": {"x": "aft (+ toward trailing edge)", "y": "spanwise, 0=centre, +right",
                 "z": "up"},
    "root_LE_x": -50.0,
    "x_aft_of_root_LE": "x_cad + 50.0",
    "glb_axis_map": "glb = (cad_y, cad_x->z): glb.x=right span, glb.y=up, glb.z=aft; nose at -z",
    "groups": {g: {"function": f} for g, f in {
        "wing_upper": "upper OML skin (simulation wing surface)",
        "wing_lower": "lower OML skin (simulation wing surface)",
        "elevon_L": "left elevon — deflectable control surface (separate)",
        "elevon_R": "right elevon — deflectable control surface (separate)",
        "structure": "ribs + spar (structural group)",
        "propulsion": "motor/prop/mount/ESC", "avionics": "FC/GPS/servos/RX/encoder",
        "power": "battery", "wiring": "harness tubes + connectors"}.items()},
    "params_schema": "params.json split format: design (authoritative) + derived "
                       "(recomputed; verify_params.py fails on divergence)",
    "regeneration": "build_all.py [--params <flat variant overrides>] [--outdir <dir>]",
}
json.dump(manifest, open(f"{D}/twin/manifest.json", "w"), indent=1)
print("wrote twin/manifest.json")

# ---------------------------------------------------------------- params verify
# MBSE §4.2: the build fails if the file's "derived" section diverges from
# what compute_derived(design) produces, or if the aero basis is stale.
print("verify_params.py:")
r = subprocess.run([PY, os.path.join(HERE, "verify_params.py"),
                    "--params", f"{D}/params.json"],
                   capture_output=True, text=True)
sys.stdout.write(r.stdout)
if r.returncode != 0:
    sys.stdout.write(r.stderr)
    sys.exit("verify_params.py FAILED")
print("BUILD_ALL complete")
