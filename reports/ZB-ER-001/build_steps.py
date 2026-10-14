"""IKEA-style line illustrations for the Z!B build plan (B-01..B-14), from the real geometry."""
import math, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle, FancyBboxPatch, Arc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures"); os.makedirs(OUT, exist_ok=True)
INK, GREY, LIGHT, ACC = "#1a1a1a", "#8a8a8a", "#ececec", "#1f6fc5"
LW = 1.6

af = np.loadtxt(REPO + "/cad/mh60.dat", skiprows=1)
C, SPAN, SWEEP, WASH = 200.0, 900.0, math.radians(25), 6.0
U_SPAR, U_H = 0.30, 0.75
RIBS = [56.25, 168.75, 281.25, 393.75]
up = af[:np.argmin(af[:, 0]) + 1][::-1]; lo = af[np.argmin(af[:, 0]):]
def surf(u, s): return np.interp(u, s[:, 0], s[:, 1]) * C
def mid(u): return 0.5 * (surf(u, up) + surf(u, lo))

# isometric projection: x aft, y span (right), z up
def P(x, y, z):
    """oblique view from above and behind the left wing: span across, chord down-screen"""
    return np.array([y + 0.35 * x, -0.95 * x + 1.3 * z])

def section_pts(y, twist_deg=None, n=1):
    """airfoil outline at span station y in 3-D (LE swept, washout about the spar axis)."""
    tw = math.radians(WASH * abs(y) / (SPAN / 2) if twist_deg is None else twist_deg)
    xs, zs = af[:, 0] * C, af[:, 1] * C
    xc, zc = U_SPAR * C, mid(U_SPAR)
    xr = xc + (xs - xc) * math.cos(tw) + (zs - zc) * math.sin(tw)
    zr = zc - (xs - xc) * math.sin(tw) + (zs - zc) * math.cos(tw)
    return np.c_[xr + abs(y) * math.tan(SWEEP), np.full_like(xr, y), zr]

def proj(pts): return np.array([P(*p) for p in pts])

def new(title, num, w=7.2, h=4.6):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    ax.set_aspect("equal"); ax.axis("off")
    fig.subplots_adjust(0.02, 0.02, 0.98, 0.98)
    return fig, ax

def badge(fig, num, title):
    fig.text(0.03, 0.93, str(num), fontsize=26, fontweight="bold", color=INK, va="top", family="DejaVu Sans")
    fig.text(0.11, 0.915, title, fontsize=11, color=INK, va="top")

def arrow(ax, a, b, col=INK, lw=1.4, rad=0.0, ms=14):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=col, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))

def note(ax, xy, s, col=INK, fs=9, ha="center", **kw):
    ax.text(xy[0], xy[1], s, fontsize=fs, color=col, ha=ha, va="center", **kw)

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white"); plt.close(fig)

def draw_rib(ax, y, col=INK, fill=LIGHT, lw=LW, holes=True, twist=None):
    pts = proj(section_pts(y, twist)); ax.add_patch(Polygon(pts, closed=True, fc=fill, ec=col, lw=lw, zorder=3))
    if holes:
        for u in (0.15, 0.42, 0.56, 0.68):
            d = (surf(u, up) - surf(u, lo)) * 0.55 / 2
            ring = np.array([[u * C + d * math.cos(t), 0, mid(u) + d * math.sin(t)] for t in np.linspace(0, 2 * math.pi, 30)])
            ring[:, 0] += abs(y) * math.tan(SWEEP); ring[:, 1] = y
            ax.add_patch(Polygon(proj(ring), closed=True, fc="white", ec=col, lw=0.8, zorder=4))
    return pts

def spar_line(y0, y1):
    return proj([[U_SPAR * C + abs(y0) * math.tan(SWEEP), y0, mid(U_SPAR)], [U_SPAR * C + abs(y1) * math.tan(SWEEP), y1, mid(U_SPAR)]])

def draw_spar(ax, col=INK, lw=3.2):
    for s in (-1, 1):
        L = spar_line(0, s * SPAN / 2 * 1.0); ax.plot(L[:, 0], L[:, 1], color=col, lw=lw, solid_capstyle="round", zorder=5)

def draw_centre(ax, col=ACC):
    xs = U_SPAR * C
    box = [[xs - 70, -56, -6], [xs + 40, -56, -6], [xs + 40, 56, -6], [xs - 70, 56, -6]]
    ax.add_patch(Polygon(proj(box), closed=True, fc=col, alpha=0.18, ec=col, lw=1.4, zorder=6))

def autoscale(ax, pad=20):
    ax.relim(); ax.autoscale_view()
    xs, ys = [], []
    for p in ax.patches:
        if isinstance(p, Polygon):
            v = p.get_xy(); xs += list(v[:, 0]); ys += list(v[:, 1])
    for l in ax.lines:
        xs += list(l.get_xdata()); ys += list(l.get_ydata())
    if xs:
        ax.set_xlim(min(xs) - pad, max(xs) + pad); ax.set_ylim(min(ys) - pad, max(ys) + pad)

def fitfig(fig, ax, w=8.0):
    xl, yl = ax.get_xlim(), ax.get_ylim(); ar = (yl[1] - yl[0]) / (xl[1] - xl[0])
    h = w * 0.96 * ar + 1.45
    fig.set_size_inches(w, h)
    fig.subplots_adjust(0.02, 0.45 / h, 0.98, 1 - 1.0 / h)
    for t in fig.texts:
        x, y = t.get_position()
        if y > 0.5: t.set_y(1 - (1 - y) * 4.6 / h if False else 1 - 0.12 / h * (6 if t.get_fontsize() > 20 else 6.6))


def scale_icon(ax, cx, cy, w, txt):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - w * 0.18), w, w * 0.18, boxstyle="round,pad=0.5", fc="white", ec=INK, lw=LW))
    ax.add_patch(Rectangle((cx - w * 0.22, cy - w * 0.14), w * 0.44, w * 0.09, fc="#dff0e0", ec=INK, lw=0.8))
    note(ax, (cx, cy - w * 0.095), txt, fs=9, fontweight="bold")

# ---------------------------------------------------------------- B-01
fig, ax = new("", 1); badge(fig, 1, "Receive and inspect")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
# tube + caliper
ax.add_patch(Rectangle((6, 30), 50, 2.4, fc=LIGHT, ec=INK, lw=LW))
ax.add_patch(Polygon([[20, 26], [20, 40], [23, 40], [23, 33], [27, 33], [27, 29], [23, 29], [23, 26]], fc="white", ec=INK, lw=LW))
ax.add_patch(Rectangle((20, 36), 34, 4, fc="white", ec=INK, lw=LW))
ax.add_patch(Rectangle((40, 36.6), 10, 2.8, fc="#dff0e0", ec=INK, lw=0.8)); note(ax, (45, 38), "4.00", fs=8, fontweight="bold")
note(ax, (40, 24), "OD 4.00 ± 0.05 mm · record ID", fs=8.5)
# FC + usb
ax.add_patch(FancyBboxPatch((66, 30), 16, 12, boxstyle="round,pad=0.6", fc=LIGHT, ec=INK, lw=LW))
ax.add_patch(Circle((74, 36), 2.2, fc="white", ec=INK, lw=1)); ax.plot([82, 90, 94], [36, 36, 44], color=INK, lw=LW)
ax.add_patch(Rectangle((93, 44), 4, 6, fc="white", ec=INK, lw=LW)); note(ax, (74, 25), "power on day 1", fs=8.5)
# receiver on scale
scale_icon(ax, 74, 12, 22, "? g"); ax.add_patch(Rectangle((69, 13.5), 10, 6, fc="white", ec=ACC, lw=LW)); note(ax, (74, 3), "weigh F-08A + encoder", fs=8.5, col=ACC)
# checklist
for i in range(4):
    ax.add_patch(Rectangle((6, 6 + i * 4.5), 3, 3, fc="white", ec=INK, lw=1)); ax.plot([6.6, 7.4, 8.6], [7.6 + i * 4.5, 6.8 + i * 4.5, 8.6 + i * 4.5], color=INK, lw=1.2)
    ax.plot([11, 32], [7.5 + i * 4.5] * 2, color=GREY, lw=1)
note(ax, (19, 2), "check against §11.2", fs=8.5)
save(fig, "B-01.png")

# ---------------------------------------------------------------- B-02 coupon
fig, ax = new("", 2); badge(fig, 2, "Coupon test (Oct 21–22)")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
# 3-point bend
ax.add_patch(Rectangle((5, 38), 40, 1.8, fc=LIGHT, ec=INK, lw=LW))
for x in (8, 42): ax.add_patch(Polygon([[x - 2, 34], [x + 2, 34], [x, 38]], fc="white", ec=INK, lw=LW))
arrow(ax, (25, 50), (25, 40.5), col=ACC, lw=2); note(ax, (25, 52.5), "F → failure", col=ACC, fs=8.5)
note(ax, (25, 29), "spare tube, 3-point bend\nE ≥ 80 GPa · σ ≥ 600 MPa", fs=8)
# foam on scale
scale_icon(ax, 72, 40, 24, "g"); ax.add_patch(Polygon([[64, 41.8], [80, 41.8], [83, 46], [67, 46]], fc=LIGHT, ec=INK, lw=LW))
note(ax, (72, 31), "100 × 100 mm Depron", fs=8)
# strip tension
ax.add_patch(Rectangle((8, 8), 30, 4, fc=LIGHT, ec=INK, lw=LW)); arrow(ax, (8, 10), (2, 10), col=ACC, lw=2); arrow(ax, (38, 10), (44, 10), col=ACC, lw=2)
note(ax, (23, 18), "Depron strip: tension", fs=8)
# joint pull
ax.add_patch(Rectangle((60, 6), 26, 3, fc=LIGHT, ec=INK, lw=LW)); ax.add_patch(Rectangle((71, 9), 3, 9, fc="white", ec=INK, lw=LW))
arrow(ax, (72.5, 18), (72.5, 25), col=ACC, lw=2); note(ax, (82, 21), "rib–skin\nCA pull", fs=8)
save(fig, "B-02.png")

# ---------------------------------------------------------------- B-03 print parts
fig, ax = new("", 3); badge(fig, 3, "Print ribs and printed parts")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
ax.add_patch(Rectangle((5, 12), 26, 30, fc="white", ec=INK, lw=LW)); ax.add_patch(Rectangle((8, 15), 20, 3, fc=LIGHT, ec=INK, lw=1))
ax.plot([5, 31], [38, 38], color=INK, lw=LW); ax.add_patch(Rectangle((15, 33), 6, 5, fc=LIGHT, ec=INK, lw=1))
note(ax, (18, 7), "PLA, flat, 3 mm", fs=8.5)
xs, zs = af[:, 0] * 30, af[:, 1] * 30
for k in range(3):
    ax.add_patch(Polygon(np.c_[40 + xs + k * 2, 36 + zs * 1 - k * 2], fc=LIGHT, ec=INK, lw=LW))
ax.add_patch(Circle((40 + 0.3 * 30, 36 + mid(0.3) / C * 30), 0.9, fc="white", ec=INK, lw=1))
note(ax, (66, 44), "× 8", fs=16, fontweight="bold"); note(ax, (56, 26), "1.5 g ± 0.3 each", fs=8.5)
# centre section
ax.add_patch(Polygon([[75, 20], [93, 20], [96, 30], [90, 40], [78, 40], [72, 30]], fc=ACC, alpha=0.15, ec=ACC, lw=LW))
ax.plot([84, 74], [30, 38], color=ACC, lw=2.5); ax.plot([84, 94], [30, 38], color=ACC, lw=2.5)
note(ax, (84, 14), "centre section ZB-110\nsocket axes in the layer plane", col=ACC, fs=8)
scale_icon(ax, 50, 9, 16, "g")
save(fig, "B-03.png")

# ---------------------------------------------------------------- B-04 cut spar
fig, ax = new("", 4); badge(fig, 4, "Cut the spar halves")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
ax.add_patch(Rectangle((5, 38), 90, 2.2, fc=LIGHT, ec=INK, lw=LW))
ax.plot([49.7, 49.7], [34, 44], color=ACC, lw=1.4, ls="--"); ax.plot([94, 94], [34, 44], color=GREY, lw=1, ls="--")
note(ax, (50, 47), "cut", col=ACC, fs=9)
ax.annotate("", (5, 32), (49.7, 32), arrowprops=dict(arrowstyle="<->", color=INK, lw=1)); note(ax, (27, 29), "497 mm", fs=9)
for k in range(2):
    ax.add_patch(Rectangle((8, 14 - k * 5), 45, 2, fc=LIGHT, ec=INK, lw=LW))
note(ax, (58, 12), "× 2", fs=16, fontweight="bold")
scale_icon(ax, 82, 12, 18, "3.9 g"); note(ax, (82, 3), "± 0.3 g each", fs=8)
save(fig, "B-04.png")

# ---------------------------------------------------------------- B-05 dry fit
fig, ax = new("", 5, 8, 4.2); badge(fig, 5, "Dry-fit spar, ribs and centre section")
draw_spar(ax)
draw_centre(ax)
for y in RIBS:
    for s in (-1, 1):
        draw_rib(ax, s * y, fill="white", lw=1.2)
# one rib being slid on
yy = 393.75 + 70
pts = proj(section_pts(yy, 6.0)); ax.add_patch(Polygon(pts, closed=True, fc=LIGHT, ec=ACC, lw=1.6, zorder=7))
a = P(U_SPAR * C + yy * math.tan(SWEEP), yy, mid(U_SPAR)); b = P(U_SPAR * C + 393.75 * math.tan(SWEEP), 393.75 + 10, mid(U_SPAR))
arrow(ax, tuple(a + [0, 30]), tuple(b + [0, 30]), col=ACC)
autoscale(ax)
fitfig(fig, ax); fig.text(0.5, 0.03, "25° ± 0.5° each side\nstations ±56 / 169 / 281 / 394 mm (along y)", fontsize=8.5, ha="center")
save(fig, "B-05.png")

# ---------------------------------------------------------------- B-06 washout jig
fig, ax = new("", 6); badge(fig, 6, "Set the washout in the jig")
ax.set_xlim(-10, 470); ax.set_ylim(-60, 170)
ys = [0] + RIBS
for i, y in enumerate(ys):
    tw = WASH * y / 450
    x0 = 30 + i * 85
    xs, zs = af[:, 0] * C * 0.36, af[:, 1] * C * 0.36
    t = math.radians(tw); xc = U_SPAR * C * 0.36
    xr = xc + (xs - xc) * math.cos(t) + zs * math.sin(t); zr = -(xs - xc) * math.sin(t) + zs * math.cos(t)
    ax.add_patch(Polygon(np.c_[x0 + xr, 60 + zr], fc=LIGHT if i else "white", ec=INK, lw=LW))
    h = 10 + (xr[np.argmax(xs)] * 0)  # shim
    ax.add_patch(Rectangle((x0 + 40, 60 + zr[0] - 14), 20, 12, fc="white", ec=GREY, lw=1, hatch="///"))
    ax.text(x0 + 36, 20, f"{tw:.1f}°", fontsize=9, ha="center", color=ACC if i == len(ys) - 1 else INK, fontweight="bold" if i == len(ys) - 1 else None)
    ax.text(x0 + 36, 5, "root" if i == 0 else f"y {y:.0f}", fontsize=7.5, ha="center", color=GREY)
ax.plot([0, 470], [40, 40], color=INK, lw=2)
note(ax, (235, -30), "nose-down twist, linear 0° → 6°; check each rib with the inclinometer, ±0.3°", fs=8.5)
note(ax, (235, 140), "jig ZB-116 + shims", fs=9, col=GREY)
save(fig, "B-06.png")

# ---------------------------------------------------------------- B-07 bond
fig, ax = new("", 7); badge(fig, 7, "Bond spar, ribs and centre section")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
xs, zs = af[:, 0] * 0.42, af[:, 1] * 0.42
ax.add_patch(Polygon(np.c_[20 + xs * 100 / 1, 30 + zs * 100], fc=LIGHT, ec=INK, lw=LW))
sx, sz = 20 + 0.3 * 42, 30 + mid(0.3) / C * 42
ax.add_patch(Circle((sx, sz), 1.3, fc=INK, ec=INK))
# CA bottle
ax.add_patch(Polygon([[sx - 3, sz + 18], [sx + 3, sz + 18], [sx + 2, sz + 8], [sx, sz + 5], [sx - 2, sz + 8]], fc="white", ec=INK, lw=LW))
ax.add_patch(Circle((sx, sz + 3), 0.8, fc=ACC, ec=ACC)); note(ax, (sx + 10, sz + 15), "thin CA, wick", fs=8.5, ha="left")
# clock
ax.add_patch(Circle((82, 40), 9, fc="white", ec=INK, lw=LW)); ax.plot([82, 82], [40, 47], color=INK, lw=1.4); ax.plot([82, 82], [40, 33], color=ACC, lw=1.4)
note(ax, (82, 26), "30 min", fs=10, fontweight="bold")
note(ax, (40, 10), "every rib slot + both sockets; re-check incidence", fs=8.5)
save(fig, "B-07.png")

# ---------------------------------------------------------------- B-08 webs
fig, ax = new("", 8); badge(fig, 8, "Install the webs (R2, R3)")
ax.set_xlim(-5, 215); ax.set_ylim(-45, 70)
ax.add_patch(Polygon(np.c_[af[:, 0] * C, af[:, 1] * C], fc=LIGHT, ec=INK, lw=LW))
for u, lab in ((0.525, "mid-chord web 52.5%\n15.9 mm high"), (U_H, "hinge-line web 75%\n7.7 mm high")):
    zt, zb = surf(u, up), surf(u, lo)
    ax.add_patch(Rectangle((u * C - 1.5, zb), 3, zt - zb, fc=ACC, ec=ACC, alpha=0.9))
    arrow(ax, (u * C, zt + 30), (u * C, zt + 3), col=ACC); note(ax, (u * C, zt + 40), lab, fs=8, col=ACC)
ax.add_patch(Circle((U_SPAR * C, mid(U_SPAR)), 2, fc=INK)); note(ax, (60, -14), "spar", fs=8)
ax.add_patch(Circle((0.525 * C, mid(0.525)), 1.8, fc="white", ec=INK, lw=0.8)); note(ax, (120, -28), "Ø 6 mm hole at each servo bay for the lead", fs=8)
save(fig, "B-08.png")

# ---------------------------------------------------------------- B-09 servos + wiring
fig, ax = new("", 9, 8, 4.2); badge(fig, 9, "Fit servos, avionics and wiring")
draw_spar(ax, col=GREY, lw=2)
for y in RIBS:
    for s in (-1, 1): draw_rib(ax, s * y, fill="white", col=GREY, lw=0.9, holes=False)
draw_centre(ax)
for s in (-1, 1):
    y = s * 250; x = 0.6 * C + 250 * math.tan(SWEEP)
    box = [[x - 10, y - 12, 0], [x + 10, y - 12, 0], [x + 10, y + 12, 0], [x - 10, y + 12, 0]]
    ax.add_patch(Polygon(proj(box), closed=True, fc=ACC, alpha=0.35, ec=ACC, lw=1.4, zorder=8))
    w = proj([[x, y, 0], [x - 40, y * 0.6, 0], [0.47 * C, s * 20, 0]]); ax.plot(w[:, 0], w[:, 1], color=ACC, lw=1.2, ls="--", zorder=8)
fc = proj([[0.4 * C, -18, 0], [0.55 * C, -18, 0], [0.55 * C, 18, 0], [0.4 * C, 18, 0]]); ax.add_patch(Polygon(fc, closed=True, fc=INK, alpha=0.6, ec=INK, zorder=9))
autoscale(ax)
fitfig(fig, ax); fig.text(0.5, 0.03, "servos at y ±250 mm, 60% chord · leads through rib holes · FC, RX, encoder, ESC on centre section", fontsize=8.5, ha="center")
save(fig, "B-09.png")

# ---------------------------------------------------------------- B-10 skinning
fig, ax = new("", 10, 8, 4.2); badge(fig, 10, "Skin the wing (in the jig)")
draw_spar(ax, col=GREY, lw=2)
for y in RIBS:
    for s in (-1, 1): draw_rib(ax, s * y, fill="white", col=GREY, lw=0.9, holes=False)
# top skin panel right half lifted
lift = 60
for s in (1,):
    pts = []
    for y in np.linspace(0, 450, 12):
        pts.append([y * math.tan(SWEEP), s * y, surf(0.0, up) + lift])
    for y in np.linspace(450, 0, 12):
        pts.append([y * math.tan(SWEEP) + U_H * C, s * y, surf(U_H, up) + lift])
    ax.add_patch(Polygon(proj(pts), closed=True, fc=ACC, alpha=0.15, ec=ACC, lw=1.4, zorder=8))
    a = P(0.4 * C + 250 * math.tan(SWEEP), 250, lift + 10); b = P(0.4 * C + 250 * math.tan(SWEEP), 250, 15)
    arrow(ax, tuple(a), tuple(b), col=ACC)
autoscale(ax)
fitfig(fig, ax); fig.text(0.5, 0.03, "top skins first, then bottom (hatch aperture, r 8 mm) · foam-safe CA · waves ≤ 1 mm", fontsize=8.5, ha="center")
save(fig, "B-10.png")

# ---------------------------------------------------------------- B-11 elevons, fins, hatch
fig, ax = new("", 11); badge(fig, 11, "Elevons, fins and hatch")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
# elevon throw side view
ax.add_patch(Polygon([[5, 36], [32, 38], [40, 36.5], [32, 35], [5, 34]], fc=LIGHT, ec=INK, lw=LW))
for ang, col, lab in ((12, ACC, "≥ 12° up"), (-8, INK, "≥ 8° down")):
    t = math.radians(ang); ax.plot([40, 40 + 14 * math.cos(t)], [36.5, 36.5 + 14 * math.sin(t)], color=col, lw=2.2)
    note(ax, (58, 36.5 + 16 * math.sin(t)), lab, fs=8.5, col=col)
ax.plot([40, 54], [36.5, 36.5], color=GREY, lw=1, ls=":"); note(ax, (22, 28), "hinge tape, top + bottom", fs=8)
# fin
ax.add_patch(Polygon([[80, 32], [90, 32], [90, 56], [84, 56]], fc=LIGHT, ec=INK, lw=LW)); ax.plot([66, 96], [32, 32], color=INK, lw=2.5)
note(ax, (80, 26), "tip fin, upright: 120 high × 60 chord\naft 30% of tip chord (PR #13)", fs=8)
# hatch lid
ax.add_patch(FancyBboxPatch((14, 6), 24, 12, boxstyle="round,pad=0.4,rounding_size=2", fc="white", ec=INK, lw=LW))
ax.add_patch(FancyBboxPatch((15.5, 7.5), 21, 9, boxstyle="round,pad=0.2,rounding_size=1.6", fc=ACC, alpha=0.2, ec=ACC, lw=1.2))
arrow(ax, (44, 12), (50, 12), col=ACC); note(ax, (64, 12), "pull-off ≥ 9.1 N\n(luggage scale)", fs=8.5, col=ACC)
note(ax, (26, 2.5), "hatch lid bears on the frame", fs=8)
save(fig, "B-11.png")

# ---------------------------------------------------------------- B-12 weigh and balance
fig, ax = new("", 12); badge(fig, 12, "Weigh and balance (Nov 5)")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
scale_icon(ax, 25, 18, 34, "≤ 250 g")
ax.add_patch(Polygon([[10, 22], [40, 22], [36, 26], [14, 26]], fc=LIGHT, ec=INK, lw=LW)); note(ax, (25, 33), "alert at 230 g", fs=8.5)
# balance side view
ax.add_patch(Polygon(np.c_[55 + af[:, 0] * 40, 34 + af[:, 1] * 40], fc=LIGHT, ec=INK, lw=LW))
cgx = 55 + 128.5 / C * 40 * 0.62
ax.add_patch(Polygon([[cgx - 2.5, 24], [cgx + 2.5, 24], [cgx, 31.5]], fc=ACC, ec=ACC))
ax.add_patch(Circle((cgx, 36), 1.6, fc="white", ec=INK, lw=1)); ax.plot([cgx - 1.6, cgx + 1.6], [36, 36], color=INK, lw=0.8); ax.plot([cgx, cgx], [34.4, 37.6], color=INK, lw=0.8)
note(ax, (75, 18), "CG 128.5 mm aft of root LE\n(SM 5–8%) · move the battery first", fs=8.5, col=ACC)
save(fig, "B-12.png")

# ---------------------------------------------------------------- B-13 systems check
fig, ax = new("", 13); badge(fig, 13, "Systems check and failsafe")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
ax.add_patch(Rectangle((6, 26), 26, 17, fc="white", ec=INK, lw=LW)); ax.add_patch(Polygon([[3, 26], [35, 26], [38, 22], [0, 22]], fc=LIGHT, ec=INK, lw=LW))
note(ax, (19, 35), "ArduPlane\nparams (VC-37)", fs=8)
# transmitter off
ax.add_patch(FancyBboxPatch((48, 24), 18, 16, boxstyle="round,pad=0.6", fc="white", ec=INK, lw=LW)); ax.plot([52, 50], [40, 48], color=INK, lw=1.4)
note(ax, (57, 32), "OFF", fs=10, fontweight="bold", col="#b3261e")
arrow(ax, (68, 32), (76, 32), col=ACC); note(ax, (86, 32), "RTL ✓", fs=12, fontweight="bold", col=ACC)
note(ax, (50, 12), "propeller fitted only now · static throttle test with the wattmeter", fs=8.5)
save(fig, "B-13.png")

# ---------------------------------------------------------------- B-14 GVT + stiffness
fig, ax = new("", 14); badge(fig, 14, "Tap test, tip torque and tip load")
ax.set_xlim(0, 100); ax.set_ylim(0, 62)
ax.add_patch(Rectangle((3, 22), 8, 22, fc="white", ec=INK, lw=LW, hatch="///")); ax.add_patch(Polygon([[11, 34], [80, 37], [80, 33], [11, 31]], fc=LIGHT, ec=INK, lw=LW))
ax.plot([80, 80], [35, 20], color=INK, lw=1); ax.add_patch(Rectangle((76, 14), 8, 6, fc=ACC, alpha=0.3, ec=ACC)); note(ax, (90, 17), "known\nweight", fs=8)
ax.add_patch(Rectangle((60, 38), 6, 10, fc="white", ec=INK, lw=LW)); note(ax, (63, 52), "phone", fs=8)
ax.annotate("", (86, 40), (86, 30), arrowprops=dict(arrowstyle="<->", color=ACC, lw=1.2, connectionstyle="arc3,rad=0.6")); note(ax, (94, 35), "twist", fs=8, col=ACC)
note(ax, (45, 8), "expect ≈ 11 Hz bending, ≈ 32 Hz torsion · record GJ, EI → confirm 16 m/s ceiling", fs=8.5)
save(fig, "B-14.png")
print("ok")
