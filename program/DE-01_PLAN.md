# DE-01: one source of truth, enforced (one-page plan)

**Owner:** Claude (GM/DE). **Reviewer:** Oubi (MBSE, parameter master). **Closes:** P-5 (plan), P-4 (inherited CE scripts), TDR action AC-TDR-02 (in part).
**Date:** 2026-10-14. **Configuration:** `cad/params.json` design hash `7be168427b4d`.

## Goal
Every number used anywhere in the program comes from `cad/params.json` or is a labeled assumption, and a machine check proves it on every push. This is RQ-09 and MBSE_FRAMEWORK §4.2 with teeth.

## What exists today (this PR)
- `scripts/divergence_check.py` finds the hard-coded copies in `zb_model/` and diffs them against `params.json`.
  - **GEOMETRY** duplicates must match exactly. All 8 pass today.
  - **BASIS** divergences (5) are values that differ because an open CE item hasn't reconciled them yet:

    | Value | Today | Reference | Closes with |
    |---|---|---|---|
    | Mass | 204.3 g | 209.0 g | CE-01 |
    | Stall speed | 3.95 m/s | 4.2 m/s | CE-01 |
    | Oswald efficiency e | 0.78 | 0.896 | CE-01 drag |
    | Neutral point | 95 mm, loop datum | 144.98 mm | CE-02 |
    | Static margin | 6% | 8.26% | CE-02 |

    They are reported, never silently accepted, and each names the item that closes it.
- `tests/test_divergence.py` runs the check in CI (`pytest -q`). A geometry mismatch now fails the build.
- The twin (`twin/` on `twin/v0.1`) already reads `params.json` and prints the design hash. The generated JSBSim model carries the hash in its header.

## Plan
| Step | What | Owner | When |
|---|---|---|---|
| 1 | Merge this PR: divergence check live in CI | Claude; Oubi reviews | Today |
| 2 | CE-01/CE-02 close: the 5 BASIS rows either converge or get a stated tolerance | Claude; Oubi reviews | Fri Oct 16 EOD |
| 3 | **Tolerances decision (P-5)**: BASIS rows become pass/fail against agreed limits. Proposed starting limits: mass ±0.5 g, NP ±2 mm, SM ±0.5 pt, e ±0.02, stall ±0.1 m/s | Claude proposes; **Oubi decides** (parameter master) | After CE-01 freeze |
| 4 | Refactor `zb_model/` consumers to read `params.json` instead of holding literals (F5, F6), so GEOMETRY rows disappear rather than being policed | Claude | Before Gate 1 freeze |
| 5 | Merge `twin/v0.1` to main so the twin is under the same CI | Claude; Oubi reviews | With step 4 |
| 6 | Gate 1 freeze: `params_GATE1_v1.0` with the check green | Claude; Oubi signs | Fri Oct 16 (roadmap Phase 0) |

## P-4 decision: inherited CE aero scripts (`aero_opt/`)
`lifting_line.py`, `glauert.py`, `mission.py`, `optimize.py` and `cad_interface.py` live only in the former GM workspace. They were never in this repo, and they carry findings F7–F9 (a duplicated twist law, a hard-coded absolute path, and `optimize.py` not reading `params.json`).

**Decision (GM/DE, 2026-10-14): retire them from the controlled path.**
- The params-driven twin now produces the controlled aero and performance numbers. It runs the VLM from `params.json`, uses the assumption ledger, reproduces the baseline 5 of 5 within tolerance, and is cross-checked by the 6-DOF run.
- Results already on record from `aero_opt/` (AERO_OPTIMIZATION.md, the A2 baseline 31.86 km / 75.8 min) stay valid as **historical record** and remain the comparison baseline for the twin. They are not re-derived from retired code.
- **One exception, offered to MBSE:** `glauert.py` is an independent lifting-line cross-check, which is exactly the "independent checks" evidence Gate 2 asks for. If Oubi wants it as Gate 2 evidence, he pushes it from his workspace on a branch (MIME and in-body copies are not a byte channel, DEV_TRACKER F-log). It then comes under CM here, with a test against the twin's VLM.
- F7, F8 and F9 close as **moot by retirement**.

## Definition of done
`python3 scripts/divergence_check.py` exits 0 with zero BASIS rows open beyond the agreed tolerances, CI green on main, and the Gate 1 freeze recorded.
