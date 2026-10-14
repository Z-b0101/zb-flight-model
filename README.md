# zb-flight-model

Clean-room flight-model math for **Project Z!B** — the mission, aero, trim,
stability, structures, and weight analysis behind our sub-250g fixed-wing
UAV family. Z!B-authored analysis only; no ArduPilot code is copied here.

## Scope

- `zb_model/mission.py` — level-flight range/endurance (V=√(2W/ρSCL), P=D·V)
- `zb_model/drag.py` — CD buildup (MH60 polar + misc + induced)
- `zb_model/propulsion.py` — efficiency derate fit scaffold + provenance
- `zb_model/trim.py` — tailless trim budget and trim drag
- `zb_model/stability.py` — neutral point / static margin / CG
- `zb_model/structures.py` — spar beam bending and margin
- `zb_model/weight.py` — weight-budget builder and CG rollup
- `zb_model/jsbsim/` — our authored JSBSim aero model + SITL wiring notes
- `zb_model/data/assumptions.yaml` — every constant, with status

## How to cite

If you use this model, cite the repo and the assumptions ledger
(`zb_model/data/assumptions.yaml`), which records the provenance and
status (measured / derived / assumed) of every constant.

## HONESTY — what is NOT claimed

- **L1 trade model, not a release claim.** Absolute range/endurance numbers
  are comparative trade-study outputs. Flight test sets the absolutes and
  promotes the twin L1 → L2.
- **Hotel load is illustrative.** The 1 W `P_hotel` term is a placeholder;
  the sensitivity analysis is unbuilt (traceability gap G2). Bench-test it.
- **Battery curve is reference data, not a measured pack trace.** The 80%
  usable-energy derate is an estimate; the real discharge curve comes from
  the battery/wattmeter bench test.
- **Propulsion pairing is unresolved.** The eta derate fit coefficients are
  engineering judgment until the wattmeter pins them.
- **XFoil optimism applies.** Real wing Cd runs ~10–20% above the polars
  (roughness, rib steps); rankings are comparative.
- **Weight budget is [VERIFY].** The 204.3 g rollup conflicts with the
  209.0 g CAD value; closure is owned by the program's CE-01/CE-02 work.
- **Coordinate datums are not mixed.** Stability defaults use the A2 loop
  datum; CAD uses root-LE. See `zb_model/stability.py`.

## License

MIT — see `LICENSE`. Clean-room: our code does not copy ArduPilot
(GPL-3.0). Using ArduPilot as a SITL *tool* is fine; embedding its code in
a product needs legal review (flagged, not resolved). MAVLink licensing is
marked NOASSERTION — verify before product use.
