#!/usr/bin/env python3
"""Z!B PoC airframe CAD generator — parametric, one-command regeneration.

Usage:
  build_cad.py [--params params.json] [--outdir DIR]

Reads the parameter schema (see parametric.py). Writes airframe parts to
<outdir>/parts/wing_structure/ and copies the canonical print files
(rib.stl, spar.stl, skin_*.stl, elevon_*.stl, assembly.stl) to <outdir>/.
"""
import argparse
import math
import shutil
import numpy as np
from stl import mesh as stl_mesh
import cadquery as cq
from parametric import OUT, WingParam, load_params, make_consistent, \
    compute_derived, hole_layout, DESIGN_KEYS

ap = argparse.ArgumentParser()
ap.add_argument("--params", default=None)
ap.add_argument("--outdir", default=OUT)
a = ap.parse_args()
P = load_params(a.params)
W = WingParam(P)
D = a.outdir
SUB = f"{D}/parts/wing_structure"

import os
os.makedirs(SUB, exist_ok=True)

# provenance sanity: MH60 = 10.08% thick @ ~27%, camber ~1.7-1.8%
af = W.af
_us = np.linspace(0.01, 0.99, 400)
_tmax = max(af.thick(u) for u in _us) * 100
print(f"airfoil: {af.name}, tmax={_tmax:.2f}%")
assert abs(_tmax - 10.08) < 0.15

CH = P["chord"]
UH = P["hinge_x_frac"]          # fraction
U_SPAR_MM = W.u_spar * CH       # root-chord mm (canonical rib)
V_SPAR_MM = W.v_spar * CH

# ---------------------------------------------------------------- rib outline (root chord, mm)
def rib_outline_mm(scale=1.0):
    # Closed loop, no duplicate points. 0.5 mm 45-deg chamfers at the
    # hinge-cut corners (printability + avoids a kernel tessellation
    # artifact at the sharp 90 deg corner).
    # cosine spacing: dense at the LE where curvature is highest
    n = 60
    ufs = 0.0025 + (UH - 0.0025) * (1 - np.cos(np.linspace(0, np.pi, n))) / 2
    top_pts = [(uf * CH * scale, af.top(uf) * CH * scale) for uf in ufs]  # LE->hinge
    bot_pts = [(uf * CH * scale, af.bot(uf) * CH * scale) for uf in ufs]  # LE->hinge
    t150, b150 = af.top(UH) * CH * scale, af.bot(UH) * CH * scale
    x150 = UH * CH * scale
    xcut = x150 - 0.5
    top_hi = [p for p in top_pts[-2::-1] if p[0] <= xcut + 1e-9]
    bot_hi = [p for p in bot_pts[1:] if p[0] <= xcut + 1e-9]
    return ([(xcut, t150)]
            + top_hi                       # hinge -> LE along the top
            + bot_hi                       # LE -> hinge along the bottom
            + [(xcut, b150),               # bottom chamfer
               (x150, b150 + 0.5),         # cut face
               (x150, t150 - 0.5)])        # top chamfer; close() returns to start

def lightening_holes():
    holes = []
    for (u, v, d) in hole_layout(P, af):
        fx = u / CH
        assert (af.top(fx) * CH - (v + d / 2)) >= P["hole_min_wall"]
        assert ((v - d / 2) - af.bot(fx) * CH) >= P["hole_min_wall"]
        assert (UH * CH - (u + d / 2)) >= P["hole_min_wall"]
        assert abs(u - U_SPAR_MM) - d / 2 - P["spar_slot_dia"] / 2 >= 5.0
        holes.append((u, v, d))
    return holes

HOLES = lightening_holes()
ST = W.rib_stations()
print(f"stations: {[round(s,2) for s in ST]}")

def build_rib_solid():
    solid = cq.Workplane("XY").polyline(rib_outline_mm()).close().extrude(P["rib_t"])
    tools = [cq.Solid.makeCylinder(P["spar_slot_dia"] / 2, P["rib_t"] + 0.4,
                                   cq.Vector(U_SPAR_MM, V_SPAR_MM, -0.2),
                                   cq.Vector(0, 0, 1))]
    for (u, v, d) in HOLES:
        tools.append(cq.Solid.makeCylinder(d / 2, P["rib_t"] + 0.4,
                                           cq.Vector(u, v, -0.2), cq.Vector(0, 0, 1)))
    for t in tools:
        solid = solid.cut(t)
    return solid

def _tube(p0, p1, r, n_side=16, n_ring=24, phase=0.0):
    """Straight capped tube between two points (numpy; controlled AR)."""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    axis = p1 - p0
    L = float(np.linalg.norm(axis))
    axis /= L
    tmp = np.array([0.0, 0.0, 1.0]) if abs(axis[2]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = np.cross(axis, tmp); e1 /= np.linalg.norm(e1)
    e2 = np.cross(axis, e1)
    th = np.linspace(0, 2 * np.pi, n_side, endpoint=False) + phase
    circ = np.cos(th)[:, None] * e1 + np.sin(th)[:, None] * e2
    rings = [p0 + (L * i / (n_ring - 1)) * axis + r * circ for i in range(n_ring)]
    tris = []
    for i in range(n_ring - 1):
        a, b = rings[i], rings[i + 1]
        for j in range(n_side):
            j2 = (j + 1) % n_side
            tris += [[a[j], b[j], b[j2]], [a[j], b[j2], a[j2]]]
    tris += [[p0, rings[0][(j + 1) % n_side], rings[0][j]] for j in range(n_side)]
    tris += [[p1, rings[-1][j], rings[-1][(j + 1) % n_side]] for j in range(n_side)]
    return np.array(tris)

def build_spar_tris():
    """V-shaped spar: two straight tubes centre->tip following the swept 30%-chord
    line, so every rib's spar slot (at its local 30% chord) sits on the tube."""
    c = W.spar_point(0.0)
    r = P["spar_dia"] / 2
    # phase-shift the second tube: the two centre caps share the apex vertex;
    # without this their z-axis ring vertices (and cap edges) coincide exactly
    t1 = _tube(c, W.spar_point(+P["span"] / 2 + 0.5), r)
    t2 = _tube(c, W.spar_point(-P["span"] / 2 - 0.5), r, phase=math.pi / 16)
    return make_consistent(np.vstack([t1, t2]))

rib_solid = build_rib_solid()
cq.exporters.export(rib_solid, f"{SUB}/rib.stl")
_spar_tris = build_spar_tris()   # exported after to_stl is defined (below)

# ---------------------------------------------------------------- numpy-stl helpers
def grid_mesh(loops):
    tris = []
    M = len(loops[0])
    for i in range(len(loops) - 1):
        a, b = loops[i], loops[i + 1]
        for j in range(M):
            j2 = (j + 1) % M
            tris += [[a[j], b[j], b[j2]], [a[j], b[j2], a[j2]]]
    return np.array(tris)

def cap_fan(loop):
    c = loop.mean(axis=0)
    M = len(loop)
    return np.array([[c, loop[j], loop[(j + 1) % M]] for j in range(M)])

def strip_cap(loop, n_out):
    """Triangulate a thin annular end cap as a quad strip between the outer
    polyline (loop[0:n_out]) and the inner polyline (loop[n_out:] reversed).
    Winding matches the grid_mesh convention so shared edges are traversed
    in opposite directions (consistent outward normals)."""
    tris = []
    N = 2 * n_out
    for i in range(n_out - 1):
        O_i, O_ip1 = loop[i], loop[i + 1]
        I_i, I_ip1 = loop[N - 1 - i], loop[N - 2 - i]
        tris += [[O_i, I_i, I_ip1], [O_i, I_ip1, O_ip1]]
    return np.array(tris)

def to_stl(tris, path):
    m = stl_mesh.Mesh(np.zeros(len(tris), dtype=stl_mesh.Mesh.dtype))
    m.vectors = np.asarray(tris, dtype=np.float64)
    m.save(path)

to_stl(_spar_tris, f"{SUB}/spar.stl")

def offset_normals(pts, dist, upper_side):
    tang = np.gradient(pts, axis=0)
    tang /= np.linalg.norm(tang, axis=1)[:, None]
    nrm = np.column_stack([-tang[:, 1], tang[:, 0]])
    cen = pts.mean(axis=0)
    for i in range(len(nrm)):
        if np.dot(nrm[i], pts[i] - cen) * (1.0 if upper_side else -1.0) < 0:
            nrm[i] *= -1.0
    return pts + nrm * dist

# ---------------------------------------------------------------- skins (u: 0 -> hinge)
# Single full-span loft (no mirrored halves) so the mesh is one closed solid.
def skin_loops(upper_side):
    ys = np.linspace(-P["span"] / 2, P["span"] / 2, 25)
    ufs = np.linspace(0.0025, UH, 28)
    prof = np.array([(uf, af.top(uf) if upper_side else af.bot(uf)) for uf in ufs])
    outer = offset_normals(prof, P["skin_t"] / CH, upper_side)   # fractions
    loops = []
    for y in ys:
        ring = [W.section_to_global(uf, vf, y) for (uf, vf) in outer]
        ring += [W.section_to_global(uf, vf, y) for (uf, vf) in prof[::-1]]
        loops.append(np.array(ring))
    return loops

# ---- bottom skin with the H1 battery-hatch aperture ----
# Single (u,y) grid with the aperture quads skipped, then explicit wall caps
# on the outer boundary and the hole boundary. No patch doubling: every edge
# is used exactly twice (edge-manifold check in build_all.py).
def bottom_skin_with_hole():
    hr = compute_derived(P)["hatch_rect"]
    hu0, hu1, hy0, hy1 = hr["u0"], hr["u1"], hr["y0"], hr["y1"]
    u_all = np.unique(np.round(np.concatenate(
        [np.linspace(0.0025, UH, 28), [hu0, hu1]]), 9))
    y_all = np.unique(np.round(np.concatenate(
        [np.linspace(-P["span"] / 2, P["span"] / 2, 25), [hy0, hy1]]), 9))
    nu, ny = len(u_all), len(y_all)
    prof = np.array([(uf, af.bot(uf)) for uf in u_all])
    outer = offset_normals(prof, P["skin_t"] / CH, False)
    O = np.zeros((ny, nu, 3))
    I = np.zeros((ny, nu, 3))
    for j, y in enumerate(y_all):
        for i, uf in enumerate(u_all):
            O[j, i] = W.section_to_global(uf, outer[i, 1], y)
            I[j, i] = W.section_to_global(uf, prof[i, 1], y)

    def in_hole(i, j):
        return (u_all[i] >= hu0 - 1e-9 and u_all[i + 1] <= hu1 + 1e-9 and
                y_all[j] >= hy0 - 1e-9 and y_all[j + 1] <= hy1 + 1e-9)

    tris = []
    for j in range(ny - 1):
        for i in range(nu - 1):
            if in_hole(i, j):
                continue
            tris += [[O[j, i], O[j, i + 1], O[j + 1, i + 1]],
                     [O[j, i], O[j + 1, i + 1], O[j + 1, i]]]
            tris += [[I[j, i], I[j + 1, i + 1], I[j, i + 1]],
                     [I[j, i], I[j + 1, i], I[j + 1, i + 1]]]

    def wall(i0, j0, i1, j1):
        """Wall quad connecting outer to inner along grid edge (i0,j0)-(i1,j1)."""
        tris.append([O[j0, i0], I[j0, i0], I[j1, i1]])
        tris.append([O[j0, i0], I[j1, i1], O[j1, i1]])

    iu0 = int(np.where(np.abs(u_all - hu0) < 1e-9)[0][0])
    iu1 = int(np.where(np.abs(u_all - hu1) < 1e-9)[0][0])
    jy0 = int(np.where(np.abs(y_all - hy0) < 1e-9)[0][0])
    jy1 = int(np.where(np.abs(y_all - hy1) < 1e-9)[0][0])
    # outer boundary
    for j in range(ny - 1):
        wall(0, j, 0, j + 1)
        wall(nu - 1, j, nu - 1, j + 1)
    for i in range(nu - 1):
        wall(i, 0, i + 1, 0)
        wall(i, ny - 1, i + 1, ny - 1)
    # hole boundary
    for j in range(jy0, jy1):
        wall(iu0, j, iu0, j + 1)
        wall(iu1, j, iu1, j + 1)
    for i in range(iu0, iu1):
        wall(i, jy0, i + 1, jy0)
        wall(i, jy1, i + 1, jy1)
    return make_consistent(np.array(tris))

loops = skin_loops(True)
tris = make_consistent(np.vstack([grid_mesh(loops), strip_cap(loops[0], 28),
                                 strip_cap(loops[-1], 28)]))
to_stl(tris, f"{SUB}/skin_top.stl")
to_stl(bottom_skin_with_hole(), f"{SUB}/skin_bottom.stl")
hr = compute_derived(P)["hatch_rect"]
print(f"bottom skin: with hatch H1 aperture "
      f"u=[{hr['u0']:.4f},{hr['u1']:.4f}] y=[{hr['y0']:.1f},{hr['y1']:.1f}]")

# ---------------------------------------------------------------- elevons (hinge -> TE)
def elevon_mesh(y0, y1, n_st=6):
    uf0 = UH + P["hinge_gap"] / CH
    ufs = np.linspace(uf0, 0.9985, 14)
    loops = []
    for y in np.linspace(y0, y1, n_st):
        ring = [W.section_to_global(uf, af.top(uf), y) for uf in ufs]
        ring += [W.section_to_global(uf, af.bot(uf), y) for uf in ufs[::-1]]
        loops.append(np.array(ring))
    return make_consistent(np.vstack([grid_mesh(loops), strip_cap(loops[0], 14),
                                     strip_cap(loops[-1], 14)]))

for sgn, tag in ((+1, "elevon_right"), (-1, "elevon_left")):
    to_stl(make_consistent(elevon_mesh(sgn * P["elevon_y0"], sgn * P["elevon_y1"])),
           f"{SUB}/{tag}.stl")

# ---------------------------------------------------------------- assembly (ribs placed via parametric transform)
rib_mesh = stl_mesh.Mesh.from_file(f"{SUB}/rib.stl")
rv = rib_mesh.vectors.reshape(-1, 3)
parts = []
for y in ST:
    s = W.chord_at(y) / CH
    th = W.twist_at(y)
    co, si = math.cos(th), math.sin(th)
    X, Y, Z = rv[:, 0], rv[:, 1], rv[:, 2]
    Xs = U_SPAR_MM + (X - U_SPAR_MM) * s
    Ys = V_SPAR_MM + (Y - V_SPAR_MM) * s
    Xr = U_SPAR_MM + (Xs - U_SPAR_MM) * co - (Ys - V_SPAR_MM) * si
    Yr = V_SPAR_MM + (Xs - U_SPAR_MM) * si + (Ys - V_SPAR_MM) * co
    v = np.column_stack([W.xle_at(y) + Xr, np.full_like(X, y) + (Z - P["rib_t"] / 2), Yr])
    parts.append(v.reshape(-1, 3, 3))
for tag in ("spar", "skin_top", "skin_bottom", "elevon_right", "elevon_left"):
    parts.append(stl_mesh.Mesh.from_file(f"{SUB}/{tag}.stl").vectors)
to_stl(np.vstack(parts), f"{SUB}/wing_structure.stl")

# canonical print files at root (backward compat: coupon test feeds on rib.stl)
for f in ("rib", "spar", "skin_top", "skin_bottom", "elevon_right", "elevon_left"):
    shutil.copy(f"{SUB}/{f}.stl", f"{D}/{f}.stl")
shutil.copy(f"{SUB}/wing_structure.stl", f"{D}/assembly.stl")

# params record — MBSE §4.2 split format: "design" (authoritative, hand-edited)
# vs "derived" (recomputed by compute_derived; never hand-edited).
# verify_params.py fails the build on any divergence.
import json
design = {k: (list(v) if isinstance(v, tuple) else v) for k, v in P.items()
          if k in DESIGN_KEYS}
rec = {
    "meta": {
        "format": "design+derived (MBSE_FRAMEWORK.md §4.2)",
        "geometry": "A2 winner: 6deg washout, 25deg sweep, rectangular, MH60, 8 ribs",
        "written_by": "build_cad.py",
        "aero_basis": {
            "x_np_vlm_aft_le_mm": 144.98,
            "source": "aero_opt/cad_loop/cyc4_wash6/sim_SM6.json",
            "sweep_deg": 25.0, "washout_deg": 6.0,
            "note": "wing-alone VLM neutral point for THIS geometry; "
                    "verify_params.py fails if design sweep/washout diverge from it",
        },
    },
    "design": design,
    "derived": compute_derived(P),
}
json.dump(rec, open(f"{D}/params.json", "w"), indent=1)
print(f"wrote parts -> {SUB}; params.json (design+derived) ready")
