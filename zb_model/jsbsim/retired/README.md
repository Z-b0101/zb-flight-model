# Retired: zb_wing.xml (MBSE decision, 2026-10-14, Oubi / DBSE)

Retired, not deleted, so the history stays traceable. Do not use it for simulation.

Findings (twin build, 2026-10-14; see program/reviews/JOINT_REPORT_GM_SECTIONS.md §4):
1. Does not load: references engine/thruster files `zb_thrust` / `zb_nozzle` that were never committed.
2. The placeholder fuel tank adds 50 g, so simulated AUW is 254.3 g, over the 250 g cap. Disqualifying on its own.
3. Aero axes return raw coefficients, which JSBSim treats as forces and moments (no qbar·S scaling).
4. Unnamed `<location>` elements put AERORP and the empty-weight CG at x = 0 (simulated CG 77 mm vs intended 116 mm).
5. `pitch-trim-cmd` is not wired to the elevon.
6. CL slope 0.109 /deg (2-D-like); the params-driven VLM gives 0.063 /deg.

Replacement (L1 reference): `twin/gen_jsbsim.py` generates the aircraft from `cad/params.json` (branch twin/v0.1).
