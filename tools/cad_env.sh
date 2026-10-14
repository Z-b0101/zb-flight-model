# source me: puts the from-source CAD toolchain on PYTHONPATH (see tools/setup_cad_env.sh)
_V=${ZIB_VENDOR:-/home/claude/vendor}
_R=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export PYTHONPATH="$_V/trimesh:$_V/manifold/build/bindings/python:$_V/numpy-stl:$_V/python-utils:$_R/tools/cq_compat${PYTHONPATH:+:$PYTHONPATH}"
unset _V _R
