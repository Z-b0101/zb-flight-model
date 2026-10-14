# Z!B Federated Operating Model

Status: PROPOSED (2026-10-14), by Claude (DE, acting GM), for review by Oubi (MBSE) and ratification by the CEO.
Directed by: CEO, 2026-10-14 00:46 PT, "a federated approach based on a shared GitHub repository, with critical development program decisions left to the CEO."

## 1. The model in one paragraph

The `Z-b0101/zb-flight-model` repository is the program's single shared home: code, controlled baseline, program record and the decision log. Each seat owns its own domain and merges there after a review from the other seat. Seats coordinate through pull requests and issues, which carry a verified author, instead of a shared mailbox. Critical program decisions go to the CEO, prepared with a recommendation, and are recorded in the repo once he decides. Everything else is decided by the domain owner and reviewed by a peer.

## 2. Domains (federation)

| Domain | Owner | Paths | Reviewer |
| --- | --- | --- | --- |
| MBSE: parameter master, controlled baseline, program record, verification matrix | Oubi (`zib-gm-oubi`) | `/cad/`, `/program/` | Claude |
| Digital Engineering & Autonomy: flight model, sim, mass/CG, structures, twin, autonomy, generators, CI | Claude (`zib-ce-claude`) | `/zb_model/`, `/twin/`, `/autonomy/`, `/.github/workflows/` | Oubi |
| Contractors (one-time agents) | Engaging owner | Branches only | Engaging owner, plus an independent verifier for high-stakes work |

Rules:
- An owner merges in their own domain only after the other seat approves. Nobody approves their own PR.
- A change that crosses domains needs both owners' approval.
- Contractors never merge and never edit the record directly.
- CODEOWNERS routes reviews to match this table.

## 3. Decision tiers

| Tier | Who decides | Examples | How it is recorded |
| --- | --- | --- | --- |
| 1. CEO | Youssef | One-way doors; scope and direction; spend above D-014 lanes; org, access and roles; regulatory strategy; gate exits (TDR, CDR); anything touching flight safety; hiring and standby of seats | Issue labeled `decision:ceo`, then an entry in `program/DECISION_LOG.md` |
| 2. Domain owner | Owner, with peer review | Two-way doors inside one domain: design choices, code, test procedures, tolerances | PR description, plus a log entry if it changes the baseline |
| 3. Routine | Anyone | Fixes, docs, refactors with no behavior change | The PR itself |

When in doubt, the decision goes up a tier. A Tier 2 decision becomes Tier 1 if either seat objects and the two cannot agree.

## 4. How a CEO decision flows

1. The owner opens an issue labeled `decision:ceo` with: the question, options, a recommendation, the cost of delay, and the date it is needed by.
2. The issue is brought to the CEO in chat, batched where possible, so he never has to watch GitHub.
3. The CEO decides in chat, by email, or on the issue.
4. The owner records the decision on the issue, adds it to `program/DECISION_LOG.md` by PR, and closes the issue.
5. Until he decides, work that depends on it waits. Silence is not consent (Operating System §3).

## 5. Where things live

| What | Where |
| --- | --- |
| Code, baseline, program record | The repo |
| Work items, blockers, dependencies | GitHub issues, with domain and status labels |
| Engineering review and findings | PR reviews and comments |
| Decisions | `decision:ceo` issues and `program/DECISION_LOG.md` |
| CEO conversation | Chat with each seat |
| Shared inbox | External mail, and a one-line pointer to a PR or issue when a seat needs attention fast |

The shared inbox stops being the place where engineering is deliberated. GitHub identities replace authorship tags, which removes the shared-sender risk behind S1 (the unattributed 23:00 UTC message).

## 6. Labels

`domain:mbse`, `domain:de`, `decision:ceo`, `decision:owner`, `blocked`, `risk`, `contractor`.

## 7. Limits and how they are covered

- Branch protection is not available on the current plan, so the review rules in §2 hold by convention until the CEO decides on the GitHub Team upgrade.
- The CEO is an org owner and can override anything in the repo. This model governs how the seats work, not his authority.
- Decisions made before this model stay where they are recorded (DEV_TRACKER §3). The new log starts from ratification.

## 8. Adoption

1. Oubi reviews this document.
2. The CEO ratifies it, and that becomes the first entry in `program/DECISION_LOG.md`.
3. Labels are created and CODEOWNERS is updated to §2.
4. Open items from the transition plan are moved into issues.
