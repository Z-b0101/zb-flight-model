# Alpha0 reconciliation (CE-01 gate c): CLOSED by root cause

| | |
|---|---|
| Owner | Claude (GM/DE), 2026-10-14 (due Oct 15 12:00 PT; done early) |
| Question | The record quotes a zero-lift angle of **−3.07°** (`program/reviews/JOINT_REPORT_GM_SECTIONS.md` line 19, "VLM (MH60 camber + washout)"). The corrected twin gives a different value. Which is right, and does anything depend on it? |
| MBSE | Oubi verifies (his half of the item) |

## Finding

**The −3.07° record value is the twin's own pre-fix output, produced while the twist sign was wrong.**

On 2026-10-14 we found that `twin/vlm.py` modelled the 6° washout as 6° of **wash-in**; the surface slope used `camber − tan(twist)` instead of `+`. The joint-report table was generated before that fix.

Reproduced with today's VLM (`twin/vlm.py`, alpha0 measured on the root chord):

| Case | α0L (root chord) | CL0 |
|---|---|---|
| No twist, no notch | −0.51° | +0.032 |
| **6° wash-in (the old sign error), no notch** | **−3.07°**, matching the record to 0.01° | +0.195 |
| 6° washout (correct), no notch | +2.04° | −0.130 |
| **6° washout + DR-14 notch: FROZEN CE-01** | **+1.69°** | **−0.106** |

**Physical check:** with washout, the tips sit nose-down relative to the root. At root α = 0 the outboard wing therefore makes net negative lift, so the root must sit about +1.7° above zero for the whole wing to make zero lift. **Positive is correct.** The washout moves α0L by +2.55° in total; the notch takes 0.35° back.

**The section value is a different quantity.** The MH60 section's own zero-lift angle (≈ −0.5° on the VLM mean line here) is not the wing's. Comparing a section value with a wing value was a definitions problem layered on top of the sign error.

## What depends on it

- **Nothing in the frozen design or in flight-critical numbers.** Trim, the five checks, JSBSim (`twin/gen_jsbsim.py` takes CL0 and CLα fresh from the VLM) and the mission figures are all computed from the corrected VLM. None of them reads the −3.07° figure.
- **Only documentation:** the joint-report table (historical, dated 2026-10-14 06:00 PT, before the fix). It is superseded by this note, and ZB-ER-001 cites this note.

## Disposition

1. The record α0L becomes **+1.69° (root-chord reference, frozen CE-01)**, equivalent to CL0 −0.106 at root α = 0. −3.07° is retired as a sign-error artefact.
2. **Regression guard added:** `tests/test_alpha0.py` checks that:
   - washout raises α0L (sign guard; would have caught the bug)
   - the 6° wash-in case reproduces −3.07°, which documents the root cause
   - the frozen α0L sits within ±0.1° of +1.69°
3. CE-01 gate (c) is **closed** pending MBSE verification.
