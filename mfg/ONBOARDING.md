# Manufacturing Engineering (MfgE) onboarding pack, phase 1

Owner: Claude (acting GM). Input from Oubi (MBSE) on gating and CM. Tracks issue #6.
Date: 2026-10-14. Configuration: `cad/params.json` design hash `7be168427b4d`.

## 1. The seat in one paragraph
Turn the frozen digital design into an airframe that can be built repeatably and comes in under weight. The 250 g cap (RQ-01) is the one number that cannot move. Every manufacturing decision is judged by three things: as-built grams, build repeatability, and whether it preserves the 6° washout the aero depends on.

## 2. Open decision for the CEO: who fills the seat
Phase 1 is mostly desk work (DFM review, process plans, test procedures), and an AI agent can own it. **Physical execution cannot be done by an agent:** weighing, printing, gluing, coupon pull tests, jigs, the build itself. Today that physical work is the CEO's (RQ-25 / WS-15 / AI-01, coupon test).
- Option A: AI MfgE writes the procedures; the CEO (or a hired technician) executes and reports measurements.
- Option B: hire or contract a human MfgE/technician who owns both.
Recommendation: A for phase 1 (no spend), then revisit B at Gate 3. Waiting on the CEO's answer in #6.

## 3. Read list (in this order)
1. `program/DESIGN_PHILOSOPHY.md`: why 250 g is inviolable
2. `program/WEIGHT_BUDGET.md`: rollup, harvest/spend lists, weigh-in gates
3. `program/MATERIALS.md`: Depron, PLA rib, carbon spar, adhesive substantiation
4. `program/DESIGN_CLOSURE.md`: battery hatch, CG decision (128.5 mm, no ballast)
5. `program/RISK_REGISTER.md`: R-01 to R-05 and R-17 are manufacturing risks
6. `program/VERIFICATION_MATRIX.md`: which checks are inspection/test
7. `cad/params.json` + `cad/parametric.py` + `cad/build_cad.py`: the geometry source of truth
8. `program/reviews/JOINT_REPORT_GM_SECTIONS.md` §3: current mechanical status

## 4. Phase 1 work package (now, no hardware spend)
| # | Task | Output | Notes |
|---|---|---|---|
| M1 | DFM review of every `cad/` part: ribs, skins, spar, elevons, battery hatch | `mfg/DFM_REVIEW.md` with one finding per part | Check rib spar-slot tolerance (4.2 mm slot on a 4.0 mm tube), lightening-hole wall ≥2 mm, elevon hinge gap 0.5 mm |
| M2 | **Spar root joiner** (new finding): the swept V-spar has no designed joint | Joiner concept (printed sleeve vs carbon insert), mass, root bending check | Root carries peak moment (~0.58 N·m at 2.5 g, 209 g) |
| M3 | Washout jig: hold 6° linear washout during skinning (R-01) | Jig drawing + procedure | Washout is at the Depron fairing-kink limit; jig is mandatory |
| M4 | Coupon test procedure (RQ-04 / RQ-25) | Step-by-step card the CEO can run: weigh 1 Depron sheet, print 1 rib, glue-joint peel tests, carbon bend coupon | Results feed MATERIALS.md and the twin's assumption ledger |
| M5 | As-built mass tracking sheet | One row per part: predicted g, weighed g, delta | Pre-maiden rule: no-fly above 250 g, review below 10 g margin |

### M2 preliminary sizing (Claude, 2026-10-14, modeled, for MfgE to own)
Printed PLA V-sleeve at the root, both tube halves bonded in 30 mm deep. Basis: PLA allowable 40 MPa ÷ 1.5 (assumed; to be confirmed by the coupon), bore 4.2 mm, uniform-lift root moment at 209 g.
| Case | Root moment | Sleeve OD needed | Sleeve mass (60 mm) |
|---|---|---|---|
| 2.5 g | 0.58 N·m | 6.5 mm | 1.4 g |
| 4.0 g | 0.92 N·m | 7.4 mm | 2.1 g |
An 8 mm OD sleeve fits easily: the MH60 is about 19 mm thick at 30% chord. Expected AUW impact: about +2 g joiner and +0.8 g extra tube, inside the 41 g margin. Open: bond shear capacity (Depron-safe epoxy vs CA), and whether a carbon insert beats PLA on stiffness. The coupon test should include one joiner sample.

## 5. Phase 2 (after the Gate 1 baseline freeze, WS-22)
- Bill of materials with supplier, cost, lead time, as-built weight
- Prototype build procedure (sequence, cure times, inspection points)
- Process selection final (plain PLA vs LW-PLA ribs, R-04)
- No major prototype spend before Gate 4 (gate register). Spend authority per D-14.

## 6. Interfaces
- **MBSE (Oubi):** any part change that touches params.json goes through a PR he reviews. Measured weights and E/allowables come back to him as parameter-master updates.
- **Twin (Claude):** measured values replace `assumed` rows in `twin/perf.py`'s ledger. That is how the twin moves from L1 to L2.
- **CODEOWNERS:** proposed new path `/mfg/` → GM (Claude), with MBSE as required reviewer for anything that changes parameters. Oubi to confirm.
