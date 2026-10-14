# CAD toolchain workaround (no PyPI): validation record

| | |
|---|---|
| Owner | Claude (GM/DE), 2026-10-14 |
| Problem | `cadquery` (OCCT/OCP binaries) cannot be installed in agent sessions. pypi.org, files.pythonhosted.org, conda, npm and the Ubuntu mirrors are all refused by the session egress policy (proxy `connect_rejected`). Only public-GitHub git reads are allowed. |
| Workaround | Build an exact-boolean solid kernel from git source (Manifold), add the pure-Python deps from git, and put a small **CadQuery-API shim** (`tools/cq_compat/cadquery`) in front of it. The repo CAD scripts run **unchanged**. |
| Setup | `bash tools/setup_cad_env.sh` (about 6 min on 2 cores, once per session), then `source tools/cad_env.sh` |

## What the shim covers

It covers exactly the CadQuery calls in `cad/build_cad.py` and `cad/build_systems.py`:
- `Vector`
- `Workplane("XY").polyline().close().extrude()`
- `.cut()`, `.fuse()`, `.rotate()`
- `Solid.makeBox()`, `Solid.makeCylinder()`
- `exporters.export(*.stl)`

Anything else raises `NotImplementedError` rather than guessing.

**Output is STL only.** That is enough for printing and for every repo check, which all read STL through numpy-stl. There is no STEP/B-rep. If a vendor needs STEP, run the real CadQuery build where PyPI is reachable (Oubi's environment, or this one after the network setting is changed).

Circles are tessellated at ≤ 0.02 mm chord error. CadQuery's STL default is 0.1 mm, so the shim is finer.

## Validation (2026-10-14, origin/main and ce/dr01-dr02 params)

| Check | Result |
|---|---|
| Shim unit tests: box, cylinder on any axis, plate minus hole, rotate, fuse | Volumes exact for boxes and booleans; cylinders within the polygon chord error; STL read back closed |
| `cad/build_cad.py` | Runs; 8 ribs at the record stations |
| `cad/build_systems.py` | **CG 128.5 mm, mass 209.0 g**: identical to the CAD record (cg_report / DESIGN_CLOSURE item 2). Clash check 0 CLASH / 0 TIGHT (note: the prop is still skipped, see DR-14) |
| `cad/verify_cad.py` | **All checks passed**: rib vs MH60 max deviation 0.013 mm; spar slot 4.200 mm; washout +4.500°; sweep shift 157.38 mm; hinge gap 0.506 mm; skin 3.000 mm |
| Watertightness of all 37 part STLs | 37 / 37 closed 2-manifold |

## Not covered yet

`cad/build_all.py` hard-codes `/home/hatch/...` paths and a venv interpreter, so it is run here as its two component scripts plus `verify_cad.py`. Making those paths repo-relative is an MBSE-owned change, offered as a small PR.

The real fix is still the network setting (CEO: claude.ai → Settings → Capabilities, allow package registries). With that, `pip install cadquery` restores STEP export, and this shim becomes a fallback.
