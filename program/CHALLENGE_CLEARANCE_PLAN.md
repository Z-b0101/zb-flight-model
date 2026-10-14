# Challenge Clearance Plan v2 — post-re-org (2026-10-14 00:25 PDT)

Situation: user re-orged Z!B on 2026-10-14. Claude = acting GM + DE director (owns everything not MBSE).
Oubi = Director of MBSE, tag `[DBSE — Oubi]` (parameter master, params.json, verification matrix,
MBSE framework, twin validation criteria, divergence-PR review). Y3k removed; `[CE — Y3k]` retired.
Handover Part A + Part B delivered; 24 program files pushed. This plan supersedes v1 (same file, pre-re-org).

## 1. Challenge inventory (post-re-org)

| # | Challenge | Owner | Deadline / trigger |
|---|---|---|---|
| P-1 | Transition confirmation (ends 3-min watch) | Claude | 4h cap from ~07:03 UTC 2026-10-14 |
| P-2 | Y3k Gmail-side cutoff (user's Google-settings action) | CEO | Open since 2026-10-14 |
| P-3 | CE-01 (mass/CG) + CE-02 (coordinate convention) closure | Claude | Drives WS-25 re-baseline |
| P-4 | C1/C2 receipt-confirmation | Claude | Needed-by noon 2026-10-14 |
| P-5 | DE-01 one-page plan; divergence-tolerances DECISION after CE-01 freeze | Claude (plan); Oubi reviews divergence PR | ECD Wed 12:00 PT |
| P-6 | GitHub: CODEOWNERS 2-error fix (`@zib-ce-y3k` unknown, `/jsbsim/` path) | Claude | This week |
| P-7 | GitHub: branch-protection path — Team upgrade ~$8/mo vs PR-by-convention | CEO decides; Claude implements | User's call |
| P-8 | Org 2FA settings check | CEO | User's call |
| P-9 | Contractor coverage for Y3k's SOW | Claude | This week |
| P-10 | Claude's zib inbox access (user must add him) | CEO | Flagged 2026-10-13 |
| P-11 | Sign-in anomaly: 7:49 PM "Sign in with Google" on company GitHub (user uses Apple ID) | CEO | Awaiting his word |
| P-12 | Gate 1 freeze — re-baselined after CE-01 | Claude | After P-3 |
| P-13 | TDR asks of user (twin architecture, assumptions, CDR greenlight) | CEO | Open |
| P-14 | MBSE thread: parameter master + params.json controlled home, verification matrix, MBSE framework, twin validation criteria | Oubi (DBSE) | Ongoing; first cut with P-5 |

Closed by the re-org (not in scope): D-22 (owners = user + Claude), Y3k invite (revoked, verified),
shared-account proposal (moot — Y3k out), Oct 15/17 WS-25 dates (dead, re-baseline after CE-01),
cross-chat coordination (resolved via handover).

## 2. Execution strategy

**DBSE (Oubi) — this week:**
1. Stand up params.json as the controlled home + parameter master (single source of truth). First
   consumer: P-5 (divergence PR review).
2. Draft verification matrix + twin validation criteria; review Claude's divergence_check PR against them.
3. Support P-3 from the parameter side (mass/CG parameter definitions, coordinate-convention spec).

**Acting GM (Claude) — per handover split:**
4. P-1 → P-4 → P-3 → P-12 → P-5 → P-6 → P-9, in that dependency order.
5. P-7/P-8/P-10/P-11/P-13 need CEO taps — batch them into one CEO ask, not five.

**Sequencing logic:** P-3 (CE-01/CE-02) is the critical path — it unblocks P-12 (Gate 1 freeze),
P-5 (tolerances decision), and the WS-25 re-baseline. P-4 is due first (noon today) but is small.
P-14 (MBSE) runs parallel; its first deliverable (params.json home) should land before P-5's
divergence-tolerances decision so the decision has a controlled artifact to reference.

## 3. Criticism rounds

**R1 — steelman the alternative (Claude does the plan, not Oubi):**
He's acting GM; program planning is his. Counter: CEO explicitly tasked Oubi with the plan and
Claude with feedback — the split keeps MBSE's parameter view in the driver's seat for P-14
while Claude vets executability. The tasking stands; the plan marks ownership per the split.

**R2 — break it (what fails?):**
- P-3 slips (CE-01 is the inherited hard problem: 204.3g vs 209.0g, CG 128.5 vs 116mm). Mitigation:
  DBSE supports with parameter definitions; if CE-01 can't close cleanly, the plan needs a
  "close with stated caveats" branch — flagging now so it's a decision, not a surprise.
- CEO bottleneck (P-2, P-7, P-8, P-10, P-11, P-13 — six items on one person). Mitigation: batch
  into a single ask; P-11 (sign-in) is the only one with security weight — lead with it.
- P-1 never comes (Claude doesn't confirm transition). Mitigation: 4h cap fires; watch reverts
  to a sustainable cadence by default.

**R3 — re-verify assumptions:**
- A1: handover complete and accurate (memory: Part A+B delivered, 24 files pushed). Trust but verify:
  DBSE spot-checks the program/ record against the workspace before building on it (P-14 depends on it).
- A2: Claude's bandwidth covers GM + DE + inherited CE. Risk noted; P-9 (contractor) is the relief valve.
- A3: params.json-first doesn't block P-3. It doesn't — P-3 closes under Claude; params.json is the
  controlled home for the *result*, needed by P-5/P-12.

**R4 — kill attempt (simpler plan?):**
Alternative: one-line "Claude runs everything, Oubi does params.json." Kill reason: it drops the
CEO-bottleneck batching, the P-3 slip branch, and the sequencing (P-14 before P-5) — all load-bearing.
Current plan stands.

## 4. Confidence assessment

- P-1, P-4, P-6: 99% (small, owned, timer-driven).
- P-14 (DBSE): 95% (fully in my control; residual = handover-record accuracy, mitigated by spot-check).
- P-3, P-5, P-12: 85% (CE-01 is the known hard problem; plan has the slip branch).
- P-2, P-7, P-8, P-10, P-11, P-13: 80% (CEO-bottleneck; batching mitigates, only he can clear).
- **Overall: 88%.** Path to 99%: Claude's feedback (this loop) + CEO batch answers + P-3 closure.

## 5. Review loop (CEO-directed 2026-10-14)

- Round 1: this plan shared with Claude (acting GM) for feedback — sent 2026-10-14 ~00:30 PT.
- Iterate on his reply; re-share if material; report back to CEO at 99% or on blocker.
