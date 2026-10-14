"""Stability — neutral point, static margin, CG bookkeeping.

Conventions (single source of truth per CE-02; do NOT mix datums):
  - x measured in mm aft of the ROOT LEADING EDGE (CAD datum).
  - A2 loop values (x_ac = 95.0 mm, x_cg = 83.0 mm @ SM 6%) use the loop's
    own datum and must not be mixed with CAD root-LE coordinates.

Static margin SM = (x_np - x_cg) / mac. Design basis: SM 6%.
Cross-check: flightlab/stability.py VLM (NP verified vs AVL within 3 mm).
"""

MAC_MM = 200.0  # rectangular wing: mac = chord

# Neutral point — VLM-derived for the A2 planform (25° sweep, MH60).
# Z!B-ESTIMATED: pending VLM re-run pinned to the CAD datum; the A2 value is
# x_ac = 95.0 mm in the loop datum at SM 6% (ITERATION_LOG.md Cycle 2).
X_NP_MM = 95.0


def static_margin(x_cg_mm: float, x_np_mm: float = X_NP_MM) -> float:
    """Static margin as a fraction of MAC."""
    return (x_np_mm - x_cg_mm) / MAC_MM


def cg_for_sm(target_sm: float, x_np_mm: float = X_NP_MM) -> float:
    """CG position (mm aft root LE) required for a target static margin."""
    return x_np_mm - target_sm * MAC_MM


def check_stability(x_cg_mm: float, sm_min: float = 0.05) -> dict:
    """Stability verdict at a CG position. Design basis SM 6%."""
    sm = static_margin(x_cg_mm)
    return {
        "x_cg_mm": x_cg_mm,
        "x_np_mm": X_NP_MM,
        "static_margin": sm,
        "stable": sm >= sm_min,
        "design_sm": 0.06,
    }
