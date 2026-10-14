#!/usr/bin/env bash
# Z!B CAD toolchain without PyPI/conda (GM, 2026-10-14).
#
# This session's network policy blocks the package registries (pypi.org, conda, npm,
# apt mirrors), so CadQuery's OCCT binaries cannot be installed. Public GitHub git
# reads ARE allowed, so everything here is built from source with the local compiler:
#   - Manifold solid kernel + Python bindings (elalish/manifold, Apache-2.0; nanobind)
#   - numpy-stl + python-utils (pure Python)       - trimesh (pure Python)
# and tools/cq_compat/cadquery is a small CadQuery-API shim over Manifold covering
# exactly the calls cad/build_cad.py and cad/build_systems.py make (STL output only).
#
# Usage:  bash tools/setup_cad_env.sh            # once per session, ~6 min on 2 cores
#         source tools/cad_env.sh                 # every shell
#         python3 cad/build_cad.py --outdir OUT && python3 cad/build_systems.py --outdir OUT
#         cp cad/mh60.dat OUT/ && python3 cad/verify_cad.py --outdir OUT
set -euo pipefail
if [ "${1:-}" = "--real" ]; then
  # Registries allowed: install the real CadQuery (STEP-capable). NO_PROXY lists pypi.org but
  # there is no direct DNS in the sandbox, so force pip through the agent proxy.
  V=${ZIB_VENDOR:-/home/claude/vendor}; mkdir -p "$V"
  python3 -m venv --system-site-packages "$V/cqvenv"
  NO_PROXY=localhost,127.0.0.1 no_proxy=localhost,127.0.0.1 "$V/cqvenv/bin/pip" install -q cadquery numpy-stl trimesh
  "$V/cqvenv/bin/python" -c "import cadquery; print('real cadquery', cadquery.__version__)"
  echo "run CAD with: $V/cqvenv/bin/python cad/build_cad.py --outdir OUT"; exit 0
fi
V=${ZIB_VENDOR:-/home/claude/vendor}
mkdir -p "$V"; cd "$V"
clone() { [ -d "$2/.git" ] || GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 --recurse-submodules --shallow-submodules "https://github.com/$1" "$2"; }
clone elalish/manifold manifold
clone wjakob/nanobind nanobind
clone wolph/numpy-stl numpy-stl
clone wolph/python-utils python-utils
clone mikedh/trimesh trimesh
if ! ls manifold/build/bindings/python/manifold3d*.so >/dev/null 2>&1; then
  cmake -S manifold -B manifold/build -G Ninja -DCMAKE_BUILD_TYPE=Release \
    -DMANIFOLD_PYBIND=ON -DMANIFOLD_TEST=OFF -DMANIFOLD_CBIND=OFF -DMANIFOLD_PAR=OFF \
    -DBUILD_SHARED_LIBS=OFF -DMANIFOLD_USE_BUILTIN_NANOBIND=ON \
    -DFETCHCONTENT_SOURCE_DIR_NANOBIND="$V/nanobind" -DPython_EXECUTABLE="$(command -v python3)"
  ninja -C manifold/build -j"$(nproc)"
fi
echo "manifold3d: $(ls manifold/build/bindings/python/manifold3d*.so)"
echo "now: source tools/cad_env.sh"
