"""Guards for scripts/cg_band.py (CE-AERO-01, proposed). Modelled values only."""
import os, sys
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import cg_band  # noqa: E402


@pytest.fixture(scope="module")
def base():
    return cg_band._twin()


def test_aft_limit_is_sm_floor(base):
    """Aft limit = NP - 5.5% MAC on the frozen record (NP 141.64 mm, MAC 200 mm)."""
    np_mm = base.d["x_np_mm"]
    assert abs(np_mm - 141.64) < 0.05
    assert abs((np_mm - 0.055 * 200.0) - 130.64) < 0.05


def test_overrides_do_not_leak(base):
    """Building a twin with overrides must leave the frozen assumptions untouched."""
    cg_band._twin(x_cg_mm=120.0, knockdown=0.6)
    t = cg_band._twin()
    assert abs(t.x_cg_mm - 130.32) < 1e-9
    assert abs(t.SM - base.SM) < 1e-12


def test_forward_limit_meets_criterion_exactly():
    """At the solved forward limit, trim at 1.3 Vs uses exactly 2/3 of the up-throw."""
    xf = cg_band.forward_limit(0.70, 12.0)
    de = cg_band.trim_elevon_13vs(xf, 0.70)
    assert abs(de + (2.0 / 3.0) * 12.0) < 0.02


def test_frozen_cg_inside_band_at_cited_knockdown(base):
    """The frozen CG (130.32 mm) is inside the band for knockdown 0.70-0.80, 12 deg up."""
    aft = base.d["x_np_mm"] - 0.055 * 200.0
    for k in (0.70, 0.80):
        assert cg_band.forward_limit(k, 12.0) < base.x_cg_mm < aft


def test_window_narrows_with_lower_knockdown_and_widens_with_throw():
    f_07_12 = cg_band.forward_limit(0.70, 12.0)
    f_06_12 = cg_band.forward_limit(0.60, 12.0)
    f_07_14 = cg_band.forward_limit(0.70, 14.0)
    assert f_06_12 > f_07_12          # less effective elevons -> forward limit moves aft
    assert f_07_14 < f_07_12          # more up-throw -> forward limit moves forward


def test_record_values_for_ce_item():
    """Pins the CE-AERO-01 table (modelled). If these move, the CE item must be re-issued."""
    assert abs(cg_band.forward_limit(0.70, 12.0) - 127.33) < 0.05
    assert abs(cg_band.forward_limit(0.60, 12.0) - 129.73) < 0.05
    assert abs(cg_band.forward_limit(0.70, 14.0) - 124.52) < 0.05
    assert abs(cg_band.forward_limit(0.60, 14.0) - 127.33) < 0.05
