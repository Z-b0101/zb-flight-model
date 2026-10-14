# SAE Alignment Audit — Z!B Development Process vs Aerospace Recommended Practice

**Date:** 2026-10-13 · **Trigger:** CEO directive — "ensure our development process and documentation follows SAE Aerospace Recommended Practice guidance."
**Auditor method:** 4 criticism rounds applied to every mapping verdict (documented in §5). Strict scoring: ALIGNED means the guidance's objective is satisfied, not merely resembled.
**Scope:** process alignment for the 204g PoC. This is *guidance*, not certification — there is no certification basis (see §3).

## 0. Naming note (for the record)

No body named "Society of Aerospace Engineering" publishes Aerospace Recommended Practices. The publisher of ARP documents is **SAE International** (formerly the Society of Automotive Engineers). Proceeding on that basis. (SAE ARP5707 exists but covers *pilot training recommendations for UAS civil operations* — human-factors taxonomy — not development process; not applicable here beyond noting it.)

## 1. Applicable ARP inventory

| Document | Title (scope) | Relevance to Z!B | Status in this audit |
|---|---|---|---|
| **ARP4754A** | Guidelines for Development of Civil Aircraft and Systems | **Primary.** Development planning, requirements capture & validation, architecture, design, verification, CM, process assurance, and the *tailoring* concept | Mapped in §4 |
| **ARP4754B** | Successor revision of ARP4754A | Current edition; adds PASA/ASA concepts aligned with ARP4761A | Noted — target remains ARP4754A per directive; migrating the tailoring statement to B is a future action (CA-11) |
| **ARP4761** (now ARP4761A) | Guidelines for conducting the safety assessment process (FHA → PSSA/PASA → SSA/ASA → CCA) | **Supporting, applied lite.** Functional Hazard Assessment at our scale; no FTA/FMEA at PoC scale (tailoring rationale in §6) | Mapped in §4.8 |
| SAE S-18UAS | Subcommittee activity assessing application of ARP4754/4761 to UAVs & AAM | Confirms tailoring-to-UAVs is live industry practice, not Z!B invention | Context only |
| RTCA DO-178C / ED-12C | Software considerations in airborne systems | Touches our ArduPlane usage — recorded as a tailoring decision (§6.4), not a compliance target | Referenced |
| RTCA DO-254 / ED-80 | Design assurance for airborne electronic hardware | N/A by tailoring — no custom complex electronic hardware (COTS flight controller); recorded in §6.4 | Referenced |
| ASTM F38 (e.g., F3266) | UAS airworthiness (non-SAE) | Outside the CEO's SAE scope; noted as the standards family that would matter if Z!B ever certifies | Noted only |

## 2. What ARP4754A asks for (working summary)

From the document's structure and published guidance summaries: (1) plan the development lifecycle; (2) run safety activities per ARP4761 and assign Development Assurance Levels (A = catastrophic … E = no safety effect); (3) define system architecture and capture requirements, then **validate** them ("are we building the right thing?" — via traceability, analysis, test, modeling, inspection); (4) **verify** the implementation against requirements ("did we build it right?" — via inspection, analysis, test), recorded in a verification matrix (requirement, function, DAL, methods, pass/fail, coverage) plus a verification summary; (5) control the configuration; (6) assure the process was followed. Tailoring — scaling rigor to the product — is itself part of the guidance, but it must be *documented and justified*, not assumed.

## 3. Regulatory basis: why certification liaison is N/A

Z!B's PoC operates under the recreational exception (**49 U.S.C. §44809**), below the **0.55 lb (250 g) registration threshold (14 CFR Part 48)**. Aircraft not required to be registered are outside the Remote ID operating rules (14 CFR Part 89) for recreational operation. There is therefore **no type-certification basis, no applicant/authority relationship, and no certification liaison activity** — explicitly, not by omission. **Program assumption, recorded:** if Z!B ever operates commercially (Part 107), exceeds 250 g, flies BVLOS, or sells a product making airworthiness claims, this section reopens and the tailoring statement (§6) must be revisited. Current FAA requirements must still be live-reverified before any operations.

## 4. Mapping: Z!B process vs ARP4754A lifecycle

Verdict scale: **ALIGNED** (objective satisfied — used sparingly) · **PARTIAL** (real substance, material shortfall) · **GAP** (absent or nominal) · **N/A** (with basis).

### 4.1 Development planning — PARTIAL
**Have:** gate structure with entry/exit criteria (DEV_TRACKER §6, Gates 0–6 + TDR/CDR); org blueprint with accountability lanes; FLM→IC SOP with work-package contracts and acceptance tests; master tracker with maintenance protocol.
**Missing:** no single controlled *development plan* consolidating lifecycle, DAL assignments, verification strategy, and tailoring; planning artifacts are distributed across five documents. No documented tailoring statement (the load-bearing gap — see CA-01).
**Strict note:** gates with exit criteria are the *shape* of planning, not a plan. ARP4754A wants the plan written before the work, not reconstructed from it.

### 4.2 Requirements capture — PARTIAL (strong)
**Have:** RQ-01–RQ-26 — numbered, dated, sourced, statused; supersession preserved append-only (DEV_TRACKER §1); requirements flow into work-package contracts per the SOP.
**Missing:** no formal requirements *validation* record per requirement (see 4.3); allocation of aircraft-level requirements to subsystems/items exists physically (CAD, twin) but not as a documented allocation matrix; several requirements are not verifiable as written (e.g., RQ-03 "optimize range, efficiency…" has no acceptance threshold).
**Strict note:** capture discipline is genuinely good; it is the validation half of "capture & validation" that is informal.

### 4.3 Requirements validation — PARTIAL
**Have:** trade studies (analysis), twin + JSBSim (modeling), criticism rounds (inspection/review), bench/flight tests planned (test) — i.e., all four ARP4754A validation methods are *practiced*.
**Missing:** validation is not recorded *against requirements* — there is no per-requirement validation rationale (why RQ-01's 250 g cap is the right requirement, why 0.90 m satisfies RQ-02's ±25% band is shown, but completeness — "are all stakeholder needs captured?" — was never checked; operational requirements like launch method, wind limits, test-area constraints are absent from the log).
**Strict note:** practicing the methods ≠ validating the requirements. The criticism rounds attack *decisions*; validation must attack the *requirements themselves*.

### 4.4 System architecture — PARTIAL (strong)
**Have:** AIRFRAME_ARCHITECTURES.md — 16 sources, ranked alternatives with win conditions checked against our operating point, 4 criticism rounds per candidate, converged ranking; platform-vs-instance framing; functional decomposition in design docs.
**Missing:** no controlled architecture description with defined interfaces (ICDs) — the wiring/CAD clash check (RQ-08) will produce the physical interfaces, but they are not yet documented as an interface baseline.
**Strict note:** the *trade* work is exemplary; the *description* work (what the architecture is, authoritatively) lags it.

### 4.5 Design & implementation — PARTIAL (in work)
**Have:** parametric CAD in work, JSBSim model authored, twin as executable design representation; COTS LRU strategy (no custom hardware design).
**Missing:** the ArduPilot software assurance decision is practiced (SITL, JSBSim backend, incremental flight test) but **not formally recorded** as a tailoring decision with accepted risk and CEO sign-off; DO-254 N/A-by-tailoring (no custom complex hardware) is true but unwritten.
**Strict note:** the most safety-significant implementation choice in the program (non-DAL flight software) currently rests on conversation context, not a decision record.

### 4.6 Verification — PARTIAL (top gap)
**Have:** verification gates defined (coupon test, weigh-ins, wattmeter bench test, flight test cards planned); requirements-based testing philosophy in the SOP; analysis/modeling credit via twin + JSBSim; hotel-power asterisk honestly disclosed.
**Missing:** **no verification matrix** — ARP4754A's core verification artifact (requirement × function × DAL × method × pass/fail × coverage) does not exist; verification *coverage* is therefore unmeasurable; several verifications are planned but not yet tied to the requirements they discharge (e.g., which RQ does the coupon test verify? RQ-04 — unstated).
**Strict note:** this is the difference between "we test things" and "we can show every requirement is verified." See CA-02.

### 4.7 Configuration management — PARTIAL
**Have:** append-only DEV_TRACKER with supersede tags; artifact index; blueprint's controlled-tree proposal (00_company…08_archive); RQ-09 single-source-of-truth requirement; CAD params.json (in work).
**Missing:** no **declared baselines** — what exactly constituted the "Gate 1 baseline" (frozen parameter set, version identity) is reconstructable but not declared; the tracker's own appendix flags three unowned geometry sources of truth (CAD params vs JSBSim XML vs twin viewer); no change-control record beyond the correction log.
**Strict note:** good CM *habits*, no CM *baseline*. See CA-03.

### 4.8 Safety assessment (ARP4761, lite) — GAP
**Have:** RISK_REGISTER.md (16 risks, mitigations, deltas reported) — a genuine risk-management practice.
**Missing:** **no Functional Hazard Assessment** — functions have never been systematically enumerated against failure conditions, effects, and severity classification; no DAL has been assigned to any function; the register tracks *program* risks (weight creep, motor mismatch) alongside *safety* effects without distinguishing them.
**Strict note:** a risk register is not a safety assessment. At our scale the assessment is small (see tailoring §6.3), but "small" still has to be written down. See CA-04. This is the largest single shortfall.

### 4.9 Process assurance — PARTIAL
**Have:** the 4-round/12-iteration criticism standard (exceeds typical review rigor); SOP independence rules ("checker distinct from builder," "never convert an agent's confident prose into program truth"); TDR/CDR gates; the consultancy traceability audit as an actual independent assessment.
**Missing:** process assurance as an **accountable role** — the GM currently builds, checks, and assures; the blueprint's Verification Director lane is unfilled; no record that the process itself was followed per workstream (only that outputs were reviewed).
**Strict note:** strong review *culture*, weak assurance *independence*. The consultancy audit is the template for what independence looks like — it should be the rule, not the exception.

### 4.10 Certification liaison — N/A
Per §3: no certification basis, no authority relationship. Recorded explicitly, with the reopen trigger.

## 5. Criticism record (4 rounds on the mapping)

- **Round 1 — naive mapping:** first pass scored planning, requirements capture, and architecture as ALIGNED on the strength of the SOP, RQ log, and literature track.
- **Round 2 — adversarial:** attacked every ALIGNED: gates≠plan (planning), capture≠validation (requirements), trade≠description (architecture), testing≠verification matrix (verification). All ALIGNED scores failed; demoted to PARTIAL.
- **Round 3 — objectives check:** re-read each ARP4754A objective literally ("verification matrix shall contain…", "validation determines requirements are correct and complete"). Confirmed: nothing in the program currently satisfies an objective *completely*. Safety confirmed as GAP, not PARTIAL — a risk register does not perform any ARP4761 activity.
- **Round 4 — kill attempt on tailoring:** tried to argue full ARP4754A application is warranted (it's an aircraft; people could be hurt). Killed by the energy analysis: 204 g at 7 m/s ≈ **5 J** kinetic energy — two orders of magnitude below manned-aviation concern thresholds — plus recreational LOS operation in controlled areas. Tailoring is justified *and must be documented* (which is exactly CA-01). Also attempted: "DO-178C applies because ArduPlane is flight-critical" — killed by no-certification-basis (§3); replaced with the recorded tailoring decision (CA-05).

## 6. Tailoring statement (the core deliverable)

Tailoring is an ARP4754A concept: rigor scales to the product. What follows is Z!B's documented tailoring — every "lite" is justified, and every justification names its boundary condition. **Status: DRAFT — requires CEO approval (CA-01) to take effect.**

### 6.1 Development Assurance Level assignment
**PoC functions assigned DAL E** (no safety effect beyond loss of the article itself). Rationale: 204 g AUW, ~5 J cruise kinetic energy, recreational line-of-sight operation, $361 article cost. DAL E per ARP4754A still expects requirements, verification, and CM — it does not mean "no process." **Boundary:** any family instance adding payload over people, BVLOS, or commercial operation re-opens DAL assignment before its hardware freeze.

### 6.2 Safety assessment (ARP4761, lite)
Full FHA → PSSA → SSA → CCA is disproportionate at 5 J. Tailored to: a **one-page Functional Hazard Assessment** (functions: lift, pitch/roll/yaw control, thrust, navigation/RTL, command link; failure conditions: loss of control, flyaway, uncontrolled descent; effects classified against the 5-J / LOS / unpopulated-area operating envelope), with the RISK_REGISTER as the living hazard log. No FTA/FMEA at PoC scale — justified by the energy analysis, not by convenience. **Boundary:** DAL rises above E → full ARP4761 activities apply.

### 6.3 Software (DO-178C touchpoint)
ArduPlane is accepted as **non-DAL open-source flight software** — no DO-178C artifacts will be produced. Mitigations recorded: (a) SITL + JSBSim-backend simulation of the actual firmware before flight; (b) angle-mode (attitude PIDs) from the maiden, auto-throttle modes only after envelope proof; (c) incremental envelope expansion with geofence; (d) extensive community flight history as service-experience evidence (stated as what it is — not certification credit). The audit's corrections stand: TECS only in auto-throttle modes; RTL loiters, autoland is separate and hwdef-gated. **Boundary:** any product step triggers the GPL-3.0/NOASSERTION legal review already flagged in GITHUB_TRACEABILITY.md §6.

### 6.4 Hardware (DO-254 touchpoint)
**N/A by tailoring:** no custom complex electronic hardware is designed (COTS SpeedyBee F405 WING MINI, COTS sensors/actuators). If Z!B ever designs a custom flight controller, DO-254-equivalent assurance is re-scoped at that time.

### 6.5 Verification credit
Requirements-based test remains the backbone, but **analysis and modeling take verification credit pre-hardware**: twin mission simulation, JSBSim 6-DOF, and VLM results count as verification *evidence* (method: analysis/modeling), each tagged with its fidelity limits — they do not replace the coupon, bench, and flight tests, which remain mandatory gates. The hotel-power asterisk (deck) is the template for how limits are disclosed.

### 6.6 Configuration management
Full CM plans are disproportionate; tailored to: DEV_TRACKER as the change record (append-only, supersede tags), declared baselines at each gate (frozen params.json + geometry + mass + aero basis, version-stamped), and the single-geometry-source rule (RQ-09). The three-source divergence flagged in the tracker appendix is the first test of this tailoring — it must be closed, not grandfathered.

### 6.7 Process assurance
A standing independent assurance role is disproportionate at this headcount; tailored to: the GM's criticism standard (4 rounds / 12 iterations) + the SOP's builder/checker separation + **periodic independent audits on the consultancy model** (the traceability audit being the first). Independence is bought per-audit, not per-headcount.

## 7. Close-out actions (numbered, owned)

**CEO-owned:**
- **CA-01** — Approve this tailoring statement (§6), including the DAL E assignment and its boundary conditions. Until approved, the program operates under *de facto* tailoring with no *de jure* basis — the audit's central finding.
- **CA-02** — (Already open as AI-03) `zb-flight-model` repo publication approval.
- **CA-03** — (Already open as AI-04) Spending-authority ratification.

**GM-owned:**
- **CA-04** — Write the one-page FHA-lite (§6.2): functions → failure conditions → effects → classification. Closes the §4.8 GAP.
- **CA-05** — Build the verification matrix: every RQ row → verification method(s) → result/evidence → coverage status. New section in DEV_TRACKER or standalone file; this is the §8.5.3 artifact. Closes the §4.6 top gap.
- **CA-06** — Declare the Gate 1 controlled baseline: frozen parameter set with version identity (params.json + geometry + mass + aero basis). Closes §4.7's "no declared baseline."
- **CA-07** — Establish the single geometry source + parameter-freeze process (already flagged in tracker appendix; now with an ARP4754A CM basis).
- **CA-08** — Formally record the ArduPilot software tailoring decision (§6.3) as a decision-log entry with CEO acceptance signature (chat confirmation suffices, logged in DEV_TRACKER).
- **CA-09** — Add operational requirements to the log (launch method, wind limits, test-area constraints, flight-termination behavior, no-fly criteria) — the completeness half of validation (§4.3).
- **CA-10** — Make DAL E assignment visible in the requirements log: tag each RQ with its DAL (all E for PoC) so the verification matrix (§8.5.3 format) is complete.
- **CA-11** — (Future) assess migration of this tailoring statement to ARP4754B/ARP4761A when the program approaches productization.

## 8. Overall verdict

**One line:** Z!B's process has the *shape* of ARP4754A — gates, numbered requirements, verification intent, CM habits, fierce review culture — but it is not yet *guided by* it: the tailoring is undocumented, safety assessment is a risk register rather than an FHA, and no requirement can currently be shown verified in a matrix.

**Scorecard:** 0 ALIGNED · 7 PARTIAL · 1 GAP (safety assessment) · 1 N/A (certification liaison, with explicit basis) · 1 cross-cutting finding (undocumented tailoring underwrites all seven PARTIALs).

**Top 3 gaps:**
1. **No documented tailoring statement / DAL assignment (CA-01)** — the one document that legitimizes every proportionality judgment in the program. Without it, all rigor is ad hoc, however good.
2. **No Functional Hazard Assessment (CA-04)** — §4.8 GAP; a risk register tracks program risks, not safety effects. At 5 J the FHA is one page — its absence is process debt, not workload.
3. **No verification matrix with coverage (CA-05)** — §4.6; the program tests things but cannot demonstrate that every requirement is verified. This is ARP4754A's central verification artifact.

**Single highest-value close-out:** **CA-01, CEO approval of the tailoring statement.** It costs one review cycle, converts seven PARTIALs from "good habits" into "documented compliance with tailored guidance," and sets the boundary conditions (DAL re-assessment, product-step triggers) that protect the company later. Everything else is execution; this is the decision that makes the execution count.

---
*Audit completed 2026-10-13. Re-run at each gate. Methods: document review (DEV_TRACKER, org blueprint/SOP, risk register, traceability audit) + public SAE guidance summaries (ARP4754A/B, ARP4761/A, S-18UAS) + 4-round adversarial mapping. No ARP full text reproduced.*
