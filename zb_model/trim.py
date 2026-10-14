"""Trim model — tailless longitudinal trim and trim drag.

Required moment at the wing AC: Cm_ac = CL * SM (SM as a fraction).
Trim budget: airfoil Cm0 + washout credit + elevon deflection.
Trim drag: dCD ~= 1.3e-4 * delta_elevon^2 (25%-chord, ~65%-span elevons).

All coefficients are Z!B thin-airfoil/lifting-line estimates (traceability
row B4a); higher-fidelity cross-checks are flightlab trim and AeroSandbox
deflected-surface data. A2 loop result at SM 6%: delta_e = -3.55 deg.
"""

# MH60 section moment (XFoil Ncrit 9, Re 100k — program record AIRFOIL_TRADE.md)
CM0_AIRFOIL = -0.022  # Cm @ CL ~= 0.5 (-0.037 @ CL 0)

# Z!B-ESTIMATED: washout credit, lifting-line estimate for our planform
# (+0.0075 wing Cm0 per degree washout; 2 deg ~= +0.015).
# CALIBRATION NOTE: the A2 VLM loop realized Cm0_wing = -0.0062 at 6° washout
# (ITERATION_LOG.md Cycle 4), i.e. an effective credit of only ~+0.0026/deg
# from the -0.022 airfoil Cm0 — roughly 3x below this hand estimate. The
# loop's trim (delta_e = -3.55°) is consistent with its own Cm0_wing and the
# -0.008/deg elevon below. Keep the estimate until VLM/flight data pins it;
# do not silently retune to match the loop.
WASHOUT_CREDIT_PER_DEG = 0.0075
WASHOUT_DEG = 6.0  # A2 winner

# Z!B-ESTIMATED: elevon effectiveness, thin-airfoil estimate.
ELEVON_DEFF_PER_DEG = -0.008  # dCm per degree elevon (trailing-edge-down +)

# Z!B-ESTIMATED: trim-drag coefficient for our elevon geometry.
TRIM_DRAG_K = 1.3e-4  # dCD = K * delta_deg^2


def wing_cm0() -> float:
    """Wing zero-lift moment: airfoil Cm0 + washout credit."""
    return CM0_AIRFOIL + WASHOUT_CREDIT_PER_DEG * WASHOUT_DEG


def elevon_for_trim(cl: float, static_margin: float) -> float:
    """Elevon deflection (deg, TED positive) to trim Cm_ac = CL * SM.

    NOTE: with the +0.0075/deg hand estimate this returns ~+0.1° at
    CL 0.37 / SM 6%. The A2 VLM loop (Cm0_wing = -0.0062) trims at
    delta_e = -3.55° (up-elevon). See the WASHOUT_CREDIT_PER_DEG
    calibration note above — the loop value is the higher-fidelity one.
    """
    cm_required = cl * static_margin
    cm_from_wing = wing_cm0()
    return (cm_required - cm_from_wing) / ELEVON_DEFF_PER_DEG


def trim_drag_cd(elevon_deg: float) -> float:
    """Trim-drag increment dCD = 1.3e-4 * delta^2."""
    return TRIM_DRAG_K * elevon_deg**2
