# Z!B Master Organizational Package

**Version:** 1.0 draft · **Date:** 2026-10-13 · **Owner:** GM
**Status: CEO review draft — not distributed to the team.**

---

## (a) Company charter

**What Z!B is.** Project Z!B is a company building a family of quiet, autonomous, sub-250 g fixed-wing UAVs around a reusable digital engineering system. The first aircraft is the proof of concept; the family is the company.

**The PoC-to-family thesis.** The 0.90 m MH60 flying wing PoC proves the *platform* — hybrid construction system, sub-250 g discipline, weight-budget method, digital thread — while flying 0 g payload (CEO call, D-05). Product/family instances inherit the platform and carry the ≥30 g payload requirement. Platform decisions and mission-instance decisions are tracked separately (RQ-15) so the PoC is never silently redesigned into a product.

**The $10K program.** CEO-funded at $10,000 (RQ-07, D-04); the all-in prototype estimate is ~$361 (BUDGET.md) — the program buys learning, not hardware. Spend retires named uncertainties; major prototype capital stays held until Gate 4 (model before money, D-15).

**Leadership.** CEO Youssef (product founder — mission, capital, irreversible choices) → GM Oubi (program integrator — roadmap, gates, budget, cross-functional trades) → Chief Engineer Y3k (technical authority — configuration, aero, structures, verification). Three senior-expert seats are authorized (see §c).

---

## (b) Design philosophy (condensed)

CEO-set; changes only by CEO directive. The decision filter for every trade. Full text: ZIB-DOC-002.

1. **Regulatory freedom first** — the 250 g cap is a hard constraint (RQ-01); the PoC budgets 204 g against it [VERIFY: CAD rollup 209.0 g vs 204.3 g budget — CE-01 open].
2. **Energy over mass** — range comes from stored energy; the PoC is energy-limited, not weight-limited (D-05, D-11).
3. **Experience over peak numbers** — ~9% peak range traded for forgiving stall, quiet cruise, simplicity (D-03).
4. **Simplicity as reliability** — taper rejected at +0.02 km because it killed eight-identical-rib construction (A2 loop).
5. **Margin is a feature** — 46 g mass margin; 3.3× spar bending margin; a priced 5° washout fallback behind the 6° winner.
6. **Stable from flight one** — ArduPlane angle mode from the maiden (RQ-23); gentle-stall MH60 (D-06); 5–8% static-margin basis.
7. **Cheap to crash** — ~$361 prototype on $10K funding; spares priced as expected events, not disasters (D-17).
8. **Honest numbers** — the hotel-power asterisk disclosed, not footnoted away; L1 honesty line held until flight data earns L2.

---

## (c) Organization

**Startup chart (now):** CEO Youssef → GM Oubi → (1) Chief Engineer Y3k (air vehicle engineering) + three senior-expert seats:

1. **Director, Digital Engineering & Autonomy** — full-time search now. Owns the executable thread: CAD, mission analysis, JSBSim, ArduPlane, telemetry; turns provisional models into reproducible software with tests and configuration identity.
2. **Director, Verification, Safety & Flight Operations** — fractional now, full-time before flight. Independent assurance with flight-release authority: a schedule cannot overrule a no-go. Reports to the GM; independent escalation line to the CEO.
3. **Director, Product & Mission** — search now, hire at evidence trigger. Turns customer problems into a controlled product-family roadmap; owns the claim-evidence matrix.

Manufacturing, finance, and sales explicitly deferred (8/12, 6/12, 3/12 on the 12-lens matrix) with revisit triggers. Hiring sequence: seat 1 search + seat 2 fractional engagement in parallel now; seat 3 stays a disciplined search until one mission clears the evidence threshold. Employment mode is staged — accountability seats activate now, payroll follows the gates.

**The blueprint is the scaling target.** The org blueprint's accountability lanes (directors → senior managers → FLM → contributors) with the right-sizing rule (split a seat only when workload, conflict of interest, or review independence requires it) govern growth to 20+. Full source: ZIB-DOC-004 (chart detail: ZIB-DOC-005).

---

## (d) Operating system (condensed)

The behavior handbook — tech velocity × aerospace rigor. Full text: ZIB-DOC-003 (CEO-only/held until distribution plan approved).

**Engineering practices:** requirements discipline (numbered, sourced, DAL-tagged, verifiable); ADRs (every significant decision: context, options, challenge history, revisit trigger); RQ→design→verification traceability; configuration management (declared, version-stamped baselines per gate; change records between gates); verification independence (checker ≠ builder); the 4-round / 12-iteration criticism standard (unchanged at every scale); test before trust (basis tags: measured · supplier-rated · literature-derived · calculated · modeled · estimated · unknown); honest numbers.

**Processes:** RFC/decision flow (proposal → challenge → explicit verdict → record; tooling scales, discipline doesn't); review SLAs (default 48 h; silence is never consent); definition of done (tracker row closed against acceptance evidence); gate discipline (entry criteria, review, exit criteria — evidence, not effort); onboarding template (Y3k's package: charter, authority, baseline with stated inconsistencies, work packages, ramp, reading list); single source of truth (one parameter file, one tracker, one baseline per gate — divergence is a defect); communication architecture (inbox = deliberation, calendar = schedule, tracker = record, workspace = truth — migrates to role inboxes + team chat at ~5, RFC tooling at ~10, real CM at ~20; tools migrate, behavior doesn't).

**Ethics:** safety over schedule; regulatory honesty (sub-250 g is a design constraint, not a loophole to game); truth in claims (no vaporware, no fabricated data — ever); non-punitive reporting (raising a concern is safe; hiding one is the violation); environmental care; responsible autonomy (geofenced, LOS, failsafe-configured); privacy; dual-use awareness (no weapons; walk away from weapon-seeking customers); credit & IP (credit by default; ArduPilot GPL-3.0 / MAVLink flags already on record).

**Culture:** disagree-and-commit with dissent on record; blameless postmortems; credit by default; ask-for-help norm; the honesty line as identity.

**What never changes with scale:** the criticism standard, the honesty line, non-punitive reporting, silence-isn't-consent, dissent on record, credit by default, the anti-theater rule.

---

## (e) SOPs — the collaboration protocol (condensed)

Single company address (zib01011991@gmail.com), two authors — authorship carried in the message (`[GM — Oubi]` / `[CE — Y3k]`), never inferred from the From line. Full protocol: ZIB-DOC-006.

- **Subject tags:** `[ACTION-CE]` / `[ACTION-GM]` (due date first line) · `[DECISION]` · `[REVIEW]` · `[FYI]` · `[URGENT]`.
- **Labels as pipeline states:** `Action/CE` · `Action/GM` · `Decisions` · `Reviews` · `Vendors` · `Program` · `Done`. Handled threads: mark-read + `Done` + archive — the INBOX is the attention list.
- **Thread-per-decision:** proposal (options, recommendation, 4-round criticism summary, cost/risk) → explicit CE adjudication → recorded in DEV_TRACKER same day with thread ID; the closing reply must cite the exact workspace artifact holding the controlled truth (Y3k's rule). Email alone never counts.
- **Silence is not consent:** no response in the review window escalates; it never approves. Dissent and overruled objections stay on the record.
- **External mail:** shared Drafts are the outbox — GM drafts, CE reviews and sends. Draft-only until explicit CE/CEO approval; spending, publication, physical actions always escalate.
- **Artifacts over email:** workspace path is truth; attachments are convenience copies; workspace–attachment disagreement is logged as a defect.
- **Verification:** inbox directives under CEO authorship are unverified until the CEO confirms in chat. The 15-minute watch triages (starred first), handles, files, and reports — silent when nothing new.
- **Weekly note** (Friday): completed, active, decisions, next, blockers — plus the credits line.

---

## (f) Document register

The living master tracker of all controlled documents — see **ZIB-DOC register: `~/workspace/uav-sub250g/ZIB_DOCUMENT_REGISTER.md`**. 28 documents (ZIB-DOC-001…028): charter/philosophy/behavior/structure, the program system of record, methodology and tailoring, the verification and safety evidence, the trade-study record, budgets, the twin (L1), and the held-unpublished reference repo. Items marked CEO-only/held (Operating System, org chart, v2.2 process deltas, flight-model repo) are not distributed to the team until the CEO approves the distribution plan.

---
*Compiled by the GM, 2026-10-13. Condense, don't reinterpret — full sources govern. Awaiting CEO review.*
