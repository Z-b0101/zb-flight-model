# GitHub Traceability Audit — Z!B Technical Logic

**Date:** 2026-10-13 · **Trigger:** independent consultancy recommendation — every claim/model mapped to referenceable GitHub material; nothing survives on assertion alone.
**Method:** three parallel domain researchers, every module path verified live via `browser.open` against the GitHub tree (repo root → file; no guessed paths), each mapping through ≥4 criticism rounds (naive match → adversarial read → maintenance/version check → kill attempt). This document is the synthesis + a fifth, synthesis-level adversarial pass.

**Counting rule (stated so the fraction is auditable):** one matrix row = one claim-unit. Literature-only claims (C6a/b/c) are excluded from the GitHub fraction and reported separately as N/A-LITERATURE. A split row (e.g. BACKED-equation / PARTIAL-value) is counted once, at the stricter status.

## Verdict

| Status | Rows | Share |
|---|---|---|
| **BACKED** (repo code implements the same logic) | 22 | **55%** |
| **PARTIAL** (covers part; or textbook physics without implementation) | 16 | **40%** |
| **GAP** (nothing referenceable; own-repo material) | 2 | **5%** |
| N/A-LITERATURE (peer-reviewed/NASA/theses citations on file, no code exists) | 3 | — |

**Plain-language verdict:** just over half our logic is directly backed by referenceable GitHub implementations, and the backed half is the *load-bearing* half — flight-control laws, SITL, 6-DOF dynamics, VLM stability, XFoil method, level-flight and stall equations. The unbacked 45% is concentrated exactly where you'd expect: **our own numbers** — the propulsion derate fit, the 80%-usable energy derate, the hotel-load sensitivity, the component weight buildup, the trim coefficients, the flat misc-drag term, and our wing's JSBSim aero model. None of those are borrowed physics; they are Z!B-authored analysis, and the consultancy-grade end state is to make *them* referenceable by publishing them as a Z!B repo (§5). Two strict GAPs exist; both close through our own repo.

---

## 1. Traceability matrix

### Domain A — Flight control logic, flight dynamics simulation, airframe monitoring

| # | Claim | Backing repo + verified module | Status | Key caveat from criticism |
|---|---|---|---|---|
| A1a | Attitude PIDs (angle-mode) | `ArduPilot/ardupilot` — `libraries/APM_Control/AP_RollController.cpp` (+ Pitch/Yaw) | BACKED | Cascaded angle→rate PID, not a single PID; structure portable, gains are ours to tune |
| A1b | Angle-mode entry (FBWA) | `ArduPilot/ardupilot` — `ArduPlane/mode_fbwa.cpp` | BACKED | **TECS is NOT active in FBWA** (auto-throttle modes only). "TECS from the maiden" requires an auto-throttle mode, not plain FBWA — see §3 |
| A1c | TECS altitude/airspeed control | `ArduPilot/ardupilot` — `libraries/AP_TECS/AP_TECS.cpp` | BACKED | True total-energy coordination incl. landing logic; controller *structure* backed, tuned gains are ours |
| A1d | L1 lateral navigation | `ArduPilot/ardupilot` — `libraries/AP_L1_Control/AP_L1_Control.cpp` | BACKED | Genuine L1 (Park's law), not PD-on-bearing; L1 period must be tuned to our scale/speed |
| A2a | Waypoint/mission execution | `ArduPilot/ardupilot` — `ArduPlane/mode_auto.cpp` + `libraries/AP_Mission/AP_Mission.cpp` | BACKED | Real mission executor feeding L1+TECS |
| A2b | RTL | `ArduPilot/ardupilot` — `ArduPlane/mode_rtl.cpp` | BACKED | **Default RTL loiters, it does not land.** Autoland-on-RTL needs `RTL_AUTOLAND` params or a mission sequence — see §3 |
| A2c | Automatic landing | `ArduPilot/ardupilot` — `ArduPlane/mode_autoland.cpp` + `libraries/AP_Landing/` | BACKED | Staged glideslope logic verified; **behind `#if MODE_AUTOLAND_ENABLED`** — confirm in F405 WING MINI hwdef before relying on it |
| A3 | SITL: real firmware vs simulated airframe | `ArduPilot/ardupilot` — `libraries/SITL/SIM_Plane.cpp` + `libraries/SITL/SIM_JSBSim.cpp` | BACKED | Same ArduPlane code under `HAL_BOARD_SITL`; but SIM_Plane's own header says "**Not aerodynamically accurate**" — twin fidelity must come from the JSBSim backend, not the default frame |
| A4a | 6-DOF FDM (aero/propulsion/atmosphere) | `JSBSim-Team/jsbsim` — `src/FGFDMExec.h` | BACKED | Nonlinear 6-DoF, ISA atmosphere, NASA check cases; **no 250g flying-wing model ships** — our MH60-based XML is ours to author → GAP (row A4a-ii) |
| A4a-ii | *Our wing's* JSBSim aero model | — | GAP | Machinery backed; coefficients are Z!B-authored. Close-out: `zb_model/jsbsim/` in our repo (§5) |
| A4b | FDM → simulated sensors | `ArduPilot/ardupilot` — `libraries/SITL/SIM_JSBSim.cpp` (`recv_fdm()`) | BACKED | Verified accel/gyro/velocity mapping lines — the actual twin sensor path |
| A5a | Onboard dataflash logging | `ArduPilot/ardupilot` — `libraries/AP_Logger/AP_Logger.cpp` | BACKED | Behind `HAL_LOGGING_ENABLED` — confirm on our board (has SD; check pending) |
| A5b | MAVLink telemetry protocol | `mavlink/mavlink` — `message_definitions/v1.0/common.xml` (+ `ardupilotmega.xml`) | BACKED | The protocol definition itself. **License: NOASSERTION — verify before product use** |
| A5c | Programmatic log/telemetry access | `ArduPilot/pymavlink` — `DFReader.py`, `tools/mavlogdump.py`, `mavutil.py` | BACKED | Log parsing + live-telemetry API verified |
| A5d | In-flight health *monitoring* (failsafes, battery) | (observability half via A5a/A5b) | PARTIAL | Failsafe *actuation* (`AP_BattMonitor`, ArduPlane failsafe handling) not path-verified this pass → follow-up |

### Domain B — Aerodynamic modeling

| # | Claim | Backing repo + verified module | Status | Key caveat from criticism |
|---|---|---|---|---|
| B1a | Level flight V=√(2W/ρSCL) | `byuflowlab/flightlab` — `flightlab/performance.py` (`speeds()`) | BACKED | Exact same algebra (W=mass·G0) |
| B1b | P_shaft=D·V | `byuflowlab/flightlab` — `flightlab/performance.py` (`power_required()`) | BACKED | Verbatim implementation |
| B1aux | q=½ρV² primitive | `peterdsharpe/AeroSandbox` — `aerosandbox/performance/operating_point.py` | PARTIAL | Primitive only; no level-flight solver in AeroSandbox |
| B2a | CD=Cd_airfoil+CDi, CDi=CL²/(π·AR·e) | `peterdsharpe/AeroSandbox` — `aerosandbox/aerodynamics/aero_3D/aero_buildup.py` (~L1130) | BACKED | Same decomposition; profile term via NeuralFoil (XFoil-trained NN), not XFoil directly |
| B2b | Oswald e (we use 0.78) | `peterdsharpe/AeroSandbox` — `aerosandbox/library/aerodynamics/inviscid.py` (`oswalds_efficiency()`, Nita & Scholz) | PARTIAL | Equation backed; **our value 0.78 is a hand estimate**, not repo output |
| B2c | Flat +0.012 misc-drag term | `peterdsharpe/AeroSandbox` — `aerosandbox/library/aerodynamics/components.py` (Hoerner-based CDA models) | PARTIAL | No repo uses a flat 0.012; AeroSandbox models misc drag per-component. Ours is an estimate; these are the referenceable analogues |
| B3a | XFoil viscous–inviscid panel method, e^N transition | `Abhyrejikumar18923/xfoil-linux` — `src/` (full Drela Fortran source) | BACKED | Actual Drela codebase, browsable. **It is a mirror** — official distribution is web.mit.edu/drela, not GitHub |
| B3b | XFoil 6.99 snapshot | `ppinuzz/xfoil` — `xfoil/xfoil6.99.tgz` | PARTIAL | Code only inside a tarball; 5 commits, 0★. Provenance cross-check only |
| B3c | XFoil interface, n_crit=9 viscous runs | `peterdsharpe/AeroSandbox` — `aerosandbox/aerodynamics/aero_2D/xfoil.py` (`n_crit: float = 9.0` default) | BACKED | Exactly how airfoiltools-style polars are produced; needs an XFoil binary on PATH (mirrors above) |
| B3d | MH60 coordinates | `peterdsharpe/AeroSandbox` — `aerosandbox/geometry/airfoil/airfoil_database/mh60.dat` | BACKED | Raw Selig-format coordinates verified present. **The polar *numbers* (Clmax 1.16, Cm0) live only on airfoiltools.com** — method + geometry backed, values regenerable (see §4) |
| B4a | Trim coefficients: Cm_ac=CL·SM, washout +0.0075/°, elevon −0.008/°, ΔCD≈1.3e-4δ² | — (textbook: Drela *Flight Vehicle Aerodynamics*; Phillips *Mechanics of Flight*) | PARTIAL | **These exact numbers are ours** — thin-airfoil/lifting-line estimates. Repos implement higher-fidelity numerical trim (B4b–d), not our analytic coefficients |
| B4b | VLM trim solution | `byuflowlab/flightlab` — `flightlab/stability.py` (`trim()`; verified vs AVL within 0.2°) | PARTIAL | Numerical trim, not our analytic form; applicable to tailless wings |
| B4c | Trim iteration (2nd implementation) | `flt-acdesign/JAVL` — `src/trim.jl` (Julia AVL reimplementation) | PARTIAL | Independent trim logic |
| B4d | Control-surface deflection → ΔCL/ΔCD/ΔCM | `peterdsharpe/AeroSandbox` — `aero_buildup.py` (~L1086, via NeuralFoil deflected-surface data) | PARTIAL | Same physics at NN fidelity, not our −0.008/° estimate |
| B4e | Thin-airfoil analytic basis | `sajidkabir/naca-airfoil` — `src/naca_airfoil/theory.py` | PARTIAL | 1★, Oct-2026, NACA-only, inviscid — cited only as the referenceable thin-airfoil implementation; cannot back MH60 numbers |
| B5a | NP / static margin / stability derivatives (VLM) | `byuflowlab/flightlab` — `flightlab/stability.py` + `flightlab/vlm/` (NP verified vs AVL 3.52 within 3 mm) | BACKED | Lifting-surfaces-only VLM (fine for tailless); our 5–6% SM is our design input, not repo output |
| B5b | NP/AC + derivatives (2nd implementation) | `peterdsharpe/AeroSandbox` — `aero_buildup.py` (~L882, empirical unsweep calibration) | BACKED | Independent implementation; NP correction is an empirical fit — caveat noted |
| B6 | Vstall=√(2W/ρS·Clmax) | `byuflowlab/flightlab` — `flightlab/performance.py` (`speeds()`) | BACKED | Exact formula; the MH60 input 1.16 is our XFoil/airfoiltools data point (method backed under B3) |

**Adversarial note carried from the researcher (do not dilute):** AeroSandbox's VLM is **inviscid-only** — it does not back viscous low-Re behavior. Viscous coupling lives in its `AeroBuildup` mode via NeuralFoil. Do not claim AeroSandbox's VLM alone backs our viscous numbers.

### Domain C — Structures, mission/energy, weight, propulsion

| # | Claim | Backing repo + verified module | Status | Key caveat from criticism |
|---|---|---|---|---|
| C1 | Propulsion derate η=min(0.55, 0.20+0.0875·P_shaft) | `aeroeng3/Fixed_Wing_UAV__Energy_Optimization` — `uavlab/energy/motor.py` (Drela 3-param BLDC model) | PARTIAL | Right physics family (Drela/QPROP canonical form), **wrong functional form** (physics-based, not our empirical fit), defaults are a 6S 110-size motor, and the repo is 2 commits / Sept 2026 — immature, cite with caution. **Our exact fit is unmapped → own repo** |
| C2 | Energy bookkeeping, E_usable=5.77 Wh | `ArduPilot/ardupilot` — `libraries/SITL/SIM_Battery.cpp` (+ unit tests) | PARTIAL | Does coulomb counting AND internal-resistance voltage sag + SoC/temperature — but it's a SITL stub with arbitrary params; our 80%-usable derate is ours alone |
| C2sub | LiPo discharge-curve modeling | `aeroeng3/Fixed_Wing_UAV__Energy_Optimization` — `uavlab/energy/battery.py` (1-RC ECM) | PARTIAL | Genuine ECM implementation; all params tagged representative-not-measured; same immaturity caveat |
| C3 | Spar bending, 4mm tube, 3.3× margin | `JWock82/Pynite` — `Pynite/Member3D.py` (beam-element FEA, CI-tested vs textbook) | PARTIAL | FEA solves the same Euler-Bernoulli mechanics numerically — but has **no material-strength margin check**; the 3.3×-vs-carbon-strength half is unmapped. Analytic fallback: Megson *Aircraft Structures* (textbook, no implementation) |
| C4 | Weight sizing tooling | `yies00/dronedesign` — `aircraft_designer/core/weights.py` (Raymer Ch.6 statistical) | PARTIAL | **Different logic**: statistical empty-weight fraction, not component buildup; 0★, "internal tool — not for external distribution". Barely survives |
| C4sub | Component mass summation | `OpenMDAO/Aviary` — `aviary/subsystems/mass/mass_builder.py` (NASA-maintained) | PARTIAL | FLOPS/GASP empirical correlations, transport scale — not a small-UAV parts-list buildup. **Our buildup + CG + margin arithmetic remains own-repo material** |
| C5 | Hotel-load sensitivity (1W → 24.9km/59min) | — | GAP | No referenceable code repo implements avionics hotel-load sensitivity analysis. Our analysis is the only implementation → own repo |
| C6a | Prandtl-D proverse yaw (NASA flight-validated) | — | N/A-LITERATURE | NASA Armstrong PRANDTL-D flight experiments; US Patent 9,382,000. No code repo exists |
| C6b | Tandem-wing interference (METU thesis) | — | N/A-LITERATURE | METU thesis 12623631 (ANSYS FLUENT CFD). No associated code |
| C6c | Box-wing win inverts at Cl≈0.5 (arXiv 2112.02872) | — | N/A-LITERATURE | Aloor et al., arXiv:2112.02872v2. No code repo linked or found |

**Repos checked and rejected (not cited as primary):** `wbunker/ardupilot` (derivative skill-summary fork, not the implementation) · `ardupilot/ardupilot_wiki_copy` (docs, not code) · `StrawsonDesign/motor_propeller_testing` (thrust-stand *data*, no efficiency-model code — noted as future validation data for our derate fit) · ArduPilot SITL motor scaling (no efficiency curve in code) · QPROP GitHub mirrors (wrappers around MIT Fortran, not implementations) · `OpenVSP/OpenVSP` as primary (NASA NOSA-1.3 license, inviscid-only, monolithic — background reference only) · `ppinuzz/xfoil` as primary (tarball blob) · FEniCS beam examples (general PDE framework, not beam theory — correctly not stretched).
**Repos found beyond the leads:** `byuflowlab/flightlab` (strongest find — implements B1, B5, B6, trim), `flt-acdesign/JAVL`, `sajidkabir/naca-airfoil`, `aeroeng3/Fixed_Wing_UAV__Energy_Optimization`, `OpenMDAO/Aviary`, `yies00/dronedesign`, `Abhyrejikumar18923/xfoil-linux`, `JWock82/Pynite`.

---
## 2. Synthesis-level criticism (round 5, adversarial)

Applied after merging the three domain tables, hunting for overstatement the domain passes missed:

1. **"55% backed" must not be read as "55% of our numbers are repo-verified."** The backed rows are overwhelmingly *method and machinery* (control-law structures, VLM, XFoil, flight equations). Our *specific numbers* — 30.0 km, −6° elevon, 3.3× spar margin, 46 g weight margin — are outputs of Z!B-authored analysis *using* backed methods. The honest statement: our methods are 55% GitHub-backed; our numbers are ours, and §5 is how they become referenceable.
2. **AeroSandbox cannot be cited for viscous low-Re behavior via its VLM.** Its VLM is inviscid-only; viscous coupling exists only through NeuralFoil in AeroBuildup mode. Any future citation must name the mode.
3. **The aeroeng3 repo is load-bearing in two PARTIAL rows and is 2 commits old (Sept 2026).** It is a lead, not a pillar. If it disappears, C1/C2-sub fall back to textbook (Drela/QPROP formulation) + our own fit — which is where the real weight already sits.
4. **xfoil-linux is a mirror.** Citable and browsable, but the canonical XFoil lives at web.mit.edu/drela. Both should be cited together; the mirror is the *referenceable* one, MIT is the *authoritative* one.
5. **flightlab is the highest-value find** (BYU FLOW Lab — Andrew Ning's group; Ning & Kroo 2010 is already in our own literature base, closing the loop). Its NP-vs-AVL verification (3 mm) is the strongest third-party numerical cross-check available to us short of our own flight test.
6. **No mapping was found to be fabricated**, but three of our *phrasings* were found to be imprecise (see §3) — the audit paid for itself there.

## 3. Corrections to our own claims (found by this audit)

These are imprecisions in how Z!B has stated things, corrected here on the record:

1. **"TECS from the maiden"** — TECS is not active in FBWA (the stabilized angle mode). It engages in auto-throttle modes (FBWB/CRUISE/AUTO/RTL/AUTOLAND). If the maiden flies FBWA, the maiden flies on attitude PIDs + manual throttle, not TECS. State the mode when claiming the controller.
2. **"RTL / autoland"** — default RTL loiters above home; it does not land. Autoland is a separate feature (`mode_autoland.cpp`), behind the `MODE_AUTOLAND_ENABLED` build flag. Our PoC plan should name them as two features and verify the flag in the F405 WING MINI hwdef before depending on autoland.
3. **"Digital twin" pre-hardware** — the backup deck already corrected this (validated digital model/digital thread until flight data calibrates it). The audit reinforces it: SIM_Plane's own header disclaims aerodynamic accuracy — twin *fidelity* must come from the JSBSim backend with our authored XML, which does not exist yet (GAP A4a-ii).
4. **Weight budget staleness (audit observation, not a GitHub gap):** `WEIGHT_BUDGET.md`'s "Weight requirements (allocated targets)" table still shows Payload 30/30 and Total 233/236 — stale after the 2026-10-13 PoC 0g-payload update (rollup now 204.3 g / 46 g margin). Flagged for the GM to reconcile; the audit does not edit it unasked.

## 4. Gap close-out plan

**Strict GAPs (2):**
- **G1 — Our wing's JSBSim aero model (A4a-ii).** Close-out: author the JSBSim XML (MH60-based aero, mass/inertia from the weight budget, 1404 propulsion deck) inside our own repo (`zb_model/jsbsim/`). Machinery (JSBSim) and the firmware↔FDM loop (SIM_JSBSim) are already backed — this is the missing authored piece, and it is required for Twin v2 anyway.
- **G2 — Hotel-load sensitivity analysis (C5).** Close-out: implement in our repo (`zb_model/mission.py` with an explicit `P_hotel` term + sensitivity sweep). No code repo exists anywhere for this; ours becomes the reference implementation.

**Nearest-miss PARTIALs (effectively ours alone — same close-out):**
- **C1-exact:** our η derate fit → `zb_model/propulsion.py` + wattmeter CSVs when measured (StrawsonDesign thrust-stand data noted as future validation data, not a model).
- **C4-exact:** component buildup + CG + margin → `zb_model/weight.py` (replaces the spreadsheet with tested code).
- **B4 coefficients / B2c 0.012 / B2b e=0.78:** our analytic estimates → `zb_model/trim.py`, `zb_model/drag.py`, with the assumptions ledger marking each as Z!B-estimated and each carrying a cross-check against the higher-fidelity repo implementations (flightlab trim, AeroSandbox component buildup).
- **B3d values:** the MH60 polar *numbers* (Clmax 1.16, Cm0) currently live only on airfoiltools.com. Strong close-out: `scripts/regenerate_polars.py` runs XFoil (xfoil-linux binary) at Ncrit 9 over `mh60.dat` (mirrored from AeroSandbox's database) and pins the outputs — converting a scraped-data dependency into a reproducible artifact.

**Follow-ups that are verification, not repo work:**
- F1: verify `AP_BattMonitor` + ArduPlane failsafe module paths (closes A5d PARTIAL).
- F2: confirm `MODE_AUTOLAND_ENABLED` and `HAL_LOGGING_ENABLED` in the F405 WING MINI hwdef before flight-planning on autoland/logging.
- F3: decide the L1 period and TECS tuning starting point for a 7 m/s 204 g wing (tuning is ours; the structures are backed).

## 5. Draft Z!B reference repo structure (DO NOT PUBLISH — CEO approval required)

Proposed name: `zb-flight-model` (org/name at CEO's discretion). Purpose: make Z!B's own math referenceable, so the next audit maps our rows to our code.

```
zb-flight-model/
├── README.md                  # scope, how to cite, what is NOT claimed (honesty header)
├── CITATION.cff
├── LICENSE                    # MIT proposed. NOTE: our code is clean-room; no ArduPilot code copied.
│                              # ArduPilot is GPL-3.0 (copyleft) — using it as a *tool* (SITL) is fine;
│                              # embedding its code in a product needs legal review. Flagged, not resolved.
├── pyproject.toml
├── zb_model/
│   ├── __init__.py
│   ├── mission.py             # V=√(2W/ρSCL), P=D·V, endurance/range integration, explicit P_hotel term (closes G2)
│   ├── drag.py                # CD=Cd_airfoil+C_misc+CL²/(π·AR·e); Hoerner-based misc buildup replacing flat 0.012
│   ├── propulsion.py          # eta derate fit + fit provenance (closes C1-exact); wattmeter CSVs land here
│   ├── trim.py                # Cm_ac=CL·SM, washout credit, elevon effectiveness, trim drag (closes B4)
│   ├── stability.py           # NP/SM/CG computation; cross-checked vs flightlab/stability.py
│   ├── structures.py          # spar beam bending + margin; cross-checked vs PyNite
│   ├── weight.py              # weight-budget builder, CG rollup, margin arithmetic (closes C4-exact)
│   ├── jsbsim/                # OUR wing's JSBSim XML + SITL wiring notes (closes G1)
│   └── data/
│       ├── polars/            # mh60.dat (UIUC, via AeroSandbox mirror) + regenerated polar tables
│       └── assumptions.yaml   # EVERY constant: value, source, status (measured/derived/assumed)
├── scripts/
│   └── regenerate_polars.py   # XFoil Ncrit 9 → polar tables; pins B3d values reproducibly
├── tests/                     # unit tests pinning every number in AIRFOIL_TRADE.md
├── notebooks/
│   └── airfoil_trade.ipynb    # re-runnable trade study
├── docs/
│   └── TRACEABILITY.md        # this audit, kept live (re-run per gate)
└── .github/workflows/ci.yml   # tests + polar regeneration on every push
```

**Publication preconditions (for the CEO):** (1) explicit approval to publish; (2) org/name decision; (3) license decision (MIT proposed); (4) scrub check — no credentials, no ITAR-sensitive content (sub-250g recreational UAV math is not ITAR, but the check is the process); (5) the assumptions ledger complete — nothing published with an untracked constant.

## 6. License & legal notes (from the audit, for the company, not the engineers)

- **ArduPilot/ardupilot is GPL-3.0 (copyleft).** Using it as a flight stack / SITL tool is normal and fine; *embedding or distributing modified ArduPilot code inside a Z!B product* triggers copyleft obligations. Flag for legal before any product step. Our `zb-flight-model` math does not copy ArduPilot code — keep it that way.
- **mavlink/mavlink license is marked NOASSERTION** on the repo page — verify before product use.
- **JSBSim is LGPL-2.1** — the most permissive of the dynamics options; relevant if the twin ever ships commercially.

---

*Audit completed 2026-10-13. Re-run at each gate. Nothing in this file was published anywhere.*
