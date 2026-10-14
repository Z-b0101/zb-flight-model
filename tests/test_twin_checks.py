"""The five twin-vs-design checks (investor deck slide 4; JOINT_REPORT twin section).

Design-team values and tolerances are the program record (05:36 PT, 2026-10-14). The twin
is computed fresh from cad/params.json. If one fails, the twin drifted: fix it or take the
residual to CE-01; never move the expectation to match.
"""
import os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin"))

import perf  # noqa: E402

DESIGN = dict(np_mm=145.0, sm=0.083, trim_deg=-4.60, range_km=31.9, endurance_min=75.8)


def _twin(p_hotel=0.0):
    T = perf.Twin(); T.p_hotel = p_hotel
    return T


def test_neutral_point_within_5mm():
    assert abs(_twin().d["x_np_mm"] - DESIGN["np_mm"]) <= 5.0


def test_static_margin_within_2p5_points():
    assert abs(_twin().SM - DESIGN["sm"]) <= 0.025


def test_trim_at_a2_cruise_within_1deg():
    T = _twin(); r, e, _ = T.mission()
    assert abs(T.trim(e["V"])["elevon"] - DESIGN["trim_deg"]) <= 1.0


def test_range_and_endurance_within_10pct_a2_basis():
    T = _twin(0.0); r, e, _ = T.mission()
    assert abs(r["range_km"] / DESIGN["range_km"] - 1) <= 0.10
    assert abs(e["endurance_min"] / DESIGN["endurance_min"] - 1) <= 0.10


def test_viscous_section_moment_is_applied():
    # the inviscid MH60 mean line gives cm_ac > 0; the twin must carry the XFoil value
    T = _twin()
    assert T.cm_thin > 0 and abs(T.dCm_visc - (perf.A("cm0_section") - T.cm_thin)) < 1e-12
