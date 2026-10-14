"""Smoke tests pinning headline program numbers.

Each test pins a number from the program record (AIRFOIL_TRADE.md,
ITERATION_LOG.md, WEIGHT_BUDGET.md). If a test fails, the model drifted
from the record — fix the model or re-ratify the number, never silently
update the expectation.
"""

import math

from zb_model import drag, mission, propulsion, stability, structures, trim, weight


def test_level_speed_at_204g():
    # Gate 1: V = sqrt(2W/(rho*S*CL)) at 204.3 g, CL 0.37 -> ~7.01 m/s,
    # right at the 7.0 m/s cruise floor (1.5*Vstall = 5.9 < 7.0).
    w = 0.2043 * mission.G0
    v = mission.level_speed_w(w, 0.37)
    assert v == math.sqrt(2 * w / (1.225 * 0.18 * 0.37))
    assert 6.9 < v < 7.2


def test_cd_buildup_sanity():
    # CD = Cd_airfoil + 0.012 + CL^2/(pi*4.5*0.78); at CL 0.5:
    # 0.0155 + 0.012 + 0.25/(pi*4.5*0.78) ~= 0.0502
    cd = drag.total_cd(0.5)
    assert abs(cd - 0.0502) < 0.002


def test_trim_elevon_sign():
    # Trim math: delta_e = (CL*SM - Cm0_wing) / (-0.008/deg).
    # With the +0.0075/deg hand estimate, Cm0_wing = +0.023 and the model
    # trims near zero elevon at CL 0.37 / SM 6%.
    # CALIBRATION GAP (documented, not hidden): the A2 VLM loop realized
    # Cm0_wing = -0.0062 and trims at delta_e = -3.55 deg (up-elevon).
    # This test pins the model's arithmetic; the loop value is the
    # higher-fidelity trim reference until VLM/flight data lands.
    de = trim.elevon_for_trim(0.37, 0.06)
    assert de == (0.37 * 0.06 - trim.wing_cm0()) / trim.ELEVON_DEFF_PER_DEG
    assert abs(de) < 1.0  # near-zero per the hand-estimate credit
    assert trim.trim_drag_cd(de) >= 0
    # Trim drag is quadratic: doubling deflection quadruples the increment.
    assert trim.trim_drag_cd(2 * de) == 4 * trim.trim_drag_cd(de)


def test_mission_headline():
    # This L1 model (e=0.78 hand estimate + 1 W illustrative hotel) lands
    # near ~26 km / ~57 min at 204.3 g. BRIDGE TO A2: the loop's 32.40 km /
    # 77.1 min @ SM 6% used e_vlm = 1.000 and no hotel load — the delta is
    # assumptions, documented in mission.py, not arithmetic. Both are L1
    # until flight test sets the absolutes.
    w = 0.2043 * mission.G0
    pt = mission.best_cruise(w)
    assert 24.0 < pt["range_km"] < 29.0
    assert 52.0 < pt["endurance_min"] < 62.0
    assert pt["v_ms"] >= 7.0 - 1e-9


def test_prop_efficiency_caps():
    assert propulsion.prop_efficiency(0) == 0.20
    assert propulsion.prop_efficiency(100) == 0.55  # capped
    assert 0.20 < propulsion.prop_efficiency(2.0) < 0.55


def test_weight_rollup():
    r = weight.rollup()
    assert abs(r["total_g"] - 204.3) < 1e-9  # [VERIFY] — see weight.py
    assert abs(r["margin_g"] - 45.7) < 1e-9


def test_stability_sm6():
    # SM 6% => CG 12 mm ahead of NP on a 200 mm MAC.
    x_cg = stability.cg_for_sm(0.06)
    assert abs(stability.static_margin(x_cg) - 0.06) < 1e-12
    assert stability.check_stability(x_cg)["stable"]


def test_spar_margin_positive():
    m = structures.bending_margin(204.3)
    assert m["margin"] > 1.0
    assert abs(structures.spar_mass_g() - 7.92) < 0.01  # 8.8 g/m * 0.9 m
