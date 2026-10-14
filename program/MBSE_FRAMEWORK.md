# Z!B Model-Based Systems Engineering (MBSE) Framework

**Version:** 1.0 · **Date:** 2026-10-13 · **Owner:** GM (held; accountable seat: Director of Engineering / Chief Engineer per org blueprint)
**Status:** Proposed — takes effect as program methodology on CEO acknowledgment. Tailored/lite by design (see §1, §2).
**Parent documents:** DEV_TRACKER.md (system of record), SAE_ALIGNMENT.md (ARP4754A tailoring), GITHUB_TRACEABILITY.md, Org Blueprint & SOP, JSBSim MODEL_NOTES.md, AIRFOIL_TRADE.md.

---

## 1. Purpose & principles

**Purpose.** Unify everything Z!B has built — requirements log, trade studies, CAD, JSBSim model, mission math, twin, risk register, verification plans — into one methodology where the *models* are the primary engineering artifacts and every decision traces to a requirement through evidence. The digital twin sits at the center as the executable system model.

**Why MBSE for a 204 g foam airplane.** Not because the airplane is complex — because the *program* is: 26 requirements, platform-vs-instance decisions for a product family, agents generating evidence in parallel, and a CEO making capital decisions on model outputs. Without a framework, parallel agent work becomes file sprawl with confident prose; with it, every file has a type, every number has a basis tag, and no two models silently disagree.

**Principles (binding):**

1. **One technical truth.** Requirements, geometry, mass, aero, power, energy, risk, cost, and verification status resolve to one controlled baseline. (Org doctrine #1.)
2. **Models first, documents second.** The parameter file, the CAD generator, the JSBSim XML, and the twin are the engineering record. Markdown files *explain and index* the models; they never *replace* them.
3. **No divergent models.** Any two representations of the same quantity must be generated from the same source or the divergence is a defect. (This is RQ-09, now with teeth — see §4.)
4. **Decisions trace to requirements through evidence.** Requirement → analysis/model/test → decision. A decision with no requirement parent and no evidence child is not a decision; it is an opinion.
5. **Lite by design, never lite by laziness.** Every proportionality judgment cites the tailoring statement (SAE_ALIGNMENT.md §6). "Small program" justifies *less paperwork*, never *less rigor*.
6. **Anti-theater rule.** Any framework artifact that no decision consumes within one gate gets deleted. The framework must cost less than the errors it prevents — measured, not asserted.
7. **Honesty line preserved.** Pre-hardware we hold a *validated digital model*; "twin" status is earned by calibration (§6). The framework names the maturity of every model it contains.

---

## 2. Modeling substrate (honest account)

**What our models actually are:** versioned Markdown (studies, notes, ledgers) + JSON parameter files + Python scripts (mission model, lifting-line, CAD generators) + JSBSim XML (6-DOF dynamics) + the web twin (interactive executable view). There is no commercial SysML tool, no requirements database, no PLM system.

**Why this substrate is sufficient at our scale:**

- **Scale fits files.** 26 requirements, ~10 subsystems, one airframe configuration. A requirements database adds schema overhead for zero additional rigor at this count.
- **Agent-native.** Our engineers are subagents; they read, diff, and generate Markdown/JSON/Python natively. A SysML tool's proprietary format would make every agent handoff *worse*, not better.
- **Diffable and auditable.** Git-style text diffs on params.json show exactly what changed between baselines — the core CM operation — with zero tooling.
- **Zero license, zero learning curve, zero lock-in.** The $10K goes to uncertainty retirement, not tooling.
- **Executable, not just descriptive.** Python + JSBSim *run*. A SysML block diagram at our scale would describe less than our scripts compute.

**Where the substrate breaks (stated boundary — migrate when any trigger fires):**

| Trigger | Migration |
|---|---|
| Requirements exceed ~200, or concurrent variants need automated impact analysis | Requirements-management database (even a structured SQLite/CSV with tooling, not necessarily DOORS) |
| A certification authority or major customer demands it | SysML/UML tooling + formal V&V tooling |
| Human team grows past ~5 engineers needing concurrent edit with merge semantics | Real PLM/PDM with check-in/check-out |
| Model-to-model interfaces exceed what JSON schema + verify scripts can police | Interface definition language + contract testing |

Until a trigger fires, adopting heavier tooling is methodology theater — see §9, objection 2.

---

## 3. Metamodel — element types and relations

Small and enforceable. Every program artifact must declare which element types it contains; anything that fits no type is either evidence (attached to an element) or clutter (deleted per the anti-theater rule).

### Element types

| Type | ID scheme | Definition | Example |
|---|---|---|---|
| Requirement | RQ-xxx | A SHALL: measurable, sourced, statused, DAL-tagged | RQ-01 sub-250g cap |
| Function | FN-xxx | What the system must do (verb-first), independent of implementation | FN-03 "cruise efficiently at 7 m/s" |
| Component / Subsystem | CP-xxx | A physical item or assembly in the product tree | CP-04 propulsion subassembly |
| Interface | IF-xxx | A connection between components (mechanical, electrical, data, thermal) | IF-07 ESC→FC signal + power |
| Parameter | P-xxx | A named value with units, basis tag, and owner | P-014 washout_deg = 2.0 (estimated) |
| VerificationCase | VC-xxx | A planned/executed check: method, requirement link, evidence, verdict | VC-04 coupon test |
| Decision | D-xxx | A choice with alternatives, challenge history, rationale, revisit trigger | D-06 MH60 over PW75 |
| Risk | R-xxx | An uncertain event with effect and mitigation | R-07 motor/prop mismatch |
| Assumption | A-xxx | A taken-as-true statement with an owner and a retirement plan | A-012 hotel load = 1 W |

**Basis tags** (from the SOP evidence ledger — mandatory on every Parameter): measured · supplier-rated · literature-derived · calculated · modeled · estimated · unknown.

### Relation semantics

| Relation | From → To | Meaning | Example |
|---|---|---|---|
| `satisfies` | Component/Parameter set → Requirement | This design element meets the requirement | CP-04 satisfies RQ-03 (partially) |
| `verifies` | VerificationCase → Requirement | This check discharges (part of) the requirement | VC-04 verifies RQ-04 |
| `refines` | Requirement → Requirement | Child requirement narrows the parent | RQ-06 refines RQ-05 (superseded) |
| `allocates_to` | Requirement/Function → Component | Responsibility for this requirement/function is assigned here | FN-03 allocates_to CP-01 (wing) |
| `derived_from` | Parameter → Parameter/Source | This value is computed from that input | P-031 (range) derived_from P-014, P-022 |
| `implements` | Component → Function | This hardware/software realizes the function | CP-04 implements FN-02 (thrust) |
| `connects` | Interface → Component(s) | This interface joins these components | IF-07 connects CP-05, CP-06 |
| `mitigates` | Action/Decision → Risk | This reduces the risk | D-06 mitigates R-16 |
| `challenges` | Criticism round → Decision | This attack tested the decision | recorded in D-xxx history |

**Enforcement:** DEV_TRACKER §1 (requirements), §3 (decisions), §5 (actions) already implement most of this. New with this framework: Parameters get IDs and basis tags (starting with the single parameter file, §4); VerificationCases get IDs (this *is* the verification matrix the SAE audit demands — see §5, verification view); Assumptions get IDs and retirement owners (today they hide inside prose).

---

## 4. The digital thread — authoritative flow and the single parameter file

### 4.1 The thread

```text
Requirement (RQ-xxx)
  → allocates_to Function (FN-xxx) / Component (CP-xxx)
    → design Parameter (P-xxx, in the single parameter file)
      → CAD geometry (generated, never hand-edited)
        → twin visualization (same geometry source)
      → simulation (mission model / JSBSim — consumes the same parameters)
    → VerificationCase (VC-xxx) evidence
  → Decision (D-xxx) with challenge history
```

Every link is navigable in both directions: from a failed verification you can walk back to the parameter, the requirement, and the decision that set it. That is the whole framework in one paragraph.

### 4.2 The single parameter file — closing the three-source divergence

**The known gap** (DEV_TRACKER appendix, SAE_ALIGNMENT §4.7/§6.6): geometry currently has three unowned sources of truth — CAD `params.json`, the JSBSim XML (2° washout baked in), and the twin's viewer. RQ-09 demands one source. This section closes it.

**The file:** `~/workspace/uav-sub250g/cad/params.json` — already exists and already drives the CAD generators. It is hereby declared the **authoritative baseline parameter file** for the program. No promotion to a new path: moving it would break the coordinator's running workstreams.

**Required refactor** (GM-owned, before Gate 2): split into two top-level sections —
- `"design"`: the ~25 authoritative design parameters (span, chord, taper, sweep, washout, airfoil, spar, rib layout, component masses + positions, battery, propulsion placeholders). Hand-edited only through the change process below.
- `"derived"`: everything computed from design (rib stations, hole layouts, CG rollup, etc.). Regenerated by script; **never hand-edited**; a verify script fails the build if derived ≠ f(design).

**Ownership:** Director of Engineering / Chief Engineer (per org blueprint: Air Vehicle Engineering owns configuration). Held by the GM until seats split (right-sizing rule).

**Freeze process:**
1. At each gate, the file is copied immutable to `~/workspace/uav-sub250g/baseline/params_<GATE>_vX.Y.json` with `version`, `frozen_at_gate`, `supersedes`, `frozen_by`, `date` fields. Gate 1's baseline declaration (SAE CA-06) is the first freeze: `params_GATE1_v1.0.json`.
2. Between gates the working copy may change only via a **change record**: DEV_TRACKER correction-log entry stating what changed, why, which dependents re-run (CAD regen, JSBSim regen, twin refresh, mission re-run), and the re-verification result.
3. **Consumers, not duplicators:** `build_cad.py`, the JSBSim generator, the twin's model basis, `mission.py`, and the weight rollup must *read* params.json (or the frozen baseline). Any hard-coded copy of a design parameter elsewhere is a defect. The weekly integration review runs the divergence check: regenerate all consumers from the file and diff — divergence must be zero.

**The 3°-washout test case:** the Gate 2 refinement (D-09) is the first change the process must survive — washout_deg 2.0 → 3.0 flows through one file into CAD, JSBSim, and twin together, or the process has failed its first audit.

---

## 5. System views

Views are **generated, not authored** — each view is a projection of the metamodel elements, never a separate document to go stale (this is the load-bearing answer to the maintenance objection, §9.4).

### 5.1 Requirements view
IS the DEV_TRACKER requirements log (§1), now with DAL tags (SAE CA-10: all PoC requirements DAL E) and allocation columns (allocates_to Function/Component). No new document.

### 5.2 Functional view
The functions the aircraft must perform, each with allocated components and the ArduPlane mode that implements it (mode named — audit correction standing):

| ID | Function | Allocates to | Implemented by (mode/feature) | Verified by |
|---|---|---|---|---|
| FN-01 | Launch safely (hand launch) | CP-01 wing, CP-04 propulsion | Manual / FBWA attitude hold | VC (flight test card) |
| FN-02 | Climb to cruise altitude | CP-04 propulsion | Auto-throttle mode (TECS active here — not FBWA) | VC (SITL + flight) |
| FN-03 | Cruise efficiently at 7 m/s | CP-01 wing (MH60), CP-04 | CRUISE / AUTO (TECS) | VC (mission sim + flight) |
| FN-04 | Loiter on station | CP-01, CP-06 avionics | LOITER | VC (flight) |
| FN-05 | Return to launch point | CP-06 (GPS), AP stack | RTL — **loiters, does not land** (audit correction) | VC (SITL + flight) |
| FN-06 | Land safely | CP-01 (belly) | AUTOLAND — separate, hwdef-gated (verify before use) | VC (SITL + flight) |
| FN-07 | Failsafe to safe state | CP-06 | Failsafe glide / RTL on link loss | VC (bench + SITL) |
| FN-08 | Stay within 250 g | all CP | Weight budget + weigh-ins | VC-01/02/03 (weigh-ins) |

### 5.3 Physical architecture view
The product tree from RQ-08 (full-subsystem CAD): wing-structure subassembly (ribs/spar/skins/elevons), propulsion subassembly (motor/prop/mount/ESC), avionics subassembly (FC/GPS+RX/servos), power subassembly (battery/distribution) + wiring harnesses (IF-xxx each). Generated from the CAD `model_tree.json` + clash report — the view IS the CAD tree, rendered.

### 5.4 Parametric view
IS the digital twin (`z-b-digital-twin`): live CG from placed components, mission simulator with Monte Carlo, E1 planform/twist lab, E3 compare bench. Every displayed number traces to the single parameter file + the equation registry (§8). The twin is the parametric view made executable.

### 5.5 Verification view — the verification matrix (SAE CA-05, sketched here; built as its own file)

Columns: `VC-ID | RQ-ID | DAL | Function(s) | Allocated to | Method (inspection/analysis/test/modeling) | Evidence | Verdict | Coverage`.

Seed rows (illustrative — the full matrix is a GM-owned build):

| VC-ID | RQ-ID | Method | Evidence | Verdict |
|---|---|---|---|---|
| VC-01 | RQ-01 (250 g) | test | Phase 1 weigh-in (scale) | open |
| VC-02 | RQ-01 | analysis | Weight budget rollup from params.json | pass (model) |
| VC-03 | RQ-06 (0 g PoC) | inspection | Configuration audit vs params.json | open |
| VC-04 | RQ-04 (hybrid airframe) | test | Coupon test: sheet weight, rib print, glue pull | open (CEO) |
| VC-05 | RQ-03 (range) | modeling | Mission sim + JSBSim (fidelity limits tagged) | pass w/ limits |
| VC-06 | RQ-23 (angle mode) | test | SITL mode verification (FBWA, not TECS) | open |
| VC-07 | RQ-09 (single source) | analysis | Divergence check = 0 across consumers | open |

**Coverage rule:** a requirement is verified only when its VCs cover it at the DAL-appropriate rigor — for DAL E, one credible method per requirement suffices, but "credible" is judged by the checker, not the builder.

---

## 6. Twin alignment — maturity ladder and the honesty line

### 6.1 Maturity ladder

| Level | Name | Definition | Promotion event |
|---|---|---|---|
| L0 | Descriptive model | Geometry + parameters + untested equations | — (where we started) |
| L1 | Validated model | Equations verified vs hand calcs + independent checks; internal consistency; limits tagged | Independent verification (twin v1: done — verified vs hand calcs) |
| L2 | Calibrated twin | Physical measurements ingested; prediction error quantified against data | Coupon + bench + flight data ingested (Gate 3/5) |
| L3 | Operational twin | Continuous calibration from operations; predicts and prescribes | Product operations (future) |

### 6.2 The honesty line (standing)

We are at **L1**. Pre-hardware, the program holds a *validated digital model and digital thread* — the word "twin" is earned at L2, not granted at L1. Every artifact that says "twin" must carry the maturity level next to it. This line has survived three separate reviews (backup deck, traceability audit, SAE alignment); the framework makes it structural.

### 6.3 Twin v1 → v2 → v3 mapped onto the ladder

- **Twin v1** (built, TDR pending): interactive 3D + live CG + mission sim + E1/E3. **L1** — validated model. Its TDR/CDR gates review *model credibility*, not twin status.
- **Twin v2**: JSBSim backend (`zb_wing.xml` authored, alpha v0.1) + ArduPlane SITL integration. Still **L1** — higher *fidelity*, same maturity: fidelity ≠ calibration. The fidelity upgrade is real (SIM_Plane disclaims aero accuracy; JSBSim doesn't), but no flight data has touched it.
- **Twin v3**: hardware-in-the-loop + flight-test ingestion (prediction-error quantification per JSBSim MODEL_NOTES §5 calibration list). **L2** — this is where "twin" becomes true.

**Anti-conflation rule:** a fidelity upgrade (v1→v2) must never be presented as a maturity upgrade (L1→L2). The ladder measures calibration against reality, not code sophistication.

---

## 7. Lifecycle operation — what each gate consumes and produces (modeling terms)

| Gate | Consumes (entry) | Produces (exit) | Framework artifact touched |
|---|---|---|---|
| Gate 0 — Mission integrity | CEO intent | RQ baseline (RQ-01…), family logic | Requirements view seeded |
| Gate 1 — Digital baseline | RQ baseline | **Frozen params v1.0** (first baseline freeze, §4.2); mass/CG/aero/energy models | Single parameter file frozen |
| TDR — Twin Design Review | Interactive twin (L1) | Review actions (architecture, assumptions challenged) | Twin + assumption ledger |
| CDR — Critical Design Review | TDR actions closed; **measured 3S discharge curve** | Go/no-go on prototype spend | Calibration input #1 |
| Gate 2 — Model credibility | Equation traceability, independent checks, sensitivity/uncertainty | Credibility package; D-09 (3° washout) adopted or rejected | Verification view seeded; params v2.0 candidate |
| Gate 3 — Physical calibration | Coupon, bench, component data | Calibrated parameters; **L1→L2 promotion begins** | Basis tags flip estimated→measured |
| Gate 4 — Prototype authorization | Closed interfaces, margins, control authority | Build authorization (Class D) | Full verification matrix |
| Gate 5 — Flight learning | Flight data, anomaly dispositions | Calibrated model (L2); residual error quantified | Twin earns the name |
| Gate 6 — Productization | Repeatable build, verified envelope | Product baseline; family variant branching | Thread forks per instance |

**Rule:** no gate consumes a model artifact above its maturity level. CDR cannot consume "twin predictions" as L2 evidence; Gate 4 cannot spend on L1-only credibility.

---

## 8. Tooling roadmap

| Stage | What | Status / trigger |
|---|---|---|
| Now | Markdown + JSON + Python + JSBSim XML + web twin (this substrate, §2) | Active |
| Next | `zb-flight-model` reference repo (GITHUB_TRACEABILITY.md §5): mission/drag/propulsion/trim/stability/structures/weight modules, assumptions ledger, regenerate_polars.py, unit tests pinning trade-study numbers, CI | Structure drafted; **publishing needs CEO approval (AI-03)** |
| On approval | Migrate working scripts (mission.py, lifting_line.py, CAD generators) into the repo; repo becomes the executable home of the thread; DEV_TRACKER points at repo tags instead of /tmp scripts | CEO greenlight |
| Deliberately deferred | Full SysML tooling; requirements-management database; PLM | Triggers in §2 unmet — adopting now is theater |
| Deliberately deferred | Custom autopilot stack (replacing ArduPlane) | No mission need; ArduPlane is BACKED and sufficient |

**Equation registry** (lives with the repo when published; until then, maintained in the backup deck + trade study): every equation the program depends on, with ID, source (repo module or literature), and fidelity limits. The registry is what makes "nothing on assertion" operational.

---

## 9. Criticism record — four rounds against this framework

*Applied per the standing standard (RQ-11). The framework does not get a pass because it is the framework.*

### Round 1 — Methodology theater ("it's a foam airplane")
**Attack:** A formal MBSE framework with metamodels and maturity ladders for a 204 g foam PoC is pure theater. The framework will cost more engineer-hours than the airplane.
**Defense:** (a) 80% of the "framework" already exists as files we wrote doing real work — the framework *names and connects* existing practice; it does not invent new paperwork. New artifacts introduced by this document: parameter-file discipline (§4.2), assumption IDs, the verification matrix sketch, the maturity ladder. (b) The CEO's decisions are platform/family decisions; undisciplined baselines compound across variants — the cost being managed is *program* cost, not *airplane* cost. (c) Falsifiable test: the three-source geometry divergence was caught by exactly this kind of thinking before it corrupted a gate package.
**Survived with:** the anti-theater rule (§1.6) — any framework artifact no decision consumes within one gate is deleted. Overhead is budgeted against errors prevented.

### Round 2 — Substrate illegitimacy ("that's not MBSE")
**Attack:** Markdown + JSON + Python is file sprawl with a fancy name. Real MBSE means SysML and a single tool; without it you have no real traceability.
**Defense:** MBSE is a discipline (models as primary artifacts, enforced traceability, single source of truth), not a tool brand. At 26 requirements and one configuration, a SysML tool adds license cost, learning curve, and *agent-hostile* formats for zero additional rigor — our engineers are subagents that read Markdown natively and diff JSON cleanly. Traceability here is enforced by convention + verify scripts, which is checkable in a way a diagram never is.
**Survived with:** the stated migration boundary (§2) — the first trigger that fires ends the argument in favor of heavier tooling.

### Round 3 — Single-file fantasy ("params.json can't hold everything")
**Attack:** One parameter file for CAD, JSBSim, the twin, and mission analysis is a fantasy. Consumers need different units, conventions, and derived values; the file becomes a dumping ground or gets bypassed within a month.
**Defense:** The file holds *authoritative design parameters only* (~25 numbers), not derived values — derived values are computed by consumers and cached, never hand-edited (§4.2 refactor into `design` vs `derived`). JSBSim's unit conventions are a *generator's* problem, not the file's. Enforcement is automated: the weekly divergence check regenerates every consumer from the file and fails on mismatch.
**Survived with:** the authoritative-vs-derived distinction plus automated enforcement. A convention without a check is a wish.

### Round 4 — Maintenance death ("frameworks die when the author leaves")
**Attack:** This entire structure depends on the GM updating everything by hand, and the record already shows lag (risk register staleness, flagged in DEV_TRACKER §8). Adding a metamodel and five views just adds more documents that will go stale. The framework's half-life is one busy week.
**Defense:** This is the strongest objection and it nearly killed the framework. It survives on three load-bearing answers: (a) **Views are generated, not authored** (§5) — the requirements view IS the tracker table, the parametric view IS the twin, the verification view IS the matrix file; there are no separate view-documents to rot. (b) Every framework element piggybacks on an artifact that already has an owner and a trigger (DEV_TRACKER maintenance protocol; weekly integration review agenda). (c) The anti-theater rule prunes dead weight automatically.
**Survived, narrowly, with:** an honest admission — if the GM stops maintaining the thread, it dies. So the framework's survival is anchored to the weekly integration review agenda (org blueprint), not to good intentions. The first review that skips the divergence check is the framework's actual death certificate, and it should be read as such.

---

## 10. Adoption

1. CEO acknowledges this framework (or amends it) — it takes effect as program methodology on acknowledgment.
2. GM executes §4.2 (params.json refactor + first freeze at Gate 1 baseline declaration) and seeds the verification matrix (§5.5) — both GM-owned, both due before Gate 2.
3. First live test: the D-09 3°-washout change flows through the single file into CAD, JSBSim, and twin together.
4. Revisit at each gate: does every framework artifact still have a consuming decision? Delete what doesn't.

**One-line essence:** *One parameter file, one thread, one truth — every number traceable, every decision challenged, nothing on assertion.*

---
*Framework v1.0 — 2026-10-13. Challenge it; that's what it's for.*
