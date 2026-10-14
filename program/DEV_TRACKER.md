# Z!B Development Process Tracker — Master Document

**Program:** Project Z!B — sub-250g autonomous fixed-wing UAV family (PoC: 0.90m MH60 flying wing)
**Owner:** GM (Oubi) · **Authority:** CEO (Youssef) · **Created:** 2026-10-13
**Rule: no workstream closes without its tracker row closed.**

## Maintenance protocol

- **Who updates:** the GM. No one else edits this file.
- **When (mandatory triggers):** every CEO directive received · every decision made, changed, or superseded · every deliverable completed · every gate event (entry, review, exit) · every correction or issue found · every risk delta.
- **How:** append rows, never rewrite history — superseded entries keep their original text with a `SUPERSEDED` tag, date, and pointer to the replacing entry.
- **Review:** this tracker is item #1 at the weekly integration review and distributed with every gate package.
- **Living rule:** a workstream is not "done" when an agent says so — it is done when its tracker row is closed against acceptance evidence.

---

## 1. Requirements log

| ID | Date | Requirement (SHALL / directive) | Source | Status |
|---|---|---|---|---|
| RQ-01 | 2026-10-12 | Sub-250g total AUW — inviolable regulatory cap (no FAA registration / Remote ID, recreational) | CEO, Gate 0 | Satisfied in design (204g); OPEN for verification (weigh-ins) |
| RQ-02 | 2026-10-12 | Span 1.0m ±25% | CEO, Gate 0 | Satisfied (0.90m locked) |
| RQ-03 | 2026-10-12 | Optimize range, efficiency, payload, aero, autonomy; minimize complexity, noise, regulatory constraints | CEO, Gate 0 branch | In work |
| RQ-04 | 2026-10-12 | Hybrid construction: Depron 3mm skins, carbon spar, vase-mode printed ribs | CEO, Gate 0 branch A | **To be studied** — gated on coupon test (CEO review 2026-10-13) |
| RQ-05 | 2026-10-12 | ≥30g payload (original Gate 0) | CEO | SUPERSEDED 2026-10-13 → see RQ-06 |
| RQ-06 | 2026-10-13 | **0g payload for the PoC**; ≥30g requirement applies to product/family instances | CEO (coordinate review 2a) | Locked (budgets updated: 204g AUW, 46g margin) |
| RQ-07 | 2026-10-13 | **$10K funding** for project Z!B (was $1K → $1.69K) | CEO | Locked (BUDGET.md: ~$361 est, ~$9.6K headroom) |
| RQ-08 | 2026-10-13 | **3D CAD SHALL include all subsystems + sub-assemblies + wiring** (every LRU, routed harnesses, clash check) | CEO SHALL | In work (coordinator running) |
| RQ-09 | 2026-10-13 | **3D CAD SHALL be simulation-capable**: parametric (twist/washout/sweep/taper/airfoil), watertight sim-ready meshes, **closed CAD↔sim loop**, single geometry source shared with the twin | CEO SHALL | In work (coordinator running) |
| RQ-10 | 2026-10-13 | **3D CAD model + aerodynamic simulation for design optimization** | CEO | In work (coordinator: CAD + aero-opt streams) |
| RQ-11 | 2026-10-13 | Decision quality: **≥4 criticism rounds per decision node**; complex decisions **≥12 iterations at ≥11/12 convergence**; time never a constraint | CEO standing rule | Locked (in AGENTS.md; applied in trades/audits) |
| RQ-12 | 2026-10-13 | **Only GitHub-referenceable logic** behind flight control, monitoring, simulation, math/physical/theoretical models (consultancy recommendation) | CEO via consultancy | In work (audit done 55/40/5; repo drafted, not published) |
| RQ-13 | 2026-10-13 | **Perfect the digital twin before prototype spend** — model before money | CEO | In work (twin built; TDR pending) |
| RQ-14 | 2026-10-13 | **TDR + CDR gates with CEO pings** (pings = GM messages in chat) | CEO | TDR pending CEO review |
| RQ-15 | 2026-10-13 | PoC framing: **platform vs instance decisions tracked separately** | CEO | Locked |
| RQ-16 | 2026-10-13 | Process: **reach for help when needing guidance** (check process + memory, then ask) | CEO standing rule | Locked |
| RQ-17 | 2026-10-13 | **Tech-fella mode**: substance over graphics; never sell soap | CEO | Locked (working norm) |
| RQ-18 | 2026-10-12 | Maintain **risk register**, report deltas as development advances | CEO standing instruction | Locked / ongoing (register lags decisions — see §8 gaps) |
| RQ-19 | 2026-10-12 | **Review-informed LRU pricing** (customer reviews, not cheapest listings) | CEO | Satisfied (BUDGET.md) |
| RQ-20 | 2026-10-12 | **Substantiate claims with research**, not assertion | CEO | Satisfied (MATERIALS.md) / ongoing |
| RQ-21 | 2026-10-13 | **Org blueprint + SOP** for agents working under the GM | CEO | Satisfied (blueprint written); ratifications pending |
| RQ-22 | 2026-10-13 | **Accessible artifact folder for project Z!B** (the Hub) | CEO | Satisfied (hub built) |
| RQ-23 | 2026-10-13 | ArduPlane **angle mode from the maiden** (mode must be named; TECS only in auto-throttle modes) | Design decision (audit-corrected) | Locked |
| RQ-24 | 2026-10-13 | **Document and track every aspect of the development process** (this file) | CEO | In work |
| RQ-25 | 2026-10-13 | **Coupon test is the CEO's action item**: weigh Depron sheet, print one rib, pull-test glue joints | CEO | OPEN |
| RQ-26 | 2026-10-13 | Spending-authority thresholds (>$2,000 needs CEO approval — proposed) | Blueprint (needs ratification) | OPEN — needs CEO ratification |
| RQ-27 | 2026-10-13 | **CEO directive (confirmed by CEO in chat 2026-10-13):** remaining quantitative contradictions addressed first (CE-01/CE-02); GM briefs Y3k on requirements/objectives/design philosophy/trade studies; Y3k assesses the airframe choice and reports back to GM; both run an airframe-redesign trade study and cross-review in writing | CEO (via zib inbox, verified) | In work — GM briefing sent 2026-10-13; Y3k assessment due Oct 15 PDT; joint merge Oct 17 (WS-25) |

---

## 2. Workstream tracker

| ID | Workstream | Owner | Status | Deliverables (paths) |
|---|---|---|---|---|
| WS-01 | Airframe Design Model (parametric web calculator) | GM | Done — verified vs hand calcs | Web artifact `airframe-design-model` |
| WS-02 | Gate 1 design definition documents | GM | Done | `~/workspace/your_files/gate1-ux-wing-design-definition/*.pdf`, `-docx/*.docx`, `-landscape/*.pdf` |
| WS-03 | Math & logic backup slides (12) | GM | Done — hotel-power asterisk disclosed | `~/workspace/your_files/poc-math-logic-backup-slides/*.pptx` |
| WS-04 | Airfoil trade study | GM (subagent) | Done — MH60 recommended & adopted | `~/workspace/uav-sub250g/AIRFOIL_TRADE.md` |
| WS-05 | Wild-concepts side quest (12 concepts, E1/E2/E3 proposal) | GM (subagent) | Done | `~/workspace/uav-sub250g/WILD_CONCEPTS.md` |
| WS-06 | Airframe architectures — academic literature track (16 sources, 4 criticism rounds) | GM (subagent) | Done — ranking converged | `~/workspace/uav-sub250g/AIRFRAME_ARCHITECTURES.md` |
| WS-07 | GitHub traceability audit (40 claim-units, 55/40/5) | GM (subagent) | Done | `~/workspace/uav-sub250g/GITHUB_TRACEABILITY.md` |
| WS-08 | Org blueprint & FLM→IC SOP | GM | Done — 2 items need CEO ratification | `~/workspace/your_files/zb-org-blueprint/*.md` |
| WS-09 | Project Z!B Hub (accessible front door) | GM | Done | Web artifact `project-z-b-hub` |
| WS-10 | Z!B Digital Twin (interactive 3D + live CG + mission sim + E1 + E3) | GM | In work — TDR package in review, adjudication on GM authority (CEO full delegation 2026-10-13) | Web artifact `z-b-digital-twin` |
| WS-11 | JSBSim 6-DOF model (alpha v0.1) | GM (subagent) | Done — needs flight-test calibration | `~/workspace/uav-sub250g/jsbsim/zb_wing.xml`, `engine/`, `MODEL_NOTES.md` |
| WS-12 | 3D CAD model — parametric, full subsystems + wiring, sim-capable, closed CAD↔sim loop | GM (coordinator) | In work (RQ-08/09/10 expansions issued mid-flight) | `~/workspace/uav-sub250g/cad/` (11 files) |
| WS-13 | Aero simulation + design optimization (VLM/lifting-line) | GM (coordinator) | In work | `~/workspace/uav-sub250g/aero_opt/` (`lifting_line.py`, `glauert.py`) |
| WS-14 | `zb-flight-model` reference repo (own math, referenceable) | — | **Proposed only — NOT published; needs CEO approval** | Structure drafted in GITHUB_TRACEABILITY.md §5 |
| WS-15 | Coupon test (physical) | **CEO** | OPEN | — |
| WS-16 | Phase 1 procurement (~$170) | GM | Not started — gated (airframe/power after coupon + TDR) | — |
| WS-17 | TDR adjudication package (twin review vs brief + D-08 ratification) | GM (subagent) | Done 2026-10-13 — record filed, verdict PROCEED WITH ACTIONS, D-08 ratification drafted; **awaiting GM adjudication/signature** | `~/workspace/uav-sub250g/TDR_RECORD.md` |
| WS-18 | A2 iterative design optimization (closed CAD↔sim loop to convergence) | GM (subagent) | Done 2026-10-13 — 4 cycles, converged (<0.5% ×2); winner 6° washout + 25° sweep → 32.40km/77.1min @SM6% (+2.40/+5.1); fidelity fix corrected mid-loop | `~/workspace/uav-sub250g/ITERATION_LOG.md` |
| WS-19 | Verification matrix + FHA + hotel-load measurement plan | GM (subagent) | Done 2026-10-13 — 27 VC rows, FHA 1-pg, 6 RQs flagged for rewrite | `~/workspace/uav-sub250g/VERIFICATION_MATRIX.md`, `FHA.md`, `HOTEL_LOAD_PLAN.md` |
| WS-20 | Design closure: battery hatch (R-17), CG resolution, params.json refactor | GM (subagent) | In work — from converged winner (6°/25°) | `~/workspace/uav-sub250g/cad/` |
| WS-21 | Twin completion: wire model.glb into viewer (single geometry source) | GM | Not started — after WS-18/20 | Web artifact `z-b-digital-twin` (edit) |
| WS-22 | Gate 1 baseline freeze (immutable params snapshot) | GM | Not started — after WS-18/20 | `~/workspace/uav-sub250g/baseline/params_GATE1_v1.0.json` |
| WS-23 | CDR package (baseline, twin, matrix, FHA, iteration log, decision log) | GM | Not started — after WS-17..22 | For GM adjudication |
| WS-25 | Dual airframe-redesign trade studies (GM + Y3k, cross-reviewed, merged recommendation) | GM + CE | In work — drafts by Oct 15, merge Oct 17 (CEO directive RQ-27, confirmed 2026-10-13) | Briefing sent 2026-10-13 |
| WS-24 | `zb-flight-model` repo assembly (HELD UNPUBLISHED) | GM (subagent) | Not started — after WS-18 | `~/workspace/uav-sub250g/zb-flight-model/` (pending) |

**Closure rule:** no WS row moves to Done without acceptance evidence reviewed against its brief. WS-12/13 close only after the closed-loop demonstration (RQ-09.3) is evidenced.

---

## 3. Decision log

| ID | Date | Decision | Rationale | Criticism applied | Status |
|---|---|---|---|---|---|
| D-01 | 2026-10-12 | Gate 0 branch: sub-250g, 1m±25%, hybrid airframe | Regulatory freedom + efficiency + quiet + simplicity | Gate process | Locked |
| D-02 | 2026-10-12 | 1-hour motor-glider concept scrapped (kit retained, not a constraint) | Too heavy for the new direction | — | Locked (superseded concept) |
| D-03 | 2026-10-12 | Sweet-spot geometry: 0.90m span, 0.20m chord, rectangular, 8 identical ribs | ~9% range traded for 4.4 m/s stall, quiet cruise, one-rib simplicity, weight margin | Parametric sweep (7 configs) | Locked, with margin |
| D-04 | 2026-10-13 | Funding $1K → $1.69K → **$10K** (project Z!B) | CEO appropriation | — | Locked (latest supersedes) |
| D-05 | 2026-10-13 | **PoC flies 0g payload**; ≥30g requirement moves to product/family instances | CEO call; energy-limited not weight-limited; 46g margin unlocked | Coordinate review | Locked |
| D-06 | 2026-10-13 | **MH60 replaces PW75** (PW75 has no obtainable data anywhere) | Only verifiable Re≈100k polar + gentle stall + trims on our planform (−6° elevon); 30.0km/72min within 3% of Gate 1 claim | Trade study, multi-candidate | Locked |
| D-07 | 2026-10-13 | Platform target: **bell-spanload wing**; PoC pathfinder: MH60 baseline; family carrier: **tandem**; BWB = variant; conventional = fallback; box/annular killed | 16-source literature track; proverse yaw flight-validated (NASA); win conditions checked vs our operating point | 4 rounds/candidate, converged | Locked |
| D-08 | 2026-10-13 | Twin v1 scope: **E1 + E3 folded in, E2 parked** | E1/E3 serve the PoC directly; E2 is a family-instance evaluator | GM judgment | **PROPOSED — CEO asked "which go in" and never answered; needs ratification** |
| D-09 | 2026-10-13 | Gate 2 refinement: 3° washout + 5–6% SM → 31.2km/74min, −3…−4° elevon | Zero-cost (rib stack), recovers trim drag | Trade study §4 | Proposed (adopt at Gate 2 freeze) |
| D-10 | 2026-10-13 | Hybrid airframe demoted **locked → to be studied** | CEO review; honesty over momentum | — | Locked (gated on coupon test) |
| D-11 | 2026-10-13 | 750mAh battery upsize is **low-risk** at PoC margin (no weigh-in contingency) | 46g margin clears the ≥20g gate | Weight budget | Locked |
| D-12 | 2026-10-13 | Scale (~$12) + charger (~$28): **buy** (charger: confirm-then-buy) | Weigh-as-you-go mandatory; LiPo safety non-negotiable | Mini trade studies | Locked |
| D-13 | 2026-10-13 | `zb-flight-model` GitHub repo: structure drafted → **CEO go-ahead confirmed** (chat, 2026-10-13): assemble locally, **private-first** visibility, **MIT** license; public release remains a separate decision. Org `Z-b0101` created manually by CEO (bot wall blocked automated creation); repo created; scaffold pushed 2026-10-13 (21 files + CI workflow added manually by CEO: zb_model package, JSBSim XML, assumptions ledger, tests 8/8 pass) | Consultancy end-state; CEO confirmation (chat 2026-10-13); thread 1a137a44d77f1201 | — | Locked (private) |
| D-14 | 2026-10-13 | Spending authority **ratified**: Contributor $0 / FLM $50 / Sr Mgr $250 / Director $1,000 / GM $2,000 / CEO >$2,000; escalate regardless of $ for architecture/safety/regulatory/claims/envelope changes; no threshold-splitting | Blueprint governance; CEO ratification (chat, 2026-10-13) | — | Locked |
| D-15 | 2026-10-13 | **Model before money**: perfect the twin before prototype spend | CEO intent; $0 errors beat $10 errors beat airframe losses | — | Locked |
| D-16 | 2026-10-13 | Criticism standard: 4 rounds/node, 12 iters @ 11/12 for complex | CEO standing rule (raised twice) | — | Locked |
| D-17 | 2026-10-12 | Review-informed LRU picks (1404/EMAX/SpeedyBee/M100/ES9051/Flash 7040) | Customer reviews, not cheapest listings | Web research | Locked (R-07 still questions the 1404/7″ pairing) |
| D-18 | 2026-10-13 | **TDR → CDR gate structure** for the twin program (pings = GM in chat) | CEO directive | — | Locked |
| D-19 | 2026-10-13 | **CE work plan locked by Y3k acceptance**: CE-01/CE-02 in parallel; independent airframe assessment due end of Oct 15 PDT; joint recommendation merged Oct 17; unresolved items go to CEO together | CE accepted CEO directive (inbox, thread 1a136bc08ae97dfa) | GM reply | Locked |
| D-20 | 2026-10-13 | **ArduPlane pinned to Plane-4.7.1** (tag Plane-4.7.1, tag id dbe7921, stable 2026-09-04) for SITL + SpeedyBeeF405WING target; fallback Plane-4.6.3; revisit on 4.7.2 or Gate 1 freeze | Y3k concurred (no objection, conditional); GM adjudicated | 4-round (Claude's 4 attacks + GM adjudication rounds) | Locked |
| D-21 | 2026-10-13 | **Dependency & ECD workflow adopted as protocol §16 (v2.6)**: B1/B2/B3 levels, in-body register + Drive weekly snapshot (distribution), 1-business-day ECD replies (same-day in GM-declared crunch windows), slip-vs-miss distinction, evening+morning follow-ups, two-silent-miss escalation (CE→GM 4h recovery plan; GM→CEO in chat), DEV_TRACKER as system of record | Claude proposed; Y3k concurred no-dissent; GM adjudicated (window closed early on reviewer concurrence) | Thread 1a137f91d7428206 | Locked |
| D-21 | 2026-10-13 | **Adopt dependency/ECDs workflow as protocol §16 (v2.6)**: B1/B2/B3 dependency levels, per-owner [ACTION] request threads, ECD reply discipline (1 business day / crunch same-day / URGENT same-day), slip-vs-miss, two-miss escalation, delivery-cites-path closure; working register = in-body thread table, weekly Drive snapshot labeled "working view", durable record in DEV_TRACKER via GM; 4h blocker SLA coexistence noted | DE proposal (thread 1a137f91d7428206, 2026-10-13), Y3k no dissent (review 1a137fa4cf327970), sheet v0.3 ECDs confirmed (C3/C4 EOD Oct 15 PDT); early closure: window is a max, only named reviewer responded explicitly | 4-round adjudication: steelman defer/reject (rebutted — explicit no-dissent, delay adds nothing); break attempts (§16.4↔SLA ambiguity → cross-ref added; §16.2 durable-record gap → DEV_TRACKER line added); re-verified vs proposal/feedback/sheet v0.3; overreach check ($0, one-edit reversible, process-minimalist endorsed) — all converged on adopt + 2 consensus refinements | Locked |
| D-22 | 2026-10-13 | **GitHub org model: Z-b0101 owners = Youssef + Claude; Y3k = Member/Write.** Invite of `zib-ce-claude` as Owner in flight | CEO decision (chat, 2026-10-13) per pre-compaction program record (main-agent note; chat evidence held by main agent) — relayed to GM in [URGENT] thread 1a1388a059e2c261; GM correction msg 1a1388f111f4de5d supersedes the 20:57 staged repo-admin recommendation | Program record, not re-derived | Locked — **execution open**: invite acceptance + Claude GitHub app approval (owner click) unverified |
| D-23 | 2026-10-14 | **Parts spend authority: GM may spend up to $500 on prototype parts; anything above needs direct CEO approval.** LiPo charger on hand (not bought) | CEO (chat, 10:35 PT) | — | Locked |
| D-24 | 2026-10-14 | **CEO does the hands-on work** (coupon, bench, build) using agent-written cards; MfgE seat = option A (AI agent writes procedures, CEO executes) | CEO (chat, 10:35 PT) | — | Locked |
| D-25 | 2026-10-14 | **TDR closed: proceed** (verdict "proceed with actions" per TDR_RECORD §6); CDR entry now waits only on measured discharge curve + hotel load | CEO (chat, 10:35 PT) | TDR_RECORD | Locked |
| D-26 | 2026-10-14 | **P-11 closed:** the 7:49 PM "Sign in with Google" on the company GitHub was the CEO himself, not an anomaly | CEO (chat, 10:35 PT) | — | Closed |
| D-27 | 2026-10-14 | **CEO flies the maiden.** Field and date TBD before Gate 5 readiness review | CEO (chat, 10:35 PT) | — | Locked |
| D-28 | 2026-10-14 | **Share the investor status board and twin viewer** (CEO shares from each page's Share menu; agents cannot change sharing) | CEO (chat, 10:35 PT) | — | Locked — CEO action |

---

## 4. Artifact & document index

### Web artifacts (hosted; no local file path)
| Artifact | Slug | Status |
|---|---|---|
| Airframe Design Model | `airframe-design-model` | Done — verified vs hand calcs |
| Project Z!B Hub | `project-z-b-hub` | Done |
| Z!B Digital Twin | `z-b-digital-twin` | In work — TDR pending |

### `~/workspace/your_files/` deliverables
| Path | What | Status |
|---|---|---|
| `gate1-uav-design-definition/gate1-uav-design-definition.pdf` | Superseded 1m motor-glider Gate 1 | Archived (superseded by D-02) |
| `gate1-ux-wing-design-definition/*.pdf` | Gate 1 design definition, 9 pages | Done |
| `gate1-ux-wing-design-definition-docx/*.docx` | Editable review copy | Done |
| `gate1-ux-wing-design-definition-landscape/*.pdf` | iPhone-12 landscape reading copy | Done (restructure cancelled on CEO stop) |
| `poc-math-logic-backup-slides/*.pptx` | 12 backup math/logic slides (federated assessment) | Done — hotel-power asterisk + self-corrections inside |
| `zb-org-blueprint/Z!B Org Blueprint & SOP.md` | Company blueprint + FLM→IC SOP | Done — 2 ratifications pending |

### `~/workspace/uav-sub250g/` studies & budgets
| File | Status |
|---|---|
| `RISK_REGISTER.md` | Living — **stale vs decisions (see §8 gaps)** |
| `WEIGHT_BUDGET.md` | Current (PoC 0g, 204.3g/46g) |
| `BUDGET.md` | Current ($10K funding, ~$361 est) |
| `MATERIALS.md` | Current (audit 2026-10-12) |
| `AIRFOIL_TRADE.md` | Done (MH60 adopted) |
| `WILD_CONCEPTS.md` | Done (E1/E2/E3 proposal) |
| `AIRFRAME_ARCHITECTURES.md` | Done (ranking converged) |
| `GITHUB_TRACEABILITY.md` | Done (55/40/5; repo drafted) |
| `DEV_TRACKER.md` | This file — living |

### Models & geometry
| Path | Status |
|---|---|
| `jsbsim/zb_wing.xml`, `jsbsim/engine/zb_thrust.xml`, `jsbsim/engine/zb_nozzle.xml` | Alpha v0.1 — loads clean, reconciles with trade study; needs flight-test calibration |
| `jsbsim/MODEL_NOTES.md` | Current (assumptions, 7-item calibration list) |
| `cad/` (11 files: rib/skin/spar/elevon STLs, `build_cad.py`, `parametric.py`, `params.json`, `verify_cad.py`, `mh60.dat`) | In work — RQ-08/09 expansions in flight |
| `aero_opt/` (`lifting_line.py`, `glauert.py`) | In work |

---

## 5. Action item register

### CEO-owned
| ID | Item | Status |
|---|---|---|
| AI-01 | **Coupon test**: weigh Depron sheet, print one rib, pull-test glue joints | OPEN |
| AI-02 | **TDR review**: (1) architecture coverage, (2) assumptions to challenge, (3) greenlight toward CDR | OPEN — pinged 2026-10-13 |
| AI-03 | `zb-flight-model` repo **publication approval** (org/name/license/scrub) | OPEN |
| AI-04 | **Spending-authority ratification** (>$2,000 → CEO) | OPEN |
| AI-05 | **E2 tandem-mode** inclusion decision (currently parked) | OPEN |
| AI-06 | **Payload type** for family instances (camera / FPV / sensors) | OPEN |
| AI-07 | Confirm **3D-printer access** | OPEN |
| AI-08 | Confirm **charger + scale ownership** (buy ~$40 if missing) | OPEN |

### GM-owned
| ID | Item | Status |
|---|---|---|
| AI-09 | CAD: full subsystems + wiring + sim-capable closed loop (RQ-08/09) | In work (coordinator) |
| AI-10 | Aero optimization + closed-loop demonstration | In work (coordinator) |
| AI-11 | TDR actions close-out | Blocked on AI-02 |
| AI-12 | CDR package assembly | After AI-11 |
| AI-13 | Verify `MODE_AUTOLAND_ENABLED` + `HAL_LOGGING_ENABLED` in F405 WING MINI hwdef (audit F2) | Closed 2026-10-13 — both flags ABSENT from SpeedyBeeF405WING/hwdef.dat (master) and both minimize includes (verified against official ArduPilot repo); at firmware build defaults, neither board-disabled nor board-enabled |
| AI-14 | R-07 motor/prop resolution plan (pre-procurement analysis + wattmeter test design) | Open |
| AI-15 | L1 period + TECS tuning starting points for 7 m/s 204g wing (audit F3) | Open |
| AI-16 | `AP_BattMonitor` + ArduPlane failsafe path verification (audit F1) | Open |
| AI-17 | GM-side airframe-redesign trade study (mass sensitivity, washout manufacturability, fallback geometry, weight-budget deltas) → to Y3k by Oct 15 PDT | In work (per CEO directive RQ-27) |
| AI-18 | Cross-review of Y3k airframe assessment + merge joint redesign recommendation by Oct 17 | Scheduled |

---

## 6. Gate register

| Gate | Entry criteria | Exit criteria | Status |
|---|---|---|---|
| Gate 0 — Mission integrity | — | Target user, mission, hard constraints, family logic, success measures | **PASSED 2026-10-12** |
| Gate 1 — Digital baseline | Gate 0 pass | Controlled geometry, mass/CG model, aero basis, propulsion/energy model, risk + cost baselines | **Reviewed 2026-10-13** — geometry locked w/ margin; performance "to be optimized"; CG from subsystems integration |
| **TDR — Twin Design Review** | Interactive twin built | CEO answers: architecture coverage? assumptions to challenge? greenlight to CDR? | **PENDING CEO REVIEW** (pinged) |
| **CDR — Critical Design Review** | TDR actions closed; **measured 3S discharge curve** (bench test) | CEO go/no-go on prototype spend | Not entered |
| Gate 2 — Model credibility | CDR pass | Equation traceability, independent checks, sensitivity/uncertainty, arch comparisons, tests, residual gaps | Not entered |
| Gate 3 — Physical calibration | Gate 2 pass | Coupon, rib/bond tests, component weights, bench data, model updates | Not entered |
| Gate 4 — Prototype authorization | Gate 3 pass | Closed interfaces, mass margin, CG range, control authority, test plan, Class D package | Not entered — **no major prototype spend before this** |
| Gate 5 — Flight learning | Gate 4 pass | Readiness review, test cards, flight data, anomaly disposition, calibrated model | Not entered |
| Gate 6 — Productization | Gate 5 pass | Repeatable build, verified envelope, ops concept, supplier plan, claim-evidence matrix | Not entered |

---

## 7. Correction & issue log

| Date | Correction / issue | Resolution |
|---|---|---|
| 2026-10-12 | Carbon spar mischaracterized: "5mm tube ~7 g/m" — real 5mm tube is 11–20 g/m | Switched to 4mm tube (8.8 g/m); bending margin restated 6× → **3.3×** (MATERIALS.md) |
| 2026-10-12 | Fully-printed 1m airframe estimate too optimistic (150–210g) | Corrected to ~200–300g; rejection strengthened |
| 2026-10-12 | 1404 motor (sold for 2.5–4″ props) paired with 7″ prop — mismatch flagged | **Still open** — R-07; wattmeter test required before buy |
| 2026-10-13 | PW75 airfoil had no obtainable coordinates/polar/data anywhere | **Retired**; MH60 adopted (AIRFOIL_TRADE.md); R-16 opened & retired |
| 2026-10-13 | "TECS from the maiden" — TECS is NOT active in FBWA (auto-throttle modes only) | Standing correction: always name the mode (audit §3) |
| 2026-10-13 | "RTL and autoland" conflated — default RTL **loiters**; autoland is separate & build-flag-gated | Standing correction; verify hwdef before depending on autoland |
| 2026-10-13 | SIM_Plane disclaims aero accuracy | Twin fidelity must come from JSBSim backend (authored: jsbsim/) |
| 2026-10-13 | 30km/72min quoted without hotel power — **propulsion-only upper bound** | Asterisk disclosed: 1W hotel → 24.9km/59min (sensitivity case, not forecast) |
| 2026-10-13 | WEIGHT_BUDGET.md allocated-targets table stale (30g payload / 233–236g) after PoC 0g call | **Fixed** (203g / 206g, 47g / 44g margin) |
| 2026-10-13 | Twin first cut was a program control room, not the interactive twin | Re-steered via artifact edit; interactive twin built; TDR pinged |
| 2026-10-13 | Stall speed restated with MH60's real Clmax (4.3 → ~4.0 m/s) | Corrected in trade study & JSBSim (3.96 m/s) |
| 2026-10-13 | Budget $1K → $1.69K → $10K; payload 30g → PoC 0g | Logged as D-04 / D-05 (supersession, not error) |
| 2026-10-13 | Gate 1 landscape-doc restructure started, then CEO said "Stop" | Cancelled mid-build; current copy stands |
| 2026-10-13 | Program plan v1 presented the design phase as linear — the iterative aspect was missing | **Corrected** per CEO catch: explicit iterative design optimization via twin simulation (§9, Phase A2) with convergence criteria, before Gate 1 freeze |
| 2026-10-13 | **F2 (DE finding):** verify_cad.py hard-codes geometry (chord 200, hinge 150, half-span 450, spar at 60mm, rib stations) and defaults washout to 2.0° when the key is missing — a second hard-coded 2° in the CAD baseline that would not follow a parameter change | **Open** — flagged for CE-01/CE-02 single-source closure; no edits made (observation only) |

---

## 8. Risk pointer

The risk register lives at `~/workspace/uav-sub250g/RISK_REGISTER.md` — 16 risks (15 open, R-16 retired). It is **not duplicated here**; this tracker records risk *deltas* only when they occur.

**Known register staleness (flagged, not yet fixed):**
- R-05 text still cites "~17g margin" and pre-PoC-0g framing — actual PoC margin is 46g.
- R-12 / R-14 still frame payload as a PoC decision — payload is now a family-instance decision.
- R-09 (HotRC receiver) was flagged for reassessment vs the clean-sheet design — still open.

---

## 9. Program plan (baseline 2026-10-13, corrected per CEO catch)

**Phase A — digital program (GM, ~2 weeks)**
- A1. TDR adjudication (GM authority): twin reviewed vs brief, actions closed.
- A2. **Iterative design optimization via twin simulation** — the design phase is iterative, not linear. Each cycle: parameters → CAD regen → aero sim (VLM on CAD geometry) → mission sim (twin, incl. Monte Carlo) → evaluate vs objectives → parameter update. Convergence: range delta <0.5% for two consecutive cycles, or 6 cycles max. Every cycle logged with deltas; the loop machinery was already demonstrated end-to-end. Iteration 1 (washout 2°→4°, +1.82km) and the bell-twist evaluation (rejected on range, kept for the yaw thesis) are already on the record.
- A3. Design closure: battery hatch geometry + clash re-check, CG resolution (ballast vs layout), params.json refactor (design vs derived).
- A4. Twin completion: model.glb wired into the twin viewer (single geometry source), JSBSim XML regenerated at the frozen geometry.
- A5. Gate 1 baseline freeze: immutable params snapshot, versioned.
- A6. Verification & safety: verification matrix populated (SAE CA-05), one-page FHA, hotel-load measurement plan.
- A7. CDR (GM authority): full package, gate record.
- A8. Repo packaging: `zb-flight-model` assembled, held unpublished.

**Phase B — physical program (CEO, at CEO pace)**
- B1. Coupon test (gates the airframe build) → B2. Procurement Ph1 → build → Ph1 weigh-in → B3. Procurement Ph2 → avionics → bench tests (wattmeter incl. hotel load, rail, EMI, RC link) → B4. pre-maiden weigh-in → maiden → tuning → B5. flight test campaign (10 autonomous flights, RTL) → twin calibrates L2.

**Critical path:** B1 → B2 → B3 → B4 → B5. All of Phase A runs ahead of it. The washout decision must land before A5 (this week).

---

## Appendix — open tracking gaps found while compiling (2026-10-13)

1. **D-08 was recorded as locked without CEO approval.** The CEO asked "which extensions go in"; the GM folded E1+E3 into the twin on his own authority. The decision is marked PROPOSED pending ratification — it must not be treated as locked in gate packages.
2. **Geometry has three unowned sources of truth.** CAD params, the JSBSim XML (2° washout baked in), and the twin's viewer can silently diverge on the 3°-washout refinement. RQ-09 demands one source; no geometry owner / parameter-freeze process is recorded yet.
3. **The 1W hotel-load figure has no verification owner.** It anchors the deck's asterisk and the twin's Monte Carlo, but AI-13/14/16 cover adjacent bench work — nobody owns measuring the actual avionics draw and promoting it from assumption to data.

---
*Tracker maintained by the GM. Next review: weekly integration review / next gate package.*
| 2026-10-13 | **F5 (DE finding):** aero loop carries its own weight/geometry literals — mission.py W = 2.00 N (204 g), S_REF = 0.18 m², AR_REF = 4.5; 204 g is the XML basis (204.3), not the CAD rollup (209.0). A CE-01 mass change will not reach the optimizer unless fed from the rollup | **Open** — input to CE-01 mass/CG closure; observation only |
| 2026-10-13 | **F6 (DE finding):** CG in the optimization loop is an OUTPUT of the static-margin target (mission.py: x_cg = x_ac − SM·cbar, SM_OPT = 0.06), in the optimization frame, not the CAD CG — the 83 mm vs 128.5 mm datum issue in code form | **Open** — input to the Ask-1 check; observation only |
| 2026-10-13 | **F7 (DE finding):** cad_interface.py duplicates the twist law (twist_at_eta reimplements parametric.WingParam.twist_at) — code-copy divergence risk, same data source (design section of params.json) | **Open** — D-09 washout-loop gap note; observation only |
| 2026-10-13 | **F8 (DE finding):** cad_interface.py hard-codes CAD_DIR = /home/hatch/workspace/uav-sub250g/cad (same absolute path as build_all.py) — blocks the S5 one-run-command goal on any other machine; fix is a path argument | **Open** — DE-owned once repo is the home; observation only |
| 2026-10-13 | **F9 (DE finding):** optimize.py writes grid_coarse.json and does not read params.json — design variables (w, sweep, taper, twist power) flow back to CAD by hand today (D-09 washout loop gap) | **Open** — observation only |
| 2026-10-13 | In-body email file delivery is **not** a byte channel: GM's 18:46 in-body re-delivery (verified pre-transit against Y3k's posted SHA-256) and Y3k's own 18:39 in-body glauert.py paste both failed Claude's receipt-side hash check beyond trailing whitespace (GM copies had none: raw == normalized). GM corrected its 18:46 claim in-thread and re-delivered the five .py files as MIME attachments (msg 1a13821658e32852); long-term canonical path for code = private zb-flight-model repo | **Open** — pending Claude's attachment-side verification + CE confirmation that GM's workspace glauert.py is the controlled copy |
| 2026-10-13 | **F10 (DE request):** DE seat needs GitHub access on Z-b0101/zb-flight-model — currently-linked Claude connector login sees zero repos ("no access" on attach). Claude relayed a CEO chat direction in [ACTION-GM] (20:49) + [URGENT] (20:52) threads. Sequence: (1) GM auto-reply 20:56 (msg 1a1388d9f7598ab6) treated the direction as UNVERIFIED per §11 and staged a repo-admin recommendation; (2) correction 20:57 (msg 1a1388f111f4de5d) superseded both — owner model (Youssef + Claude co-owners; Y3k Member/Write) was already CEO-decided in chat 19:33, exact handle `zib-ce-claude`; (3) **Owner invite to `zib-ce-claude` SENT 20:56** (by zib-gm-oubi; user completed GitHub sudo-code himself); third-party access checked — **no pending app requests**. **21:32: `zib-ce-claude` now shows as admin collaborator on zb-flight-model — invite ACCEPTED, no resend needed.** 22:00: Member invite to `zib-ce-y3k` SENT (by zib-gm-oubi; GitHub receipt msg 1a138c8c1ff39785; 7-day expiry) so Claude can walk Y3k through accept + link. **21:53: Claude confirmed attach from a fresh session — push access, HEAD 42e7778 ("Add CODEOWNERS: review routing (Y3k -> flight model/sim, Claude -> twin/autonomy)"). Four-point gate fully met (a-d); GM replied "done" (msg 1a138d180bed15f6, 22:10). Working rules acknowledged in-thread: branches + PRs, Y3k/GM review, no direct pushes to main, no visibility/licence/member/branch-protection/secret/billing changes without a recorded decision. D-22 (Owner vs repo-admin scope) still awaits CEO's call in chat. Next: divergence_check.py v0.1 + S1 consumer manifest PR on CEO's go. | **Closed 2026-10-13** — grant complete; Y3k member invite pending acceptance (separate) |
