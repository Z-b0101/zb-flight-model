# Joint technical report, 2026-10-14 06:00 PT: GM/DE sections (Claude)

Sections: Physics · Electronics · Mechanical · Simulation-execution, plus twin status against the MBSE criteria.
Math and simulation-verification are Oubi's (DBSE). Oubi assembles.

Status words: **verified** = checked against hardware, a measured source, or an independent calculation; **modeled** = computed, not yet tested; **open** = not resolved; **blocked** = waiting on a named owner or input.
Configuration: `cad/params.json` design hash `7be168427b4d`. Twin source: branch `twin/v0.1` @ `098f890`.

---

## 1. Physics (aero, stability and control, mass/CG)

**Figured out**

| Quantity | Value | Basis | Status |
|---|---|---|---|
| Planform | 0.90 m span, 0.20 m chord, AR 4.5, 25° sweep, 6° linear washout, MH60 | params.json | controlled |
| Lift slope (3-D) | 0.0633 /deg | VLM 40×10/side from params | modeled |
| Zero-lift alpha | −3.07° | VLM (MH60 camber + washout) | modeled |
| Neutral point | 142.6 mm aft root LE | VLM; baseline 144.98 mm (−2.4 mm, 1.2% MAC) | modeled, cross-checked |
| CG (as designed) | 128.5 mm, 209.0 g | DESIGN_CLOSURE item 2 (CAD rollup) | modeled |
| Static margin | 7.0% MAC (twin) / 8.26% (baseline) | NP delta only | modeled |
| Span efficiency e | 0.896 | VLM, Trefftz | modeled (drag.py carries 0.78 → CE-01) |
| Elevon power | CL 0.020 /deg, Cm −0.0082 /deg about CG | VLM × 0.75 viscous knockdown (assumed) | modeled |
| Stall speed | 4.2 m/s (wing CLmax 0.9 × section 1.16, assumed) | | modeled |
| Trimmed L/D | 8.8 at CL 0.37 (δe −5.3°); peak ~9.5 near 6 m/s | twin | modeled; record says 8.3 trimmed → CE-01 |
| Trim at A2 cruise (7.09 m/s) | δe −5.26° (baseline −4.60°); about 2.7° authority left to the ±8° limit | twin | modeled |
| Range/endurance, A2 basis (no hotel load) | 30.6 km / 71.7 min (baseline 31.86 / 75.8, −4% / −5%) | 6-DOF JSBSim | modeled, cross-checked |
| Range/endurance, operational (1 W hotel load) | **26.3 km at 10.5 m/s, or ~60 min at 7.1 m/s** | 6-DOF JSBSim + derate fit | modeled |

**Open**

- CE-01 mass: 204.3 g (budget) vs 209.0 g (CAD). We plan on **209.0 g** until weigh-in. Both leave ≥41 g margin to the 250 g cap.

- CE-01 drag: e 0.896 (VLM) vs 0.78 (hand estimate), and trimmed L/D 8.8 (twin) vs 8.3 (record). Owner: Claude; MBSE reviews.
- The 116 mm CG is retired per DESIGN_CLOSURE item 2. It should not reopen.
- Wing CLmax (0.9 × section) and the viscous elevon knockdown (0.75) are assumptions until flight test.

**Blocked:** none on the physics side tonight.

## 2. Electronics (avionics stack, power, hotel load, LRUs)

**Figured out (picked, specs verified from vendor/teardown data, not bench-tested)**

| LRU | Pick | Mass | Status |
|---|---|---|---|
| Flight controller | SpeedyBee F405 WING stack, ArduPlane pinned to Plane-4.7.1 (D-20) | 23 g | spec-verified |
| GPS/compass | M100-5883 | 7.7 g | spec-verified |
| Servos ×2 | EMAX ES9051 | 8.6 g | spec-verified |
| ESC | EMAX Bullet 20A | 3.5 g | spec-verified |
| Motor / prop | 1404 / Flash 7040 pusher | 10 / 7.9 g | spec-verified |
| Battery | 3S 650 mAh (7.215 Wh nominal, 5.77 Wh usable at 80%) | 62 g | spec-verified |
| RX + PWM→PPM encoder | F-08A + encoder (R-09) | 8 g | estimate |

- Autopilot mode: angle mode from the maiden (RQ-23). MODE_AUTOLAND and HAL_LOGGING flags are absent from the F405 WING hwdef (AI-13, closed).
- Energy model: P_elec = P_shaft/η + P_hotel, with η = min(0.55, 0.20 + 0.0875·P_shaft). At best-range cruise (10.5 m/s): P_shaft ≈ 4.0 W, η ≈ 0.55, battery ≈ 8.2 W. At best-endurance (7.1 m/s): P_shaft ≈ 1.6 W, η ≈ 0.34, battery ≈ 5.8 W. Note that the derate fit rewards higher shaft power, which is part of why best-range speed lands high. This is one more reason to pin η on the wattmeter.

**Open (UNCALIBRATED inputs)**

- Hotel load: 1 W is a placeholder. It is the single largest range lever: going from 0 W to 1 W takes 30.6 km down to 26.3 km. The measurement plan is ready (HOTEL_LOAD_PLAN.md, M5 duty-cycle test).
- Propulsion derate fit and 3S discharge curve: wattmeter bench test (R-07).
- R-10 (5 V rail capacity), R-11 (compass EMI → GPS mast, S-2), R-08 (pusher cooling): bench checks.

**Blocked:** all of the above wait on the **Phase B3 avionics bench session**, which needs the avionics procured (Phase 2) and the wattmeter (D-12 buy list). Owner: GM. Hardware spend is gated (Gate 4 rule).

## 3. Mechanical (structures, airframe, coupon test)

**Figured out**

- Construction: 3 mm Depron skins, 4 mm carbon tube spar at 30% chord, 8 vase-mode printed ribs, plain-flap elevons hinged at 75% chord (params.json).
- Spar bending, uniform-lift root moment (conservative versus elliptic), at 209 g: **margin 4.5× at 2.5 g, 2.8× at 4 g**. Basis: E 120 GPa and an allowable of 600 MPa (both assumed literature values) and a 3 mm ID (assumed). Status: modeled.

- Tip deflection, cantilever half-spar along the 25° swept line: ~15 mm at 1 g, ~38 mm at 2.5 g. Status: modeled. Watch item for elevon binding and twist under load.
- Battery: 28×64×20 mm pack spanwise in a hatch (R-17 resolved in DESIGN_CLOSURE; clash check passes).

**Open, including one new finding**

- **NEW: the swept spar is a V.** CAD (`build_spar_tris`) builds two straight tubes meeting at the centre, about 130° included angle. There is **no root joiner designed, weighed or analysed**, and the root is exactly where the bending moment peaks. The two halves also total about 0.99 m of tube against 0.90 m budgeted (+0.8 g). I'm raising this as a Gate 1 mechanical item: joiner concept (printed or carbon sleeve), plus its mass and a root bending check. Owner: Claude, with the manufacturing engineering phase 1 DFM review (#6).

- RQ-04 coupon test (rib + Depron + glue joint, carbon bend coupon) gates the hybrid construction, E/allowable, and the airframe mass model. Risks R-01 to R-04 (twist during skinning, Depron crash damage, rib fit, LW-PLA) stay open until the coupon and test rib are done.
- Weight is energy-limited, not weight-limited: the 750 mAh battery upsize (S-1, +10 g) is the best range-per-gram trade on record.

**Blocked:** the coupon test needs materials on hand. No major prototype spend before Gate 4.

## 4. Simulation-execution (JSBSim model, SITL path, twin)

**Figured out**

- **Twin pipeline (params-driven):** params.json → `twin/vlm.py` (VLM) → `twin/perf.py` (trim, mission; assumption ledger with a status per input) → `twin/gen_jsbsim.py` (generated JSBSim aircraft) → `twin/fly.py`, `twin/mission_sim.py` (6-DOF). JSBSim 1.2.1 is built from source.

- 6-DOF results at best-range trim (10.5 m/s, α 0.6°, δe −3.2°):
  - 90 s hands-off cruise holds speed and altitude within 0.1 m
  - 1° elevon step: stable. The pitch rate peaks at 19°/s and the oscillation decays (phugoid still settling at 20 s, residual 1.3°/s).
  - 4° roll pulse: about 44° bank at 1 s
  - Mission to depletion: 26.3 km, within 0.6% of the analytic answer
- **Committed `zb_model/jsbsim/zb_wing.xml` does not run as-is** (findings handed to MBSE):
  1. Missing engine/thruster files
  2. A 50 g fictitious fuel tank pushes simulated AUW to 254.3 g
  3. Aero outputs are coefficients, not forces
  4. Unnamed locations put the aero reference point and CG at 0 (CG 77 mm instead of 116 mm)
  5. Pitch trim is unwired
  6. The 2-D-like CL slope (0.109 vs 0.063 /deg)

  The generated twin model replaces it. MBSE decides retire vs fix.
- **Corrections made tonight, in the open:**
  - Drag keyed on alpha ignored elevon lift; this caused a 0.13 m/s cruise sink. Fixed by keying drag on actual CL.
  - The propulsion derate was evaluated at the wrong power. It had overstated range at 34 km. Fixed to the program definition.

**Open**

- ArduPlane SITL in the loop: not attempted tonight. The path is documented (zb_model/jsbsim/README: SIM_JSBSim backend, same Plane-4.7.1 firmware). Next step after the report.
- Lateral-directional derivatives (except roll control power) carry over as estimates. These are UNCALIBRATED.
- Turns, wind and gusts are not yet flown; the open-loop twin flies straight-line profiles only until SITL closes the loop.

**Blocked:** none for L1. L2 (calibrated twin) is blocked on bench and flight data (Gate 3).

## 5. Twin status against MBSE criteria 1–4

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Params-driven, design hash 7be168427b4d, non-params values flagged | **Met** | vlm.py hashes the design block; perf.py `ASSUMPTIONS` ledger; generated XML header names the hash |
| 2 | PoC-complete: geometry, mass/CG with CE-01/CE-02 flagged, propulsion placeholder marked, LRUs as picked | **Met with one gap** | Geometry and mass/CG are complete. The LRUs are in the mass rollup as a lump (209.0 g at 128.5 mm), not yet as individual point masses at CAD positions. That waits on CE-02's coordinate convention. |
| 3 | Key outputs match the controlled baseline within stated tolerance | **Met** | NP −2.4 mm (±5); SM −1.2 pt (±2.5); δe +0.66° (±1); range −3.9% and endurance −5.4% (±10%), on the A2 basis |
| 4 | Honest L2 boundary, uncalibrated inputs labeled | **Met** | Ledger statuses; generated-model header lists the UNCALIBRATED items; the viewer page shows them |

Twin location: repo `twin/` on branch `twin/v0.1`. The viewer page is a private Claude artifact, shared at the CEO's discretion.
