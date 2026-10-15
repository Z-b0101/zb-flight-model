# CE-02: Live digital-twin link (aircraft ⇄ twin in real time)

| | |
|---|---|
| Owner | Claude (GM/DE), at CEO direction ("take ownership", 2026-10-14 19:40 PT) |
| Rev | **Rev A (19:55 PT):** re-optimised for design, not cost. CEO direction 19:48 PT: "don't worry about money unless ≥ $500; we don't need to use the exact receiver I have; focus on design optimization" |
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

## 3. Flight-link options (re-optimised for mass, power and link quality; cost is not a driver below $500)

| Option | Aircraft mass | Aircraft power | Telemetry downlink (MAVLink) | Range | Verdict |
|---|---|---|---|---|---|
| **A. ExpressLRS LR1121 + ESP32-C3 receiver, MAVLink mode (ELRS ≥ 3.5). RadioMaster XR3 Nano (diversity) or XR1 Nano** | **1.0–1.3 g + antenna (~1.8 g total, est.)** | 100 mW telemetry; est. **~0.3–0.5 W** total. Measure on the bench | 900 MHz LR1121: up to ~4.4 kB/s (K1000 Full), ~0.9 kB/s dual-band 100 Hz. ELRS docs **recommend LR1121** for MAVLink | 900 MHz LoRa, long range. To be range-tested (VC-L4) | **RECOMMENDED.** Lightest, lowest power, single RC + MAVLink link. The XR3 is in stock at RadioMaster ($29.99); the XR1 dual-band is in stock ($11.99) |
| B. mLRS 900 MHz (Matek mR900-30 RX) | 5.3 g | Up to 1.7 W at 30 dBm | Full MAVLink | 7–87 km (mLRS docs) | Strongest long-range story, but **+3.5 g and up to +1.2 W** vs A. Keep as the upgrade if VC-L4 shows A falls short |
| C. 4G/LTE modem | 15–30 g | 1–2 W | Unlimited | Coverage | Too heavy and power-hungry. Revisit for beyond-line-of-sight work |

**Ground kit (cost not a driver, total < $500):**
- **RadioMaster Nomad**: dual 1 W, Gemini Xrossband, two LR1121, ESP32 + ESP32-C3 backpack (WiFi/Bluetooth MAVLink to the ground station). ~$50–58.
- **An EdgeTX handset with an external module bay**, e.g. RadioMaster TX16S MKII (JR bay), ~$250.
- Stock is patchy: the Nomad is sold out at Pyrodrone and BuddyRC, unconfirmed at RaceDayQuads; the TX16S MKII is sold out at RadioMaster. **Buy from any dealer in stock.** Model choice is the CEO's (he flies the maiden, D-27).

## 4. Effect on the frozen CE-01 baseline (option A)

| Item | Change |
|---|---|
| Mass | Remove the F-08A RX (5 g) + PWM→PPM encoder (3 g); add an XR3 + antenna (~1.8 g est.) → **−6.2 g net** (226.8 g AUW, **margin 23.2 g**) |
| CG / SM | **Taking 8 g out ahead of the CG moves the CG aft**, and the tiny receiver can't compensate:<br>• receiver at x = 106 mm: SM 5.33% (**fails the 5.5% rule**)<br>• receiver at x = 80 mm: 5.43%<br>• receiver at x = 60 mm: 5.51%<br>• receiver at x = 40 mm: **5.59%**<br>**Requirement: receiver at x ≤ 60 mm (nose bay)**, or recover about 1 mm of CG with the battery (`battery_u` 0.160 → ~0.155, if the tray fits). MBSE decision |
| Hotel power | +0.3 to 0.5 W est. → about 4–6% range at 7 m/s vs the 1 W budget. **Bench VC-L3 measures it** |
| FC ports | UART1: ELRS/CRSF RC + MAVLink. In ELRS MAVLink mode, RC and MAVLink share one UART: `SERIAL1_PROTOCOL 2`, `SERIAL1_BAUD 460`, `RSSI_TYPE 5`; set the SRx/MAVx rates per the ELRS docs. SERIAL6: onboard wireless for the bench. Integrated V/A sensor: **calibrate `BATT_AMP_PERVLT` against the WM150** |
| CAD | Replace the `rx`/`encoder` LRUs with `elrs_rx` at x ≤ 60 mm; antenna-route wire clear of the spar and motor leads; re-run clash and CG |
| Regulatory | 902–928 MHz and 2.4 GHz unlicensed (FCC Part 15). Confirm the power and antenna settings |

**Design-optimisation note:** the link frees **6.2 g**, which raises the margin to 23.2 g. That strengthens the 850 mAh battery case in the 17 g trade study (+12 g battery → +27% range). The battery also sits forward of the CG, so it **raises** SM and would offset the receiver's CG penalty. CE-02 and the battery decision should be reviewed together after parts are weighed.

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
| VC-L3 | Bench: link RX current at the chosen telemetry power | Measured and entered into the hotel budget; range re-issued |
| VC-L4 | Ground range test, aircraft on a stand | Link quality > 80% at 1 km with a 2–5 Hz telemetry stream; RC failsafe triggers RTL on link loss |
| VC-L5 | Flight 1–2 | Twin shadow residuals logged; estimators converge inside the D-32 bands, or a drift finding is raised |

## 7. Plan and ECDs

| Step | Owner | ECD |
|---|---|---|
| CE-02 review (this doc) | Oubi (MBSE) | 09:00 sync, Oct 15 |
| Ground-kit + RX order (Nomad + EdgeTX handset + XR3/XR1) | CEO (cost < $500, no money gate) | With the parts order |
| SITL + bridge + shadow-mode prototype (VC-L1) | Claude | Oct 20 |
| CAD/CG update for the RX move, after MBSE approval | Claude | Oct 21 |
| Bench VC-L2/L3 (added to the Oct 26–27 session) | Claude + CEO hands | Oct 27 |
| Range test VC-L4 | CEO (field) + Claude (data) | Before Gate 5 |
