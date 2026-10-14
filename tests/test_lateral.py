"""DR-01: yaw stability derived from geometry, not typed in."""
import copy, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "twin"))
import lateral, vlm  # noqa: E402

_, D, _ = vlm.load()


def test_fins_give_target_yaw_stability():
    for CL in (0.17, 0.37, 0.6):
        assert lateral.derive(D, 130.9, 142.6, CL)["cn_beta_per_deg"] >= 0.001


def test_bare_wing_is_weak_in_yaw():
    bare = copy.deepcopy(D); bare["fin_height"] = 0.0
    r = lateral.derive(bare, 128.5, 142.6, 0.17)
    assert r["fin"] is None and r["cn_beta_per_deg"] < 0.0003


def test_fin_orientation_matters():
    flat = copy.deepcopy(D); flat["fin_height"], flat["fin_chord"] = 60.0, 120.0
    assert lateral.derive(flat, 130.9, 142.6, 0.37)["cn_beta_per_deg"] < 0.001
