import importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("divergence_check", os.path.join(HERE, "..", "scripts", "divergence_check.py"))
dc = importlib.util.module_from_spec(spec); spec.loader.exec_module(dc)


def test_geometry_duplicates_match_params():
    r = dc.run()
    bad = [g for g in r["geometry"] if not g["ok"]]
    assert not bad, f"geometry literals diverge from cad/params.json: {bad}"


def test_design_hash_is_controlled_baseline():
    assert dc.run()["params_hash"] == "479399d88b60"   # CE-01 frozen baseline (2026-10-14); was 7be168427b4d


def test_every_basis_divergence_names_its_closing_item():
    assert all(b["closes_with"] for b in dc.run()["basis"])
