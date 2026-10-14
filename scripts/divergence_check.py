"""DE-01 divergence check: every hard-coded copy of a design quantity vs cad/params.json.

Rule (MBSE_FRAMEWORK §4.2, RQ-09): two representations of the same quantity that come from
different sources are a defect. This script finds the copies and diffs them against the
controlled file. It does not change anything.

Two classes:
  GEOMETRY  literal duplicates of a params.json design value. Must match exactly. A mismatch
            is a defect and fails the check (exit 1).
  BASIS     quantities whose value legitimately differs today because the consumer runs on a
            different basis or convention that an open CE item is reconciling. Reported,
            never silently accepted; each names the item that closes it. They do not fail
            the check until the tolerances decision (P-5, after the CE-01 freeze) sets limits.

Usage: python3 scripts/divergence_check.py [--json]
"""
import importlib, json, os, sys, hashlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

PARAMS = os.path.join(REPO, "cad", "params.json")


def design_hash(design):
    return hashlib.sha256(json.dumps(design, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:12]


# (consumer module, attribute, params key, scale applied to the params value)
GEOMETRY = [
    ("zb_model.mission", "SPAN", "span", 1e-3),
    ("zb_model.mission", "CHORD", "chord", 1e-3),
    ("zb_model.mission", "WASHOUT_DEG", "washout_deg", 1.0),
    ("zb_model.mission", "SWEEP_DEG", "sweep_deg", 1.0),
    ("zb_model.trim", "WASHOUT_DEG", "washout_deg", 1.0),
    ("zb_model.structures", "SPAR_OD_MM", "spar_dia", 1.0),
    ("zb_model.structures", "SPAR_LENGTH_M", "span", 1e-3),
    ("zb_model.stability", "MAC_MM", "chord", 1.0),
]

# (consumer, attribute, controlled reference value, unit, reference basis, closing item)
BASIS = [
    ("zb_model.weight", "BUDGET_TOTAL_G", 209.0, "g", "CAD rollup (DESIGN_CLOSURE item 2); planning 211.9 g incl. spar joint", "CE-01"),
    ("zb_model.mission", "VSTALL_MS", 4.2, "m/s", "joint report: 0.9 x section CLmax at 209 g", "CE-01"),
    ("zb_model.drag", "OSWALD_E", 0.896, "-", "twin VLM (Trefftz)", "CE-01 drag"),
    ("zb_model.stability", "X_NP_MM", 144.98, "mm aft root LE", "VLM baseline; zb_model value is in the loop datum", "CE-02"),
    ("zb_model.mission", "STATIC_MARGIN", 0.0826, "-", "baseline SM at CG 128.5 mm (twin 0.070)", "CE-02"),
]


def run():
    raw = json.load(open(PARAMS))
    design = raw["design"]
    out = {"params_hash": design_hash(design), "geometry": [], "basis": [], "defects": 0}
    for mod, attr, key, scale in GEOMETRY:
        val = getattr(importlib.import_module(mod), attr)
        ref = design[key] * scale
        ok = abs(val - ref) <= 1e-9 * max(1.0, abs(ref))
        out["geometry"].append(dict(consumer=f"{mod}.{attr}", value=val, params=f"{key}={design[key]}", expected=ref, ok=ok))
        out["defects"] += 0 if ok else 1
    for mod, attr, ref, unit, basis, item in BASIS:
        val = getattr(importlib.import_module(mod), attr)
        out["basis"].append(dict(consumer=f"{mod}.{attr}", value=val, reference=ref, unit=unit,
                                 reference_basis=basis, delta=val - ref, closes_with=item))
    return out


def main():
    r = run()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=1))
    else:
        print(f"params.json design hash {r['params_hash']}")
        print("GEOMETRY duplicates (must match):")
        for g in r["geometry"]:
            print(f"  {'OK  ' if g['ok'] else 'FAIL'} {g['consumer']:32s} {g['value']!s:>8}  vs {g['params']}")
        print("BASIS divergences (reported; limits set by the P-5 tolerances decision):")
        for b in r["basis"]:
            print(f"  OPEN {b['consumer']:32s} {b['value']!s:>8} vs {b['reference']} {b['unit']}  -> {b['closes_with']} ({b['reference_basis']})")
        print(f"defects: {r['defects']}")
    sys.exit(1 if r["defects"] else 0)


if __name__ == "__main__":
    main()
