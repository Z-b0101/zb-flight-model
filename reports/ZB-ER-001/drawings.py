"""Appendix A engineering drawings + Appendix B engineering plots for ZB-ER-001."""
import math, os, sys, json
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle, FancyBboxPatch
sys.path.insert(0, REPO); sys.path.insert(0, REPO + "/twin")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures"); os.makedirs(OUT, exist_ok=True)
INK, GREY, LIGHT, ACC = "#1a1a1a", "#7a7a7a", "#eeeeee", "#1f6fc5"
P = json.load(open(REPO + "/cad/params.json"))
D = P["design"]; DER = P["derived"]
C, B, SW = D["chord"], D["span"], math.radians(D["sweep_deg"])
af = np.loadtxt(REPO + "/cad/mh60.dat", skiprows=1)
up = af[:np.argmin(af[:, 0]) + 1][::-1]; lo = af[np.argmin(af[:, 0]):]
def top(u): return np.interp(u, up[:, 0], up[:, 1]) * C
def bot(u): return np.interp(u, lo[:, 0], lo[:, 1]) * C
def xle(y): return abs(y) * math.tan(SW)

def frame(fig, title, num, scale="1:5 (not to scale on screen; dimensions in mm)"):
    fig.text(0.015, 0.975, title, fontsize=12, fontweight="bold", va="top")
    # title block
    fig.patches.append(Rectangle((0.66, 0.012), 0.33, 0.085, transform=fig.transFigure, fill=False, ec=INK, lw=1))
    fig.text(0.67, 0.08, f"Z!B · ZB-ER-001 · Drawing {num}", fontsize=8, fontweight="bold")
    fig.text(0.67, 0.055, f"params.json hash 7be168427b4d · rev A · {scale}", fontsize=6.8)
    fig.text(0.67, 0.03, "x aft of root LE, y right, z up · drawn by Claude 2026-10-14", fontsize=6.8)

def dim(ax, a, b, txt, off=(0, 0), fs=8, col=INK):
    ax.annotate("", a, b, arrowprops=dict(arrowstyle="<->", color=col, lw=0.8))
    ax.text((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1], txt, fontsize=fs, ha="center", va="center", color=col,
            bbox=dict(fc="white", ec="none", pad=0.6))

def save(fig, n): fig.savefig(os.path.join(OUT, n), facecolor="white"); plt.close(fig)

# ======================================================== A-1 planform (top view)
fig, ax = plt.subplots(figsize=(10, 6.4), dpi=150); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(0.02, 0.12, 0.98, 0.93)
yy = np.array([-450, 0, 450])
le = [(-450, xle(450)), (0, 0), (450, xle(450))]; te = [(450, xle(450) + C), (0, C), (-450, xle(450) + C)]
ax.add_patch(Polygon([(y, -x) for y, x in le + te], fc=LIGHT, ec=INK, lw=1.4))
# elevons
for s in (-1, 1):
    y0, y1 = D["elevon_y0"], D["elevon_y1"]
    pts = [(s * y0, -(xle(y0) + 0.75 * C)), (s * y1, -(xle(y1) + 0.75 * C)), (s * y1, -(xle(y1) + C)), (s * y0, -(xle(y0) + C))]
    ax.add_patch(Polygon(pts, fc=ACC, alpha=0.25, ec=ACC, lw=1))
# hinge line, spar, webs
for u, ls, col, lab in ((0.30, "-", INK, "spar 4 mm @30%"), (0.525, "--", ACC, "mid-chord web @52.5% (R3)"), (0.75, "--", ACC, "hinge-line web @75% (R2)")):
    ax.plot([-450, 0, 450], [-(xle(450) + u * C), -(u * C), -(xle(450) + u * C)], ls=ls, color=col, lw=1.6 if u == 0.3 else 1)
    ax.text(460, -(xle(450) + u * C), lab, fontsize=7.5, va="center", color=col)
# ribs
for y in DER["rib_stations_y"]:
    ax.plot([y, y], [-xle(y), -(xle(y) + C)], color=GREY, lw=0.8)
# hatch
h = DER["hatch_rect"]
ax.add_patch(Rectangle((h["y0"], -h["u1"] * C), h["y1"] - h["y0"], (h["u1"] - h["u0"]) * C, fc="none", ec=INK, lw=1, ls=":"))
ax.text(-40, -h["u0"] * C + 4, "hatch H1 (underside)", fontsize=6.5, ha="right")
# battery
ax.add_patch(Rectangle((-32, -(0.205 * C + 14)), 64, 28, fc="none", ec=GREY, lw=0.8))
# CG / NP
for xv, lab, col in ((128.5, "CG 128.5", INK), (142.6, "NP 142.6", ACC)):
    ax.plot([-12, 12], [-xv, -xv], color=col, lw=1.4); ax.plot([-120, -14], [-xv, -xv], color=col, lw=0.5, ls=":"); ax.text(-124, -xv, lab, fontsize=7.5, ha="right", va="center", color=col)
# fins (proposed)
for s in (-1, 1):
    ax.plot([s * 450, s * 450], [-(xle(450) + 80), -(xle(450) + 200)], color=ACC, lw=3, alpha=0.6)
ax.text(450, -(xle(450) + 215), "tip fin (proposed, DR-01)", fontsize=7, ha="center", color=ACC)
# servos
for s in (-1, 1):
    ax.add_patch(Rectangle((s * 250 - 12, -(xle(250) + 0.6 * C + 10)), 24, 20, fc="white", ec=INK, lw=0.8))
# motor + prop
ax.add_patch(Rectangle((-10, -(0.96 * C + 6)), 20, 12, fc="white", ec=INK, lw=0.8))
ax.plot([-89, 89], [-(1.03 * C)] * 2, color=INK, lw=2)
ax.text(95, -(1.03 * C), "Ø178 prop", fontsize=7, va="center")
# dims
dim(ax, (-450, 40), (450, 40), "span 900")
dim(ax, (-480, 0), (-480, -C), "c 200", off=(-14, 0))
dim(ax, (450, -xle(450)), (450, 0), f"{xle(450):.0f}", off=(18, 0))
ax.text(330, -50, "Λ LE = 25°", fontsize=8)
dim(ax, (D["elevon_y0"], -(xle(450) + C) - 30), (D["elevon_y1"], -(xle(450) + C) - 30), "elevon 112.5 → 405")
for y in DER["rib_stations_y"]:
    ax.text(y, -(xle(y) + C) - 8, f"{abs(y):.0f}", fontsize=6.5, ha="center", color=GREY)
ax.set_xlim(-560, 620); ax.set_ylim(-470, 70)
frame(fig, "A-1  Planform, top view, with structure and equipment", "A-1")
save(fig, "A-1.png")

# ======================================================== A-2 root section
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(0.02, 0.16, 0.98, 0.9)
ax.add_patch(Polygon(np.c_[af[:, 0] * C, af[:, 1] * C], fc=LIGHT, ec=INK, lw=1.4))
# skins thickness indicator (inner offset)
ax.add_patch(Circle((0.3 * C, (top(0.3) + bot(0.3)) / 2), 2.0, fc=INK))
for u in (0.525, 0.75):
    ax.add_patch(Rectangle((u * C - 1.5, bot(u)), 3, top(u) - bot(u), fc=ACC, ec=ACC))
# battery + hatch
bz = DER["battery_zc_mm"]
ax.add_patch(Rectangle((0.205 * C - 14, bz - 10), 28, 20, fc="white", ec=INK, lw=1))
ax.text(0.205 * C, bz, "3S 650\n28×20", fontsize=6, ha="center", va="center")
ax.plot([0.12 * C, 0.29 * C], [bot(0.2) - 3, bot(0.2) - 3], color=ACC, lw=2.2); ax.text(0.205 * C, bot(0.2) - 9, "hatch lid 24–58", fontsize=7, ha="center", color=ACC)
# elevon
ax.plot([0.75 * C, 0.75 * C], [bot(0.75), top(0.75)], color=INK, lw=0.8, ls=":")
# dims
dim(ax, (0, -26), (C, -26), "chord 200")
dim(ax, (0, -18), (0.3 * C, -18), "60")
dim(ax, (0, 22), (0.525 * C, 22), "105")
dim(ax, (0, 30), (0.75 * C, 30), "150 (hinge)")
dim(ax, (0.3 * C + 10, bot(0.3)), (0.3 * C + 10, top(0.3)), "20.1", off=(8, 0))
dim(ax, (0.525 * C + 8, bot(0.525)), (0.525 * C + 8, top(0.525)), "15.9", off=(8, 0))
dim(ax, (0.75 * C + 8, bot(0.75)), (0.75 * C + 8, top(0.75)), "7.7", off=(7, 0))
ax.text(0.3 * C, -10, "spar Ø4.0 (slot 4.2)", fontsize=7, ha="center")
ax.text(176, 6, "elevon 25% c", fontsize=7, ha="center")
ax.text(4, -38, "MH60, t/c 10.1% · skins 3 mm Depron LE→hinge · webs 3 mm Depron (blue, proposed R2/R3)", fontsize=7.5)
ax.set_xlim(-10, 215); ax.set_ylim(-45, 38)
frame(fig, "A-2  Root section: MH60 with spar, webs, battery and hatch", "A-2", "1:1 geometry")
save(fig, "A-2.png")

# ======================================================== A-3 rib drawing
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=150); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(0.02, 0.17, 0.98, 0.9)
ax.add_patch(Polygon(np.c_[af[:, 0] * C, af[:, 1] * C], fc=LIGHT, ec=INK, lw=1.4))
ax.add_patch(Circle((0.3 * C, (top(0.3) + bot(0.3)) / 2), 2.1, fc="white", ec=INK, lw=1))
for u in D["hole_x_fracs"]:
    d = max((top(u) - bot(u)) * D["hole_dia_frac"], D["hole_min_dia"]) / 2
    if (top(u) - bot(u)) - 2 * d < 2 * D["hole_min_wall"]: d = (top(u) - bot(u)) / 2 - D["hole_min_wall"]
    ax.add_patch(Circle((u * C, (top(u) + bot(u)) / 2), d, fc="white", ec=INK, lw=0.9))
    ax.text(u * C, bot(u) - 6, f"Ø{2*d:.1f} @{u*100:.0f}%", fontsize=6.5, ha="center")
ax.text(0.3 * C, top(0.3) + 5, "slot Ø4.2 @30%", fontsize=7, ha="center")
dim(ax, (0, -22), (C, -22), "200 (root); ribs identical, set at washout in jig")
ax.text(2, -32, "ZB-101 rib · PLA 3 mm, printed flat · qty 8 · stations y = ±56.25, ±168.75, ±281.25, ±393.75 · 1.5 g target", fontsize=7.5)
ax.set_xlim(-8, 210); ax.set_ylim(-38, 26)
frame(fig, "A-3  Rib ZB-101", "A-3", "1:1 geometry")
save(fig, "A-3.png")

# ======================================================== A-4 hatch + centre section
fig, ax = plt.subplots(figsize=(10, 5.4), dpi=150); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(0.02, 0.14, 0.98, 0.9)
# bottom view of root bay (x down)
ax.add_patch(Rectangle((-56.25, -C), 112.5, C, fc=LIGHT, ec=INK, lw=1.2))
x0, x1 = DER["hatch_rect"]["u0"] * C, DER["hatch_rect"]["u1"] * C
ax.add_patch(FancyBboxPatch((-36, -x1), 72, x1 - x0, boxstyle="round,pad=0,rounding_size=8", fc="white", ec=INK, lw=1.2))
ax.add_patch(FancyBboxPatch((-42, -x1 - 6), 84, x1 - x0 + 12, boxstyle="round,pad=0,rounding_size=12", fc="none", ec=ACC, lw=1.4, ls="--"))
ax.text(48, -x0 + 4, "PLA frame 6 × 1.2 (R4)", fontsize=7, color=ACC)
dim(ax, (-36, -x0 + 8), (36, -x0 + 8), "72")
dim(ax, (-44, -x0), (-44, -x1), "34", off=(-6, 0))
ax.text(0, -(x0 + x1) / 2, "battery bay\nr = 8 corners", fontsize=7, ha="center", va="center")
# V joiner
for s in (-1, 1):
    ax.plot([0, s * 56], [-0.3 * C, -(0.3 * C + 56 * math.tan(SW))], color=INK, lw=3)
ax.add_patch(Rectangle((-14, -0.3 * C - 6), 28, 12, fc=ACC, alpha=0.25, ec=ACC))
ax.text(0, -0.3 * C - 14, "V-joiner block 12×12, sockets 40 mm, 130°", fontsize=7, ha="center", color=ACC)
ax.add_patch(Rectangle((-18, -0.55 * C), 36, 26, fc="white", ec=INK, lw=0.8)); ax.text(0, -0.55 * C + 13, "FC", fontsize=7, ha="center")
ax.add_patch(Rectangle((-15, -0.98 * C), 30, 26, fc="white", ec=INK, lw=0.8)); ax.text(0, -0.98 * C + 13, "motor mount", fontsize=7, ha="center")
ax.add_patch(Rectangle((-56.25, -0.62 * C), 6, 30, fc="none", ec=GREY, ls=":")); ax.text(-70, -0.55 * C, "grip zone", fontsize=7, ha="right", color=GREY)
ax.set_xlim(-110, 140); ax.set_ylim(-C - 12, 18)
fig.text(0.02, 0.07, "Bottom view of the root bay (between ribs y = ±56.25). ZB-110 integrated centre section (R5) carries joiner, tray, frame, FC and motor mount.\n[DATA PENDING] detailed CAD of ZB-110 · ECD Oct 16", fontsize=7.5)
frame(fig, "A-4  Root bay: hatch H1, frame and integrated centre section (concept)", "A-4", "concept, 1:1 positions")
save(fig, "A-4.png")

# ======================================================== B plots
import perf
from structures import model as SM
T = perf.Twin()
V = np.arange(5.4, 16.01, 0.1); tr = [T.trim(v) for v in V]
# B-1 power / range
fig, ax = plt.subplots(figsize=(8, 4), dpi=150); fig.subplots_adjust(0.09, 0.14, 0.9, 0.86)
Pb = [t["P_batt"] for t in tr]; E = 7.215 * 0.8 * 3600
rng = [E / p * v / 1000 for p, v in zip(Pb, V)]; end = [E / p / 60 for p in Pb]
ax.plot(V, Pb, color=INK, lw=1.8); ax.set_xlabel("airspeed (m/s)"); ax.set_ylabel("battery power (W)")
ax2 = ax.twinx(); ax2.plot(V, rng, color=ACC, lw=1.8); ax2.set_ylabel("range (km)", color=ACC)
iv = int(np.argmax(rng)); ax2.plot(V[iv], rng[iv], "o", color=ACC); ax2.annotate(f"best range {rng[iv]:.1f} km @ {V[iv]:.1f} m/s", (V[iv], rng[iv]), (V[iv] + 0.6, rng[iv] - 1.6), fontsize=8, color=ACC)
ok = V >= 7.0 - 1e-9; ie = int(np.where(ok)[0][np.argmin(np.array(Pb)[ok])]); ax.plot(V[ie], Pb[ie], "o", color=INK); ax.annotate(f"best endurance {end[ie]:.0f} min @ {V[ie]:.1f} m/s", (V[ie], Pb[ie]), (V[ie] + 0.6, Pb[ie] + 4), fontsize=8)
ax.axvspan(V[0], 7.0, color=LIGHT, zorder=0); ax.text(5.6, 20, "below the\n7.0 m/s\noperating floor", fontsize=7, color=GREY)
ax.axvline(16, color=GREY, ls="--", lw=1); ax.text(15.9, max(Pb) * 0.9, "16 m/s ceiling", fontsize=7.5, ha="right", color=GREY)
ax.axvline(T.vstall(), color=GREY, ls=":", lw=1); ax.text(T.vstall() + 0.1, max(Pb) * 0.9, "Vs 4.22", fontsize=7.5, color=GREY)
fig.text(0.01, 0.95, "B-1  Power and range vs airspeed: the range peak sits on the efficiency-fit kink (DR-12)", fontsize=10, fontweight="bold")
save(fig, "B-1.png")
# B-2 trim elevon
fig, ax = plt.subplots(figsize=(8, 3.6), dpi=150); fig.subplots_adjust(0.09, 0.16, 0.97, 0.84)
de = [t["elevon"] for t in tr]
ax.plot(V, de, color=ACC, lw=2); ax.axhline(-8, color="#b3261e", ls="--", lw=1.2); ax.text(15.8, -7.6, "assumed −8° up-elevon limit", fontsize=8, ha="right", color="#b3261e")
ax.axvline(1.3 * T.vstall(), color=GREY, ls=":", lw=1); ax.text(1.3 * T.vstall() + 0.1, -1.2, "1.3 Vs", fontsize=8, color=GREY)
ax.annotate(f"{T.trim(5.5)['elevon']:.1f}° at 5.5 m/s", (5.5, T.trim(5.5)["elevon"]), (7.0, -7.2), fontsize=8, arrowprops=dict(arrowstyle="-", color=INK, lw=0.6))
ax.set_xlabel("airspeed (m/s)"); ax.set_ylabel("trim elevon (deg, + TE down)"); ax.set_ylim(-9, 0)
fig.text(0.01, 0.95, "B-2  Trim elevon vs airspeed: only 0.8° of up-elevon left at 1.3 Vs (DR-02)", fontsize=10, fontweight="bold")
save(fig, "B-2.png")
# B-3 V-n diagram
fig, ax = plt.subplots(figsize=(8, 4), dpi=150); fig.subplots_adjust(0.09, 0.14, 0.97, 0.86)
W = 0.2119 * 9.80665; S = 0.18; rho = 1.225; clmax = 0.9 * 1.16
vv = np.linspace(0, 25, 300); nst = 0.5 * rho * vv**2 * S * clmax / W
ax.plot(vv, np.minimum(nst, 4), color=INK, lw=1.6); ax.plot(vv, -np.minimum(0.5 * rho * vv**2 * S * 0.4 / W, 1.5), color=INK, lw=1.2)
mu = 2 * (W / S) / (rho * 0.2 * 3.64 * 9.80665); Kg = 0.88 * mu / (5.3 + mu)
ng = 1 + rho * vv * 3.64 * Kg * 7.6 / (2 * W / S)
ax.plot(vv, ng, color=ACC, lw=1, ls="--"); ax.plot(vv, 2 - ng, color=ACC, lw=1, ls="--")
ax.axhline(4, color=GREY, lw=0.8, ls=":"); ax.axvline(16, color=GREY, lw=1, ls="--"); ax.axvline(25, color=GREY, lw=0.8, ls=":")
for (v, n, lab) in ((10.5, 1, "C1"), (12, 2.5, "C2"), (15, 4, "C3"), (12, 6.15, "C4"), (25, 1, "C5")):
    ax.plot(v, n, "o", color=ACC if lab == "C4" else INK); ax.text(v + 0.3, n + 0.15, lab, fontsize=8)
ax.text(16.2, -1.3, "16 m/s ceiling", fontsize=7.5, color=GREY); ax.text(24.8, 3.2, "25 m/s (out of envelope)", fontsize=7, ha="right", color=GREY)
ax.text(5.2, 5.5, "gust lines 7.6 m/s\n(FAR 23.341 method)", fontsize=7.5, color=ACC)
ax.set_xlim(0, 26); ax.set_ylim(-2, 7.5); ax.set_xlabel("equivalent airspeed (m/s)"); ax.set_ylabel("load factor n")
fig.text(0.01, 0.95, "B-3  Flight envelope (V-n) and load cases C1–C5 at 211.9 g", fontsize=10, fontweight="bold")
save(fig, "B-3.png")
# B-4 spanload at C4 + bending moment
geo = SM.Geometry(); fe, ys, sec = SM.build(geo, spar="nominal", web=True)
de4 = T.trim(12)["elevon"]; F, info = SM.nodal_loads(geo, fe, ys, 12.0, 6.146, elevon_deg=de4)
u = fe.solve(F); ef = fe.element_forces(u)
y, lift = info["y"], info["lift"]
m = y > 0
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6), dpi=150); fig.subplots_adjust(0.08, 0.16, 0.98, 0.84, wspace=0.3)
dy = np.gradient(y[m]); a1.plot(y[m] * 1000, lift[m] / dy, color=ACC, lw=1.8); a1.set_xlabel("y (mm)"); a1.set_ylabel("lift per span (N/m)"); a1.set_title("spanload, gust C4", fontsize=9)
My = [abs(e["My"]) for e in ef]; a2.plot(ys[:-1] * 1000, My, color=INK, lw=1.8); a2.set_xlabel("y (mm)"); a2.set_ylabel("bending moment (N·m)"); a2.set_title(f"root {My[0]:.2f} N·m (limit)", fontsize=9)
fig.text(0.01, 0.95, "B-4  Gust case C4: spanload and spar bending moment along the span (nominal tube, web)", fontsize=10, fontweight="bold")
save(fig, "B-4.png")
# B-5 roll effectiveness
fig, ax = plt.subplots(figsize=(8, 3.6), dpi=150); fig.subplots_adjust(0.09, 0.16, 0.97, 0.84)
data = {"nominal tube, web": [(10, 0.748), (15, 0.484), (20, 0.082), (25, -0.434)], "low-grade tube, web": [(10, 0.623), (15, 0.230), (20, -0.370), (25, -1.142)],
        "skin 2.5× stiffer in shear": [(15, 0.612), (20, 0.309), (25, -0.079), (30, -0.554)]}
for (k, v), col, ls in zip(data.items(), (ACC, GREY, INK), ("-", "--", ":")):
    vv_, ee = zip(*v); ax.plot([0] + list(vv_), [1] + list(ee), color=col, ls=ls, lw=1.8, marker="o", ms=3, label=k)
ax.axhline(0, color="#b3261e", lw=1); ax.axvline(16, color=GREY, ls="--", lw=1); ax.text(16.2, 0.85, "16 m/s ceiling", fontsize=8, color=GREY)
ax.set_xlabel("airspeed (m/s)"); ax.set_ylabel("roll effectiveness (flex / rigid)"); ax.legend(fontsize=7.5, frameon=False); ax.set_xlim(0, 31)
fig.text(0.01, 0.95, "B-5  Elevon roll effectiveness: reversal at ≈ 21 m/s (nominal tube, with web)", fontsize=10, fontweight="bold")
save(fig, "B-5.png")
print("ok")
