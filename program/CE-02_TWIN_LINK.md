# CE-02: Live digital-twin link (aircraft ⇄ twin in real time)

| | |
|---|---|
| Owner | Claude (GM/DE), at CEO direction ("take ownership", 2026-10-14 19:40 PT) |
| Status | **Proposed.** MBSE review (Oubi) required: changes the frozen CE-01 avionics and CG. CEO buys the ground kit |
| Raised because | The frozen design has **no downlink**. The HotRC F-08A is a PWM-only receiver, and the twin can only learn from logs after landing. A digital twin needs live state from its physical twin |
| Fits | D-32 (simulation-first): the live link becomes the drift monitor. Provisional values are checked in flight, not only at the bench |

## 1. What the link must carry

| Data (ArduPilot MAVLink) | Rate | Twin use |
|---|---|---|
| ATTITUDE, VFR_HUD (airspeed, climb, throttle) | 5–10 Hz | Shadow-sim residuals (attitude, speed, climb) |
| GLOBAL_POSITION_INT, GPS_RAW_INT | 2–5 Hz | Track, ground speed, wind estimate |
| SYS_STATUS / BATTERY_STATUS (V, A, mAh used) | 2 Hz | Live η and drag estimate; remaining range and endurance; motor-heat estimate |
| SERVO_OUTPUT_RAW (elevons, throttle) | 5 Hz | Feeds the same control inputs to the twin (shadow mode) |
| WIND, AHRS2 / NAV_CONTROLLER_OUTPUT | 1–2 Hz | Wind for the twin; autopilot tracking error |
| RADIO_STATUS / link quality | 1 Hz | Link health; failsafe evidence |

**Budget:** about 1–3 kB/s downlink, plus a small uplink for commands and mission updates. Full-rate DataFlash logs (.bin) remain the post-flight calibration source.

## 2. Architecture

```
AIRCRAFT                               GROUND                                  TWIN
SpeedyBee F405 Wing (ArduPlane)        mLRS TX module ── USB/BT/WiFi ──►       mavlink-router / MAVProxy
  UART4: MAVLink2  ◄──►  mLRS RX ~~~~~ 900 MHz LoRa ~~~~~►                        ├─► Mission Planner / QGC (pilot)
  UART1: CRSF RC   ◄───  (RC + telem                                             └─► twin bridge (pymavlink, new: twin/live/)
  integrated V/A sensor   on one link)                                                ├─ JSBSim shadow run: same servo/throttle inputs + estimated wind
                                                                                      ├─ residuals: V, climb, attitude, current (predicted − measured)
  SERIAL6: onboard wireless (APP board)                                               ├─ online estimates: η(P), CD0, e (recursive least squares)
  → short-range MAVLink for BENCH and                                                 ├─ live range/endurance remaining from measured Wh/km
    preflight twin link (no new hardware)                                             └─ dashboard (twin viewer page) + residual log
```

**Two link tiers, one software stack:**
- **Bench and pre-flight:** the flight controller's onboard wireless already runs MAVLink2 on SERIAL6. That gives a twin link at the Oct 26–27 bench with no new hardware.
- **Flight:** a combined RC + MAVLink radio replaces the HotRC receiver and the PWM→PPM encoder.

## 3. Flight-link options

| Option | Aircraft mass | Power (aircraft side) | Range (LoS) | Fit |
|---|---|---|---|---|
| **A. mLRS 900 MHz (Matek mR900-30 RX)** | **5.3 g** with antenna | Up to 340 mA @ 5 V = 1.7 W at 30 dBm. Set to 21 dBm minimum for test flights. **Measure on the bench** | mLRS LoRa modes about 7–87 km depending on rate and power | **Recommended.** MAVLink-native, RC + telemetry on one link, ArduPilot-documented. The only option able to cover the 26 km mission later |
| B. ExpressLRS 2.4 GHz (ESP-based RX, MAVLink mode, ELRS ≥ 3.5) | ~1–2 g | ~0.2–0.5 W | A few km at telemetry-capable packet rates | Lightest. Telemetry downlink ~110 B/s at 50 Hz to ~2.4 kB/s at 1000 Hz, so the high rates needed cost range. Good fallback for local flights |
| C. 4G/LTE modem | 15–30 g | 1–2 W | Wherever there is coverage | Too heavy and power-hungry for now. Regulatory and operational questions. Revisit for beyond-line-of-sight work |

The lower-power Matek mR900-22 (2.3 g, ~0.34 W) is listed as **discontinued** at ReadyMadeRC.

## 4. Effect on the frozen CE-01 baseline

| Item | Change |
|---|---|
| Mass | Remove the F-08A RX (5 g) and the PWM→PPM encoder (3 g); add the mR900-30 RX (5.3 g) → **−2.7 g net** (230.3 g AUW, margin 19.7 g) |
| CG / SM | Depends on where the receiver sits:<br>• receiver at x = 106 mm (old RX spot): SM **5.52%** (barely meets 5.5%)<br>• receiver at x = 60 mm: SM **6.05%**<br>• receiver at x = 40 mm: SM **6.28%**<br>**Mount the receiver forward, at x ≤ 80 mm.** The antenna is routed clear of the carbon spar and the motor leads |
| Hotel power | +0.3 to +1.7 W depending on output power. The current 1 W hotel budget may not cover it at 30 dBm, so it is a bench item (HOTEL_LOAD_PLAN M-new). At 21 dBm and an estimated 0.7 W, 7 m/s range drops ~10–12% vs the 1 W budget case. This is the main cost of the link |
| FC ports | UART1: CRSF RC (`SERIAL1_PROTOCOL 23`) from the mLRS RX RC output. UART4: MAVLink2 (`SERIAL4_PROTOCOL 2`). SERIAL6: onboard wireless MAVLink for the bench. The flight controller has an integrated V/A sensor (120 A range). **Calibrate `BATT_AMP_PERVLT` against the WM150 wattmeter:** resolution at our 1.5–2.5 A cruise currents is the limiting factor for live η estimation |
| CAD | Replace the `rx`/`encoder` LRUs with the `mlrs_rx` LRU (29 × 21 mm) at x ≤ 80 mm; add an antenna-route wire. Re-run clash and CG |
| Ground kit (CEO purchase) | **mLRS TX module + EdgeTX handset with an external (JR) module bay.** The HotRC HT-8A cannot drive mLRS. The mR900-30-TX kit is listed at $41.99 (RaceDayQuads, stock unconfirmed); the handset is ~$60–200 depending on model. **The CEO flies the maiden (D-27):** handset choice and familiarisation are his call |
| Regulatory | 902–928 MHz unlicensed band (FCC Part 15). Confirm the output power and antenna-gain limits for the chosen setting before flight |

## 5. Twin software (D-32 simulation work, Claude)

1. **`twin/live/bridge.py`:** pymavlink client on the MAVLink router's UDP port. Logs every message to a time-stamped parquet file.
2. **Shadow mode:** JSBSim runs in real time and is driven by the measured SERVO_OUTPUT_RAW and the estimated wind. Residuals (predicted − measured airspeed, climb rate, pitch, current) are published at 2 Hz.
3. **Online estimators:**
   - η(P_shaft) from (thrust ≈ drag at steady level flight) × V / (V_batt × I)
   - CD0 and e from glide and steady segments, using recursive least squares with confidence bounds
   - motor-heat estimate from I²R with a first-order thermal time constant, calibrated by bench VC-R07-4
4. **Live mission numbers:** remaining range and endurance from the measured Wh/km and the remaining battery energy. These are shown against the twin's prediction band (D-32 confidence banding).
5. **Dashboard:** the twin viewer page gains a live panel (link quality, residuals, estimates, remaining range).
6. **Replay:** the same pipeline runs on .bin logs, so every flight becomes a calibration run.
7. **SITL first:** the whole chain is tested against ArduPlane SITL feeding JSBSim before any hardware exists. That is purely simulation-first and within D-32.

## 6. Verification

| # | Check | Accept |
|---|---|---|
| VC-L1 | SITL end-to-end: SITL → router → bridge → shadow JSBSim | Residuals < 1 m/s, < 0.5 m/s climb, < 3° pitch on the scripted circuit |
| VC-L2 | Bench, onboard wireless: live V/A vs the WM150 wattmeter | Current within ±0.1 A at 1–3 A after calibration |
| VC-L3 | Bench: mLRS RX current at the chosen power setting | Measured and entered into the hotel budget; range re-issued |
| VC-L4 | Ground range test, aircraft on a stand | Link quality > 80% at 1 km with a 2–5 Hz telemetry stream; RC failsafe triggers RTL on link loss |
| VC-L5 | Flight 1–2 | Twin shadow residuals logged; estimators converge inside the D-32 bands, or a drift finding is raised |

## 7. Plan and ECDs

| Step | Owner | ECD |
|---|---|---|
| CE-02 review (this doc) | Oubi (MBSE) | 09:00 sync, Oct 15 |
| Ground-kit decision and order (handset + mLRS TX + RX) | CEO | With the parts order |
| SITL + bridge + shadow-mode prototype (VC-L1) | Claude | Oct 20 |
| CAD/CG update for the RX move, after MBSE approval | Claude | Oct 21 |
| Bench VC-L2/L3 (added to the Oct 26–27 session) | Claude + CEO hands | Oct 27 |
| Range test VC-L4 | CEO (field) + Claude (data) | Before Gate 5 |
