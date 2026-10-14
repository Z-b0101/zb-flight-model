"""Structures — spar beam bending and margin.

4 mm carbon tube spar (program record: real 8.8 g/m; 3.3x bending margin).
Cross-check: PyNite frame model. Clean-room beam theory — no copied code.
"""

import math

# --- Spar (verified spec values) ---
SPAR_OD_MM = 4.0  # outer diameter
SPAR_ID_MM = 3.0  # Z!B-ESTIMATED: inner diameter (1 mm wall); verify by caliper
SPAR_LENGTH_M = 0.90  # full-span spar
SPAR_MASS_G_PER_M = 8.8  # verified (corrected 2026-10-12)

# Carbon tube properties
# Z!B-ESTIMATED: E and allowable from pultruded-carbon literature band;
# confirm against the actual tube via coupon bend test.
E_GPA = 120.0  # flexural modulus, pultruded carbon
SIGMA_ALLOW_MPA = 600.0  # allowable bending stress with knockdown

G0 = 9.80665


def tube_inertia_m4(od_mm: float = SPAR_OD_MM, id_mm: float = SPAR_ID_MM) -> float:
    """Second moment of area for a circular tube, m^4."""
    od, id_ = od_mm / 1000.0, id_mm / 1000.0
    return math.pi / 64.0 * (od**4 - id_**4)


def max_bending_moment_nm(mass_g: float, span_m: float = SPAR_LENGTH_M,
                          load_factor: float = 2.5) -> float:
    """Worst-case root bending moment: uniform lift, n-g pull-up.

    M_root = n * W * span / 8 (uniformly loaded beam, both halves).
    """
    w_n = mass_g / 1000.0 * G0
    return load_factor * w_n * span_m / 8.0


def bending_margin(mass_g: float, load_factor: float = 2.5) -> dict:
    """Bending stress vs allowable; margin = allowable/actual.

    Program record: 3.3x bending margin at the design mass.
    """
    m = max_bending_moment_nm(mass_g, load_factor=load_factor)
    i = tube_inertia_m4()
    c = (SPAR_OD_MM / 1000.0) / 2.0
    sigma_mpa = m * c / i / 1e6
    return {
        "moment_nm": m,
        "stress_mpa": sigma_mpa,
        "allowable_mpa": SIGMA_ALLOW_MPA,
        "margin": SIGMA_ALLOW_MPA / sigma_mpa,
    }


def spar_mass_g(length_m: float = SPAR_LENGTH_M) -> float:
    """Spar mass from the verified 8.8 g/m rate."""
    return SPAR_MASS_G_PER_M * length_m
