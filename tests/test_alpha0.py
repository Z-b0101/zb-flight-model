"""CE-01 gate (c) alpha0 reconciliation guards (program/ALPHA0_RECONCILIATION.md)."""
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin"))
import vlm  # noqa: E402

_, D, _ = vlm.load()


def _a0(**kw):
    d = dict(D); d.update(kw)
    return vlm.Wing(d).derivatives()["alpha0L_deg"]


def test_washout_raises_root_zero_lift_angle():
    # sign guard: nose-down tip twist must push the root-chord zero-lift angle UP
    assert _a0(prop_notch_halfspan=0.0) > _a0(washout_deg=0.0, prop_notch_halfspan=0.0) + 2.0


def test_old_record_is_the_wash_in_sign_error():
    # the retired -3.07 deg record value is exactly what 6 deg of WASH-IN gives
    assert abs(_a0(washout_deg=-6.0, prop_notch_halfspan=0.0) - (-3.07)) < 0.05


def test_frozen_alpha0_record():
    assert abs(_a0() - 1.69) < 0.1
