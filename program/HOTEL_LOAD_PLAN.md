# Hotel-Load Measurement Plan — promoting 1 W from assumption to data

**Date:** 2026-10-13 · **Owner:** GM · **Closes:** DEV_TRACKER appendix gap #3 ("the 1 W hotel-load figure has no verification owner")
**Why it matters:** the 1 W hotel-load assumption anchors the energy asterisk (30.0 km / 72 min propulsion-only → **24.9 km / 59 min** at 1 W) and the twin's Monte Carlo. It is currently `estimated` (MBSE basis tag); this plan retires it to `measured`.
**Execution slot:** **Phase B3 avionics bench session** — one bench session, three data products: hotel load (this plan) + motor wattmeter test (R-07) + measured 3S discharge curve (CDR entry criterion). Assigned: **GM-owned**; CEO pace governs the calendar, GM governs the procedure.

## 1. What to measure (all on the 3S rail, nominal 11.1 V — record V and I, compute P)

| # | Condition | What it captures | Method |
|---|---|---|---|
| M1 | FC + GPS + RX quiescent, disarmed | Baseline avionics floor | Power on, no arm, 60 s steady-state average |
| M2 | Armed, servos centered, no input | Servo quiescent × 2 (EMAX ES9051) | Arm (props OFF — motor disconnected), 60 s average |
| M3 | Servo sweep profile: ±15° elevon at 0.5 Hz, 60 s | Per-deflection dynamic draw, cruise-like corrections | FC-driven servo test (ArduPlane servo output test) or standalone servo tester |
| M4 | Servo sweep profile: ±30° at 1 Hz, 60 s | High-activity bound (turbulence / aggressive maneuvering) | Same as M3 |
| M5 | **Simulated cruise duty cycle: M3 profile at 30% duty (18 s on / 42 s off), 3 min** | **The operating-point number the mission model actually needs** | Scripted FC sweep; time-averaged P over the full 3 min |
| M6 | Full M1–M5 set repeated at 12.6 V (full) and 10.5 V (near-empty) | Voltage dependence of the avionics draw | Bench supply or battery at two SoC points |

**The single most important measurement is M5** — the time-averaged draw at a simulated cruise duty cycle. The mission model's 1 W is a *cruise-average*, not a quiescent floor: M1/M2 alone will under-read it (servos under duty cycle dominate the avionics budget), and M4 alone will over-read it. M5 is the number that replaces 1 W.

## 2. With what

- **Inline wattmeter** on the 3S rail between battery and power distribution (from the D-12 buy list; the same unit serves the R-07 motor test — one purchase, two tests).
- **Servo drive:** ArduPlane servo-output test via Mission Planner / MAVLink (preferred — exercises the real FC path), fallback: standalone servo tester.
- **Logging:** wattmeter peak/average readout + timestamped notes; 60 s minimum per condition for steady state.
- **Safety:** LiPo precautions per the bench SOP (charge state supervised, motor physically disconnected for all servo tests — **props off, motor leads unplugged**, not just disarmed in software).

## 3. Pass / fail and the decision rule

There is no "pass" in the go/no-go sense — the measurement *always* succeeds by producing a number. The decision rule governs what the number does to the program:

| Measured P_hotel (M5) | Verdict | Action |
|---|---|---|
| 0.5 – 1.5 W | **Within model tolerance** | Adopt measured value in mission model; re-run range/endurance; update deck asterisk, twin Monte Carlo, AIRFOIL_TRADE sensitivity note; basis tag → `measured` |
| < 0.5 W | **Better than assumed** | Same updates; range claim improves — re-run and re-freeze the energy numbers before CDR |
| 1.5 – 2.0 W | **Material miss** | Same updates **plus** RQ-03-threshold check: does the range objective (once RQ-03 is decomposed per VERIFICATION_MATRIX §A) still hold? Log a risk-register delta (R-new: hotel-load exceedance) |
| > 2.0 W | **Design flag** | All of the above **plus** escalate to CEO before CDR: energy budget re-opened; options are reduce avionics draw, accept reduced range, or increase battery (weight-budget impact). CDR does not proceed on a flagged energy budget without CEO direction |

**Mandatory regardless of outcome:** re-run the energy numbers with the measured value, update the deck's asterisk, the twin's Monte Carlo distribution, and the traceability audit's C5/G2 close-out (the repo's `mission.py` takes the measured `P_hotel`); log the retirement of assumption A-012 in DEV_TRACKER.

## 4. Assignment and schedule

- **Owner:** GM. **Executor:** whoever runs the B3 bench session (GM or delegated agent, same procedure).
- **Prerequisite:** avionics procured (Phase 2: FC, GPS, servos) — no earlier slot exists; do not estimate it away in Phase A.
- **Gate linkage:** measured P_hotel is a CDR input alongside the measured discharge curve. CDR entry criterion is amended: *"TDR actions closed + measured 3S discharge curve + measured hotel load (M5)."*
- **Cost:** $0 incremental — the wattmeter is already on the buy list for R-07.

*The asterisk dies here: after this test, the energy numbers are either confirmed or corrected — never again "propulsion-only."*
