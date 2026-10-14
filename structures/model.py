"""Z!B structural model: geometry, section properties, VLM-derived loads, 3D beam FE.

Everything geometric comes from cad/params.json through the twin's VLM (twin/vlm.py),
so the structure and the aero always describe the same wing (RQ-09).

Frames: x aft of root leading edge, y right (span), z up. SI units (m, N, Pa, kg).
Half model: right wing, clamped at the centreline (root joiner). Symmetric load cases
use it directly; antisymmetric (aileron) cases use it as an approximation (stated).
"""
import os, sys, math
import numpy as np
from scipy.linalg import eigh

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin"))
sys.path.insert(0, REPO)
import vlm  # noqa: E402
from structures import materials as MAT  # noqa: E402

G0, RHO = 9.80665, 1.225

# Mass model (g), from WEIGHT_BUDGET.md airframe rollup and BUDGET.md LRU picks.
# Wing-borne (relieves bending) vs centre-borne (does not).
MASS = dict(total_g=211.9, skins_g=36.0, ribs_g=12.0, spar_g=7.9, misc_wing_g=8.85,
            servo_g=4.3, servo_y_frac=0.55)


class FlexWing(vlm.Wing):
    """VLM wing whose twist can be perturbed by a structural twist distribution (rad, + nose-up)."""

    def __init__(self, design, dtheta=None, **kw):
        super().__init__(design, **kw)
        self.dtheta = dtheta  # callable |y| -> rad nose-up, or None

    def twist(self, y):
        base = super().twist(y)  # + nose-down
        if self.dtheta is None:
            return base
        return base - self.dtheta(abs(y))


def strip_loads(wing, alpha_deg, elevon_deg=0.0, aileron_deg=0.0):
    """Per-strip lift (unit rho, unit V) and centre of pressure from the VLM.

    Returns arrays over all strips: y_mid, dy, lift, x_cp (m, aft of root LE).
    Multiply lift by rho*V^2 for newtons.
    """
    A, B, C, N = wing._panels(elevon_deg, aileron_deg)
    a = math.radians(alpha_deg); V = np.array([math.cos(a), 0.0, math.sin(a)])
    AIC = np.einsum("ijk,ik->ij", wing._hs(C, A, B), N)
    G = np.linalg.solve(AIC, -N @ V)
    mid = 0.5 * (A + B); dl = B - A
    v_ind = np.einsum("ijk,j->ik", wing._hs(mid, A, B), G)
    F = np.cross(V[None] + v_ind, dl) * G[:, None]
    lift_dir = np.array([-math.sin(a), 0, math.cos(a)])
    Lp = F @ lift_dir
    ns, nc = 2 * wing.ns, wing.nc
    Lp = Lp.reshape(ns, nc); xm = mid[:, 0].reshape(ns, nc)
    lift = Lp.sum(1)
    xcp = np.where(np.abs(lift) > 1e-12, (Lp * xm).sum(1) / np.where(np.abs(lift) > 1e-12, lift, 1), xm.mean(1))
    y = 0.5 * (wing.yb[1:] + wing.yb[:-1]); dy = np.diff(wing.yb)
    return y, dy, lift, xcp


class Geometry:
    def __init__(self):
        raw, self.design, self.hash = vlm.load()
        P = self.design
        self.wing = vlm.Wing(P)
        self.af = self.wing.W.af
        self.b = P["span"] / 1000; self.c = P["chord"] / 1000
        self.lam = math.radians(P["sweep_deg"])
        self.u_spar = P["spar_x_frac"]; self.u_h = P["hinge_x_frac"]
        self.od = P["spar_dia"] / 1000; self.id = 0.003  # ID 3 mm ASSUMED (structures.py; caliper at coupon)
        self.rib_y = [y / 1000 for y in raw["derived"]["rib_stations_y"] if y > 0]
        self.hatch = raw["derived"]["hatch_rect"]
        self.elevon = (P["elevon_y0"] / 1000, P["elevon_y1"] / 1000)

    def x_spar(self, y):
        return self.wing.xle(y) + self.u_spar * self.wing.chord(y)


def section(geo, spar="nominal", web=False, od=None, id_=None, caps=None):
    """Section properties perpendicular to the swept spar axis.

    web: True = a 3 mm Depron web closes the skin at the hinge line (closed torsion box);
         False = as drawn in CAD today (skins stop at the hinge: open C-section between ribs).
    caps: optional dict(w, t, E) for carbon strip caps bonded on top and bottom skins at the spar.
    """
    S = MAT.SPAR_GRADES[spar]; D = MAT.DEPRON
    od = od or geo.od; id_ = id_ if id_ is not None else geo.id
    cp = geo.c * math.cos(geo.lam)           # chord perpendicular to the spar
    cz = geo.c                                # thickness is the streamwise one
    u = np.linspace(0, geo.u_h, 81)
    top = np.array([[ui * cp, geo.af.top(ui) * cz] for ui in u])
    bot = np.array([[ui * cp, geo.af.bot(ui) * cz] for ui in u])
    t = D["t"]
    segs = []
    for pts in (top, bot):
        for p, q in zip(pts[:-1], pts[1:]):
            segs.append((0.5 * (p + q), np.linalg.norm(q - p), t))
    h_web = (geo.af.top(geo.u_h) - geo.af.bot(geo.u_h)) * cz
    if web:
        segs.append((np.array([geo.u_h * cp, 0.5 * (geo.af.top(geo.u_h) + geo.af.bot(geo.u_h)) * cz]), h_web, t))
    xs = geo.u_spar * cp; zs = geo.af.mid(geo.u_spar) * cz
    A_t = math.pi / 4 * (od**2 - id_**2); I_t = math.pi / 64 * (od**4 - id_**4); J_t = 2 * I_t
    # modulus-weighted centroid
    EA_sk = sum(D["E"] * L * tt for (_, L, tt) in segs)
    zbar_sk = sum(D["E"] * L * tt * m[1] for (m, L, tt) in segs) / EA_sk
    xbar_sk = sum(D["E"] * L * tt * m[0] for (m, L, tt) in segs) / EA_sk
    EA = EA_sk + S["E"] * A_t
    zna = (EA_sk * zbar_sk + S["E"] * A_t * zs) / EA
    xna = (EA_sk * xbar_sk + S["E"] * A_t * xs) / EA
    EI_flap = S["E"] * (I_t + A_t * (zs - zna)**2) + sum(D["E"] * L * tt * (m[1] - zna)**2 for (m, L, tt) in segs)
    EI_chord = S["E"] * (I_t + A_t * (xs - xna)**2) + sum(D["E"] * L * tt * (m[0] - xna)**2 for (m, L, tt) in segs)
    cap_EI = 0.0
    if caps:
        # caps bonded to the INNER face of each skin over the spar (needs a full-depth spar-line web to stay stable)
        zt = geo.af.top(geo.u_spar) * cz - t - caps["t"] / 2; zb = geo.af.bot(geo.u_spar) * cz + t + caps["t"] / 2
        for zc in (zt, zb):
            cap_EI += caps["E"] * caps["w"] * caps["t"] * (zc - zna)**2
        EI_flap += cap_EI
    # torsion
    if web:
        poly = np.vstack([top, bot[::-1]])
        Aenc = 0.5 * abs(np.dot(poly[:, 0], np.roll(poly[:, 1], 1)) - np.dot(poly[:, 1], np.roll(poly[:, 0], 1)))
        ds_t = sum(L / tt for (_, L, tt) in segs)
        J_sk = 4 * Aenc**2 / ds_t
    else:
        Aenc = None
        J_sk = sum(L * tt**3 / 3 for (_, L, tt) in segs)
    GJ = S["G"] * J_t + D["G"] * J_sk
    ztop = max(p[1] for p in top); zbot = min(p[1] for p in bot)
    return dict(EA=EA, EI_flap=EI_flap, EI_chord=EI_chord, GJ=GJ, GJ_spar=S["G"] * J_t, GJ_skin=D["G"] * J_sk,
                E_s=S["E"], G_s=S["G"], sigma_allow=S["sigma_allow"], I_t=I_t, J_t=J_t, A_t=A_t, od=od,
                zna=zna, zs=zs, ztop=ztop, zbot=zbot, Aenc=Aenc, J_sk=J_sk, web=web, h_web=h_web,
                chord_perp=cp, cap_EI=cap_EI, spar=spar)


# ------------------------------------------------------------------ 3D frame FE
def frame_k_local(L, EA, EIy, EIz, GJ):
    k = np.zeros((12, 12))
    k[0, 0] = k[6, 6] = EA / L; k[0, 6] = -EA / L
    k[3, 3] = k[9, 9] = GJ / L; k[3, 9] = -GJ / L
    # bending in x-y plane (v, theta_z) uses EIz
    a, b_, c_, d = 12 * EIz / L**3, 6 * EIz / L**2, 4 * EIz / L, 2 * EIz / L
    k[1, 1] = k[7, 7] = a; k[1, 7] = -a
    k[1, 5] = k[1, 11] = b_; k[5, 7] = k[7, 11] = -b_
    k[5, 5] = k[11, 11] = c_; k[5, 11] = d
    # bending in x-z plane (w, theta_y) uses EIy
    a, b_, c_, d = 12 * EIy / L**3, 6 * EIy / L**2, 4 * EIy / L, 2 * EIy / L
    k[2, 2] = k[8, 8] = a; k[2, 8] = -a
    k[2, 4] = k[2, 10] = -b_; k[4, 8] = k[8, 10] = b_
    k[4, 4] = k[10, 10] = c_; k[4, 10] = d
    return k + np.triu(k, 1).T


def rot_matrix(p1, p2):
    ex = (p2 - p1) / np.linalg.norm(p2 - p1)
    ez0 = np.array([0.0, 0.0, 1.0])
    ey = np.cross(ez0, ex); ey /= np.linalg.norm(ey)
    ez = np.cross(ex, ey)
    return np.vstack([ex, ey, ez])


class BeamFE:
    """Clamped-root 3D frame along a polyline of nodes (n x 3), uniform or per-element sections."""

    def __init__(self, nodes, sections):
        self.X = np.asarray(nodes, float); self.n = len(self.X)
        self.secs = sections if isinstance(sections, list) else [sections] * (self.n - 1)
        nd = 6 * self.n; self.K = np.zeros((nd, nd)); self.el = []
        for e in range(self.n - 1):
            p1, p2 = self.X[e], self.X[e + 1]; L = np.linalg.norm(p2 - p1); s = self.secs[e]
            kl = frame_k_local(L, s["EA"], s["EI_flap"], s["EI_chord"], s["GJ"])
            R = rot_matrix(p1, p2); T = np.kron(np.eye(4), R)
            kg = T.T @ kl @ T
            idx = np.r_[6 * e:6 * e + 6, 6 * e + 6:6 * e + 12]
            self.K[np.ix_(idx, idx)] += kg
            self.el.append(dict(L=L, kl=kl, T=T, idx=idx, sec=s))
        self.free = np.arange(6, nd)  # node 0 clamped

    def solve(self, F):
        u = np.zeros(6 * self.n)
        Kf = self.K[np.ix_(self.free, self.free)]
        u[self.free] = np.linalg.solve(Kf, F[self.free])
        self.u = u
        return u

    def element_forces(self, u=None):
        u = self.u if u is None else u
        out = []
        for e in self.el:
            f = e["kl"] @ (e["T"] @ u[e["idx"]])
            # internal forces at element start (sign: force exerted ON element by node 1)
            out.append(dict(N=-f[0], Vy=-f[1], Vz=-f[2], T=-f[3], My=-f[4], Mz=-f[5]))
        return out


def build(geo, n_el=30, **seckw):
    ytip = geo.b / 2
    ys = np.linspace(0, ytip, n_el + 1)
    nodes = np.array([[geo.x_spar(y), y, 0.0] for y in ys])
    sec = section(geo, **seckw)
    return BeamFE(nodes, sec), ys, sec


# ------------------------------------------------------------------ loads
def mass_strips(geo, y, dy):
    """Wing-borne mass per strip (kg) and its chordwise x, right half only (y>0)."""
    half = geo.b / 2
    m = np.zeros_like(y); xm = np.zeros_like(y)
    per_len = (MASS["skins_g"] + MASS["spar_g"] + MASS["misc_wing_g"]) / 1000 / geo.b
    for i, (yi, d) in enumerate(zip(y, dy)):
        if yi <= 0:
            continue
        m[i] = per_len * d
        xm[i] = geo.wing.xle(yi) + 0.40 * geo.wing.chord(yi)
    # ribs (point masses) and servo
    rib_m = MASS["ribs_g"] / 1000 / 8
    for yr in geo.rib_y:
        i = int(np.argmin(np.abs(y - yr))); xm[i] = (xm[i] * m[i] + (geo.wing.xle(yr) + 0.45 * geo.wing.chord(yr)) * rib_m) / (m[i] + rib_m); m[i] += rib_m
    ysv = MASS["servo_y_frac"] * half; i = int(np.argmin(np.abs(y - ysv)))
    sv = MASS["servo_g"] / 1000
    xm[i] = (xm[i] * m[i] + (geo.wing.xle(ysv) + 0.6 * geo.wing.chord(ysv)) * sv) / (m[i] + sv); m[i] += sv
    return m, xm


def trim_lift(geo, wing, CL_req, elevon_deg):
    """alpha that gives CL_req with the given elevon (linear VLM)."""
    s0 = wing.solve(0.0, elevon_deg=elevon_deg); s1 = wing.solve(1.0, elevon_deg=elevon_deg)
    return (CL_req - s0["CL"]) / (s1["CL"] - s0["CL"])


def nodal_loads(geo, fe, ys, V, n, elevon_deg=0.0, aileron_deg=0.0, wing=None, alpha=None, CL_req=None):
    """Assemble nodal force vector for a symmetric (or aileron) load case on the right half."""
    wing = wing or geo.wing
    W = MASS["total_g"] / 1000 * G0
    q = 0.5 * RHO * V**2
    if alpha is None:
        CL_req = CL_req if CL_req is not None else n * W / (q * wing.S)
        alpha = trim_lift(geo, wing, CL_req, elevon_deg)
    y, dy, lift, xcp = strip_loads(wing, alpha, elevon_deg, aileron_deg)
    Lstrip = lift * RHO * V**2
    m, xm = mass_strips(geo, y, dy)
    F = np.zeros(6 * fe.n)
    for i in range(len(y)):
        if y[i] <= 0:
            continue
        k = int(np.argmin(np.abs(ys - y[i])))
        node = fe.X[k]
        for Fz, x in ((Lstrip[i], xcp[i]), (-n * m[i] * G0, xm[i])):
            r = np.array([x, y[i], 0.0]) - node
            Fv = np.array([0.0, 0.0, Fz])
            F[6 * k:6 * k + 3] += Fv
            F[6 * k + 3:6 * k + 6] += np.cross(r, Fv)
    return F, dict(alpha=alpha, y=y, lift=Lstrip, xcp=xcp, q=q, wing_lift_half=Lstrip[y > 0].sum(),
                   inertia_half=n * m[y > 0].sum() * G0)


def stresses(sec, ef):
    """Peak stresses at one element end from its internal forces."""
    M = abs(ef["My"]); T = abs(ef["T"])
    kappa = M / sec["EI_flap"]
    sig_spar = sec["E_s"] * kappa * (abs(sec["zs"] - sec["zna"]) + sec["od"] / 2)
    E_f = MAT.DEPRON["E"]
    sig_top = E_f * kappa * (sec["ztop"] - sec["zna"])      # compression for positive lift
    sig_bot = E_f * kappa * (sec["zna"] - sec["zbot"])      # tension
    T_sp = T * sec["GJ_spar"] / sec["GJ"]; T_sk = T * sec["GJ_skin"] / sec["GJ"]
    tau_spar = T_sp * (sec["od"] / 2) / sec["J_t"]
    t = MAT.DEPRON["t"]
    tau_skin = T_sk / (2 * sec["Aenc"] * t) if sec["web"] else T_sk * t / sec["J_sk"]
    return dict(M=M, T=T, sig_spar=sig_spar, sig_top=sig_top, sig_bot=sig_bot, tau_spar=tau_spar, tau_skin=tau_skin)


def streamwise_twist(fe, u):
    """Nose-up rotation about the global y (pitch) axis at each node, rad."""
    return u[4::6].copy()


def tip_deflection(u):
    return u[2::6][-1]


def skin_buckling_stress(geo, width_frac=0.45):
    """Flat-plate buckling of the top skin panel between spar and hinge (k=4, conservative: ignores curvature).
    width_frac=0.45 is the panel as drawn (spar 30% to hinge 75%); 0.225 with a mid-chord web at 52.5%."""
    D = MAT.DEPRON
    b = width_frac * geo.c
    return 4 * math.pi**2 * D["E"] / (12 * (1 - D["nu"]**2)) * (D["t"] / b)**2


# ------------------------------------------------------------------ modes
def mass_matrix(geo, fe, ys, at_ea=False):
    """Lumped mass matrix. at_ea=True puts each strip's mass on the spar axis (r = 0) and its
    offset into the torsional inertia: this gives the UNCOUPLED bending and torsion modes the
    typical-section flutter screen needs (its own x_alpha carries the inertial coupling)."""
    y = np.linspace(0, geo.b / 2, 201); dy = np.gradient(y)
    m, xm = mass_strips(geo, y, dy)
    Mg = np.zeros((6 * fe.n, 6 * fe.n))
    ax = np.array([math.sin(geo.lam), math.cos(geo.lam), 0.0])
    kg = 0.25 * geo.c  # chordwise radius of gyration of the section mass about its own cg (assumed)
    for yi, mi, xi in zip(y, m, xm):
        if mi <= 0:
            continue
        k = int(np.argmin(np.abs(ys - yi))); r = np.array([xi, yi, 0.0]) - fe.X[k]
        if at_ea:
            d = float(np.linalg.norm(r - (r @ ax) * ax))  # perpendicular offset from the spar axis
            Mp = np.zeros((6, 6)); Mp[:3, :3] = mi * np.eye(3)
            Mp[3:, 3:] = mi * (kg**2 + d**2) * np.outer(ax, ax) + mi * kg**2 * 1e-3 * np.eye(3)
        else:
            S = np.array([[0, -r[2], r[1]], [r[2], 0, -r[0]], [-r[1], r[0], 0]])
            T = np.hstack([np.eye(3), -S])
            Mp = mi * T.T @ T
            Mp[4, 4] += mi * kg**2; Mp[5, 5] += mi * kg**2; Mp[3, 3] += mi * 1e-6
        idx = slice(6 * k, 6 * k + 6)
        Mg[idx, idx] += Mp
    return Mg


def modes(geo, fe, ys, nmodes=6, at_ea=False):
    """Natural modes. kind is judged in the spar's local axes at the tip: bending (heave w),
    torsion (twist about the spar axis x half-chord), coupled (within 2x), or in-plane."""
    Mg = mass_matrix(geo, fe, ys, at_ea=at_ea)
    f = fe.free
    w2, phi = eigh(fe.K[np.ix_(f, f)], Mg[np.ix_(f, f)] + 1e-12 * np.eye(len(f)))
    ax = np.array([math.sin(geo.lam), math.cos(geo.lam), 0.0])
    out = []
    for i in range(nmodes):
        v = np.zeros(6 * fe.n); v[f] = phi[:, i]
        rot = np.c_[v[3::6], v[4::6], v[5::6]]
        w = np.abs(v[2::6]).max(); t = np.abs(rot @ ax).max() * geo.c / 2
        ip = np.hypot(v[0::6], v[1::6]).max()
        if ip > max(w, t):
            kind = "in-plane"
        elif w > 2 * t:
            kind = "bending"
        elif t > 2 * w:
            kind = "torsion"
        else:
            kind = "coupled"
        out.append(dict(f_hz=math.sqrt(max(w2[i], 0)) / (2 * math.pi), kind=kind, shape=v))
    return out
