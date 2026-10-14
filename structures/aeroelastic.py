"""Static and dynamic aeroelastics: structure (beam FE) coupled to the twin's VLM.

1. Static coupled trim: loaded twist feeds back into the VLM; re-trimmed for lift AND pitch
   (alpha, elevon), so the effect on washout, trim elevon and induced drag is explicit.
2. Elevon roll effectiveness vs speed (reversal check), antisymmetric deflection.
3. Flutter screen: Theodorsen typical section (k-method) at 75% semispan, using the FE
   first bending and first torsion frequencies. Screening only (strip theory, swept by cos).
"""
import os, sys, math
import numpy as np
from scipy.special import hankel2

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "twin"))
from structures import model as SM  # noqa: E402
import perf  # noqa: E402

TWIN = perf.Twin()
XCG = perf.A("x_cg_mm") / 1000


class FlexWingAS(SM.FlexWing):
    """Twist perturbation, symmetric (sign=+1) or antisymmetric (right +, left -)."""

    def __init__(self, design, dtheta=None, anti=False, **kw):
        super().__init__(design, dtheta=dtheta, **kw); self.anti = anti

    def twist(self, y):
        base = SM.vlm.Wing.twist(self, y)
        if self.dtheta is None:
            return base
        s = (1 if y >= 0 else -1) if self.anti else 1
        return base - s * self.dtheta(abs(y))


def trim2(wing, CL_req):
    """Solve alpha, elevon for CL = CL_req and Cm about the CG = 0 (linear VLM)."""
    c = wing.cref
    def f(a, d):
        s = wing.solve(a, elevon_deg=d); return np.array([s["CL"], s["Cm"] + s["CL"] * XCG / c + TWIN.dCm_visc]), s
    f0, s0 = f(0, 0); fa, _ = f(1, 0); fd, _ = f(0, 1)
    J = np.c_[fa - f0, fd - f0]
    a, d = np.linalg.solve(J, np.array([CL_req, 0.0]) - f0)
    _, s = f(a, d)
    return a, d, s


def coupled_trim(geo, V, n, iters=7, relax=0.7, **seckw):
    fe, ys, sec = SM.build(geo, **seckw)
    W = SM.MASS["total_g"] / 1000 * SM.G0; q = 0.5 * SM.RHO * V**2
    CL = n * W / (q * geo.wing.S)
    d = np.zeros_like(ys); hist = []
    rigid = None
    for it in range(iters + 1):
        dfun = (lambda yy, dd=d.copy(): float(np.interp(yy, ys, dd))) if it else None
        wing = SM.FlexWing(geo.design, dtheta=dfun)
        a, de, s = trim2(wing, CL)
        if rigid is None:
            rigid = dict(alpha=a, elevon=de, CDi=s["CDi"])
        F, info = SM.nodal_loads(geo, fe, ys, V, n, elevon_deg=de, wing=wing, alpha=a)
        u = fe.solve(F)
        dn = SM.streamwise_twist(fe, u)
        hist.append(math.degrees(dn[-1]))
        d = relax * dn + (1 - relax) * d
        if it > 1 and abs(hist[-1] - hist[-2]) < 0.01:
            break
    return dict(V=V, n=n, tip_twist_deg=math.degrees(d[-1]), mid_twist_deg=math.degrees(np.interp(0.225, ys, d)),
                alpha=a, elevon=de, CDi=s["CDi"], rigid=rigid, iterations=len(hist), history=hist,
                diverging=bool(len(hist) > 2 and abs(hist[-1]) > abs(hist[-2]) * 1.5 and abs(hist[-1]) > 5))


def roll_effectiveness(geo, V, da=2.0, **seckw):
    fe, ys, sec = SM.build(geo, **seckw)
    W = SM.MASS["total_g"] / 1000 * SM.G0; q = 0.5 * SM.RHO * V**2
    CL = W / (q * geo.wing.S)
    base = SM.vlm.Wing(geo.design)
    a, de, _ = trim2(base, CL)
    Cl_rigid = base.solve(a, elevon_deg=de, aileron_deg=da)["Cl"]
    d = np.zeros_like(ys)
    for it in range(8):
        wing = FlexWingAS(geo.design, dtheta=(lambda yy, dd=d.copy(): float(np.interp(yy, ys, dd))), anti=True) if it else base
        y, dy, L1, x1 = SM.strip_loads(wing, a, de, da)
        y, dy, L0, x0 = SM.strip_loads(wing, a, de, 0.0)
        F = np.zeros(6 * fe.n)
        for i in range(len(y)):
            if y[i] <= 0:
                continue
            k = int(np.argmin(np.abs(ys - y[i]))); node = fe.X[k]
            for Lr, x in ((L1[i] * SM.RHO * V**2, x1[i]), (-L0[i] * SM.RHO * V**2, x0[i])):
                Fv = np.array([0, 0, Lr]); r = np.array([x, y[i], 0]) - node
                F[6 * k:6 * k + 3] += Fv; F[6 * k + 3:6 * k + 6] += np.cross(r, Fv)
        u = fe.solve(F); dn = SM.streamwise_twist(fe, u)
        d = 0.7 * dn + 0.3 * d
    wing = FlexWingAS(geo.design, dtheta=(lambda yy, dd=d.copy(): float(np.interp(yy, ys, dd))), anti=True)
    Cl_flex = wing.solve(a, elevon_deg=de, aileron_deg=da)["Cl"]
    return dict(V=V, eff=Cl_flex / Cl_rigid, Cl_rigid=Cl_rigid, Cl_flex=Cl_flex)


# ------------------------------------------------------------------ flutter
def theodorsen_C(k):
    H1, H0 = hankel2(1, k), hankel2(0, k)
    return H1 / (H1 + 1j * H0)


def flutter_typical_section(mu, a, x_a, r2, sigma, k_grid=None, g_s=0.0):
    """k-method; returns U_F/(b*omega_alpha) or None. Hodges & Pierce sign convention."""
    k_grid = np.geomspace(3.0, 0.02, 600) if k_grid is None else k_grid
    prev = None; res = []
    for k in k_grid:
        C = theodorsen_C(k)
        Lh = 1 - 2j * C / k
        La = 0.5 - 1j * (1 + 2 * C) / k - 2 * C / k**2
        Mh = 0.5
        Ma = 3 / 8 - 1j / k
        A11 = mu + Lh
        A12 = mu * x_a + La - (0.5 + a) * Lh
        A21 = mu * x_a + Mh - (0.5 + a) * Lh
        A22 = mu * r2 + Ma - (0.5 + a) * (La + Mh) + (0.5 + a)**2 * Lh
        # det(A - Z*B) with B = diag(mu sigma^2, mu r2)
        a2 = mu**2 * sigma**2 * r2
        a1 = -(mu * sigma**2 * A22 + mu * r2 * A11)
        a0 = A11 * A22 - A12 * A21
        Z = np.roots([a2, a1, a0])
        pts = []
        for z in Z:
            if z.real <= 0:
                continue
            w_ratio = 1 / math.sqrt(z.real)   # omega/omega_alpha
            g = z.imag / z.real
            U = w_ratio / k                    # U / (b omega_alpha)
            pts.append((U, g))
        res.append(pts)
    # find lowest U where any branch g crosses g_s (from below)
    best = None
    for i in range(1, len(res)):
        for (U0, g0), (U1, g1) in zip(sorted(res[i - 1]), sorted(res[i])):
            if (g0 - g_s) * (g1 - g_s) < 0:
                Uc = U0 + (U1 - U0) * (g_s - g0) / (g1 - g0)
                best = Uc if best is None else min(best, Uc)
    return best


def flutter_screen(geo, **seckw):
    fe, ys, sec = SM.build(geo, **seckw)
    md = SM.modes(geo, fe, ys, nmodes=8, at_ea=True)          # uncoupled, for the typical section
    coupled = SM.modes(geo, fe, ys, nmodes=6)                  # as-built mass offsets (reported)
    fb = next(m["f_hz"] for m in md if m["kind"] == "bending")
    ft = next((m["f_hz"] for m in md if m["kind"] == "torsion"), None)
    c = geo.c; b = c / 2
    # section mass per unit span at 75% semispan (wing-borne mass / span) and its distribution
    m_len = (SM.MASS["skins_g"] + SM.MASS["spar_g"] + SM.MASS["misc_wing_g"] + SM.MASS["ribs_g"]) / 1000 / geo.b
    x_ea = geo.u_spar; x_cg = 0.40
    a = (x_ea - 0.5) / 0.5; x_a = (x_cg - x_ea) / 0.5
    r2 = ((0.25 * c)**2 + ((x_cg - x_ea) * c)**2) / b**2
    mu = m_len / (math.pi * SM.RHO * b**2)
    if ft is None:
        return dict(f_bend=fb, f_tors=None, note="no torsion mode found in the first 8")
    # typical-section static divergence (unswept, conservative: ignores sweep-back bending washout)
    UD_nd = math.sqrt(mu * r2 / (2 * (0.5 + a))) if a > -0.5 else None
    sigma = fb / ft
    Uf = flutter_typical_section(mu, a, x_a, r2, sigma)
    w_a = 2 * math.pi * ft
    V_n = Uf * b * w_a if Uf else None
    VD_n = UD_nd * b * 2 * math.pi * ft if UD_nd else None
    return dict(f_bend=fb, f_tors=ft, V_div_typical_unswept=VD_n, mu=mu, a=a, x_a=x_a, r2=r2, sigma=sigma, U_nd=Uf,
                V_flutter_normal=V_n, V_flutter=(V_n / math.cos(geo.lam)) if V_n else None,
                modes=[(round(m["f_hz"], 2), m["kind"]) for m in md],
                coupled_modes=[(round(m["f_hz"], 2), m["kind"]) for m in coupled])


if __name__ == "__main__":
    # verification: Hodges & Pierce typical section (mu=20, a=-1/5, x_a=1/10, r2=6/25, sigma=2/5) -> U_F ~ 2.17
    print("verification U_F/(b w_a) =", flutter_typical_section(20, -0.2, 0.1, 6 / 25, 0.4))
