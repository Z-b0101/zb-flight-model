# JSBSim model — wiring notes

`zb_wing.xml` is Z!B's authored JSBSim aero model for the 0.9 m MH60 wing
(traceability row A4a-ii / gap G1). It loads clean in JSBSim 1.3.2 and
reconciles with the trade study (L/D 9.25, trim elevon −5.9°, Vstall
3.96 m/s at the authored mass).

Shakiest parts (flagged honestly): lateral-directional derivatives,
propulsion placeholder, and the α₀ assumption. Twin fidelity must come
from this JSBSim backend — not from ArduPilot SIM_Plane, whose own header
disclaims aero accuracy.

## SITL wiring

1. Point ArduPilot SITL at the JSBSim backend (`SIM_JSBSim.cpp` is the
   verified FDM→sensor path: `recv_fdm()` maps accel/gyro/velocity).
2. The same ArduPlane firmware runs under `HAL_BOARD_SITL`; only the
   airframe model changes.
3. Flight-test calibration promotes this model L1 → L2 (twin fidelity gate).

## Clean-room note

This XML is Z!B-authored. It drives JSBSim (LGPL-2.1) as a tool; no
ArduPilot code is copied or embedded here.
