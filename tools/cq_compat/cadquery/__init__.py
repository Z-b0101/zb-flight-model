"""Minimal CadQuery-compatible shim on the Manifold solid kernel (Z!B CAD fallback).

Why: the session's package proxy blocks PyPI/conda, so real CadQuery (OCCT/OCP binaries)
cannot be installed. Manifold (github.com/elalish/manifold, Apache-2.0) builds from git
source with only a C++ compiler, and gives exact-topology mesh booleans.

Scope: ONLY the CadQuery API that cad/build_cad.py and cad/build_systems.py use:
  Vector, Workplane("XY").polyline(pts).close().extrude(h), .cut(),
  Solid.makeBox(dx, dy, dz, pnt), Solid.makeCylinder(r, h, pnt, dir), .fuse(*), .rotate(c, axis, deg),
  exporters.export(shape, "*.stl").
Output is STL (what the printer and the repo's numpy-stl checks consume). No STEP/B-rep:
if a supplier needs STEP, run the real CadQuery build where PyPI is reachable.
Tessellation: circles get n = max(24, ceil(pi / acos(1 - TOL/r))) segments with TOL = 0.02 mm
chord error (CadQuery's STL default tolerance is 0.1 mm), so this shim is at least as fine.
"""
import math
import numpy as np
import manifold3d as _m

TOL = 0.02
__version__ = "0.1-zib-manifold-shim"


def _nseg(r):
    if r <= TOL:
        return 24
    return max(24, int(math.ceil(math.pi / math.acos(max(-1.0, 1 - TOL / r)))))


class Vector:
    def __init__(self, *a):
        if len(a) == 1:
            a = tuple(a[0])
        self.x, self.y, self.z = (float(v) for v in (tuple(a) + (0.0, 0.0, 0.0))[:3])

    def toTuple(self): return (self.x, self.y, self.z)
    def __iter__(self): return iter(self.toTuple())
    def __repr__(self): return f"Vector{self.toTuple()}"


def _rot_to(d):
    """3x3 rotation taking +z onto unit vector d."""
    d = np.asarray(d, float); d = d / np.linalg.norm(d)
    z = np.array([0.0, 0.0, 1.0])
    v = np.cross(z, d); c = float(np.dot(z, d))
    if np.linalg.norm(v) < 1e-12:
        return np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * (1 / (1 + c))


def _axis_angle(axis, deg):
    k = np.asarray(axis, float); k = k / np.linalg.norm(k)
    a = math.radians(deg)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + math.sin(a) * K + (1 - math.cos(a)) * K @ K


def _affine(M, t):
    A = np.zeros((3, 4)); A[:, :3] = M; A[:, 3] = t
    return A


class Shape:
    """Wraps a manifold3d.Manifold; mimics cq.Solid / cq.Workplane result objects."""
    def __init__(self, man):
        self.m = man

    def _wrap(self, man): return type(self)(man)
    def cut(self, other): return self._wrap(self.m - _man(other))
    def fuse(self, *others):
        out = self.m
        for o in others:
            out = out + _man(o)
        return self._wrap(out)
    union = fuse
    def intersect(self, other): return self._wrap(self.m ^ _man(other))

    def rotate(self, center, axis, deg):
        c = np.array(tuple(center)); R = _axis_angle(tuple(axis), deg)
        return self._wrap(self.m.transform(_affine(R, c - R @ c)))

    def translate(self, v): return self._wrap(self.m.translate(tuple(v)))
    def val(self): return self
    def Volume(self): return self.m.volume()

    def triangles(self):
        mesh = self.m.to_mesh()
        V = np.asarray(mesh.vert_properties)[:, :3]
        T = np.asarray(mesh.tri_verts)
        return V[T]


def _man(s):
    if isinstance(s, Shape):
        return s.m
    raise TypeError(f"not a shim shape: {type(s)}")


class Solid(Shape):
    @staticmethod
    def makeBox(dx, dy, dz, pnt=Vector(0, 0, 0), dir=Vector(0, 0, 1)):
        if tuple(dir) != (0.0, 0.0, 1.0):
            raise NotImplementedError("makeBox: only dir=+z is used in the Z!B scripts")
        return Solid(_m.Manifold.cube((dx, dy, dz)).translate(tuple(pnt)))

    @staticmethod
    def makeCylinder(radius, height, pnt=Vector(0, 0, 0), dir=Vector(0, 0, 1)):
        cyl = _m.Manifold.cylinder(height, radius, radius, _nseg(radius))
        return Solid(cyl.transform(_affine(_rot_to(tuple(dir)), np.array(tuple(pnt)))))


class Workplane(Shape):
    def __init__(self, plane="XY", man=None):
        if isinstance(plane, _m.Manifold):          # internal re-wrap
            man, plane = plane, "XY"
        if plane != "XY":
            raise NotImplementedError("Workplane: only 'XY' is used in the Z!B scripts")
        super().__init__(man)
        self._pts = None

    def _wrap(self, man): return Workplane("XY", man)

    def polyline(self, pts):
        self._pts = [tuple(map(float, p[:2])) for p in pts]
        return self

    def close(self):
        p = self._pts
        if p and np.allclose(p[0], p[-1]):
            self._pts = p[:-1]
        return self

    def extrude(self, h):
        pts = self._pts
        area = 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]))
        if area < 0:
            pts = pts[::-1]                         # Manifold wants CCW outer contours
        cs = _m.CrossSection([pts])
        return Workplane("XY", _m.Manifold.extrude(cs, float(h)))


class exporters:
    @staticmethod
    def export(shape, path, *a, **k):
        if not str(path).lower().endswith(".stl"):
            raise NotImplementedError("shim exports STL only (no B-rep/STEP); see module docstring")
        tris = shape.triangles()
        n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        ln = np.linalg.norm(n, axis=1, keepdims=True); n = np.divide(n, ln, out=np.zeros_like(n), where=ln > 0)
        rec = np.zeros(len(tris), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
        rec["n"] = n; rec["v"] = tris
        with open(path, "wb") as f:
            f.write(b"Z!B manifold shim".ljust(80, b" "))
            f.write(np.uint32(len(tris)).tobytes()); f.write(rec.tobytes())
