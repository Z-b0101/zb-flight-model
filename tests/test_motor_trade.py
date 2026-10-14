"""R-07 motor trade guards (scripts/motor_trade.py, scripts/prop_notch.py)."""
import os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts")); sys.path.insert(0, os.path.join(REPO, "twin"))
import motor_trade as mt  # noqa: E402

M, P = mt.MOTORS["Suppo 2204/14 1400kv"], mt.PROPS["APC 8x6SF"]
THR_MAX = 0.65


def test_unnotched_wing_is_struck_by_the_prop():
    # DR-14: without a TE notch the 8 in disc passes through the wing (guards against silently dropping the notch)
    import prop_notch, vlm
    _, design, _ = vlm.load()
    assert prop_notch.intersection(vlm.Wing(design).W, 8.0) is not None


def test_thr_max_keeps_motor_inside_rating_on_a_fresh_pack():
    ft = mt.full_throttle(M, P, 0.0, 12.6 * THR_MAX)
    assert ft["I"] <= M["I_max"]


def test_thr_max_still_gives_hand_launch_thrust():
    ft = mt.full_throttle(M, P, 0.0, 12.6 * THR_MAX)
    assert ft["T"] >= 1.6           # bench acceptance floor (prediction ~2.4 N)


def test_slow_flyer_rpm_limit_respected_even_unlimited():
    assert mt.full_throttle(M, P, 0.0, 12.6)["rpm"] < P["rpm_limit"]
