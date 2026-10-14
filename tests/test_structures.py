"""Verification tests for the structural and aeroelastic tools (structures/).

These pin the tools to closed-form answers, not to program numbers: if one fails, the
solver is wrong, whatever the design does.
"""
import math, os, sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO); sys.path.insert(0, os.path.join(REPO, "twin"))

from structures import model as SM, aeroelastic as AE, hatch_fe as HF  # noqa: E402

SEC = dict(EA=1e6, EI_flap=2.0, EI_chord=50.0, GJ=0.8)


def cantilever(sweep_deg, L=0.5, n=20):
    lam = math.radians(sweep_deg)
    s = np.linspace(0, L, n + 1)
    nodes = np.c_[s * math.sin(lam), s * math.cos(lam), np.zeros_like(s)]
    return SM.BeamFE(nodes, SEC), lam, L


def test_tip_load_deflection_and_root_moment():
    for sweep in (0.0, 25.0):
        fe, lam, L = cantilever(sweep)
        F = np.zeros(6 * fe.n); P = 1.0; F[6 * (fe.n - 1) + 2] = P
        u = fe.solve(F)
        assert abs(u[6 * (fe.n - 1) + 2] - P * L**3 / (3 * SEC["EI_flap"])) < 1e-9
        assert abs(abs(fe.element_forces(u)[0]["My"]) - P * L) < 1e-9


def test_tip_torque_twist():
    fe, lam, L = cantilever(0.0)
    F = np.zeros(6 * fe.n); T = 0.1; F[6 * (fe.n - 1) + 4] = T   # about global y = spar axis when unswept
    u = fe.solve(F)
    assert abs(u[6 * (fe.n - 1) + 4] - T * L / SEC["GJ"]) < 1e-9


def test_uniform_load_tip_deflection():
    fe, lam, L = cantilever(0.0, n=40)
    w = 2.0; F = np.zeros(6 * fe.n); le = L / 40
    for k in range(1, fe.n):
        F[6 * k + 2] = w * le * (0.5 if k == fe.n - 1 else 1.0)
    u = fe.solve(F)
    exact = w * L**4 / (8 * SEC["EI_flap"])
    assert abs(u[6 * (fe.n - 1) + 2] / exact - 1) < 2e-3


def test_flutter_typical_section_textbook():
    # Hodges & Pierce typical section: mu=20, a=-1/5, x_a=1/10, r2=6/25, sigma=2/5 -> U_F/(b w_a) ~ 2.17
    U = AE.flutter_typical_section(20, -0.2, 0.1, 6 / 25, 0.4)
    assert 2.10 < U < 2.25


def test_hatch_fe_circular_hole_kt():
    # Small circular hole in a wide plate: Kt -> 3 (Peterson 3.03-3.1 for this width ratio)
    r = HF.solve(W=150.0, Hs=300.0, hole=(65.0, 85.0, -10.0, 10.0), r=10.0, h=1.0)
    assert 2.9 < r["Kt"] < 3.25


def test_vlm_washout_unloads_the_tips():
    # Washout (+ = tip nose-down) must REDUCE lift at fixed alpha and raise Cm0 (sign bug found 2026-10-14)
    import copy, vlm
    raw, P, h = vlm.load()
    Q0 = copy.deepcopy(P); Q0["washout_deg"] = 0.0; Q0.pop("twist_stations", None)
    Q6 = copy.deepcopy(P); Q6["washout_deg"] = 6.0; Q6.pop("twist_stations", None)
    s0 = vlm.Wing(Q0).solve(2.0); s6 = vlm.Wing(Q6).solve(2.0)
    assert s6["CL"] < s0["CL"]
    assert s6["Cm"] > s0["Cm"]
