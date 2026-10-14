"""Weight budget builder + CG rollup (closes traceability row C4-exact).

Budget: WEIGHT_BUDGET.md, 2026-10-12 rollup. Total 204.3 g, margin 46 g
against the 250 g regulatory cap.

[VERIFY] — known conflict: the CAD mass rollup reads 209.0 g and the CAD CG
is 128.5 mm aft root LE vs the 116.0 mm target. CE-01/CE-02 own closure;
this module tracks the spreadsheet basis until the single source of truth
lands. Do not silently "fix" the 204.3 g number.
"""

# --- Budget line items (grams). Basis from WEIGHT_BUDGET.md ---
BUDGET_ITEMS = [
    # (name, mass_g, basis, x_mm aft root LE or None)
    ("airframe", 73.6, "modeled: skins 36 + ribs 12 + spar 7.9 + misc 17.7", None),
    ("battery_3s_650", 62.0, "verified spec (GNB)", None),
    ("motor_1404", 10.0, "verified spec", None),
    ("esc_20a", 3.5, "verified spec (EMAX Bullet)", None),
    ("fc_stack", 23.0, "verified (oga.global teardown)", None),
    ("gps_compass", 7.7, "verified spec (M100-5883)", None),
    ("servos_x2", 8.6, "verified spec (ES9051)", None),
    ("rx_encoder", 8.0, "estimate", None),  # Z!B-ESTIMATED
    ("prop_7x4", 7.9, "verified spec (Flash 7040)", None),
    ("payload_poc", 0.0, "0 g PoC; 30 g requirement applies to family instances", None),
]

REGULATORY_CAP_G = 250.0
BUDGET_TOTAL_G = 204.3  # [VERIFY] — see module docstring


def rollup(items=BUDGET_ITEMS) -> dict:
    """Sum the budget; return total, margin, and per-line table."""
    total = sum(m for _, m, _, _ in items)
    return {
        "items": [{"name": n, "mass_g": m, "basis": b} for n, m, b, _ in items],
        "total_g": total,
        "cap_g": REGULATORY_CAP_G,
        "margin_g": REGULATORY_CAP_G - total,
    }


def cg_rollup(components: list) -> dict:
    """CG from placed components: [(name, mass_g, x_mm)] -> x_cg_mm.

    Pass measured/placed x positions once CE-01 closes; until then every
    caller must state its datum explicitly (root LE, mm aft).
    """
    if not components:
        return {"x_cg_mm": None, "note": "no placed components — CG unplaced"}
    m_tot = sum(m for _, m, _ in components)
    x_cg = sum(m * x for _, m, x in components) / m_tot
    return {"x_cg_mm": x_cg, "mass_g": m_tot, "n_components": len(components)}
