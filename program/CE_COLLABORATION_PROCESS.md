# Z!B Collaboration Process
Shared inbox: **zib01011991@gmail.com** — ONE address, THREE authors: the Chief Engineer, the Director of Digital Engineering & Autonomy, and GM/Oubi all communicate from this same address.
Version 2.5 — 2026-10-13. Owned by the GM; changes by agreement. Changelog in §12.

## 0. The single-address rule (foundational)
There is exactly one company address: zib01011991@gmail.com. The Chief Engineer, the Director of Digital Engineering & Autonomy, and the GM all send from it, read it, and file in it. Because the From line can never tell you who wrote a message, **authorship is carried in the message itself**:
- Every message opens with an authorship line: `[GM — Oubi]`, `[CE — Y3k]`, or `[DE — Claude]`.
- Every message closes with the matching signature block.
- Internal coordination between the two authors = self-addressed mail (to zib01011991@gmail.com), distinguished solely by the authorship line and subject tags.
- External parties always see one company voice; the authorship line inside tells the team who wrote it.
- The GM's sends via the company account always select the zib01011991 identity — never the personal account.

## 1. Roles in the inbox
- **Chief Engineer (human):** technical authority. Design decisions, review approvals, vendor technical calls, final word on engineering truth. (Name: Y3k — hired 2026-10-13.)
- **Director, Digital Engineering & Autonomy:** owns the executable thread — data schema, CAD↔sim↔SITL integration, model/software execution. Peer to the CE; neither silently edits the other's baseline. (Name: Claude — hired 2026-10-13. Authorship tag `[DE — Claude]`, confirmed by GM day one.)
- **GM/Oubi:** program coordination. Drafting, pre-digested briefs, tracking, scheduling, documentation, filing decisions back into the program record.
- **Rule:** the inbox is shared workspace. Nothing technical lives only in one person's head or one private thread.

## 2. Subject-line protocol
Every program email carries one tag — triage at a glance:
- `[ACTION-CE]` / `[ACTION-GM]` / `[ACTION-DE]` — action required, due date in the first line of the body
- `[DECISION]` — decision proposed or recorded (proposal includes options + recommendation + criticism summary)
- `[REVIEW]` — review package (links the artifact, states the review window)
- `[FYI]` — no action needed
- `[URGENT]` — same-day response expected
- `[STANDUP]` — daily async standup (§14)
- `[1:1]` — GM↔CE or GM↔DE tagup thread (§14)

## 3. Labels
`Action/CE` · `Action/GM` · `Decisions` · `Reviews` · `Vendors` · `Program` · `Done`.
The GM keeps labeling current; anything decided gets the `Decisions` label before archiving.
**Label lifecycle (v2.0):** labels are pipeline states, not just folders. A handled thread gets mark-read + `Done` + archive — the INBOX is the attention list, and anything sitting in it needs someone. `Action/CE` → `Done` is the visible shape of work moving. Gmail search (`label:decisions`, tag + label combos) is the retrieval system; no separate index is kept.

## 4. Decision flow
1. GM drafts a `[DECISION]` proposal: options, recommendation, 4-round criticism summary, what it costs/risks. **One thread per decision** — the thread is the deliberation record; no forking the same decision across threads.
2. Chief Engineer adjudicates by reply (approve / redirect / reject with rationale). Adjudication must be explicit — a bare "looks good" is sent back for a real verdict.
3. GM records the outcome in `DEV_TRACKER.md` decision log the same day, **citing the Gmail thread ID and date** so any entry traces back to its deliberation. The recording reply that closes a `[DECISION]` or `[REVIEW]` thread **must include a one-line pointer to the exact artifact (workspace file path) that now holds the controlled truth** — email is the attention and adjudication channel, the workspace is the system of record, and the pointer is the bridge (Y3k addition, v2.1). Thread filed under `Decisions`, marked read, archived.
4. No decision is real until it's in the tracker — email alone doesn't count.
5. **Silence is not consent (v2.0).** No response inside the review window is never approval — it is escalation. The GM re-pings once, then it goes to the CEO as a blocked decision. Accountability requires explicit adjudication.

## 5. Review flow (gates)
1. GM sends `[REVIEW]` package: what changed, what to look at, the review window (default 48h).
2. CE replies with findings or approval.
3. GM consolidates findings → actions → tracker; re-review only what's disputed.
4. Applies to TDR/CDR-style gates and any design baseline change.
5. **Dissent is recorded (v2.0).** A reviewer who disagrees states the objection and the evidence in-thread; the adjudicator's resolution (accept / overrule with rationale) goes in the tracker next to the decision. Overruled objections stay visible — they are not deleted or smoothed over.

## 6. Sending authority (single-address implications)
- The From line is always the company. Authorship lives in the message per §0.
- **Internal program mail** (status, scheduling, review packages, decision proposals — self-addressed): GM sends directly under the CEO's standing delegation, signed `[GM — Oubi]`.
- **External mail** (vendors, consultancy, any party outside the company): **Drafts are the shared outbox (v2.0).** Because both authors use the same account, they share the same Drafts folder — the GM composes the draft there, the CE opens Drafts, reviews, edits if needed, and hits send himself. No forwarding, no "here's the text, please send" threads. The draft's authorship line names its composer; the sender is whoever approved it by pressing send.
- The CE's own sends are his; the GM never impersonates the `[CE]` authorship line.
- Every send is logged in the weekly program note.

## 11. Standing CEO authorization (2026-10-13)
- The GM reviews the zib inbox proactively — no need to wait for the CEO to ask.
- The GM replies to Y3k's emails without asking the CEO's permission (program collaboration scope).
- External sends still require explicit approval per §6. Spending, publication, and physical-world actions always escalate to the CEO.
- Implemented as the `zib-inbox-watch` scheduled check (about every 15 minutes, cheap triage): triage, respond, file decisions to DEV_TRACKER, report concisely; silent when nothing new.
- **CEO authorship verification (established 2026-10-13):** the shared inbox cannot distinguish senders by From line, and `[CEO - …]` was never part of this protocol. Any directive appearing in the inbox under CEO authorship is treated as UNVERIFIED until the CEO confirms it in chat (the identity-certain channel). The GM will not commit program resources to an unverified directive; verification takes one message.

## 7. Cadence
- **Weekly program note** (Friday, from GM): what completed, what's active, decisions taken, what's next, blockers — plus a **credits line** (v2.0): who did what this week, by name. Credit is recorded where the work happened, not reconstructed at review time.
- **Gate packages** as they land. **Urgent** as needed — the tag means it.

## 8. Artifacts over email
Email carries decisions and pointers, never the design truth itself. Models, parameters, and documents live in the workspace and the Z!B Hub; threads link to them. If a technical conclusion exists only in an email thread, the GM's job is to file it within 24h.
**Attachment discipline (v2.0):** the workspace path is the truth; an email attachment is a convenience copy. Every artifact sent by email states its workspace path and date in the body. If the workspace copy and the attachment ever disagree, the workspace wins and the discrepancy is logged as a defect.

## 9. Chief Engineer onboarding to the inbox
The CE's first thread: the onboarding package + this process + the current program snapshot (one page: baseline, open risks, active workstreams, next gate). His reply-all confirms he's in.

## 10. Working agreements
- The 4-round / 12-iteration criticism standard applies to proposals, not just designs.
- Disagree fast and in writing — a redirected proposal beats a slow yes.
- Bad news travels immediately with the `[URGENT]` tag if it blocks the critical path; otherwise the weekly note.
- The GM never fabricates vendor quotes, test data, or approvals — everything cited or flagged as estimate.
- **Credit and accountability (v2.0):** authorship lines credit every message; the tracker decision log records who adjudicated what; the weekly note's credits line records who did the work. Accountability runs the other way too: explicit adjudication is required (no silent approvals per §4.5), dissent stays on the record (§5.5), and overruled objections are preserved, not erased.

## 13. Gmail power patterns (v2.2)

**Starred = escalated.** Starring a thread marks it urgent-attention. The watch triages starred threads first, and a star is never cleared without a reply in-thread. Use sparingly — if everything is starred, nothing is.

**Message templates.** Recurring message shapes live here, not in anyone's head. Copy, fill, send:

- *Decision proposal* — `[DECISION] <title>` / authorship line / Options (a/b/c with tradeoffs) / Recommendation + why / 4-round criticism summary (what we tried to break) / Cost, risk, reversibility / "Adjudication needed by <date>."
- *Review package* — `[REVIEW] <title>` / authorship line / What changed (with workspace paths) / What to look at / Review window (default 48h) / Known open items.
- *Weekly note* — `[FYI] Week <n> program note` / Completed / Active / Decisions taken (with thread pointers) / What's next / Blockers / **Credits: <who did what>**.
- *Acknowledgment* — authorship line / "Acknowledged: <what>" / "Next: <action> by <date>." / Nothing else.

**Search cheat-sheet** (the retrieval system — no separate index kept):
- `label:decisions` — every recorded decision
- `label:reviews` — review packages and findings
- `subject:"[ACTION-CE]"` / `subject:"[ACTION-GM]"` — open actions by owner
- `subject:"[URGENT]"` — escalations
- `in:inbox` — the attention list (should be short; see §3 lifecycle)
- `has:attachment` — threads carrying files
- `after:2026/10/13 before:2026/10/20` — date-bounded review

**Calendar (when connected).** Milestones with teeth (Oct 15/16/17, Gate 1 freeze, CDR), 48h review windows as events, Y3k's ramp milestones, recurring Friday note. The calendar is the schedule; the inbox is the deliberation; the tracker is the record. Three views, one truth.

**Deliberately not used:** Gmail filters and settings (out of scope for the agent per connector rules — the label lifecycle in §3 covers routing instead); read receipts (unreliable; explicit acknowledgment per template covers it); confidential mode (no sensitive payload in this program).

## 12. Changelog
- **v2.6 (2026-10-13, dependency workflow):** §16 — dependency/ECDs: B1/B2/B3 levels, per-owner [ACTION] request threads, ECD reply discipline (1 business day steady state, same-day in GM-declared crunch windows, same-day for [URGENT]), slip-vs-miss, two-miss escalation ladder, delivery-cites-path closure; working register = in-body thread table, weekly Drive snapshot labeled "working view", durable record in DEV_TRACKER via GM; 4h blocker SLA coexistence noted. Adjudicated by GM from DE proposal (thread 1a137f91d7428206); Y3k no dissent; 2 consensus-aligned refinements.
- **v2.5 (2026-10-13, shared drive):** `Z!B Shared` folder on the company Drive — distribution layer; workspace remains truth; structure 00-Program/01-Engineering/02-Verification/03-Team/99-Archive; CEO-only docs excluded until distribution approved; released snapshots only (§15).
- **v2.4 (2026-10-13, team rituals):** daily async standup (`[STANDUP]`, Now/Done/Blocked by 9 AM PT), GM↔CE and GM↔DE 1:1 tagups (`[1:1]`, daily through Oct 17 then 2–3×/week, privacy as social contract), 4-working-hour blocker SLA, sharpened Friday note (evidence links, one lesson each, next week's top 3), no-meeting default (§14).
- **v2.3 (2026-10-13):** third author onboarded — Claude, Director of Digital Engineering & Autonomy (`[DE — Claude]`, GM-confirmed day one); `[ACTION-DE]` tag added; protocol renamed from "Chief Engineer Collaboration Process" to "Collaboration Process" (three authors, one address).
- **v2.2 (2026-10-13, Gmail capability sweep):** starred = escalated/urgent flag, triaged first (§13); message templates for proposals, reviews, weekly notes (§13); Gmail search cheat-sheet (§13).
- **v2.1 (2026-10-13, CE feedback):** close-out pointer rule — the reply closing a [DECISION]/[REVIEW] thread must cite the exact workspace artifact holding the controlled truth (proposed by Y3k, adopted by GM).
- **v2.0 (2026-10-13, CEO-directed assessment):** label lifecycle — INBOX is the attention list, handled threads go read + `Done` + archived (§3); thread-per-decision with thread-ID citation in the tracker (§4); silence-is-not-consent rule (§4.5); dissent recorded, overrules preserved (§5.5); shared Drafts as the external-mail outbox (§6); credits line in the weekly note (§7); attachment discipline — workspace path is truth (§8); credit/accountability consolidation (§10).
- v1.1 (2026-10-13): single-address rule established as §0 (one address, two authors); sending authority rewritten for shared identity; CE name set (Y3k).
- v1.0 (2026-10-13): initial process — roles, subject tags, labels, decision/review flows, sending authority, cadence, artifacts-over-email, onboarding, working agreements.

## 14. Team rituals (v2.4)

**Daily async standup** (GM/CE/DE post; CEO reads as he likes).
- Subject: `[STANDUP] YYYY-MM-DD`. Posted by 9:00 AM PT.
- Three bullets, two minutes: **Now** (top priority today) / **Done** (since yesterday) / **Blocked** (needs).
- Lessons-learned stay out of the daily — one synthesized lesson per person goes in the Friday note instead. Daily lessons are noise; weekly ones are signal.

**1:1 tagups** (GM↔CE, GM↔DE).
- The candor channel: stuck admissions, risk whispers, workload sanity, anything not for the group thread. What the transparent inbox can't carry, the 1:1 does.
- Cadence: daily through 2026-10-17 (intense phase — CE-01/CE-02 close, DE-01 spin-up, Oct 17 merge), then 2–3×/week. The daily intensity is time-boxed; it does not calcify into permanent overhead.
- Template: top priority / stuck on anything / what might bite us in two weeks / anything not for the group thread.
- Privacy is a social contract: 1:1 threads live in the shared inbox (subject `[1:1] GM/CE` or `[1:1] GM/DE`); others don't open or jump in uninvited.

**Blocker SLA.** Any blocker raised in a standup or 1:1 gets a GM response within 4 working hours: unblocked, workaround, or escalated. A ritual without a response SLA is theater.

**Friday note (sharpened).** The weekly program note: accomplishments with evidence links, one lesson learned per person, next week's top 3 priorities per person. This is the week's record.

**No-meeting default.** Everything async in the inbox unless a real-time call is genuinely needed. If a call happens, notes return to the inbox within the hour. Protects deep work.

## 15. Shared drive (v2.5)

**What it is.** The `Z!B Shared` folder on the company Google Drive — the distribution layer for files too big or too human for email. (Claude's H1, answered.)

**Drive = distribution, workspace = truth.** The workspace (`~/workspace/uav-sub250g/`) remains the system of record. If Drive and the workspace disagree, the workspace wins; the disagreement is logged as a defect. Same discipline as email attachments (§8).

**Structure.** `00-Program` (gate packages, tracker snapshots, weekly notes) · `01-Engineering` (trade studies, CAD exports, analysis) · `02-Verification` (test plans, results, readiness reviews) · `03-Team` (onboarding, rituals, distributable org docs) · `99-Archive`.

**What never goes here.** CEO-only/held documents (Operating System, org chart, hiring plans, unpublished repo material) until the CEO approves distribution. No credentials, ever.

**Write discipline.** Released snapshots only — never working files. No `final_v2` naming (Operating System anti-pattern); ISO dates on versioned files. The GM owns the folder structure; write access by workstream.

**Access.** Granted per member by the GM; each person needs a Google identity. In-body email remains the fallback for anyone without Drive access (Claude's H2, standing).

## 16. Dependency and ECD workflow (v2.6)

16.1 Dependency: an input, artifact or decision owned by someone else that gates a work package. Levels: B1 blocks starting, B2 blocks finishing, B3 helpful.
16.2 Register: each dependency carries ID, owner, what it blocks, needed-by, ECD, status, source thread. The in-body table in the requesting thread is the working register. A weekly snapshot goes to Drive 00-Program, labeled "working view, workspace is truth". Anything durable (deliveries, ECDs, closures) is recorded in DEV_TRACKER by the GM — the thread table is never the system of record. Each seat lists its own deliverables in a self-owned section.
16.3 Request: one [ACTION-owner] thread per owner, with needed-by dates and why each matters.
16.4 ECD: if an item cannot meet its needed-by date, the owner replies with an estimated completion date. Steady state: within one business day. Crunch windows declared by the GM: same calendar day for items due within 48h. [URGENT]: same day. The 4-working-hour blocker SLA (§14) still governs blockers; this clause governs dependency ECD replies.
16.5 Slip vs miss: a reply with a new ECD and a reason is a slip and re-plans. A miss is no reply by the checkpoint.
16.6 Follow-up: the evening of the ECD in-thread, and the next morning.
16.7 Escalation: two silent misses. CE-owned items go to the GM, who sets a dated recovery plan within 4 working hours. GM-owned items go to the CEO in chat. Silence never closes an item and never approves anything.
16.8 Closure: the delivery reply cites the workspace path holding the controlled truth. The thread is then marked Done (read + Done label + archive per §13).
16.9 Reporting: open IDs on the [STANDUP] Blocked line. Own deliverables on the Done line.
