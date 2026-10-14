# Aerodynamic Simulation + Design Optimization — Z!B PoC Flying Wing

**Workstream 2 · 2026-10-13 · Status: complete, loop demonstrated**
**Scripts:** `~/workspace/uav-sub250g/aero_opt/` (`lifting_line.py`, `glauert.py`, `mission.py`, `optimize.py`, `cad_interface.py`; re-runnable; grid results in `grid_coarse.json`)

---

## 1. Method

**Weissinger L-method lifting-line**, implemented from first principles in `lifting_line.py` (documented in its docstring). N spanwise horseshoe vortices (bound on the quarter-chord line, trailing legs to +50 spans), flow-tangency BC at 3/4-chord control points: `A·Γ = −V·(α−α₀)`. Induced drag via Trefftz-plane far-wake analysis (downwash at the lifting line = ½ the far-wake value — the classical result, derived in code comments). MH60 section: a₀=2π, α₀=−3.0° (assumed, per MODEL_NOTES), cm=−0.022, clmax=1.16.

**AeroSandbox:** pip install failed in this environment (PEP 668 system-numpy conflict; retry with `--break-system-packages` also failed on the Debian numpy). Per the task's fallback clause, the first-principles implementation is the primary tool, cross-validated two independent ways instead (§2).

**Mission model:** used exactly as specified — `CD(Cl) = Cd_airfoil(Cl) + 0.012 + Cl²/(π·4.5·e)`, `V=√(2W/ρSCl)`, `P_shaft=½ρV³S·CD`, `η=min(0.55, 0.20+0.0875·P_shaft)`, endurance `= 5.772 Wh/P_elec`, range `= endurance·V·3.6` — with **one refinement the task of this workstream exists to provide**: the span-efficiency `e` comes from the VLM per geometry instead of the assumed 0.78. Profile drag is spanwise-integrated (`cd(cl)=0.0155+0.0128·(cl−0.45)²`, the MODEL_NOTES fit) so twist is captured. Trim: `δe = (CL·SM − Cm0_wing)/Cmδe`, `Cmδe=−0.008°/°`, trim drag `1.3e-4·δe²`; `|δe|≤8°` at cruise CL. Constraints: V≥7.0 m/s, Re≥80k, tip-stall check (section cl vs 1.16 at 1.3×Vstall, tips must not be critical).

**CAD↔sim loop** (`cad_interface.py`): reads `cad/params.json` → reconstructs (chord, x_qc, twist) with the CAD generator's exact formulas → **verifies against the STL meshes** (chord/LE-x/twist sampled from `skin_top.stl`; PASS on baseline and both regenerated geometries) → VLM + mission. The STL check proves the CAD built what the params claim; the VLM consumes distributions, not triangles (meshing facets into a lattice adds noise, no physics — documented fidelity choice).

---

## 2. Validation

**Solver self-tests** (`python3 lifting_line.py`): elliptic AR=4.5 wing → e=1.017 (theory 1.000; 1.7% discretization); CLa within 9% of `a₀/(1+a₀/πAR)` (known L-method approximation band; does not affect any validation target below).

**Independent cross-check** (`glauert.py`): classical Prandtl/Glauert Fourier lifting-line (the exact theory Weissinger approximates). Washout-induced Δcl distributions agree within ~15% — this adjudicated the one serious discrepancy found (below).

**Baseline reproduction** (0.90 m, rect, MH60, 20° sweep, 2° washout, 204 g):

| Quantity | Trade study | This analysis | Verdict |
|---|---|---|---|
| Vstall | 3.95 m/s | 3.95 m/s | ✅ exact (same CLmax=1.16 assumption) |
| Aero-only L/D @CL 0.37 | 9.25 | 9.90 | ⚠️ +7% — explained: VLM computes **e≈1.0** (Glauert: 0.98) vs assumed **0.78**. The 0.78 was conservative; lifting-line theory says a rectangular AR-4.5 wing is near 1.0. |
| Trim elevon | −5.9° | −5.9° at cruise CL | ✅ reconciled, different path (see below) |
| Range / endurance | 30.0 km / 72 min | 31.1 / 74 @SM 8% | ✅ +3.7%/+2.8% — entirely the e correction |

**The washout-credit correction (Glauert-confirmed finding).** The trade study estimated +0.0075/° washout Cm credit (→ Cm0_wing=−0.007). Both lifting-line methods (Weissinger **and** Glauert, agreeing) give **+0.0021/°** → Cm0_wing=**−0.0179**. The geometric washout is largely cancelled by its own induced upwash ("induced twist" ≈ +2.1° at the tip vs −2° geometric). The trade-study number was optimistic. **But the mission impact cancels:** the study evaluated trim at CL=0.5 (→−5.9°); the correct cruise-CL (0.37) trim with the corrected Cm0 is *also* −5.9°. Same trim drag, same range contribution — honest numbers, same bottom line.

**Two discrepancies flagged for Twin v2 (do not move the targets above):**
1. `MODEL_NOTES.md` CLa=0.109/° is a units slip (2D slope plugged into the finite-wing formula in °/°); lifting-line/DATCOM give ≈0.070/°. Affects the JSBSim α-tables and stall-α (7.64°→~13.6°), not performance.
2. If the true MH60 cm is −0.037 (value at CL=0) rather than the −0.022 used (value at CL≈0.5), range drops ~1.1 km. Carried as a sensitivity; flight test (trim-elevon vs CL) resolves it.

---

## 3. Optimization results

Grid: twist `ε=−w·|η|ᵖ`, p∈{1…3}, w∈{0…8°} (ext. to 12°), sweep∈{10…35°}, taper∈{0.5…1.0}; SM=6%; span/S fixed. 1350 geometries, then 2× refinement.

| Config (p / w / sweep / taper) | Range | Endurance | δe | e | Note |
|---|---|---|---|---|---|
| Baseline (1.0 / 2° / 20° / 1.0) | 31.66 km | 75 min | −5.0° | 1.00 | VLM baseline @SM 6% |
| Gate-2 (1.0 / 3° / 20° / 1.0) | 31.80 | 76 | −4.8° | 1.00 | +0.14 km |
| **Winner (1.0 / 4° / 25° / 1.0)** | **32.10** | **76** | **−4.2°** | 1.00 | **+0.44 km / +1 min** |
| Wash-only (1.0 / 4° / 20° / 1.0) | 31.94 | 76 | −4.5° | 1.00 | +0.28 km — the single change |
| Unconstrained (1.0 / 10° / 35° / 1.0) | 33.17 | 79 | −0.6° | 1.00 | **VETOED** (unbuildable) |
| True Prandtl bell (inverse-designed, 11.6° tip twist) | 31.42 | 75 | −1.4° | 0.76 | **−0.24 km vs baseline** |

**Does bell twist beat the 2° washout baseline? No: −0.24 km / −1 min.** The inverse-designed bell (twist solved to produce the exact `(1−η²)^1.5` spanload) needs 11–15° of twist, gets e=0.76 (fixed span → elliptic beats bell on induced drag, as theory demands), and its trim advantage (−1.4° vs −5.0°) cannot cover the induced-drag penalty. Power-law "bell-like" twists (p=2–3) likewise lose to linear by ~0.05 km throughout the grid. The bell's documented value (L3/L4: proverse yaw → delete winglets) is a parts-count trade, not a range trade — evaluated separately, not here.

**What the optimizer wants that we VETO:**
- **w→10–12°, sweep→35°** (the unconstrained optimum, 33.17 km). Vetoed: tip sections at −10° incidence (separation risk at Re 90k, negative-stall territory); Depron skin cannot fair >6° twist over rib bays without kinking; AC at 73% chord forces the 62 g battery to 67% chord (no fuselage volume there); 35° spar sweep kills bending efficiency. The gain over the buildable winner is +1.07 km — not worth a redesign.
- **Taper <0.7.** Vetoed/marginal: tip chord <140 mm leaves no room for the 4 mm spar + lightening holes + elevon hinge, and breaks the 8-identical-ribs simplicity (each rib becomes a unique outline). Aero gain of taper 0.8 over 1.0 is ~0.02 km — zero justification.
- **Kept:** w≤4°, sweep≤25°, taper=1.0, linear twist. All within demonstrated build practice; CG at 31–41% chord is battery-placeable.

---

## 4. CAD loop (closed, demonstrated with evidence)

**Parameter contract:** the CAD schema (`parametric.py`) already supports everything needed — `washout_deg`, `sweep_deg`, `taper`, and `twist_stations` (per-station nonlinear twist). No schema extension required for this recommendation. (Had it not existed, the need would have been: `taper` + `twist_deg_per_station[8]` aligned to `rib_stations_y`.)

**Loop, all steps executed by this workstream in `aero_opt/cad_loop/` (CAD stream's own directory untouched):**

| Step | Evidence |
|---|---|
| (a) Baseline on CAD geometry | `params.json` (wash 2°, sweep 20°) → STL verify **PASS** → VLM: **31.59 km / 75 min, δe=−5.1°** (@SM 6%); 30.99/74 @SM 8% |
| (b) Updated parameter set | `optimized/params_opt.json`: `washout_deg` 2.0→**4.0**, `sweep_deg` 20→**25**, `taper` 1.0, linear — in-schema |
| (c) Regeneration | Ran the CAD stream's own `build_cad.py --params … --outdir optimized` (their venv): all 7 STLs regenerated, STL verify **PASS** |
| (d) Re-simulation | **31.95 km / 76 min, δe=−4.5°** (@SM 6%); 31.40/75 @SM 8% |

**Loop delta (CAD geometry, @SM 6%): +0.36 km / +1 min, trim −5.1°→−4.5°.** Direction and magnitude match the idealized prediction (+0.44 km); the 0.08 km gap is the CAD's spar-axis twist application vs idealized pure incidence — second order, documented.

**Separating the three numbers the CEO asked for:**
- (i) **Idealized-model optimum:** (linear, 4°, 25°, rect) → **32.10 km / 76 min** @SM 6% (+0.44 vs VLM baseline; **+2.10 km / +4 min vs the 30.0/72 trade-study baseline**).
- (ii) **CAD-geometry-validated optimum:** **31.95 km / 76 min** @SM 6% (re-simulated on regenerated STLs; +1.95/+4 vs 30.0/72).
- (iii) **Loop-iteration delta:** **+0.36 km / +1 min** baseline→optimized, both on CAD geometry.

**Single geometry change recommended: washout 2°→4° (keep 20° sweep, rectangular).** Wash-only on CAD geometry: **31.82 km / 76 min** (+0.23 km vs CAD baseline, +1.82/+4 vs 30.0/72) — captures two-thirds of the available gain as a pure parameter change (ribs rotate further about the spar; no structural redesign). The 25° sweep adds only +0.13 km more and forces a spar/rib-station rebuild; keep it as a follow-on option, not the PoC change.

---

## 5. Criticism rounds (audit trail)

- **R1 — Grid refinement (2× around optimum):** optimum drifted p=1/w=4/sw=25 → p=1.2/w=4.5/sw=27 (+0.14 km), asymptoting toward the vetoed region with diminishing returns. **Mind changed:** stopped chasing; recommendation pinned to round buildable values (4°/25°) rather than the numerical peak.
- **R2 — Assumption swaps:** Cmδe ±25%, misc drag ±30%, section cm −0.022→−0.037, profile +15%: **winner unchanged in all cases.** Absolute range moves (−1.1 km for cm=−0.037 — the largest sensitivity, flagged §2), ranking does not.
- **R3 — Constraint sensitivity:** SM 5→8% costs 0.77 km (winner unchanged); relaxing V≥7.0 gains only 0.23 km (floor barely binds); |δe|≤8° never binds for buildable configs (max −5.1°).
- **R4 — Kill attempts:** (a) true bell inverse-design loses (−0.24 km) — killed as a range play, retained as a proverse-yaw/parts-removal study; (b) zero-washout-credit adversarial: optimum collapses to baseline, confirming the win is entirely the trim-drag mechanism (no hidden driver); (c) buildability vetoes (above) removed +1.07 km of unbuildable gain. Converged: no round moved the recommendation.

## 6. What the optimizer couldn't decide (needs flight test)

1. **True span efficiency e** — VLM says ~1.0, trade study assumed 0.78. The 0.23 km between them is the largest absolute uncertainty. Glide-polar power-off descents (flight-test item 4) set the XFoil-optimism correction and the real e.
2. **Washout Cm credit** — VLM/Glauert say +0.0021/°, strip estimate said +0.0075/°. Trim-elevon-vs-CL flight data (item 1) measures the true Cm0_wing and Cmδe directly.
3. **Section cm (−0.022 vs −0.037)** — 1.1 km swing; same flight test resolves it.
4. **Tip-stall behavior with 4° washout** — analysis says tip margin 0.47 (safe, tips unload), but XFoil's "gentle" stall on the as-built rib/skin steps is unverified (item 5).
5. **Bell twist's proverse yaw at Re 90k** — the literature's biggest open question (no flight data below ~3 m span); the drag trade says don't do it for range, but a dedicated yaw-response flight test is the only way to value the winglet-deletion prize.

---

## 7. Reconciliation with references

- **AIRFOIL_TRADE.md:** baseline performance reproduced within 4% after the two documented corrections (e: 0.78→VLM ~1.0; washout credit +0.0075→+0.0021/°, with cancelling trim effect). The 30.0 km / 72 min claim **stands**, now on firmer (less conservative, more self-consistent) footing. The 3°-washout Gate-2 refinement is validated (+0.14 km); this work extends it to 4° (+0.28 km) as the recommended single change.
- **jsbsim/MODEL_NOTES.md:** CLa units slip flagged (§2, affects Twin v2 α/stall tables, not performance). All other constants (CD model structure, trim-drag law, elevon effectiveness, SM convention) reused unchanged. The 3°/5–6%-SM Gate-2 variant constants in §1 remain valid; the 4° recommendation only changes the washout credit (+0.0084 vs +0.015 assumed) and trim elevon (−4.7° vs −3…−4°).
- **AIRFRAME_ARCHITECTURES.md:** bell-spanload assessment confirmed quantitatively — drag claim does not survive at our operating point (−0.24 km); the proverse-yaw/parts-removal thesis is untouched and remains the reason to keep bell on the roadmap.
