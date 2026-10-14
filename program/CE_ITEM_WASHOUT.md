# CE item: washout 6° → 3–4° (against `cad/params.json`)

| | |
|---|---|
| Raised by | Claude (GM/DE), 2026-10-14 |
| Owner of the decision | MBSE (Oubi), at the CE-01/CE-02 review |
| Parameter | `design.washout_deg` (locked value **6.0**; stays locked until review) |
| Origin | VLM washout-sign fix (`twin/v0.1 @532559c`, independently confirmed by MBSE, 12:29 PT) and SA-01 R6 |

## Proposal
Reduce linear washout from 6° to 3–4°.

## Evidence for
Source: the corrected twin, `perf.Twin` with only `washout_deg` changed. All other parameters are at the controlled baseline (hash 7be168427b4d), at 209 g.

| Washout | Cm0 (CG) | Best range (1 W hotel) | Best endurance | Cruise trim at 10.5 m/s | Up-elevon at 1.3 Vs |
|---|---|---|---|---|---|
| 0° | +0.004 | 26.9 km | 62.8 min | −0.8° | −5.4° |
| 2° | +0.013 | 27.0 km | 63.4 min | −0.1° | −4.7° |
| 3° | +0.018 | 27.0 km | 63.5 min | +0.3° | −4.3° |
| **4°** | +0.022 | 27.0 km | 63.4 min | +0.7° | −3.9° |
| 5° | +0.027 | 26.8 km | 62.6 min | +1.1° | −3.5° |
| **6° (locked)** | +0.031 | 26.6 km | 60.7 min | +1.5° | −3.2° |

- **Range and endurance** are flat to slightly better: +0.4 km and +3 min at 3–4°.
- **Trim:** cruise trim is near 0°, which means less trim drag and more elevon travel left for control.
- **R-01 relief:** 6° is at the Depron forming limit (R-01). 3–4° is an easier skin layup on the jig.
- **Structures (SA-01):** less washout loads the tips more at high CL. The bending effect is small: flight root moments went down 7–16% when washout was corrected from wash-in, and landing (inertia only) governs the spar anyway.

## Evidence against / caveats (MBSE, 12:29 PT)
- **The VLM is inviscid and linear.** It says nothing about tip stall, which is where washout earns its keep.
  - The table shows the tip's local cl at 1.3 Vs staying at 0.27–0.32 of the root value at every washout. That is a linear result, not a stall margin.
- **A2 chose 6° on a different basis** (aero_opt, not this VLM). This is new evidence, not a correction of A2.
- **The span-efficiency values from the twin are suspect:** e > 1 at 2–4° washout is not physical for a planar wing. Range differences of a few tenths of a km are within that uncertainty.

## What would decide it
1. **Stall/tip-stall evidence at 3–4°:** XFoil section clmax along the span with the corrected spanload, or a nonlinear lifting-line check.
2. **The CE-01 trim reconciliation:** design loop −4.6° vs twin −0.6° (at 7.1 m/s, 6°).
3. **Flight evidence:** stall-approach test card on an early flight. Only after the maiden, at the locked 6°.

## Status
**Open.** The locked value stays 6° until the CE-01/CE-02 review.
