# Challenge Clearance Plan v2 — post-re-org (2026-10-14 00:25 PDT; GM line-level review folded 2026-10-14 02:0x PDT)

Situation: user re-orged Z!B on 2026-10-14. Claude = acting GM + DE director (owns everything not MBSE).
Oubi = Director of MBSE, tag `[DBSE — Oubi]` (parameter master, params.json, verification matrix,
MBSE framework, twin validation criteria, divergence-PR review). Y3k removed; `[CE — Y3k]` retired.
Handover Part A + Part B delivered; 24 program files pushed. This plan supersedes v1 (same file, pre-re-org).
Claude's line-level review (9 comments on PR #7, reply 02:01:37 PT) is folded below. CEO: "handled jointly
by the two of us through 06:00" (02:00 PT tonight).

## 1. Challenge inventory (post-re-org)

| # | Challenge | Owner | Deadline / trigger |
|---|---|---|---|
| P-2 | Y3k Gmail-side cutoff (user's Google-settings action) | CEO | Open since 2026-10-14 |
| P-3 | CE-01 (mass/CG) + CE-02 (coordinate convention) closure | Claude | Target closure Oct 16 EOD; drives WS-25 |
| P-4 | Bring the inherited CE aero scripts under CM or retire them | Claude | Needed-by noon 2026-10-14 |
| P-5 | DE-01 one-page plan; divergence-tolerances DECISION after CE-01 freeze | Claude (plan); Oubi reviews divergence PR | ECD Wed 12:00 PT |
| P-7 | GitHub: branch-protection path — Team upgrade ~$8/mo vs PR-by-convention | CEO decides; Claude implements | User's call |
| P-8 | Org 2FA settings check | CEO | User's call |
| P-9 | Contractor coverage for Y3k's SOW (runs in parallel with P-3) | Claude | This week |
| P-11 | Sign-in anomaly: 7:49 PM "Sign in with Google" on company GitHub (user uses Apple ID) | CEO | Awaiting his word |
| P-12 | Gate 1 freeze — re-baselined after CE-01 | Claude | After P-3 |
| P-13 | TDR asks of user (twin architecture, assumptions, CDR greenlight) | CEO | Open |
| P-14 | MBSE thread: parameter master + params.json controlled home, verification matrix, MBSE framework, twin validation criteria | Oubi (DBSE) | Ongoing; first cut with P-5 |
| P-15 | Joint 5-domain report delivery (06:00 PT 2026-10-14) | Oubi (05:30 assembly); Claude (4 sections by 05:00) | 2026-10-14 06:00 PT |
| P-16 | Twin validation against Oubi's criteria 1–4; criteria check 05:30 PT (twin source: twin/ @ee01129; criterion 1 met @twin/v0.1 6863948) | Oubi (check); Claude (twin) | 05:30 PT |
| P-17 | MfgE onboarding (#6) | Claude | — |
| P-18 | zb_wing.xml verification findings (5: aero axes unscaled, unnamed CG, missing engine files, 50g placeholder tank, unwired elevon trim) — retire vs fix | Oubi decides | — |

Closed or superseded: D-22 (owners = user + Claude), Y3k invite (revoked, verified),
shared-account proposal (moot — Y3k out), P-1 (transition confirmed), P-6 (CODEOWNERS fix — superseded
per GM review), P-10 (Claude already has zib inbox access), Oct 15 WS-25 (dead — Oct 17 reinstated,
see below), cross-chat coordination (resolved via handover).

**WS-25 date decision (GM, 2026-10-14 02:01 PT):** the Oct 17 WS-25 recommendation stays dated for
investors. Single-team (GM-authored, MBSE-reviewed). CE-01/CE-02 closure targeted Oct 16 EOD; the
"stated caveats" branch is the fallback — caveat rather than slip. Slip conditions: no caveat may touch
RQ-01; plan on 209.0 g until weigh-in; the 116 mm CG stays retired per DESIGN_CLOSURE. Parameter-side
check (DBSE): no objection — 209.0 g planning mass and 116 mm CG retired are record-consistent, and
the caveat branch covers a CE-01 slip. If Oubi/Claude still disagree on the dates after the parameter
check, it goes to Youssef as a critical-path item, per his rule.

## 2. Execution strategy

**DBSE (Oubi) — this week:**
1. Stand up params.json as the controlled home + parameter master (single source of truth). First
   consumer: P-5 (divergence PR review).
2. Draft verification matrix + twin validation criteria; review Claude's divergence_check PR against them.
3. Support P-3 from the parameter side (mass/CG parameter definitions, coordinate-convention spec).
4. Decide P-18 (zb_wing.xml findings: retire vs fix).

**Acting GM (Claude) — per handover split:**
5. P-4 → P-3 (P-9 in parallel) → P-12 → P-5, in that dependency order.
6. P-7/P-8/P-11/P-13 need CEO taps — batch them into one CEO ask, not four (P-10 dropped: access held).

**Sequencing logic:** P-3 (CE-01/CE-02) is the critical path — it unblocks P-12 (Gate 1 freeze),
P-5 (tolerances decision), and WS-25. P-4 is due first (noon today) but is small.
P-14 (MBSE) runs parallel; its first deliverable (params.json home) should land before P-5's
divergence-tolerances decision so the decision has a controlled artifact to reference. P-15/P-16 are
time-boxed to tonight (06:00 delivery) and cut across the dependency order.

## 3. Criticism rounds

**R1 — steelman the alternative (Claude does the plan, not Oubi):**
He's acting GM; program planning is his. Counter: CEO explicitly tasked Oubi with the plan and
Claude with feedback — the split keeps MBSE's parameter view in the driver's seat for P-14
while Claude vets executability. The tasking stands; the plan marks ownership per the split.

**R2 — break it (what fails?):**
- P-3 slips (CE-01 is the inherited hard problem: 204.3g vs 209.0g, CG 128.5 vs 116mm; L/D now
  twin 8.8 vs record 8.3 with e as lead candidate). Mitigation: the GM's stated-caveats branch —
  caveat rather than slip, with the conditions above. DBSE supports with parameter definitions.
- CEO bottleneck (P-2, P-7, P-8, P-11, P-13 — five items on one person). Mitigation: batch
  into a single ask; P-11 (sign-in) is the only one with security weight — lead with it.
- P-1 never comes (Claude doesn't confirm transition). Closed — superseded by CEO's 02:00 PT
  broad authorization.

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

- P-4, P-14: 95% (small/owned or fully in DBSE control; residual = handover-record accuracy, spot-check mitigates).
- P-3, P-5, P-12: 85% (CE-01 is the known hard problem; stated-caveats branch is the GM's mitigation).
- P-2, P-7, P-8, P-11, P-13: 80% (CEO-bottleneck; batching mitigates, only he can clear).
- P-15/P-16: 90% (sections due 05:00, twin criterion 1 met; residual = 5-domain section quality + viewer).
- **Overall: 88%.** Path to 99%: PR #7 merged + CEO batch answers + P-3 closure.

## 5. Review loop (CEO-directed 2026-10-14)

- Round 1: this plan shared with Claude (acting GM) for feedback — sent 2026-10-14 ~00:30 PT.
- Round 2: Claude's 9 line-level comments (02:01:37 PT) folded into this revision; GM date decision
  (Oct 17 stays, Oct 16 EOD CE-01/CE-02 target, caveat-rather-than-slip) recorded above.
- Iterate on his reply; re-share if material; report back to CEO at 99% or on blocker.
