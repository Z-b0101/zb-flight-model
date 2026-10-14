# TDR Record — Z!B Digital Twin (Twin Design Review)

**Program:** Project Z!B — sub-250g autonomous flying-wing UAV (PoC: 0.90m MH60, 204g AUW, 0g payload)
**Review:** Twin Design Review (TDR) — per DEV_TRACKER §6 gate register
**Review basis:** Builder live-probe evidence (interactive 3D+CG, mission sim + Monte Carlo, E1 lab, E3 bench, program scaffolding, honesty line) + JSBSim alpha v0.1 (`jsbsim/zb_wing.xml`, loads clean in JSBSim 1.3.2, reconciles with AIRFOIL_TRADE.md: L/D 9.25, trim elevon −5.9°, Vstall 3.96 m/s)
**Prepared by:** GM staff (subagent) for GM adjudication — this record recommends; it does not adjudicate.
**Date:** 2026-10-13

---

## 1. TDR purpose and scope

**Purpose.** Answer the CEO's three TDR asks: (1) does the twin's architecture cover what needs review; (2) is any assumption in the ledger challenge-worthy; (3) greenlight toward CDR.

**Scope of review.** Twin v1 as built (web artifact `z-b-digital-twin`): interactive 3D wing with movable hardware and live CG/static-margin readout; phase-resolved mission simulator (launch/climb/cruise/loiter/RTL) with per-phase energy integration, wind, and 500-case Monte Carlo; E1 planform/twist lab (bell-twist preset → planform, spanload, finite outputs); E3 compare bench (save/compare a second configuration); program scaffolding (work packages, risks, source spine, review briefs); the pre-hardware honesty line ("validated digital model, not a calibrated twin"). Plus the separately authored JSBSim 6-DOF backend (Twin v2 physics, alpha v0.1) and the MBSE_FRAMEWORK.md contract it is held to.

**Out of scope.** Twin v2 (JSBSim+SITL integration) and Twin v3 (hardware-in-the-loop, flight-test calibration) — the MBSE maturity ladder (§6) keeps fidelity upgrades (v1→v2) distinct from maturity upgrades (L1→L2). TDR reviews model credibility at L1, not twin status.

---

## 2. Findings

### F-01 — Geometry has three unowned sources of truth (ACTION)
- **Evidence:** DEV_TRACKER appendix gap 2; MBSE_FRAMEWORK §4.2. CAD `params.json`, the JSBSim XML (2° washout baked in; MODEL_NOTES §1 records the 4° washout recommendation making the baked constants stale), and the twin's viewer geometry are not generated from one source. RQ-09 demands a single source; the framework declares `cad/params.json` authoritative and requires consumers to read it, with a weekly divergence check — neither the wiring nor the check is running yet.
- **Why it matters:** Any two models of the same quantity that silently disagree are a defect under the framework. The D-09 washout refinement is the first change this process must survive; it cannot flow through one file today.
- **Severity:** ACTION — fix is fully defined (Phase A A4 + MBSE §4.2 freeze/change process); not a blocker on twin v1's internal consistency, which was verified.
- **Disposition:** AC-TDR-02.

### F-02 — The mission sim's energy anchors are unmeasured, though honestly labeled (ACTION)
- **Evidence:** (a) The 3S discharge curve is engineering reference data, NOT a measured pack trace — the page says so; flagged as required before CDR (known open finding, not a TDR blocker). (b) The 1W hotel load has no verification owner (DEV_TRACKER appendix gap 3) — it anchors both the backup deck's asterisk and the Monte Carlo, but AI-13/14/16 cover adjacent bench work only. (c) Propulsion is an explicit placeholder (R-07; fictitious rocket-engine thrust actuator, 1.5N full-throttle T/W 0.75 — the absurdity is intentional per MODEL_NOTES §4).
- **Why it matters:** The 500-case Monte Carlo quantifies uncertainty in parameters it *has*; it cannot quantify the uncertainty in the three anchors it *assumes*. Range/endurance outputs (e.g. 30.8km/73min on 3S 650mAh) are aero-energy projections, not propulsion-verified predictions. The hotel-load sensitivity (24.9km/59min at 1W, deck asterisk) already shows how fragile range is to one unverified watt.
- **Severity:** ACTION — schedule and own the measurements; CDR entry requires the measured curve (CDR gate criteria). The honest labeling is exactly what keeps this from being a blocker.
- **Disposition:** AC-TDR-03, AC-TDR-04, AC-TDR-05.

### F-03 — Bell-twist lab's yaw output must not be read as prediction (ACTION)
- **Evidence:** E1's bell-twist preset includes a proverse/adverse yaw hint flag (WILD_CONCEPTS E1). MODEL_NOTES §3.2: all lateral-directional derivatives are typical-value estimates; Cnβ is load-bearing on the *unconfirmed winglet assumption*; calibration requires flight test (list items 3). D-07 locked "bell-spanload wing" as the platform target with "proverse yaw flight-validated (NASA)" cited — a literature claim, not our-geometry evidence.
- **Why it matters:** The platform target (D-07) leans on the bell spanload thesis; the only executable evaluator of that thesis today is E1's hint flag, whose yaw fidelity is qualitative. A reader can easily mistake the flag for a validated prediction about *our* wing.
- **Severity:** ACTION — fidelity-tag the yaw output and its limits in the twin before it feeds any design decision; confirm winglet geometry at Gate 2 freeze (MODEL_NOTES §3.2 already requires this).
- **Disposition:** AC-TDR-06.

### F-04 — Twin v1 was built on an unratified scope decision (ACTION)
- **Evidence:** D-08 (twin v1 scope: E1+E3 in, E2 parked) was recorded as PROPOSED — the CEO asked "which extensions go in" and never answered (DEV_TRACKER appendix gap 1; D-08 row). The twin shipped with E1+E3 folded in anyway.
- **Why it matters:** A gate cannot fully close while its scope decision is unratified. The content of the decision is sound (see D-08 ratification, §5), but the paper trail must match the build.
- **Severity:** ACTION — the draft ratification record is included in this package (§5) for GM adjudication under the CEO's full-authority delegation.
- **Disposition:** AC-TDR-01.

### F-05 — Twin's architecture covers twin v1's review needs; v2/v3 needs are defined, not covered (OBSERVATION)
- **Evidence:** The twin's parametric view (MBSE §5.4) is fully present: live CG from placed components, mission sim + Monte Carlo, E1 lab, E3 bench. Verified by builder live probes. The 6-DOF JSBSim backend exists as a separate alpha (authored, loads, reconciles) but is NOT integrated into the twin — SITL mapping, hotel-load power model, and measured inertias are open (MODEL_NOTES §7).
- **Why it matters:** This is the honest scope boundary of TDR. Ask (1) is answered "yes for v1/L1 model-credibility review; v2 integration is the defined next scope, not a TDR gap."
- **Severity:** OBSERVATION — schedule E2-related family-instance evaluation before family-instance Gate 1 (AC-TDR-07), and Twin v2 integration per the program plan (Phase A).

### F-06 — Program scaffolding is present but must survive the anti-theater rule (OBSERVATION)
- **Evidence:** Work packages, risks, source spine, review briefs are intact in the twin (builder probes). MBSE §1.6: any framework artifact no decision consumes within one gate gets deleted.
- **Severity:** OBSERVATION — at CDR, any scaffolding module that fed no decision gets cut. The twin is an engineering tool (RQ-17: substance over graphics), not a control room.
- **Disposition:** Review at CDR package assembly (AC-TDR-08 scope).

---

## 3. Actions

| ID | Action | Owner | Due |
|---|---|---|---|
| AC-TDR-01 | Adjudicate and sign the D-08 ratification record (§5); update DEV_TRACKER D-08 row from PROPOSED on signature | GM | TDR package close (this week) |
| AC-TDR-02 | Wire the twin viewer + JSBSim generator to the single parameter file (`cad/params.json`, design-vs-derived split); run the first divergence check; establish the Gate 1 freeze (MBSE §4.2, Phase A A3–A5) | GM (coordinator) | Before CDR |
| AC-TDR-03 | Bench-measure the 3S discharge curve — real pack trace replaces engineering reference data in the mission sim | CEO (Phase B bench) | CDR entry (gate criterion) |
| AC-TDR-04 | Assign a verification owner for the 1W hotel load; measure avionics draw on the bench; promote assumption → data in the twin | GM | Before CDR |
| AC-TDR-05 | R-07 wattmeter bench test of the 1404 + 7040-3 pairing; replace the propulsion placeholder with measured thrust tables | GM | Before CDR |
| AC-TDR-06 | Fidelity-tag E1's bell-twist yaw hint + its limits in the twin; confirm winglet geometry at Gate 2 freeze | GM | Gate 2 freeze |
| AC-TDR-07 | Schedule the E2 (multi-surface/tandem) evaluator before the first family-instance Gate 1 decision; keep AI-05 open | GM | PoC CDR |
| AC-TDR-08 | CDR package: prune twin scaffolding modules that fed no decision (anti-theater); reconcile RISK_REGISTER staleness (DEV_TRACKER §8) | GM | CDR package assembly |

---

## 4. Assumptions ledger — challenge record

The top 5 assumptions behind the twin, stress-tested. Each entry: the assumption, what breaks if wrong, retirement plan.

### A-01 — Hotel/avionics load = 1 W
- **If wrong:** Avionics draw under servo load is plausibly 2–3 W. On a 3S 650 mAh pack at ~7 m/s cruise, every extra watt is taken straight off propulsion energy — the deck's own sensitivity case (1 W → 24.9 km/59 min) shows range is fragile to this single number. The "energy-limited, not weight-limited" claim (D-05) weakens as hotel load grows.
- **Retirement:** AC-TDR-04 — bench-measure the rail draw (FC + GPS + RX + 2 servos under load), promote to measured data before CDR.
- **Challenge verdict:** CHALLENGED — no verification owner; highest-priority unmeasured assumption in the mission sim.

### A-02 — 3S discharge curve = engineering reference data
- **If wrong:** Voltage sag under load and the end-of-discharge knee shift usable capacity and misplace the RTL energy reserve. A reference curve can overstate usable energy ~5–15% and, worse, mis-time the low-voltage point where the mission plan assumes energy remains.
- **Retirement:** AC-TDR-03 — measured pack trace before CDR (already a CDR entry criterion).
- **Challenge verdict:** ACKNOWLEDGED AND LABELED — the twin states this honestly; not a TDR blocker, is a CDR blocker.

### A-03 — Propulsion = placeholder (1.5 N full throttle, fictitious thrust actuator)
- **If wrong:** The 1404 + 7040-3 pairing is under R-07 question (motor sold for 2.5–4″ props). If static thrust or cruise efficiency is materially worse than the placeholder, climb-phase energy and cruise throttle don't match, and range falls disproportionately because climb is the hungriest phase.
- **Retirement:** AC-TDR-05 — wattmeter static + in-flight current; measured tables replace the placeholder.
- **Challenge verdict:** CHALLENGED — the twin's range numbers must be read as aero-energy projections, never as propulsion-verified predictions, until this retires.

### A-04 — MH60 aero basis: XFoil Re≈100k polar, α₀ = −3.0° assumed, fixed e = 0.78
- **If wrong:** XFoil at Re≈100k is optimistic 10–20% (laminar-separation-bubble drag adder is S2 — deferred, not in the twin). A higher true CD0 shrinks L/D 9.25 and the 30 km range claim roughly in proportion. α₀ = −3.0° was never found for MH60 (MODEL_NOTES §3.1) — it shifts the α reference for every table. (Mitigating: the aero-optimization workstream independently reproduced the tables within a few % and corrected the internal path — CLa 3D, washout credit +0.0021/°, e≈1.0 — leaving headline numbers unchanged.)
- **Retirement:** Flight-test glide polar (calibration list item 4) quantifies the XFoil optimism correction; trim-elevon-vs-CL flight data kills the Cm0/α₀ uncertainty (item 1).
- **Challenge verdict:** CHALLENGED — directionally credible, magnitude uncertain until the glide polar is flown. E1's 20-station lifting line replacing the fixed 0.78 e is the right structural fix on the induced side.

### A-05 — Component masses/positions in the CG model = budget estimates
- **If wrong:** The hybrid airframe (73.6 g empty) is "to be studied" pending the coupon test (D-10); the battery estimate moved 55 g → 62 g once (R-06). If the as-built airframe is heavier, the twin's live CG readout is precisely wrong — and the 46 g margin erodes, which is the armor against weight creep (R-05). The twin's CG sensitivity display is only as good as its input weights.
- **Retirement:** Weigh-ins VC-01/02/03 (phase 1, pre-maiden); coupon test for the airframe construction (AI-01, CEO-owned).
- **Challenge verdict:** CHALLENGED — the twin should flag every component mass with its basis tag (measured / estimated) per MBSE §3, so the CG readout's credibility is visible, not implied.

**Bonus stress (mission sim environment):** the wind model in the phase-resolved sim — a constant-wind assumption breaks against gusts and the RTL-against-headwind case, where energy to home can exceed the plan by a large factor. The Monte Carlo should include a headwind-on-RTL stress case before CDR.

---

## 5. D-08 RATIFICATION — GM decision record (DRAFT for GM signature)

*Format per the DEV_TRACKER decision log (§3). This ratifies the PROPOSED D-08 row of 2026-10-13. It is a draft: it takes effect on GM signature, not before.*

| Field | Record |
|---|---|
| **ID** | D-08 (ratification of the 2026-10-13 PROPOSED row) |
| **Date** | 2026-10-13 |
| **Decision** | **Ratify twin v1 scope: E1 (planform/twist module) + E3 (side-by-side compare bench) folded into the digital twin; E2 (multi-surface/tandem configuration mode) parked.** AI-05 (E2 inclusion decision) stays open for the family-instance program. |
| **Rationale** | (1) **The CEO asked "which extensions go in" and never answered; the program needed to proceed.** The twin workstream (WS-10) was the pacing item of Phase A; holding it on an unanswered scoping question was the worse option. Under the CEO's full-authority delegation to the GM, an unanswered operational scoping question is decided, recorded, and left amendable — not deferred indefinitely. (2) **E1 and E3 directly serve the twin's purpose as the executable system model** (MBSE_FRAMEWORK §1, §5.4: "the parametric view IS the digital twin"). E1 makes the parametric view executable over the design space the PoC actually explores — twist/washout is the live variable for the D-09 refinement, and the bell-spanload pathfinder thesis (D-07) needed an evaluator. E3 is the decision-tool function: it turns trade-study rankings from prose into tables (WILD_CONCEPTS.md: "the feature that makes the model a *decision* tool rather than a calculator"), and the suggested build order was E1 → E3 precisely because E1 immediately supplies configs to compare. (3) **E2 has no consuming PoC decision.** E2 evaluates tandem/box configurations — the tandem is the *family carrier* (D-07), a family-instance decision (D-05, AI-06). The PoC pathfinder is the MH60 monoplane. Parking E2 obeys the anti-theater rule (MBSE §1.6): no framework artifact without a consuming decision. (4) **The decision is reversible.** E1/E3 are additive modules; E2's interface is fully specified in WILD_CONCEPTS.md (inputs, physics, outputs) and is unaffected — it can be built later without disturbing the twin. (5) **Scope discipline held:** secondary extensions S1/S2/S3 remain deferred; the twin did not accumulate speculative physics. |
| **Criticism applied** | Four rounds, per RQ-11: **R1 — "E1 scope creep: does ogee/double-delta belong in a PoC twin?"** The twist side (washout/bell presets, per-station table) is the live D-09 design variable; the planform presets are cheap variants of the same 20-station solver — keeping only twist would fork the module later. Survived. **R2 — "E3 is premature: a compare bench with nothing to compare."** E1 immediately supplies configs (rectangular vs tapered vs bell-twist); the WILD_CONCEPTS build order anticipated exactly this. Survived. **R3 — "Parking E2 kills the D-07 tandem thesis."** D-07's platform target is the bell-spanload wing; tandem is the family carrier — E2 is required before family-instance Gate 1, not PoC CDR; parked ≠ killed, and AI-05 remains open to force the revisit. Survived. **R4 — "The GM ratifying his own proposed decision under delegation is self-dealing."** The decision was recorded as PROPOSED *because* CEO approval was missing (DEV_TRACKER appendix gap 1) — the paper trail shows the gap rather than hiding it; ratification under written delegation is the documented mechanism; the CEO's unanswered question is preserved in this record and he can amend on acknowledgment. Survived with the amendment path explicit. |
| **Status** | **DRAFT — for GM adjudication and signature.** On signature: D-08 becomes RATIFIED (superseding the 2026-10-13 PROPOSED row); the GM updates the DEV_TRACKER D-08 row and closes AC-TDR-01. The CEO may amend on acknowledgment. |

---

## 6. Verdict recommendation

### RECOMMENDATION: PROCEED WITH ACTIONS (toward CDR)

The twin's architecture covers what twin v1 must review (ask 1 — yes, for the L1 model-credibility scope; v2/v3 needs are defined, not TDR gaps). The assumption ledger has been challenged (ask 2 — §4; the three heaviest assumptions have measurement actions with owners and CDR-entry teeth). The greenlight (ask 3) is therefore **conditional, not blank**: proceed toward CDR with the eight actions in §3 assigned; CDR is entered when the TDR actions are closed and the measured 3S discharge curve exists (the CDR entry criterion). No finding rises to blocker — the twin is internally consistent, its limits are labeled, and every open item has a defined retirement path.

### Four-round criticism of this verdict (trying to kill it)

**Round 1 — "Proceed with actions" is a dodge; the honest verdicts are proceed-to-CDR or recycle.**
*Attack:* The verdict splits the difference. Either the twin is credible enough for CDR or it isn't.
*Defense:* The three-way choice is real, not a hedge: "proceed to CDR" would be false because CDR has entry criteria (measured discharge curve, closed TDR actions) that are not yet met; "recycle" would be false because no finding invalidates the twin's architecture or honesty. "Proceed with actions" is the only verdict consistent with the evidence — and it has teeth: AC-TDR-03 is a hard CDR gate, not a suggestion. **Survived.**

**Round 2 — The verdict is too lenient: the mission sim's three anchors are unmeasured, so the twin can't support CDR spend decisions.**
*Attack:* Reference discharge curve, ownerless 1 W hotel load, fictitious propulsion — the Monte Carlo is uncertainty theater over a hollow core.
*Defense:* The twin at TDR is an L1 *validated model*, and its job is model credibility, not spend authorization — prototype spend is gated at Gate 4, two gates downstream, after calibration data lands (coupon, bench, flight test). The verdict does not let CDR consume the twin as L2 evidence (MBSE §7 rule: no gate consumes a model above its maturity). The anchors' fragility is exactly why AC-TDR-03/04/05 exist with CDR-entry teeth. **Survived.**

**Round 3 — The verdict ignores the process failure: the twin was scoped by an unratified decision (F-04).**
*Attack:* You can't greenlight a build whose scope was never approved — that's how programs drift.
*Defense:* The verdict doesn't ignore it; F-04 is a finding and AC-TDR-01 plus the §5 ratification record close it in this package. The GM adjudicates the ratification *as part of* the TDR close-out — the verdict is "proceed with actions," and ratification is action #1. The process failure was recorded in the tracker (appendix gap 1) rather than concealed, which is the system working. **Survived.**

**Round 4 — Steelman recycle: the twin's E1 bell-twist lab could launder the D-07 bell-spanload platform target into "validated" before any flight data exists.**
*Attack:* D-07 locked bell-spanload as the platform target; the only executable evaluator is E1's hint flag with qualitative yaw fidelity (F-03). The verdict lets a literature claim wear the twin's clothes.
*Defense:* This is the sharpest attack and it lands a real constraint — which is why F-03/AC-TDR-06 require fidelity tags and limits on the yaw output *before it feeds any design decision*, and why the twin's honesty line ("validated digital model, not a calibrated twin") is structural, not decorative. The verdict does not claim the twin validates the bell thesis; it claims the twin is a credible L1 model with labeled limits. The bell thesis is validated by flight test (Gate 5), not by the twin. **Survived, with the F-03 constraint as the load-bearing condition.**

**Convergence: 4/4 rounds survived — the verdict stands.** The one condition the GM should weigh hardest is Round 4's: the E1 yaw-hint fidelity tags (AC-TDR-06) must be in place before any design decision leans on the bell-spanload thesis.

---

*Record prepared for GM adjudication. The GM signs the D-08 ratification (§5), rules on the three CEO asks from this package, and closes the TDR.*
