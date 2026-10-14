#!/usr/bin/env python3
"""verify_params.py — MBSE §4.2 enforcement for the split params.json.

Checks:
  1. The file has the split format (meta/design/derived).
  2. Every "derived" value recomputed from "design" matches the file
     (tolerance 1e-6) — fails on divergence (hand-edited derived values,
     stale records, generator drift).
  3. The aero basis stamped in meta matches the design geometry
     (sweep_deg/washout_deg) — fails on stale aero basis.
  4. No unknown keys in "design" (typo guard); all DESIGN_KEYS present.

Usage: verify_params.py [--params params.json]
Exit 0 only if every check passes.
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parametric import DESIGN_KEYS, compute_derived, WingParam  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--params", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "params.json"))
a = ap.parse_args()

fails = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
    if not ok:
        fails.append(name)


rec = json.load(open(a.params))
check("split format (meta/design/derived)",
      all(k in rec for k in ("meta", "design", "derived")),
      f"top-level keys: {sorted(rec.keys())}")
if fails:
    print(f"\nRESULT: {len(fails)} FAILURES: {fails}")
    sys.exit(1)

design, derived, meta = rec["design"], rec["derived"], rec["meta"]

missing = [k for k in DESIGN_KEYS if k not in design]
check("all DESIGN_KEYS present in design", not missing, f"missing: {missing}")
unknown = [k for k in design if k not in DESIGN_KEYS]
check("no unknown design keys (typo guard)", not unknown, f"unknown: {unknown}")

# rebuild a flat P the way the generators see it, then recompute
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parametric import load_params  # noqa: E402
P = load_params(a.params)
recomputed = compute_derived(P)


def _diff(path, want, got, tol=1e-6):
    if isinstance(want, dict) and isinstance(got, dict):
        if set(want) != set(got):
            return [f"{path}: key mismatch {sorted(set(want)^set(got))}"]
        out = []
        for k in want:
            out += _diff(f"{path}.{k}", want[k], got[k], tol)
        return out
    if isinstance(want, (list, tuple)) and isinstance(got, (list, tuple)):
        if len(want) != len(got):
            return [f"{path}: len {len(want)} != {len(got)}"]
        out = []
        for i, (w, g) in enumerate(zip(want, got)):
            out += _diff(f"{path}[{i}]", w, g, tol)
        return out
    if isinstance(want, float) or isinstance(got, float):
        try:
            ok = abs(float(want) - float(got)) <= tol * max(1.0, abs(float(want)))
        except (TypeError, ValueError):
            ok = want == got
        return [] if ok else [f"{path}: {want} != {got}"]
    return [] if want == got else [f"{path}: {want!r} != {got!r}"]


div = _diff("derived", recomputed, derived)
for line in div[:20]:
    print(f"    DIVERGENCE: {line}")
check("derived == compute_derived(design)", not div,
      f"{len(div)} divergent fields" if div else "all derived fields recompute clean")

# aero-basis staleness: the stamped VLM neutral point belongs to a geometry
ab = meta.get("aero_basis", {})
for k in ("sweep_deg", "washout_deg"):
    check(f"aero basis {k} matches design", ab.get(k) == design.get(k),
          f"basis={ab.get(k)} design={design.get(k)}")

print(f"\nRESULT: {'all checks passed' if not fails else f'{len(fails)} FAILURES: {fails}'}")
sys.exit(1 if fails else 0)
