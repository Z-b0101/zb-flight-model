# CE-01 design freeze record, Z!B PoC

| | |
|---|---|
| Date | **2026-10-14, 16:48 PT** (brought forward from Oct 16 by the CEO) |
| Authority | Youssef (CEO): decisions A–E at 15:55 PT; "take ownership, design freeze today" at 16:26 PT. Executed by Claude (GM/DE). MBSE (Oubi) was informed at each step and owns the post-freeze review |
| Frozen design hash | **`479399d88b60`** (`cad/params.json` design block). Was `7be168427b4d`; proposals `752301fb9dc8` and `9d4f5b2e493a` are superseded |
| Git | Merged to `main` (PR #17, plus the PR #13 remainder); frozen ref = branch `freeze/ce01-2026-10-14` (git tags are blocked by the session proxy, so the program convention `freeze/...` is used, as for `freeze/report-2026-10-14`) |
| **MBSE post-freeze review** | **APPROVED** by Oubi (Director of MBSE), 2026-10-14 17:00 PT. Verified independently: hash reproduces; battery_u 0.160; SM (141.64 − 130.32)/200 = 5.66%; the five-check structure; decisions A–E recorded with authority; PR containment; all open items owned and dated. "The freeze stands. Changes from here go through new CE items." |
| Contains | PR #13 (DR-01 fins, DR-02 elevon throw; MBSE APPROVED), PR #14 (R-07 power train, DR-14 notch, CG layout; CEO approved), PR #12 (SA-01 structures), PR #10 (prototype roadmap) |

## 1. What is frozen

### Geometry (design block)

| Item | Value | Decision |
|---|---|---|
| Planform | 900 mm span, 200 mm chord, 25° sweep, 6° linear washout, MH60 | Unchanged |
| DR-01 tip fins | Upright, 120 high × 60 chord, leading edge at 70% of the tip chord, 3 mm Depron | MBSE recommended; CE-01 |
| DR-02 elevon throw | ≥ 12° up / ≥ 8° down (linkage geometry) | MBSE concurred; VC-29 by measurement |
| DR-14 prop notch | Cut aft of x = 195 mm for \|y\| ≤ 106.6 mm; prop 8 in | CEO, 15:55 PT |
| Battery position | `battery_u` 0.160 (9 mm forward of 0.205) | CEO option 1 (as built) |
| FC position | Section u 0.450 (5 mm forward) | CEO option 1 (as built; +10 mm hits the spar) |

### Structure, outside the hash (SA-01, R1–R5)

| Item | Value |
|---|---|
| R1 spar | Bought to spec: E ≥ 100 GPa, σ ≥ 1 GPa |
| R2 web | Hinge line; ends at the notch, \|y\| = 96.5 mm |
| R3 web | Mid-chord |
| R4 hatch | r8 corners, PLA frame and tray, bearing lid |
| R5 | Printed centre section |

### Power train (R-07)

| Item | Pick |
|---|---|
| Motor | Suppo 2204/14 1400kv |
| Prop | APC 8x6SF |
| Adapter | Scorpion 3 mm |
| ESC | EMAX Bullet 30A |
| Throttle | ArduPlane THR_MAX 65% |

## 2. Frozen mass, CG and stability

From `scripts/mass_rollup.py --motor-g 20 --prop-g 7.1 --adapter-g 5.1 --notch-dia-in 8 --battery-fwd-mm 9 --esc-to-mm 95 --fc-fwd-mm 5`; the NP comes from the twin VLM with the notch.

| Quantity | Frozen value |
|---|---|
| All-up mass | **233.0 g**, 17.0 g under the 250 g limit |
| CG | **130.32 mm** aft of root LE |
| NP (notched wing) | 141.64 mm |
| **Static margin** | **5.66%**: meets the ≥ 5.5% rule, inside the 5–8% band |
| CAD-basis check | `cad/build_all.py`: 223.3 g (LRUs and airframe only; webs and fins are in the roll-up) |

**CE-01 acceptance line:** "CE-01 accepts SM 5.66% (233.0 g, CG 130.32 mm, notched NP 141.64 mm) as the design static margin. The 8.3% record is superseded. The five-check SM row becomes a frozen-value regression guard (±0.1 pt, ≥ 5.5%). Weigh-as-built at B-12 replaces the roll-up."

**The twin now carries two mass bases** (`twin/perf.py`):
- **Frozen** (233.0 g / 130.32 mm): used for operation, structures and SM.
- **Record** (211.9 g + fins): used only to compare the other four checks like-for-like with the design-team record. The record values are not moved.

## 3. Verification at freeze (all on the merged tree)

| Check | Result |
|---|---|
| Unit and regression tests (6 suites) | **29 / 29 pass**: divergence 3, lateral 3, motor trade 4, smoke 8, structures 6, five checks 5 |
| `cad/verify_params.py` | All checks passed |
| `cad/build_all.py` (real CadQuery 2.8.0) | **0 CLASH / 0 TIGHT**; all parts watertight; twin exports written |
| `cad/verify_cad.py` | All checks passed (rib profile 0.013 mm; washout +4.500°; sweep; hinge gap) |
| New: prop-disc clash check | **5.0 mm** with the notch (VC-R07-7 needs ≥ 5 mm). The negative test without the notch gives **CLASH, 0.12 mm**, which proves the check now sees the strike |
| Five checks, record basis | NP 141.6 vs 145.0 (≤ 5 mm) ✓; trim −4.2° vs −4.60° ✓; range 30.4 vs 31.9 km ✓; endurance 71.4 vs 75.8 min ✓ |

### Structures re-run at the frozen 233.0 g

`structures/checks.py`, `analysis.py`, `aeroelastic.py`, `hatch_fe.py`. Motor and prop mass is now 32.2 g.

| Case | RF at 233 g | Note |
|---|---|---|
| Gust C4, spar to the R1 spec ("premium") | **3.53** | The low grade gives 0.88: that is why R1 exists |
| Top-skin buckling, with the R3 mid-chord web | ≥ 1.88 | The landing case governs |
| Landing, wing dynamic | Unchanged | The dynamic bending model uses the wing-borne mass only |
| Hatch FE | Unchanged | Kt is a property of the cutout geometry; the move is chordwise at the root, where bottom-skin bending stress is chordwise-uniform in the beam model. Kt 2.68 with the PLA frame |
| Battery into the hatch | 23.25 N, unchanged | The bearing lid is still mandatory |
| Motor-mount landing load | 12.1 N (was 9.4 N) | The mount must tie into the R5 centre section (PLA bond area ≥ 6 mm²) |

## 4. Changes made in this freeze (beyond PR #12/#13/#14 as reviewed)

| File | Change | Why |
|---|---|---|
| `cad/params.json`, `cad/parametric.py` | Design keys `prop_dia_in`, `prop_notch_x`, `prop_notch_halfspan` | DR-14 is now in the controlled design |
| `twin/vlm.py` | The notch is in the twin VLM (strip edges snapped to the notch edge) | Single source: the NP includes the notch. Verified identical to the R-07 analysis (ΔNP −0.98 mm at ns = 80) |
| `cad/build_cad.py` | Notch cut in the skins (Manifold boolean); new part `te_centre` | The fixed inboard trailing edge, hinge to TE for \|y\| < 112 mm, was never modelled. That is the second reason the strike was invisible |
| `cad/build_systems.py` | Motor and prop LRUs set to the frozen parts (CAD-basis masses, prop envelope); prop-disc vs skins clash check | Close the gap that hid DR-14 |
| `cad/verify_cad.py` | Rib-angle check reads rib material only (x ≤ rib cut face) | The new `te_centre` part sits next to the root rib |
| `cad/build_all.py` | `te_centre` added to the twin "structure" group | — |
| `twin/perf.py` | Frozen and record mass bases | §2 |
| `tests/test_twin_checks.py` | SM row becomes the frozen guard; other rows compared on the record basis | §2 |
| `tests/test_divergence.py` | Controlled hash pinned to `479399d88b60` | Freeze |
| `structures/model.py`, `checks.py` | Total 233.0 g; motor and prop 32.2 g; results re-generated | §3 |
| `scripts/mass_rollup.py`, `scripts/prop_notch.py` | Read the notch from params; no double-count of ΔNP | — |

## 5. Not frozen / open after freeze (does not change the design definition)

| # | Item | Owner | ECD |
|---|---|---|---|
| 1 | Alpha0 reconciliation (CE-01 gate c). The twin's VLM shows washout alone moves the wing's zero-lift angle by about 2.5°, so the gap is likely section (−3.0°) vs wing. Write-up pending | Claude | Oct 15, 12:00 PT |
| 2 | Dimensioned drawings and STEP for R2–R5, the fins, the notch and the motor mount (manufacturing data) | Claude | Oct 16, 12:00 PT |
| 3 | Fixed tip trailing edge (y 405–450, aft of the hinge) is also not modelled in CAD; add it as `te_tip`. MBSE nit: confirm it does not move the CAD-basis mass (223.3 g) or the frozen roll-up | Claude | Oct 16 |
| 4 | Prop clearance is exactly 5.0 mm at the notch side edge: hold ±0.5 mm at the cut; bench VC-R07-7 | Build | B-11 |
| 5 | Twin η derate → physics propulsion model, after VC-R07-5. **MBSE CONCUR (17:00 PT)** | Claude (implement), MBSE (accept) | Oct 28 (CDR) |
| 6 | Order the parts (re-check stock first) | CEO | After freeze |
| 7 | MBSE post-freeze review of this record | Oubi | **Done: APPROVED 17:00 PT** |
