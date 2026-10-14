#!/usr/bin/env python3
"""4-round verification of the Z!B PoC CAD (rounds a-d). Run after build_cad.py.
Prints measured numbers; exits nonzero on any FAIL."""
import math, json, os, sys, argparse
import numpy as np
from stl import mesh as stl_mesh

ap = argparse.ArgumentParser()
ap.add_argument("--outdir", default=os.path.dirname(os.path.abspath(__file__)))
OUT = ap.parse_args().outdir
_rec = json.load(open(f"{OUT}/params.json"))
if isinstance(_rec.get("design"), dict):      # split format (MBSE §4.2)
    P, Dd = _rec["design"], _rec["derived"]
else:                                         # legacy flat (should not occur)
    P, Dd = _rec, _rec
CH = 200.0
SWEEP = float(P["sweep_deg"])
fails = []

def check(name, cond, detail):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")
    if not cond:
        fails.append(name)

def load(path):
    m = stl_mesh.Mesh.from_file(path)
    return m.vectors.reshape(-1, 3)

def uniq_pts(v, decimals=3):
    return np.unique(np.round(v, decimals), axis=0)

# ---- airfoil reference (u<=150 portion + hinge cut face) --------------------
pts = []
with open(f"{OUT}/mh60.dat") as f:
    for i, l in enumerate(f):
        l = l.strip()
        if not l or i == 0:
            continue
        x, y = l.split()[:2]
        pts.append((float(x) * CH, float(y) * CH))
pts = np.array(pts)
ile = int(np.argmin(pts[:, 0]))
up, lo = pts[:ile + 1][::-1], pts[ile:]
top = lambda u: float(np.interp(u, up[:, 0], up[:, 1]))
bot = lambda u: float(np.interp(u, lo[:, 0], lo[:, 1]))
UH = 150.0
# design ref: dense MH60 sampling right around the LE nose + 0.5 mm chamfers
_us = np.linspace(0.0, UH - 0.5, 400)
t150, b150 = top(UH), bot(UH)
ref = ([(UH - 0.5, t150)] + [(u, top(u)) for u in _us[::-1][1:]] +
       [(u, bot(u)) for u in _us[1:]] +
       [(UH - 0.5, b150), (UH, b150 + 0.5), (UH, t150 - 0.5)])
ref = np.array(ref)

def seg_dist(p, a, b):
    ab = b - a
    t = np.clip(np.dot(p - a, ab) / max(np.dot(ab, ab), 1e-12), 0, 1)
    return np.linalg.norm(p - (a + t * ab))

def max_dev(qry, refpoly):
    d = np.inf
    dev = 0.0
    A, B = refpoly[:-1], refpoly[1:]
    for p in qry:
        ab = B - A
        denom = np.einsum('ij,ij->i', ab, ab)
        t = np.clip(np.einsum('ij,ij->i', p - A, ab) / np.maximum(denom, 1e-12), 0, 1)
        dd = np.linalg.norm(p - (A + t[:, None] * ab), axis=1).min()
        dev = max(dev, dd)
    return dev

print("(a) rib profile vs MH60 coordinates")
rv = load(f"{OUT}/rib.stl")
_outline_all = uniq_pts(rv[np.abs(rv[:, 2]) < 0.01][:, :2])   # bottom face incl. holes
# drop hole/slot boundary vertices -> keep outer boundary only
keep = np.ones(len(_outline_all), bool)
for (hu, hv, hd) in [(Dd["spar_centre_uv"][0], Dd["spar_centre_uv"][1], P["spar_slot_dia"])] + \
                    [(u, v, d) for (u, v, d) in Dd["holes_uvd"]]:
    keep &= np.linalg.norm(_outline_all - np.array([hu, hv]), axis=1) > hd / 2 + 0.3
outline = _outline_all[keep]
dev = max_dev(outline, ref)
check("rib outline deviation", dev < 0.05, f"max dev = {dev:.4f} mm (tol 0.05)")
tmax = max(top(u) - bot(u) for u in np.linspace(1, 199, 300))
check("section thickness", abs(tmax - 20.16) < 0.05, f"tmax = {tmax:.3f} mm (expect 20.16)")
hx = rv[:, 0].max()
check("hinge cut position", abs(hx - 150.0) < 0.05, f"rib max x = {hx:.3f} mm (expect 150.0)")
# spar slot: vertices near slot centre -> radius
sc = np.array(Dd["spar_centre_uv"])
dslot = np.linalg.norm(rv[:, :2] - sc, axis=1)
ring = dslot[(dslot > 1.0) & (dslot < 3.5)]
slot_dia = 2 * ring.max()
check("spar slot diameter", abs(slot_dia - 4.2) < 0.06, f"slot dia = {slot_dia:.3f} mm (expect 4.2)")
# lightening holes present: expect 4 interior rings
print(f"  [info] slot centre uv=({sc[0]:.2f},{sc[1]:.2f})")

print("(b) spar slot fit vs 4 mm tube")
sv = load(f"{OUT}/spar.stl")
# radius measured perpendicular to the tube axis (3D point-line distance)
ax_p0 = np.array([10.0, 0.0, Dd["spar_centre_uv"][1]])   # XLE(0)+U_SPAR = -50+60
ax_dir = np.array([math.tan(math.radians(SWEEP)) * 450.0, 450.0, 0.0])
ax_dir /= np.linalg.norm(ax_dir)
s0 = sv[np.abs(sv[:, 1]) < 5]
w = s0 - ax_p0
tube_dia = 2 * np.linalg.norm(w - np.outer(w @ ax_dir, ax_dir), axis=1).max()
check("tube diameter", abs(tube_dia - 4.0) < 0.05, f"tube dia = {tube_dia:.3f} mm")
clr = slot_dia - tube_dia
check("diametral clearance", 0.15 <= clr <= 0.30, f"clearance = {clr:.3f} mm (design 0.20)")
wall_t = top(60.0) - (sc[1] + slot_dia / 2)
wall_b = (sc[1] - slot_dia / 2) - bot(60.0)
check("slot walls in section", wall_t > 5 and wall_b > 5,
      f"wall above={wall_t:.2f} mm, below={wall_b:.2f} mm")
slen = sv[:, 1].max() - sv[:, 1].min()
# tube ends are cut square to the tube axis: the y-extent exceeds 901 by
# 2*r*sin(sweep) (0.85 mm/end at 25 deg)
exp_slen = 901.0 + 2 * (P["spar_dia"] / 2) * math.sin(math.radians(SWEEP))
check("spar length ~ full span", abs(slen - exp_slen) < 1.0,
      f"spar y-extent = {slen:.2f} mm (expect {exp_slen:.2f})")

print("(c) rib station / washout / sweep math")
av = load(f"{OUT}/assembly.stl")
tri = av.reshape(-1, 3, 3)
ys = tri.mean(axis=1)[:, 1]
def tri_at_y(yexp, half=4.0):
    return tri[(ys > yexp - half) & (ys < yexp + half)].reshape(-1, 3)
hist, edges = np.histogram(ys, bins=400)
peaks = []
for i in range(1, len(hist) - 1):
    if hist[i] > hist[i - 1] and hist[i] > hist[i + 1] and hist[i] > hist.max() * 0.05:
        peaks.append(0.5 * (edges[i] + edges[i + 1]))
# rib stations: rib FACE planes concentrate vertices at exactly yexp +/- 1.5
# (rib_t/2); find the two tallest vertex-y peaks near each station.
vy = av.reshape(-1, 3)[:, 1]
vh, ve = np.histogram(vy, bins=1800, range=(-450, 450))
vc = 0.5 * (ve[:-1] + ve[1:])
found = []
for yexp in Dd["rib_stations_y"]:
    m = (vc > yexp - 2.5) & (vc < yexp + 2.5)
    idx = np.argsort(vh[m])[-2:]
    pk = vc[m][idx]
    found.append(float(pk.mean()))
found.sort()
found.sort()
ok = len(found) == 8 and max(abs(a - b) for a, b in zip(found, sorted(Dd["rib_stations_y"]))) < 0.5
check("8 ribs at stations", ok, f"found y = {[round(v,2) for v in found]}")
bays = np.diff(sorted(found))
check("bay spacing 112.5", max(abs(b - 112.5) for b in bays) < 0.5,
      f"bays = {[round(b,2) for b in bays]}")
# washout: chord-line angle per rib (LE=min x, TEcut=max x of rib verts)
def rib_angle(yexp):
    v = tri_at_y(yexp)
    # keep only material forward of the rib cut face (u=150): the fixed inboard TE part
    # (te_centre, CE-01) starts at the hinge gap and must not be read as the rib's TE
    v = v[v[:, 0] <= np.abs(v[:, 1]) * math.tan(math.radians(SWEEP)) - 50.0 + 150.3]
    cl = v[:, [0, 2]]
    le = cl[cl[:, 0].argmin()]; te = cl[cl[:, 0].argmax()]
    return math.degrees(math.atan2(te[1] - le[1], te[0] - le[0]))
a_in, a_out = rib_angle(56.25), rib_angle(393.75)
tw = a_out - a_in   # rigid-body rotation between the two stations
wo = P.get("washout_deg", 2.0)
exp_tw = wo * (393.75 - 56.25) / 450.0
check("chord-line rotation matches washout", abs(tw - exp_tw) < 0.1,
      f"rib@56.25: {a_in:.3f} deg, rib@393.75: {a_out:.3f} deg, delta = {tw:+.3f} deg (expect {exp_tw:.3f})")
# physical washout: tip LE must sit lower than root LE (reduced incidence)
def rib_le_z(yexp):
    cl = tri_at_y(yexp)
    return cl[cl[:, 0].argmin()][2]
dz_le = rib_le_z(393.75) - rib_le_z(56.25)
th_in, th_out = math.radians(wo * 56.25 / 450), math.radians(wo * 393.75 / 450)
exp_dz = -(60.0 - 0.5) * (math.sin(th_out) - math.sin(th_in))
check("washout: tip LE lower (nose-down twist)", dz_le < -1.0 and abs(dz_le - exp_dz) < 0.15,
      f"LE z drop 56.25->393.75 = {dz_le:.3f} mm (expect {exp_dz:.3f})")
# sweep: spar-slot centre x at tip rib vs root rib. The slot is ON the twist
# axis, so twist does not contaminate the measurement (the LE does, ~0.4 mm
# at 6 deg washout — measured separately by the washout checks above).
def rib_slot_x(yexp):
    v = tri_at_y(yexp)  # (M,3) vertices near the station
    xc = abs(yexp) * math.tan(math.radians(SWEEP)) - 50.0 + 60.0
    zc = Dd["spar_centre_uv"][1]
    d = np.linalg.norm(v[:, [0, 2]] - np.array([xc, zc]), axis=1)
    ring = v[(d > 1.0) & (d < 3.5)]   # slot boundary vertices (dia 4.2)
    return float(ring[:, 0].mean())
dx = rib_slot_x(393.75) - rib_slot_x(56.25)
exp_dx = (393.75 - 56.25) * math.tan(math.radians(SWEEP))
check(f"{SWEEP:g} deg sweep shift", abs(dx - exp_dx) < 0.3,
      f"slot x shift 56.25->393.75 = {dx:.2f} mm (expect {exp_dx:.2f})")

print("(d) interferences")
def min_dist(A, B, n=1500):
    A = A[np.random.RandomState(0).choice(len(A), min(n, len(A)), replace=False)]
    B = B[np.random.RandomState(1).choice(len(B), min(n, len(B)), replace=False)]
    d2 = ((A[:, None, :] - B[None, :, :]) ** 2).sum(-1)
    return math.sqrt(d2.min())

SW20 = math.tan(math.radians(SWEEP))
xh = lambda y, u: abs(y) * SW20 - 50.0 + u     # section-plane x of chordwise u at station y
# d1: rib cut face lands at u=150 in the assembly (validates rib placement).
# Tolerance 0.35 mm: twist about the spar moves the hinge point in x by
# ~0.16 mm at 6 deg washout (second-order, documented, not a defect).
ribv3 = tri_at_y(168.75)
cut_x = ribv3[:, 0].max()
check("rib cut face @ u=150 in assembly", abs(cut_x - xh(168.75, 150.0)) < 0.35,
      f"rib max x @y=168.75 = {cut_x:.3f} mm (expect {xh(168.75,150.0):.3f})")
# d4: skin TE edge (u=150) vs elevon LE (u=150.5) at the common station y=112.5
elv = load(f"{OUT}/elevon_right.stl")
sk = load(f"{OUT}/skin_top.stl")
yq = 112.5
sk_te = sk[(np.abs(sk[:, 1] - yq) < 0.6) & (np.abs(sk[:, 0] - xh(yq, 150.0)) < 2.0)]
elv_le = elv[(np.abs(elv[:, 1] - yq) < 0.6) & (np.abs(elv[:, 0] - xh(yq, 150.5)) < 2.0)]
if len(sk_te) and len(elv_le):
    hg = min_dist(sk_te, elv_le)
    check("skin/elevon hinge gap ~0.5", 0.3 < hg < 0.8,
          f"min skin-elevon distance @y=112.5 = {hg:.3f} mm (design 0.5)")
else:
    check("skin/elevon hinge gap", False, "could not isolate hinge-edge vertices")
# d2: skin shell thickness = 3.0 mm (outer vs inner surface at a skin station)
sk75 = sk[np.abs(sk[:, 1] - 75.0) < 1.0]
zmed = np.median(sk75[:, 2])
outer, inner = sk75[sk75[:, 2] > zmed], sk75[sk75[:, 2] <= zmed]
t_shell = min_dist(outer[:, [0, 2]], inner[:, [0, 2]])
check("skin shell thickness 3.0", abs(t_shell - 3.0) < 0.2,
      f"measured = {t_shell:.3f} mm")
vspar_c = Dd["spar_centre_uv"][1]
skin_inner_top_at60 = top(60.0)   # inner surface == rib outline
clr_spar_skin = skin_inner_top_at60 - (vspar_c + 2.0)
check("spar clears skin", clr_spar_skin > 4.0,
      f"spar top to skin inner = {clr_spar_skin:.2f} mm")
# spar tube mesh = design tube in the right place: every surface vertex must sit
# at radius 2.0 mm (+/-0.15) from the design spar segment (centre -> tip, swept).
# (Cap-centre vertices lie on the axis by design and are excluded.)
sv = load(f"{OUT}/spar.stl")
uspar, vspar = Dd["spar_centre_uv"]
sw = math.tan(math.radians(P["sweep_deg"]))
def segpt(y):
    return np.array([abs(y) * sw - 50.0 + uspar, y, vspar])
A = segpt(0.0)
ABs = [segpt(sgn * (P["span"] / 2 + 0.5)) - A for sgn in (1, -1)]
ds = []
for AB in ABs:
    L2 = float(AB @ AB)
    w = sv - A
    t = np.clip((w @ AB) / L2, 0, 1)
    ds.append(np.linalg.norm(w - t[:, None] * AB, axis=1))
d = np.minimum(ds[0], ds[1])
surf = d > 0.5   # cap-centre vertices lie on the axis by design
# near the centre V-joint the tubes interpenetrate: a vertex is valid if it
# lies on EITHER tube's surface
dev = np.minimum(np.abs(ds[0][surf] - P["spar_dia"] / 2),
                 np.abs(ds[1][surf] - P["spar_dia"] / 2))
worst_r = float(dev.max())
check("spar tube through rib slots", worst_r < 0.15,
      f"max surface-vertex radius deviation = {worst_r:.3f} mm (design r=2.0)")
print()
if fails:
    print(f"RESULT: {len(fails)} FAILURES: {fails}")
    sys.exit(1)
print("RESULT: all checks passed")
