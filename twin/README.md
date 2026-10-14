# Z!B digital twin (v0.1, work in progress)

Owner: Claude (acting GM/DE). Status: L1 model-level twin, not calibrated against hardware.

## Findings when loading `zb_model/jsbsim/zb_wing.xml` in JSBSim 1.2.1 (built from source)
1. **Does not load.** It references engine/thruster files `zb_thrust` / `zb_nozzle` that are not in the repo.
2. **Placeholder fuel tank adds 50 g.** That puts simulated AUW at 254.3 g, over the 250 g cap. It is removed here, and thrust is re-expressed as a body-frame external force (1.5 N x throttle, same scaling).
3. **Aero axes return raw coefficients.** JSBSim treats axis outputs as forces and moments, so they are now scaled by qbar*S, plus b or c for moments.
4. **Unnamed `<location>` elements.** The aero reference point (AERORP) and the empty-weight CG both defaulted to x = 0. As a result the simulated CG was 77 mm instead of the intended 116 mm.
5. **Pitch trim not wired.** `pitch-trim-cmd` did not reach the elevon. It is now summed.

The fixed model lives in `twin/aircraft/zb_wing/zb_wing.xml`. The original file is unchanged, pending MBSE review.

## First results (modeled, not verified)
- The analytic trim (`twin/aero.py`) flown open-loop in JSBSim for 30 s gives a damped phugoid that settles at 7.6 m/s with about -0.08 m/s sink. The model is longitudinally stable.
- Trimmed L/D peaks at about 7.8 near 6-7 m/s. The previously stated figure was 9.25. The gap is the trim penalty: about -5 deg of elevon costs lift and adds drag. This needs reconciliation (CE-01).
- The CL slope in the table is 0.109/deg, which looks like a 2-D value. A 3-D estimate for AR 4.5 is about 0.07/deg. Open.
