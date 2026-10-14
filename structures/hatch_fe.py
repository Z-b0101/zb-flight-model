"""Plane-stress FE (constant-strain triangles) of the bottom skin around the battery hatch.

The bottom skin is flattened into its plane: x chordwise (LE -> hinge), y spanwise.
Wing bending puts it in spanwise tension (positive g). The hatch H1 aperture sits at
the root, where that tension peaks. We compute the stress concentration factor Kt
(peak spanwise stress / far-field stress) for:
  - the aperture as drawn (Depron only, corner radius r),
  - the aperture with a bonded printed PLA frame (doubler) of width w and thickness tf.
"""
import math
import numpy as np
from scipy.spatial import Delaunay
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve


def rounded_rect_inside(x, y, x0, x1, y0, y1, r):
    cx = np.clip(x, x0 + r, x1 - r); cy = np.clip(y, y0 + r, y1 - r)
    return (x > x0) & (x < x1) & (y > y0) & (y < y1) & ((x - cx)**2 + (y - cy)**2 < r**2 - 1e-12)


def boundary_points(x0, x1, y0, y1, r, h):
    pts = []
    def line(p, q):
        L = math.dist(p, q); n = max(int(L / h), 1)
        for t in np.linspace(0, 1, n, endpoint=False): pts.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    def arc(c, a0, a1):
        n = max(int(r * abs(a1 - a0) / h), 3)
        for a in np.linspace(a0, a1, n, endpoint=False): pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
    line((x0 + r, y0), (x1 - r, y0)); arc((x1 - r, y0 + r), -math.pi / 2, 0)
    line((x1, y0 + r), (x1, y1 - r)); arc((x1 - r, y1 - r), 0, math.pi / 2)
    line((x1 - r, y1), (x0 + r, y1)); arc((x0 + r, y1 - r), math.pi / 2, math.pi)
    line((x0, y1 - r), (x0, y0 + r)); arc((x0 + r, y0 + r), math.pi, 1.5 * math.pi)
    return np.array(pts)


def solve(W=150.0, Hs=300.0, hole=(24.0, 58.0, -36.0, 36.0), r=4.0, h=1.5, E=12.0, nu=0.3,
          frame_w=0.0, frame_E_ratio=0.0, sigma0=1.0):
    """Units: mm, MPa. Returns Kt and the mesh size used. frame_E_ratio = (E_pla*t_frame)/(E_foam*t_skin)."""
    x0, x1, y0, y1 = hole
    # background grid (includes the domain edges exactly) + refined band around the hole
    def grid(xa, xb, ya, yb, hh):
        nx = max(int(round((xb - xa) / hh)), 1) + 1; ny = max(int(round((yb - ya) / hh)), 1) + 1
        X, Y = np.meshgrid(np.linspace(xa, xb, nx), np.linspace(ya, yb, ny)); return np.c_[X.ravel(), Y.ravel()]
    hb = 4.0
    pad = 15.0
    G1 = grid(0, W, -Hs / 2, Hs / 2, hb)
    G1 = G1[~((G1[:, 0] > x0 - pad) & (G1[:, 0] < x1 + pad) & (G1[:, 1] > y0 - pad) & (G1[:, 1] < y1 + pad))]
    xa, xb = max(0.0, x0 - pad), min(W, x1 + pad)
    G2 = grid(xa, xb, y0 - pad, y1 + pad, h)
    # keep only refined points inside the band (avoid clustering against the coarse grid)
    P = np.vstack([G1, G2])
    cx = np.clip(P[:, 0], x0 + r, x1 - r); cy = np.clip(P[:, 1], y0 + r, y1 - r)
    dhole = np.hypot(P[:, 0] - cx, P[:, 1] - cy) - r
    inside = rounded_rect_inside(P[:, 0], P[:, 1], x0, x1, y0, y1, r)
    P = P[(~inside) & (dhole > 0.5 * h)]
    P = np.vstack([P, boundary_points(x0, x1, y0, y1, r, h)])
    P = np.unique(np.round(P, 6), axis=0)
    tri = Delaunay(P).simplices
    cen = P[tri].mean(1)
    tri = tri[~rounded_rect_inside(cen[:, 0], cen[:, 1], x0, x1, y0, y1, r)]
    d1 = P[tri[:, 1]] - P[tri[:, 0]]; d2 = P[tri[:, 2]] - P[tri[:, 0]]
    area = 0.5 * np.abs(d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0])
    tri = tri[area > 1e-6]
    used = np.unique(tri); remap = -np.ones(len(P), int); remap[used] = np.arange(len(used))
    P = P[used]; tri = remap[tri]
    n = len(P); K = lil_matrix((2 * n, 2 * n))
    D0 = 1 / (1 - nu**2) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])
    Bs, Ds = [], []
    cen = P[tri].mean(1)
    # distance from hole edge (for the frame band)
    cx = np.clip(cen[:, 0], x0 + r, x1 - r); cy = np.clip(cen[:, 1], y0 + r, y1 - r)
    dist = np.hypot(cen[:, 0] - cx, cen[:, 1] - cy) - r
    for e, t3 in enumerate(tri):
        (xa, ya), (xb, yb), (xc, yc) = P[t3]
        A2 = (xb - xa) * (yc - ya) - (xc - xa) * (yb - ya)
        b_ = np.array([yb - yc, yc - ya, ya - yb]); c_ = np.array([xc - xb, xa - xc, xb - xa])
        B = np.zeros((3, 6)); B[0, 0::2] = b_; B[1, 1::2] = c_; B[2, 0::2] = c_; B[2, 1::2] = b_; B /= A2
        Ee = E * (1 + (frame_E_ratio if (frame_w > 0 and dist[e] < frame_w) else 0.0))
        D = Ee * D0
        ke = abs(A2) / 2 * B.T @ D @ B
        idx = np.r_[2 * t3[0], 2 * t3[0] + 1, 2 * t3[1], 2 * t3[1] + 1, 2 * t3[2], 2 * t3[2] + 1]
        for i in range(6):
            for j in range(6):
                K[idx[i], idx[j]] += ke[i, j]
        Bs.append(B); Ds.append(D)
    # loads: uniform tension sigma0 on y = +/- Hs/2 edges (unit thickness)
    F = np.zeros(2 * n)
    for s in (1, -1):
        edge = np.where(np.abs(P[:, 1] - s * Hs / 2) < 1e-6)[0]
        edge = edge[np.argsort(P[edge, 0])]
        for i, j in zip(edge[:-1], edge[1:]):
            L = P[j, 0] - P[i, 0]
            F[2 * i + 1] += s * sigma0 * L / 2; F[2 * j + 1] += s * sigma0 * L / 2
    # constraints: rigid-body only (one point fixed, one roller)
    fixed = set()
    i0 = int(np.argmin(np.hypot(P[:, 0] - 0, P[:, 1] - 0) + 1e3 * (P[:, 0] > 1e-6)))
    i1 = int(np.argmin(np.hypot(P[:, 0] - W, P[:, 1] - 0) + 1e3 * (P[:, 0] < W - 1e-6)))
    fixed |= {2 * i0, 2 * i0 + 1, 2 * i1 + 1}
    free = np.array(sorted(set(range(2 * n)) - fixed))
    Kc = K.tocsr()[free][:, free]
    u = np.zeros(2 * n); u[free] = spsolve(Kc.tocsc(), F[free])
    syy = np.empty(len(tri))
    for e, t3 in enumerate(tri):
        idx = np.r_[2 * t3[0], 2 * t3[0] + 1, 2 * t3[1], 2 * t3[1] + 1, 2 * t3[2], 2 * t3[2] + 1]
        s = Ds[e] @ Bs[e] @ u[idx]; syy[e] = s[1]
    foam = ~((frame_w > 0) & (dist < frame_w))
    Kt_foam = syy[foam].max() / sigma0
    # frame stress (per unit skin thickness basis) -> PLA stress
    Kt_frame = syy[~foam].max() / sigma0 if (~foam).any() else 0.0
    return dict(Kt=Kt_foam, Kt_frame_resultant=Kt_frame, n_nodes=n, n_el=len(tri), h=h, r=r)


if __name__ == "__main__":
    for h in (2.0, 1.2, 0.8):
        print("as drawn r=4", solve(h=h))
    print("as drawn r=8", solve(h=1.0, r=8.0))
    print("frame 6 mm x 1.2 mm PLA", solve(h=1.0, frame_w=6.0, frame_E_ratio=3000.0 * 1.2 / (12.0 * 3.0)))
