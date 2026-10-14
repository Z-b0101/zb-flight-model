"""Propulsion — efficiency derate fit scaffold with provenance fields.

The eta derate fit is Z!B-authored (traceability row C1-exact: unbacked —
our own numbers). Fit form from the program record (AIRFOIL_TRADE.md §3):
eta = min(0.55, 0.20 + 0.0875 * P_shaft). Both coefficients are estimates
until the wattmeter bench test pins them; wattmeter CSVs land in
zb_model/data/ (see README there).
"""

# Z!B-ESTIMATED: derate fit coefficients. Fit provenance:
#   source: engineering judgment, program record AIRFOIL_TRADE.md §3
#   status: assumed — replace with wattmeter/thrust-stand fit
#   form:   eta = min(ETA_MAX, ETA_0 + ETA_SLOPE * P_shaft_W)
ETA_MAX = 0.55
ETA_0 = 0.20
ETA_SLOPE = 0.0875  # per watt of shaft power


def prop_efficiency(p_shaft_w: float) -> float:
    """Propulsion chain efficiency (motor + prop) at given shaft power."""
    if p_shaft_w <= 0:
        return ETA_0
    return min(ETA_MAX, ETA_0 + ETA_SLOPE * p_shaft_w)


def fit_provenance() -> dict:
    """Provenance ledger for the derate fit (closes C1-exact when measured)."""
    return {
        "form": "eta = min(0.55, 0.20 + 0.0875 * P_shaft)",
        "coefficients": {"eta_max": ETA_MAX, "eta_0": ETA_0, "eta_slope": ETA_SLOPE},
        "status": "assumed",
        "source": "engineering judgment; program record AIRFOIL_TRADE.md §3",
        "validation_plan": "wattmeter bench test + thrust-stand data; "
                           "CSVs to zb_model/data/, refit coefficients, "
                           "flip status to measured",
    }
