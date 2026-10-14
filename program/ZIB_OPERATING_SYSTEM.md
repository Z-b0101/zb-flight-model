# Z!B Operating System

**Version:** 1.0 · **Date:** 2026-10-13 · **Owner:** GM · **Status:** Living handbook
**Companions (not duplicated here):** Org Blueprint & SOP (STRUCTURE — who decides), this document (BEHAVIOR — how we work), MBSE Framework (method), SAE Alignment (aerospace tailoring), CE Collaboration Process (communication protocol), DEV_TRACKER (system of record).

---

## 1. Purpose & living-document rule

This document is how Z!B works, written down so a new hire on day one and a team of twenty in two years inherit the same discipline. It blends aerospace rigor (ARP4754A/ARP4761, AS9100 configuration thinking) with tech velocity (ADRs, RFCs, blameless reviews) — each practice adopted for a failure it prevents, not for ceremony.

**"Open for improvement" is a mechanism, not a slogan:**
- Anyone — human or agent — can propose a change to this document, in writing, with a rationale and the failure it prevents.
- Every change gets a **trial period** (one gate cycle or 30 days, whichever is shorter) before it becomes permanent.
- **Quarterly review:** the GM puts this document on the integration review agenda; dead rules are deleted, not grandfathered (anti-theater rule, inherited from the MBSE framework).
- Versioned, changelog at the end. If it isn't in the changelog, it didn't happen.

---

## 2. Engineering best practices

Format per practice: **WHAT** · **WHY** (source industry + failure prevented) · **HOW at scale** · **ANTI-PATTERN killed**.

**Requirements discipline.** WHAT: every requirement is numbered, sourced, statused, DAL-tagged, and verifiable as written — "optimize range" is not a requirement until it has an acceptance threshold. WHY: ARP4754A — prevents building the wrong thing confidently and arguing about scope forever. HOW: DEV_TRACKER §1 today; at 5+ people the requirements owner per directorate maintains their slice, GM owns the log. ANTI-PATTERN: hallway requirements that appear in a design review and die in an argument.

**ADRs — Architecture Decision Records.** WHAT: every significant decision is a one-page record: context, options, decision, rationale, challenge history, revisit trigger. Our decision log (DEV_TRACKER §3) formalized. WHY: tech industry — prevents re-litigating settled decisions and losing the "why" when people leave. HOW: GM drafts, adjudicator signs; at 10+ people, ADRs live in version control with the code/models they govern. ANTI-PATTERN: "we decided X" with no one able to say why six months later.

**Traceability RQ → design → verification.** WHAT: every requirement allocates to a component and is discharged by a named verification case; the chain is walkable both ways. WHY: ARP4754A §8.5 — prevents the gap between "we tested things" and "every requirement is verified." HOW: verification matrix today (VC-xxx); at 20 people this becomes the audit artifact a customer or authority reads first. ANTI-PATTERN: test theater — impressive tests that verify nothing required.

**Configuration management & baselines.** WHAT: declared, version-stamped baselines at each gate (params file + geometry + mass + aero basis); changes between gates go through a change record stating what, why, and what re-runs. WHY: AS9100 — prevents two engineers building from two different "currents." HOW: `baseline/params_<GATE>_vX.Y.json` today; formal CM with check-in semantics at ~20 people. ANTI-PATTERN: "final_v2_REAL.json."

**Verification independence.** WHAT: the checker is never the builder — every model, analysis, and test result is reviewed by someone (or some agent) who didn't produce it. WHY: aerospace process assurance + SOP doctrine — prevents confident prose becoming program truth. HOW: GM-enforced today (criticism rounds, independent audits on the consultancy model); dedicated Verification seat at ~10 people. ANTI-PATTERN: self-graded homework.

**The 4-round / 12-iteration criticism standard.** WHAT: every decision node gets ≥4 rounds of steelman-then-try-to-break; complex decisions need 12 genuinely distinct iterations with ≥11 converging. WHY: CEO standing rule, battle-tested across our trade studies — prevents the first plausible answer winning. HOW: unchanged at every scale; the standard is the standard. ANTI-PATTERN: the loudest engineer wins.

**Test before trust.** WHAT: measured beats modeled, always. Basis tags on every number (measured · supplier-rated · literature-derived · calculated · modeled · estimated · unknown); a tag can only move toward "measured" through evidence. WHY: aviation's credibility ladder + the L1/L2 honesty line — prevents a beautiful model authorizing a real spend. HOW: coupon/bench/flight gates today; at scale, no gate passes on modeled-only evidence for anything above DAL E. ANTI-PATTERN: "the sim says it works, ship it."

**Honest numbers.** WHAT: state the number, its basis, its limits, and what would change it — in the same breath. The hotel-power asterisk is the template. WHY: both industries, and the company's identity — prevents mirages surviving until they cost money. HOW: the honesty ledger travels with every external claim, forever. ANTI-PATTERN: the footnote that contradicts the headline.

---

## 3. Smart processes

**RFC / decision flow, scaled.** 2 people: the collaboration process (§4 decision flow) — proposal, explicit adjudication, tracker record. 5+: lightweight RFC docs for cross-team decisions, 48h comment window, dissent on record. 10+: RFCs get an owner and a decision log per directorate. The shape never changes: proposal → challenge → explicit verdict → record. What scales is the tooling, not the discipline.

**Review SLAs.** Every review states its window (default 48h). Silence is never consent — no response escalates, it doesn't approve. Prevents decisions dying in inboxes and the slow yes.

**Definition of done.** A workstream is done when its tracker row closes against acceptance evidence — not when the builder says so. Prevents 90%-done forever.

**Gate discipline (TDR/CDR generalized).** Every gate has entry criteria, a review, and exit criteria recorded before the next phase starts. Gates review *evidence against criteria*, not effort. Prevents momentum authorizing spend.

**Onboarding standard.** Every hire gets, on day one: role charter + authority boundaries, the current baseline with known inconsistencies stated honestly, first work packages, a ramp plan, the reading list in order, and this document. Y3k's onboarding package is the template. Prevents new hires inventing numbers in the dark.

**Single source of truth.** One parameter file, one tracker, one baseline per gate. Any two representations of the same quantity generated from different sources is a defect, not a discrepancy. Prevents the three-source divergence class of failure permanently.

**Communication architecture — what lives where, and how it evolves:**
- *Now (≤5):* inbox = deliberation, calendar = schedule, tracker = record, workspace = truth. One shared inbox, authorship lines, thread-per-decision.
- *~5 people:* split the first role inbox (e.g., engineering@, vendors@) — the single-address trick doesn't survive five authors. Introduce team channels (chat) for ephemeral coordination; keep decisions in email/tracker.
- *~10:* RFC tooling (tracked docs, not threads) for cross-team decisions; inbox becomes external + escalations.
- *~20:* the tracker graduates to a real requirements/CM tool (per MBSE migration triggers); the *protocol* — explicit adjudication, dissent on record, silence-isn't-consent — survives the tooling change. Tools migrate; behavior doesn't.

---

## 4. Ethical guidelines

**Safety over schedule.** State real risk plainly — never minimize it to hold a date, never inflate it to buy cover. At 5 J the honest classification is usually "no safety effect"; say so explicitly, and name the one combination that isn't (launch phase, people close). Prevents both recklessness and safety theater.

**Regulatory honesty.** The sub-250g discipline is a design constraint, not a loophole to game. We don't creep the scale, don't misdeclare mass, don't fly where we shouldn't. If a future instance needs certification, we say so and do the work. Prevents the company becoming a cautionary tale.

**Truth in claims.** No vaporware, no fabricated data, no renders presented as flights — ever. A claim without evidence is labeled as a claim. Prevents the slow rot of credibility that kills hardware startups.

**Non-punitive reporting.** Raising a concern is always safe; hiding one is the violation. Anyone — intern, agent, vendor — can flag a safety or integrity concern without blame, and the flag gets a written disposition. Aviation's ASRS model: the system learns from near-misses only if reporting them is safe. Prevents the silence that precedes accidents.

**Environmental care.** Quiet, low-impact aircraft, flown in appropriate places. We minimize noise and disturbance as a design objective (RQ-03), not a PR line. Prevents us becoming the nuisance that gets the airspace closed.

**Responsible autonomy.** Geofenced, line-of-sight, failsafe-configured operations. Autonomous capability is exercised inside envelopes we've earned through testing, not beyond them. Prevents the flyaway that ends the program.

**Privacy.** Cameras and sensors point at our test objectives, not at other people. If a family instance carries imaging, privacy impact is a design input from day one. Prevents creeping surveillance by accident.

**Dual-use awareness.** We build tools for peaceful, productive uses. We stay alert to misuse potential, we don't build weapons or weapon-enabling features, and we walk away from customers who want them. Prevents the "we didn't think about it" defense.

**Credit & IP.** Credit by default — authorship on everything, weekly credits, no idea laundering. Company IP is respected and protected; open-source licenses are honored as written — ArduPilot's GPL-3.0 copyleft and the MAVLink licensing flags are already on record and go through legal review before any product step. Prevents both plagiarism and license contamination.

---

## 5. Culture

**Disagree and commit, with dissent on record.** Argue hard in the deliberation; once adjudicated, execute fully. The dissent stays visible — being overruled is not being erased. Prevents both groupthink and quiet sabotage.

**Blameless postmortems.** When something fails, we ask what in the system allowed it, not who to punish. The output is a process fix, not a verdict on a person. (Non-punitive reporting's twin.) Prevents the cover-up reflex.

**Credit by default.** Name who did the work, where the work happened. Prevents the quiet resentment that rots small teams.

**Ask-for-help norm.** Check the process and memory first, then ask — never guess forward alone. Asking is competence, not weakness; guessing is the expensive option. Prevents confident errors compounding.

**The honesty line as identity.** "Validated model, not a twin — until the data says so" isn't a disclaimer, it's who we are. We would rather be precisely uncertain than impressively wrong. Prevents the entire category of self-deception.

---

## 6. Scale ladder — what explicitly changes, and what triggers it

Headcount is a proxy; the **triggers** are the real tripwires. When a trigger fires, the change happens — waiting for a round headcount is how process debt accrues.

**~5 people — the inbox splits.**
- Triggers: two authors can't triage one inbox without stepping on each other; a decision thread has >3 active participants; external mail volume exceeds internal.
- Changes: first role inboxes (engineering, vendors); team chat for ephemeral coordination (decisions stay in email/tracker); lightweight RFC docs replace long decision threads; per-directorate tracker slices with GM owning the rollup.

**~10 people — verification becomes independent.**
- Triggers: the GM is checking work they also directed; a gate package has >50 verification cases; anyone says "who verified this?" and the answer is a name that built it.
- Changes: dedicated Verification seat (checker ≠ builder, structurally); safety review board lite (monthly: FHA review, incident/near-miss dispositions, DAL re-checks); ADRs move into version control alongside models.

**~20 people — formal configuration management.**
- Triggers: requirements exceed ~200; concurrent variants need automated impact analysis; a customer or authority asks "show me your QMS"; merge conflicts in the parameter file.
- Changes: AS9100-lite QMS (documented, audited, still tailored — certification only if a customer demands it); real CM with check-in/check-out; the MBSE migration triggers fire (requirements DB, PLM); the behavior in this document doesn't change — the tooling finally catches up to it.

**What never changes with scale:** the criticism standard, the honesty line, non-punitive reporting, silence-isn't-consent, dissent on record, credit by default, and the anti-theater rule. If a practice can't survive growth, it wasn't a practice — it was a habit.

---

## Changelog

- **v1.0 (2026-10-13):** Initial issue. Blends ARP4754A/ARP4761 tailoring (SAE_ALIGNMENT.md), AS9100 CM thinking, ASRS non-punitive reporting, ADRs/RFCs, blameless postmortems, and the existing MBSE framework, collaboration process (v2.2), and org blueprint. Written for 2 people, laddered to 20+. Next review: quarterly, or when any scale trigger fires.
