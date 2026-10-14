"""Z!B twin — vortex-lattice aero, generated from the controlled cad/params.json.

Geometry, sweep, washout (linear, about the spar axis), MH60 camber and the elevon
hinge/span all come from params.json via cad/parametric.py. Nothing about the
planform is hard-coded here.

Frame: x aft from ROOT LEADING EDGE (mm -> m internally), y right, z up.
Method: horseshoe vortex lattice, cosine spanwise spacing, uniform chordwise
panels, camber + twist + elevon deflection applied through panel normals
(small-angle, flat wake). Standard Katz & Plotkin formulation.
Outputs are inviscid: CL, Cm about root LE, induced drag (Trefftz), neutral point.
"""
import math, os, sys, json, hashlib
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "cad"))
import parametric as pm  # noqa: E402


def load(path=None):
    path = path or os.path.join(REPO, "cad", "params.json")
    raw = json.load(open(path))
    design = raw["design"]
    h = hashlib.sha256(json.dumps(design, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:12]
    return raw, design, h


class Wing:
    def __init__(self, design, ns=40, nc=10):
        self.P = design
        self.W = pm.WingParam(design, dat_dir=os.path.join(REPO, "cad"))
        self.ns, self.nc = ns, nc
        b = design["span"] / 1000.0
        self.b = b
        # cosine spanwise spacing
        th = np.linspace(0, math.pi, 2 * ns + 1)
        self.yb = -0.5 * b * np.cos(th)          # strip edges (m)
        self.S = sum((self.yb[i + 1] - self.yb[i]) * self.chord(0.5 * (self.yb[i] + self.yb[i + 1]))
                     for i in range(2 * ns))
        self.AR = b * b / self.S
        self.cref = design["chord"] / 1000.0

    def chord(self, y): return self.W.chord_at(y * 1000) / 1000.0
    def xle(self, y):   return (self.W.xle_at(y * 1000) + 0.25 * self.P["chord"]) / 1000.0  # aft root LE
    def twist(self, y): return self.W.twist_at(y * 1000)   # rad, + nose-down
    def camber_slope(self, uf):
        h = 1e-3
        return (self.W.af.mid(min(uf + h, 1)) - self.W.af.mid(max(uf - h, 0))) / (min(uf + h, 1) - max(uf - h, 0))

    def _panels(self, elevon_deg=0.0, aileron_deg=0.0):
        P = self.P; nc = self.nc
        A, B, C, N = [], [], [], []
        hinge = P["hinge_x_frac"]; ey0, ey1 = P["elevon_y0"] / 1000, P["elevon_y1"] / 1000
        for i in range(2 * self.ns):
            ya, yb = self.yb[i], self.yb[i + 1]; ym = 0.5 * (ya + yb)
            for k in range(nc):
                u0, u1 = k / nc, (k + 1) / nc
                def pt(y, u): return np.array([self.xle(y) + u * self.chord(y), y, 0.0])
                A.append(pt(ya, u0 + 0.25 / nc)); B.append(pt(yb, u0 + 0.25 / nc))
                C.append(pt(ym, u0 + 0.75 / nc))
                uc = u0 + 0.75 / nc
                # surface slope dz/dx; effective angle is alpha - slope. Washout (twist + = nose-DOWN)
                # raises the trailing edge, i.e. ADDS to dz/dx. (Fixed 2026-10-14: this was "- tan",
                # which modelled the 6 deg washout as 6 deg wash-in; found by the structures work.)
                slope = self.camber_slope(uc) + math.tan(self.twist(ym))
                if uc > hinge and ey0 <= abs(ym) <= ey1:
                    # + elevon = trailing edge DOWN; aileron + = right TE up / left TE down
                    d = elevon_deg + (aileron_deg if ym < 0 else -aileron_deg)
                    slope -= math.tan(math.radians(d))
                n = np.array([-slope, 0.0, 1.0]); N.append(n / np.linalg.norm(n))
        return np.array(A), np.array(B), np.array(C), np.array(N)

    @staticmethod
    def _seg(P, A, B):
        """Induced velocity at points P from unit-strength segments A->B (vectorised)."""
        r1 = P[:, None, :] - A[None, :, :]; r2 = P[:, None, :] - B[None, :, :]
        cr = np.cross(r1, r2); cr2 = np.sum(cr * cr, -1)
        n1 = np.linalg.norm(r1, axis=-1); n2 = np.linalg.norm(r2, axis=-1)
        r0 = B - A
        dot = np.sum(r0[None] * (r1 / n1[..., None] - r2 / n2[..., None]), -1)
        cr2 = np.where(cr2 < 1e-12, np.inf, cr2)
        return cr / (4 * math.pi) * (dot / cr2)[..., None]

    def _hs(self, P, A, B, far=50.0):
        Af = A + np.array([far, 0, 0]); Bf = B + np.array([far, 0, 0])
        return self._seg(P, Af, A) + self._seg(P, A, B) + self._seg(P, B, Bf)

    def solve(self, alpha_deg, elevon_deg=0.0, aileron_deg=0.0, xref=None):
        A, B, C, N = self._panels(elevon_deg, aileron_deg)
        a = math.radians(alpha_deg); V = np.array([math.cos(a), 0.0, math.sin(a)])
        AIC = np.einsum("ijk,ik->ij", self._hs(C, A, B), N)
        G = np.linalg.solve(AIC, -N @ V)
        # bound-vortex forces (Kutta-Joukowski, unit rho and V)
        mid = 0.5 * (A + B); dl = B - A
        v_ind = np.einsum("ijk,j->ik", self._hs(mid, A, B), G)
        # exclude self-induced bound singularity handled by cr2 guard
        F = np.cross(V[None] + v_ind, dl) * G[:, None]
        lift_dir = np.array([-math.sin(a), 0, math.cos(a)]); drag_dir = V
        L = F @ lift_dir; D = F @ drag_dir
        q = 0.5  # unit rho, unit V
        CL = L.sum() / (q * self.S); CDi = D.sum() / (q * self.S)
        xref = 0.0 if xref is None else xref
        My = np.sum((mid[:, 0] - xref) * -F[:, 2] + mid[:, 2] * F[:, 0])  # nose-up +
        Cm = My / (q * self.S * self.cref)
        Mx = np.sum(mid[:, 1] * F[:, 2])  # right-wing-down negative
        Cl_roll = -Mx / (q * self.S * self.b)
        return dict(CL=CL, CDi=CDi, Cm=Cm, Cl=Cl_roll)

    def derivatives(self):
        s0 = self.solve(0.0); s2 = self.solve(2.0)
        CLa = (s2["CL"] - s0["CL"]) / 2.0
        Cma = (s2["Cm"] - s0["Cm"]) / 2.0
        x_np = -Cma / CLa * self.cref           # aft of root LE (m)
        e0 = self.solve(0.0, elevon_deg=5.0)
        a5 = self.solve(0.0, aileron_deg=5.0)
        CL0 = s0["CL"]; a0L = -CL0 / CLa
        # Oswald from induced drag at a mid CL
        s4 = self.solve(4.0); e_osw = s4["CL"] ** 2 / (math.pi * self.AR * s4["CDi"])
        return dict(S=self.S, AR=self.AR, CLa_per_deg=CLa, CL0=CL0, alpha0L_deg=a0L,
                    Cm0_rootLE=s0["Cm"], x_np_mm=x_np * 1000, oswald_e=e_osw,
                    CLde_per_deg=(e0["CL"] - CL0) / 5.0, Cmde_rootLE_per_deg=(e0["Cm"] - s0["Cm"]) / 5.0,
                    Clda_per_deg=a5["Cl"] / 5.0)


if __name__ == "__main__":
    raw, design, h = load()
    w = Wing(design)
    d = w.derivatives()
    print("params design hash", h)
    for k, v in d.items(): print(f"{k:22s} {v: .5f}")
    print("controlled NP (VLM basis, meta) mm", raw["meta"]["aero_basis"]["x_np_vlm_aft_le_mm"])
