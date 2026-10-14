# Z!B Verification Matrix — Phase A

**Date:** 2026-10-13 · **Owner:** GM · **Closes:** SAE CA-05 (verification GAP, §4.6)
**Basis:** ARP4754A §8.5.3 (tailored) · DAL: E for all PoC requirements (SAE_ALIGNMENT.md §6.1 — 204 g, ~5 J, recreational LOS)
**Honesty rule:** most rows are OPEN/PENDING. That is the point of the matrix — it shows what is claimed vs what is evidenced.
**Coverage rule (MBSE §5.5):** a requirement is verified only when its VCs cover it at DAL-E-appropriate rigor — one credible method suffices; "credible" is judged by the checker, not the builder.

Method key: **T** = test · **A** = analysis · **I** = inspection · **M** = modeling/simulation.
Evidence artifacts: `cad/` = CAD + clash check · `twin` = z-b-digital-twin (L1) · `jsbsim` = jsbsim/zb_wing.xml · `mission` = mission model/AIRFOIL_TRADE · bench = wattmeter/bench session (Phase B3) · flight = flight-test campaign (Phase B5).

| VC-ID | RQ-ID | Requirement (short) | DAL | Method + artifact | Pass criteria | Coverage | Status |
|---|---|---|---|---|---|---|---|
| VC-01 | RQ-01 | Sub-250 g AUW (inviolable) | E | T — bench scale, Ph1/Ph2/pre-maiden weigh-ins | AUW ≤ 250 g at every weigh-in (internal alert ≤ 230 g) | Full (planned) | OPEN — design satisfies (204 g); weigh-ins pending |
| VC-02 | RQ-01 | (same) | E | A — WEIGHT_BUDGET.md rollup from params.json | Rollup ≤ 250 g with ≥ 40 g margin | Partial (model) | PASS (model) — 204.3 g, 46 g margin |
| VC-03 | RQ-02 | Span 1.0 m ± 25% | E | I — measure built wing (Ph1) | 0.75 m ≤ span ≤ 1.25 m | Full (planned) | OPEN — design 0.90 m |
| VC-04 | RQ-02 | (same) | E | A — CAD params.json | span = 0.90 m in frozen params | Partial (model) | PASS (model) |
| VC-05 | RQ-03 | Optimize range/efficiency/payload/aero/autonomy; minimize complexity/noise/regs | E | — | — | None | **FLAGGED — not verifiable as written; see §A** |
| VC-06 | RQ-04 | Hybrid airframe (Depron 3 mm skins, 4 mm spar, vase-mode ribs) | E | T — coupon test (CEO, AI-01) | Sheet weighed; rib printed; glue joint pull-tested; results logged | Partial (gates decision) | OPEN — requirement itself "to be studied" |
| VC-07 | RQ-04 | (same) | E | I — build inspection (Phase B2) | Built airframe matches hybrid spec or adopted alternative | Full (planned) | PENDING decision |
| — | RQ-05 | ≥30 g payload (original Gate 0) | — | — | — | — | **SUPERSEDED 2026-10-13 → RQ-06** (no verification) |
| VC-08 | RQ-06 | PoC flies 0 g payload; ≥30 g = family instances | E | I — configuration audit at pre-maiden weigh-in | No payload installed; payload mass = 0 g on scale | Full (planned) | OPEN — locked, budgets updated |
| VC-09 | RQ-07 | $10K funding for Z!B | E | I — funding ledger (BUDGET.md) | Funds appropriated ≥ $10K; spend tracked | Partial | OPEN — locked; ledger not yet audited |
| VC-10 | RQ-08 | CAD: all subsystems + sub-assemblies + wiring | E | I — CAD review checklist + clash report | Every BOM LRU has geometry; harnesses routed; zero unresolved clashes | Full (planned) | IN WORK (coordinator) |
| VC-11 | RQ-09 | CAD sim-capable; parametric; closed CAD↔sim loop; single geometry source | E | T/A — closed-loop demo: params.json → CAD regen → VLM → mission | Divergence check = 0 across consumers; one full loop cycle evidenced | Partial | IN WORK — loop machinery already demonstrated end-to-end once |
| VC-12 | RQ-10 | CAD + aero sim for design optimization | E | M — aero_opt/lifting_line.py, glauert.py | Optimization run completed; results documented vs objectives | Partial | IN WORK (coordinator) |
| VC-13 | RQ-11 | ≥4 criticism rounds/node; ≥12 iters @ 11/12 for complex | E | I — DEV_TRACKER §3 criticism records | Every D-xxx carries its round/iteration log | Partial | **FLAGGED — "complex" undefined; see §A** |
| VC-14 | RQ-12 | Only GitHub-referenceable logic behind flight/monitor/sim/math | E | A — GITHUB_TRACEABILITY.md audit | zb-flight-model repo published; 100% claim-units BACKED or with retirement owner | Partial | IN WORK — 55/40/5; repo NOT published (AI-03) |
| VC-15 | RQ-13 | Perfect the twin before prototype spend | E | I — gate records | No prototype spend before CDR exit | None | **FLAGGED — "perfect" unmeasurable; see §A** |
| VC-16 | RQ-14 | TDR + CDR gates with CEO pings | E | I — gate records + chat pings | TDR actions closed; CDR held; pings delivered by GM | Full (planned) | OPEN — TDR pending CEO review |
| VC-17 | RQ-15 | Platform vs instance decisions tracked separately | E | I — DEV_TRACKER §3 tag audit | Every D-xxx tagged platform or instance | Full (planned) | OPEN — locked; tag sweep not yet done |
| VC-18 | RQ-16 | Reach for help when needing guidance | E | I — guidance-request log at integration review | — | None | **FLAGGED — behavior norm; see §A** |
| VC-19 | RQ-17 | Tech-fella mode: substance over graphics | E | — | — | None | **FLAGGED — style norm, not a requirement; see §A** |
| VC-20 | RQ-18 | Maintain risk register; report deltas | E | I — RISK_REGISTER.md vs DEV_TRACKER §3 | Register current at each gate; deltas logged | Partial | OPEN — register **stale** vs decisions (DEV_TRACKER §8) |
| VC-21 | RQ-19 | Review-informed LRU pricing | E | I — BUDGET.md | Every LRU pick cites customer reviews | Full | SATISFIED |
| VC-22 | RQ-20 | Substantiate claims with research | E | I — traceability audit (MATERIALS.md) | Claims carry sources, not assertion | Full (ongoing) | SATISFIED / ongoing |
| VC-23 | RQ-21 | Org blueprint + SOP | E | I — artifact exists | Blueprint + SOP written | Partial | PARTIAL — written; 2 ratifications pending (AI-04, D-08) |
| VC-24 | RQ-22 | Accessible artifact folder (the Hub) | E | I/T — hub loads, links resolve | Hub reachable; all listed artifacts resolve | Full | SATISFIED |
| VC-25 | RQ-23 | Angle mode from the maiden (mode named) | E | T — SITL + maiden log | Maiden flown in FBWA (logged); TECS only in auto-throttle modes | Full (planned) | OPEN |
| VC-26 | RQ-24 | Document every aspect (DEV_TRACKER) | E | I — integration-review audit of tracker | Maintenance protocol followed; append-only; no rewrites | Full (ongoing) | IN WORK / ongoing |
| VC-27 | RQ-25 | Coupon test (CEO action item) | E | T — CEO bench | Sheet weighed; rib printed; glue joints pull-tested; logged | Full (planned) | OPEN — CEO-owned (AI-01) |
| — | RQ-26 | Spending-authority thresholds | — | — | — | — | **NOT YET A REQUIREMENT — proposed, needs CEO ratification (AI-04)** |

## §A — Verifiability audit (4-round criticism on the RQ set, per RQ-11)

**Round 1 — literal read:** is each RQ stated with a measurable acceptance criterion? RQ-03, RQ-13, RQ-16, RQ-17 fail immediately. RQ-11 and RQ-26 partially.
**Round 2 — method assignment:** can a credible T/A/I/M check discharge it? RQ-03 has no threshold to check against; RQ-17's "never sell soap" has no falsifiable test; RQ-16's "when needing guidance" is self-referential.
**Round 3 — kill attempt on the flags:** tried to keep RQ-17 as verifiable ("peer review of tone") — killed: no pass/fail, no artifact. Tried to keep RQ-16 ("count help requests") — killed: counting requests measures the opposite of the intent (fewer requests could mean mastery *or* silent flailing).
**Round 4 — rewrite proposals (below).** Converged: 3 RQs need rewrite, 2 need operationalization, 1 is not yet a requirement.

### Flags and rewrite proposals

1. **RQ-03 — UNVERIFIABLE as written.** "Optimize range, efficiency, payload, aero, autonomy; minimize complexity, noise, regulatory constraints" has no acceptance threshold, no weights between competing objectives, and "minimize" is unbounded. *Proposal:* decompose into measurable children — e.g. RQ-03a "range ≥ 24 km / endurance ≥ 55 min on 3S 650 mAh with measured hotel load (mission model + flight)"; RQ-03b "stall speed ≤ 5 m/s (mission model + flight)"; RQ-03c "part count ≤ 40 unique parts"; RQ-03d "recreational LOS, no waivers." CEO approval required; until then RQ-03 stays flagged.
2. **RQ-13 — UNVERIFIABLE as written.** "Perfect the twin" has no measurable definition of perfect. *Proposal:* rewrite as "No prototype spend before CDR exit; CDR entry requires TDR actions closed + measured 3S discharge curve" — already the gate criteria (DEV_TRACKER §6). The gates *are* the requirement.
3. **RQ-17 — NOT A REQUIREMENT.** "Tech-fella mode" is a working norm / style directive with no falsifiable test. *Proposal:* move to the SOP's norms section; remove from the requirements log at the next integration review.
4. **RQ-16 — MARGINAL.** Behavior norm, verifiable only indirectly. *Proposal:* operationalize as a weekly integration-review checklist item ("guidance requests this week: __; stuck-silently incidents: __"); verify the *log exists and is reviewed*, not the behavior itself.
5. **RQ-11 — PARTIAL.** "Complex decisions" is undefined, so the 12-iteration trigger cannot be audited. *Proposal:* define complexity trigger = decision affecting ≥2 subsystems OR spend > $500 OR gating a gate. Until defined, verify only the 4-round minimum.
6. **RQ-26 — NOT YET A REQUIREMENT.** Proposed, unratified. *Proposal:* keep in matrix as a placeholder; becomes verifiable (I — spend log vs thresholds) only after CEO ratification (AI-04).

## §B — Coverage summary

26 RQs logged · 1 superseded (RQ-05) · 1 pre-requirement (RQ-26) · 24 active.
Of the 24 active: **2 SATISFIED** (RQ-19, RQ-22) · **1 satisfied-pending-ratification** (RQ-21, partial) · **3 PASS(model) only** (RQ-01, RQ-02 — analysis credit per tailoring §6.5) · **19 OPEN/IN WORK/PENDING** · **6 flagged** (§A).
Highest-leverage closures this phase: VC-11 (closed-loop demo — discharges RQ-09), VC-27 (coupon — gates RQ-04), VC-20 (risk-register currency — RQ-18 is currently failing its own pass criterion).

*Next update: weekly integration review. Rows close only against acceptance evidence, never on prose.*
