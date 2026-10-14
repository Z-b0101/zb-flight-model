# Z!B Functional Hazard Assessment (ARP4761-lite)

**Date:** 2026-10-13 · **Owner:** GM · **Closes:** SAE CA-04 (§4.8 GAP)
**Tailoring basis:** SAE_ALIGNMENT.md §6.2 — full FHA→PSSA→SSA→CCA is disproportionate at 5 J; this one page IS the assessment.
**Operating envelope assumed:** 204 g AUW · cruise 7 m/s → KE ≈ ½·0.204·7² ≈ **5 J** · recreational LOS · unpopulated test area · geofence + failsafe (ArduPlane).
**DAL:** E for all PoC functions (SAE_ALIGNMENT.md §6.1). Severity classes per ARP4761: Catastrophic / Hazardous / Major / Minor / No Safety Effect.
**Reading rule:** at 5 J — two orders of magnitude below manned-aviation concern thresholds, comparable to a gently thrown tennis ball — the honest classification is almost always "No Safety Effect." The FHA's job is to say so *explicitly* and to name the one combination that isn't.

| # | Function | Failure condition | Effect (in the stated envelope) | Severity | Rationale |
|---|---|---|---|---|---|
| 1 | Hand launch | Loss of control during launch (tip stall / torque roll into operator) | Aircraft contacts operator or bystander at ≤ 5 J | **Minor** | Only phase where people are necessarily close. 5 J is below common injury thresholds (~15 J cited for small-UAS concern); worst credible case is a cut/bruise. Mitigation: launch procedure, clear area, prop guard optional. |
| 2 | Climb | Loss of thrust on climb-out | Forced glide to ground; article damage | **No Safety Effect** | Effect is loss of the $361 article only. Unpopulated area + LOS means no third-party exposure. |
| 3 | Cruise | Loss of attitude control (servo/FC fault) | Uncontrolled descent; ground impact at ≤ terminal velocity of a 204 g foam wing | **No Safety Effect** | Foam + 204 g + low ballistic coefficient: impact energy stays in the single-digit-joule class. Area controls bound the exposure. |
| 4 | Loiter | Navigation fault (GPS loss) | Drift with wind; eventual failsafe or battery exhaustion | **No Safety Effect** | Degrades to F5/F6. No people under the area. |
| 5 | RTL | RTL fails to return (GPS fault + wind) | Flyaway beyond LOS | **Minor** | The top program-level hazard (see §B). Geofence + RC-link failsafe bound it; residual is nuisance/property, not injury, at 5 J. Escalates only if combined with over-people flight — prohibited by the operating envelope. |
| 6 | Failsafe glide | Failsafe fails (no glide; uncontrolled descent) | Same as #3 | **No Safety Effect** | Single-fault effect identical to loss of control; article loss only. Verified by bench + SITL (VC; AI-16). |
| 7 | Belly landing | Hard/arrested landing (stall, wind gust) | Airframe damage; prop/motor strike on ground | **No Safety Effect** | Belly landing on grass at ~4 m/s stall: energy ≈ 1.6 J. Operator retrieves on foot after motor disarm. |

## §B — The two hazards that matter

1. **Flyaway (F5):** the only failure condition that can *leave* the controlled envelope. Severity stays Minor only while the envelope holds (unpopulated area, geofence armed, failsafe verified per AI-16). If Z!B ever flies over people, BVLOS, or without geofence, this row re-opens and the DAL assignment re-opens with it (SAE_ALIGNMENT.md §6.1 boundary).
2. **Launch-phase contact (F1):** the only phase with guaranteed human proximity. Bounded by procedure, not by physics. The pre-maiden checklist must include a launch-area-clear callout.

## §C — Boundary conditions (re-open triggers)

Any of these invalidates this FHA and re-opens DAL assignment + full ARP4761 scoping: payload carried over people · BVLOS operation · commercial (Part 107) operation · AUW exceeding 250 g · removal of geofence/failsafe. The living hazard log is RISK_REGISTER.md; FHA deltas are reported at each gate.

*One page, as required. Proportionality is the requirement.*
