# Z!B Phase A · Workstream A2 — Closed CAD↔Simulation Iteration Log

**Loop:** parameters → CAD regen (variant outdir, CAD stream's `build_cad.py`
--params/--outdir) → STL verify (`cad_interface.verify_against_stl`) → VLM on
verified reconstruction → mission sim → evaluate → parameter update.
**Decision basis:** range @ SM=6% (prior optimization basis), 64 panels.
**Runner:** `aero_opt/cad_loop/cycle_runner.py`. Variant dirs: `aero_opt/cad_loop/cyc<N>_<tag>/`
(each holds `params_in.json`, regenerated STLs, `params.json`, `sim_SM6.json`).
**Design band:** washout 3–6°, sweep 20–25°, taper 0.7–1.0, linear twist
(power-law screened, rejected). **Vetoes respected:** no 10–12° washout, no
35° sweep, no taper <0.7. **Mission model:** exactly per task spec
(P_shaft=D·V; CD=Cd_airfoil+0.012+Cl²/(π·4.5·e_vlm); eta=min(0.55,
0.20+0.0875·P_shaft); 5.772 Wh; V≥max(1.5·Vstall,7.0)=7.0 m/s binds, CL*=0.37).
**Params schema:** overrides only — the `params.json` schema was NOT modified.

## Fidelity fix (cycle 0, before the loop)

`cad_interface.wing_from_cad` sampled twist on a **linear** y-grid while
`build_wing` uses **cosine-spaced** panels → tip panels received less washout
than the CAD built (under-washed tips: pessimistic range/trim, spurious
`tip_critical=True`). Fixed by sampling the CAD's exact THETA(y) law at the
panel centers (`twist_at_eta`), as the docstring always claimed. The old
pipeline's CAD-geometry numbers were pessimistic by ~0.11 km, increasingly so
with washout — the variable this loop sweeps — so the fix was mandatory, not
optional. Re-baselined iteration-1 point (wash 4°, sweep 20°):
**31.9341 km / 76.0 min, δe=−4.50°, e=1.000, tip margin 0.486** (was 31.82 with
the bug). STL verification PASS on all cycles (chord/LE-x/twist at 5 stations).

## Pre-loop screening (idealized, 32 panels — candidate selection only)

| Candidate | Range | Δ vs iter-1 | Verdict |
|---|---|---|---|
| sweep 25° (wash 4°) | 32.11 | +0.16 | → Cycle 2 |
| + wash 5° | 32.27 | +0.32 | → Cycle 3 |
| + taper 0.85 | 32.29 | +0.34 | **rejected**: +0.02 km (0.06%) for breaking 8-identical-rib simplicity; below mesh-noise significance |
| + taper 0.70 | 32.30 | +0.35 | **rejected**: same, +0.03 |
| twist exponent p=1.2 | 32.28 | +0.33 | **rejected**: +0.01 vs linear; keeps twist law simple |
| wash 6° linear (sw 25°) | 32.42 | +0.47 | → Cycle 4 (top of allowed 3–6° band) |

Bell twist and 10–12° washout / 35° sweep were already evaluated and
vetoed/rejected in AERO_OPTIMIZATION.md §3 — not re-litigated.

## Cycle 2 — sweep 20° → 25° (wash 4°, taper 1.0, linear)

**Why:** largest single remaining idealized gain (+0.16 km); isolated change
for clean delta attribution; inside the 20–25° band.
**Result:** 32.0940 km / 76.4 min, δe=−4.21° (−4.50→−4.21), e=1.000,
tip margin 0.479 (not critical), x_ac=95.0mm, x_cg=83.0mm @SM6%.
CL*=0.37, V=7.00, Re=94.8k ✓, |δe|<8 ✓.
**Delta:** +0.1599 km = **+0.5007%** (not <0.5% → continue).
**Verdict:** accept as new incumbent. Note: x_ac moved 73.7→95.0mm (sweep
geometry); CG datum convention — 83mm aft of root QC = 41.5% chord from QC
datum, inside the prior "31–41% battery-placeable" assessment; no new CG risk.

## Cycle 3 — washout 4° → 5° (sweep 25°, taper 1.0, linear)

**Why:** refinement-grid optimum had drifted toward w≈4.5; probe upward along
the trim-drag gradient (each washout degree buys ≈+0.0021 Cm0 credit →
≈0.33° less |δe| → quadratic trim-drag saving).
**Result:** 32.2540 km / 76.8 min, δe=−3.88°, Cm0_wing=−0.0089
(−0.0115→−0.0089), tip margin 0.487.
**Delta:** +0.1600 km = **+0.4985%** (<0.5% — first sub-threshold step).
**Verdict:** accept. Gain mechanism confirmed again as pure trim-drag
(Cm0 path, e unchanged at 1.000).

## Cycle 4 — washout 5° → 6° (sweep 25°, taper 1.0, linear)

**Why:** continue while gains ≥ threshold; 6° is the top of the allowed band
and the Depron-fairing kink limit — this is the last legal step.
**Result:** 32.4015 km / 77.1 min, δe=−3.55°, Cm0_wing=−0.0062, e=1.000,
tip margin 0.496 (improves with washout — tips unload), x_ac=95.0mm.
**Delta:** +0.1475 km = **+0.4572%** (<0.5% — second consecutive).
**Verdict:** accept. **LOOP CONVERGED** — two consecutive cycles <0.5%
(C3: 0.4985%, C4: 0.4572%). Stopped by the convergence rule at 4 cycles
(under the 6-cycle cap). The design space is also exhausted: washout and
sweep at band maxima, taper/p-exponent rejected at screening.

## Winner — linear 6° washout, 25° sweep, taper 1.0 (rectangular, 8 ribs, MH60)

| SM | Range | Endurance | δe | x_cg | Verdict |
|---|---|---|---|---|---|
| 5% | 32.60 km | 77.6 min | −3.09° | 85.0mm | feasible |
| **6% (loop basis)** | **32.40 km** | **77.1 min** | **−3.55°** | 83.0mm | **locked** |
| 8% | 31.93 km | 76.0 min | −4.48° | 79.0mm | feasible |

All: CL*=0.37, V=7.00 (floor binds), Re=94.8k≥80k ✓, |δe|≤8 ✓, tip margin
0.50, tips not critical ✓. Winner unchanged across SM 5–8% (ranking
SM-independent, consistent with prior R2/R3).

**Deltas vs 30.0 km / 72 min trade-study baseline:** +2.40 km (+8.0%) /
+5.1 min (+7.1%) @SM6%; **+1.93 km (+6.4%) / +4.0 min (+5.6%) @SM8%**
(the trade study's SM — the apples-to-apples comparison).
**Deltas vs iteration-1 (31.93/76.0):** +0.47 km (+1.5%) / +1.1 min (+1.4%).

**Mesh convergence (winner @SM6%):** 32.4141 (32 panels) → 32.4015 (64) →
32.3966 (96): 64→96 Δ=0.015% — the ~0.5% cycle deltas are 30× the mesh noise.
The gains are resolved, not discretization.

## 4-round criticism of the winner (audit trail)

- **R1 — Real or noise?** Mesh-converged (0.015%). Mechanism isolated: the
  whole C2–C4 chain is the trim-drag path (Cm0 −0.0138→−0.0062, |δe|
  4.50°→3.55°, trim drag 0.00263→0.00164); e stays 1.000 throughout. The
  washout Cm credit (+0.0021/°) is confirmed by two independent lifting-line
  methods (Weissinger + Glauert). Absolute range still carries the known
  XFoil-optimism and section-cm (−0.022 vs −0.037) uncertainties — ranking is
  robust to both (prior R2 assumption swaps).
- **R2 — Steelman staying at iteration-1:** the +0.47 km costs a spar/skin
  re-cut for 25° sweep and builds washout exactly at the Depron kink limit
  with zero process margin. Counter: nothing is built yet (first build, not
  rebuild — the CAD regen is automatic), all constraints hold with margin,
  and 8-identical-rib simplicity is preserved (rectangular, linear twist).
- **R3 — Break it:** halve the washout credit → the w4→w6 gain roughly
  halves but stays positive; sign robust, magnitude credit-sensitive. Only a
  manufacturing veto (6° skin kinking in the coupon test) flips the lock —
  fallback priced: (5°, 25°) = 32.25 km, or (4°, 25°) = 32.09 km.
- **R4 — Source reconciliation:** mission model matches the task spec
  term-by-term; AIRFOIL_TRADE.md anchors hold (Vstall 3.95 ✓, MH60,
  L/D 9.47 with trim drag vs 9.25 aero-only — consistent via e≈1.0 vs 0.78);
  MODEL_NOTES.md constants reused unchanged (CLmax=1.16, Cmδe=−0.008/°,
  1.3e-4·δe² trim law); veto list fully respected (washout 6°≠10–12°,
  sweep 25°≠35°, taper 1.0≮0.7); SM band 5–8% verified feasible.

## Recommendation for Gate 1

**Lock the converged winner: linear 6° washout, 25° quarter-chord sweep,
rectangular (taper 1.0), 8 ribs, MH60 — 32.40 km / 77.1 min @SM6%.**
The single highest-leverage change inside it is washout 4°→6° (+0.31 of the
+0.47 km, pure parameter change — ribs rotate further about the spar, no
structural redesign). **Gate:** the coupon test must validate 6° Depron skin
fairing (at the kink limit); fallback (5°, 25°) = 32.25 km is priced and
requires no re-loop.
