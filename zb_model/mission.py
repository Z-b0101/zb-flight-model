"""Mission performance model — level-flight range/endurance integration.

L1 trade model: V = sqrt(2W / (rho * S * CL)), P_shaft = D * V,
P_elec = P_shaft / eta + P_hotel, endurance = E_usable / P_elec.

All numbers below come from the program record (AIRFOIL_TRADE.md,
ITERATION_LOG.md, WEIGHT_BUDGET.md). Estimated constants are marked
``# Z!B-ESTIMATED:`` and registered in zb_model/data/assumptions.yaml.

CALIBRATION NOTE (stated plainly): the A2 loop reported 32.40 km / 77.1 min
@ SM 6% using e_vlm = 1.000 (VLM-computed) and no hotel load. This L1 module
uses e = 0.78 (hand estimate) and the illustrative 1 W hotel term, and lands
near ~26 km / ~57 min. The delta is assumptions, not arithmetic — both are
L1 until flight test sets the absolutes. Do not "tune" constants to match
A2; calibrate against measured data instead.
"""

import math

from zb_model import drag, propulsion, trim

RHO_SL = 1.225  # kg/m^3, ISA sea level
G0 = 9.80665  # m/s^2

# --- Aircraft (PoC, Gate 1 + A2 locked geometry) ---
SPAN = 0.90  # m
CHORD = 0.20  # m, rectangular
WING_AREA = SPAN * CHORD  # 0.18 m^2
ASPECT_RATIO = SPAN / CHORD  # 4.5
WASHOUT_DEG = 6.0  # A2 winner, linear
SWEEP_DEG = 25.0  # A2 winner
STATIC_MARGIN = 0.06  # A2 loop basis

# --- Battery (3S 650 mAh, GNB spec) ---
PACK_VOLTAGE_NOM = 11.1  # V, 3S nominal
PACK_CAPACITY_AH = 0.65  # Ah
PACK_ENERGY_WH = PACK_VOLTAGE_NOM * PACK_CAPACITY_AH  # 7.215 Wh nominal
USABLE_FRACTION = 0.80  # Z!B-ESTIMATED: 80% usable-energy derate
E_USABLE_WH = PACK_ENERGY_WH * USABLE_FRACTION  # 5.772 Wh

# --- Hotel load ---
# Z!B-ESTIMATED: 1 W illustrative placeholder. Sensitivity analysis (G2) is the
# highest-value unbacked claim in the traceability audit; measure on the bench.
P_HOTEL_W = 1.0

# --- Cruise constraints (AIRFOIL_TRADE.md §3) ---
V_FLOOR_MS = 7.0  # m/s; 1.5*Vstall = 5.9 < 7.0, so the floor governs
VSTALL_MS = 3.95  # Z!B-ESTIMATED: from Clmax 1.16 @ 204.3 g


def level_speed_w(weight_n: float, cl: float, rho: float = RHO_SL) -> float:
    """Level-flight speed V = sqrt(2W / (rho * S * CL))."""
    return math.sqrt(2.0 * weight_n / (rho * WING_AREA * cl))


def shaft_power_w(weight_n: float, cl: float, rho: float = RHO_SL) -> float:
    """Shaft power P = D * V = 1/2 * rho * V^3 * S * CD."""
    v = level_speed_w(weight_n, cl, rho)
    cd = drag.total_cd(cl)
    return 0.5 * rho * v**3 * WING_AREA * cd


def electric_power_w(weight_n: float, cl: float, rho: float = RHO_SL) -> float:
    """Electrical power draw incl. propulsion derate and hotel load."""
    p_shaft = shaft_power_w(weight_n, cl, rho)
    eta = propulsion.prop_efficiency(p_shaft)
    return p_shaft / eta + P_HOTEL_W


def mission_point(weight_n: float, cl: float, rho: float = RHO_SL) -> dict:
    """Range/endurance at one cruise CL, with trim drag folded in.

    Returns dict with V, P_elec, endurance_min, range_km, L/D, elevon_deg.
    """
    v = max(level_speed_w(weight_n, cl, rho), V_FLOOR_MS)
    # Recompute at the floored speed: CL needed, then full CD incl. trim
    cl_eff = 2.0 * weight_n / (rho * v**2 * WING_AREA)
    elevon = trim.elevon_for_trim(cl_eff, STATIC_MARGIN)
    cd = drag.total_cd(cl_eff) + trim.trim_drag_cd(elevon)
    d = 0.5 * rho * v**2 * WING_AREA * cd
    p_elec = d * v / propulsion.prop_efficiency(d * v) + P_HOTEL_W
    endurance_h = E_USABLE_WH / p_elec
    return {
        "cl": cl_eff,
        "v_ms": v,
        "p_elec_w": p_elec,
        "endurance_min": endurance_h * 60.0,
        "range_km": endurance_h * v * 3.6,
        "ld": cl_eff / cd,
        "elevon_deg": elevon,
    }


def best_cruise(weight_n: float, rho: float = RHO_SL) -> dict:
    """Sweep CL 0.30–0.55, return the max-range cruise point."""
    best = None
    cl = 0.30
    while cl <= 0.551:
        pt = mission_point(weight_n, cl, rho)
        if best is None or pt["range_km"] > best["range_km"]:
            best = pt
        cl += 0.01
    return best


if __name__ == "__main__":
    w = 0.2043 * G0  # PoC AUW [VERIFY] — see weight.py
    pt = best_cruise(w)
    print(f"V={pt['v_ms']:.2f} m/s  P_elec={pt['p_elec_w']:.2f} W  "
          f"endurance={pt['endurance_min']:.0f} min  range={pt['range_km']:.1f} km  "
          f"L/D={pt['ld']:.1f}  elevon={pt['elevon_deg']:.1f} deg")
