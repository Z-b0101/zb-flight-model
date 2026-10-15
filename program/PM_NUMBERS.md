# Z!B program numbers: single source for status and investor material

| | |
|---|---|
| Owner | PM (`[PM — Claude]`), lane: one plain-language program status view (Constitution Art I.5, Amendment 2) |
| Basis | `main` @86936d4; frozen design hash `479399d88b60` (D-31); unmerged PR #22 @3c1f0ba for CE-03 |
| Status | Draft for STF and MBSE check. **Not a design record**: `cad/params.json` and the freeze record govern. This file only says which number to quote, and where it comes from |
| Labels | **measured** / **modelled** / **provisional** (Law V.1). Nothing on this page is measured yet |

## 1. Numbers to quote

| Quantity | Quote | Label | Source | Checked by PM |
|---|---|---|---|---|
| All-up mass | **233.0 g** | modelled (roll-up) | `program/CE-01_FREEZE.md` §2; `scripts/mass_rollup.py` (flags in §2) | Re-ran the script on @86936d4: 233.0 g, CG 130.32 mm |
| Margin to 250 g | **17.0 g** | modelled | 250 − 233.0 | Arithmetic |
| CG | **130.32 mm** aft of root LE | modelled | as above | Re-ran |
| Neutral point (notched wing) | **141.64 mm** | modelled (twin VLM) | `CE-01_FREEZE.md` §2 | Not re-run |
| Static margin, frozen | **5.66%** | modelled | (141.64 − 130.32) / 200 mm chord | Arithmetic: 5.66% |
| Static margin, as built (CE-03 finding) | **5.25%**, below the 5.5% rule, above the 5.0% floor | modelled, open | `program/TE_PARTS_MASS_CHECK.md` (PR #22, not merged) | Arithmetic: (141.64 − 131.13)/200 = 5.25% |
| Range / endurance at 233 g | **No traceable figure on `main`** | — | Only record-basis values exist (30.4 km / 71.4 min at 211.9 g, `CE-01_FREEZE.md` §3). The ~20 km figure in the inbox is not in the repo | Gap: see §3 |
| Propulsion efficiency | **0.42** | provisional | D-32, `mfg/MOTOR_TRADE.md` | Not re-run |
| Hardware cost | **~$361 project total** ($328 subtotal) | modelled (quotes, not orders) | `program/BUDGET.md` "Total" | Read only |
| CDR / Gate 4 | **Wed Oct 28 / Fri Oct 30** | plan | D-30; `PROTOTYPE_ROADMAP.md` | CEO confirmed availability (D-30d) |
| Bench session B3 | **Mon–Tue Oct 26–27** | plan | `PROTOTYPE_ROADMAP.md` Phase 1 | — |
| First flight | **Nov 10–13**, weather permitting | plan | `PROTOTYPE_ROADMAP.md` | — |

How to quote stability externally, until CE-03 closes: "static margin 5.66% (frozen, modelled); an open finding (CE-03) puts the as-built value at 5.25%, to be closed with the CE-02 and battery review before CDR." This follows the finding's own instruction.

## 2. Superseded numbers still in circulation

| Number | Where it appears | Why it is superseded | Action |
|---|---|---|---|
| 209 g, 41 g margin | 06:00 investor brief (inbox); `CE_ITEM_WASHOUT.md` at old hash `7be168427b4d` | Pre-freeze baseline | Washout file is correctly labelled with its hash, no change. Investor brief: correct via BIZ draft, CEO sends (Art II.3) |
| 221 g | Oct 14 decision record (inbox) | Intermediate value, not on `main` | Correct in the decision record (STF + MBSE) |
| SM 8.3% | Old record | Superseded at CE-01 | Already marked in `CE-01_FREEZE.md` |

## 3. Gaps (PM lane, for the 09:00 tagup)

1. **Range and endurance at the frozen 233 g** have no traceable source on `main`. Ask: STF runs the twin at the frozen basis (hotel load provisional, η 0.42) and commits the output, so BIZ can quote one labelled number. Owner STF; ECD at STF's call.
2. **`program/PROVISIONAL_VALUES.md`** is cited by Law V.2 but is not on `main`. Owner STF; may already be planned.
3. **CE-03** (SM 5.25% as built) is a safety-floor item: the 5.5% design rule. It closes only through MBSE review; no seat can risk-accept it (Law V.6). Owner STF raises, MBSE decides; PM tracks.

## 4. How this file is kept current

PM updates it when a D-number, freeze or merged CE item changes a quoted value, and cites the commit. If this file and a design record disagree, the design record wins and this file is wrong.
