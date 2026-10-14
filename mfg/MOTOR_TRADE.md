# R-07: Motor / ESC / propeller trade (closure proposal)

| | |
|---|---|
| Owner | Claude (GM/DE), 2026-10-14 |
| Status | **Proposed.** Mass/CG acceptance and the DR-14 notch are MBSE decisions (CE-01, Fri Oct 16). The CEO places the order. |
| Branch | `r07/motor-trade` (from `ce/dr01-dr02` @d0173d5) |
| Tools | `scripts/motor_trade.py` (prop + motor physics), `scripts/prop_notch.py` (clearance + notched-wing VLM), `scripts/mass_rollup.py` (extended: `--prop-g --adapter-g --notch-dia-in`), `tests/test_motor_trade.py` |

## 1. Recommendation

| Item | Pick | Mass | Why |
|---|---|---|---|
| Motor | **Suppo 2204/14 1400kv** (Park 300 class), ×2 (one spare, D-17) | 20 g | Fixed-wing outrunner made for 8 in props on 2–3S. Published Kv / Rm / Io. In stock in the US. Best motor constant available at ≤ 20 g |
| Prop | **APC 8x6SF** (slow flyer), ×3 | 7.1 g | Best measured efficiency of the four 8 in props with UIUC wind-tunnel data (η_prop 0.70–0.72 in cruise). Lighter than the 7040-3 it replaces |
| Prop adapter | Scorpion 3 mm threaded adapter (M5), ×2 | 5.1 g | APC hub has a 6.35 mm bore. The motor's O-ring prop saver has a reported prop-loss review, so it is not used |
| ESC | **EMAX Bullet 30A** (BLHeli_S, DShot), ×1 | 3.5 g | Same board and mass as the Bullet 20A in CAD, so no layout change. Meets MBSE's 30 A floor. 2.5× the worst-case current |
| Setting | **ArduPlane THR_MAX = 65%** | — | Holds full-throttle motor current at 7.0 A (rating 7.5 A / 60 s) on a fresh pack |
| Design change | **DR-14: trailing-edge prop notch** (see §3) | −1.0 g net | Without it the propeller strikes the wing (any prop from 5 to 8 in) |

Rejected: HGLRC Specter 1404 4800KV (2.5–4 in props, ~66 A at full throttle on a 7 in prop). EMAX ECO II 2004 (cinewhoop motor, 1.5 mm T-mount). EMAX MT1806, DYS D2822 (38 g), A2204 / X2204 (no data, sold out). HobbyStar 2204-27 and Scorpion SII-2205 (30–35 g, over the CG cap). Gemfan 7040 3-blade (a quad prop; see §4).

## 2. Requirements (twin, 213.9 g basis; stacked 233 g checked in §6)

| Point | Airspeed | Thrust needed | Source |
|---|---|---|---|
| A2 endurance cruise | 7.05 m/s | 0.240 N | twin `mission()` |
| A2 range cruise | 10.45 m/s | 0.375 N | twin `mission()` |
| Fast cruise | 14 m/s | 0.622 N | twin `trim(14)` |
| Climb, 2 m/s at 10 m/s | 10 m/s | 0.770 N | D + W·sinγ |
| Hand launch | 0 | ≥ 1.1 N (T/W ≥ 0.5), prefer ≥ 2 N | program launch rule |
| Motor current | — | ≤ rated, every mode | vendor rating |

## 3. Finding: the pusher prop cuts through the wing (DR-14)

The prop plane sits at 205.6 mm aft of the root LE (CAD `prop` u = 1.028), 5.6 mm behind the root trailing edge. With 25° of sweep, the trailing edge is aft of that plane everywhere outboard of |y| ≈ 12 mm. As modelled:

| Prop | Blade inside the wing for | Clear without a notch needs the prop plane at |
|---|---|---|
| 5 in | 12–64 mm each side | ≥ 234.6 mm (+29 mm) |
| 7 in | 13–89 mm | ≥ 246.5 mm (+41 mm) |
| 8 in | 15–102 mm | ≥ 252.4 mm (+47 mm) |

**Why it was missed:** `cad/build_systems.py` skips prop-vs-anything in the clash check, and there is no prop-disc vs skin check. Proposed fix to the check (MBSE-owned code): add the swept prop disc as a volume and test it against the skins.

**Options considered:**
- **Stand-off mount (rejected).** Moving the motor about 47 mm aft costs about 2.5 points of static margin and leaves a long lever arm for belly landings.
- **TE notch (proposed).** Cut the wing aft of x_n = 195 mm for |y| ≤ r + 5 mm. For an 8 in prop that is ±106.6 mm.

**Notch (8 in prop), from `scripts/prop_notch.py`:**

| Quantity | Value |
|---|---|
| Planform removed | 63.6 cm² (3.5% of S) |
| Foam removed | 1.5 g at 213 mm |
| Edge closure | +0.5 g (3 mm Depron strip along x_n, plus two chordwise closures at y = ±106.6 mm) |
| NP shift (twin VLM re-run with notched chord, ns = 80) | **−0.98 mm** (142.35 → 141.37) |
| CLα | 0.0632 → 0.0623 /deg (−1.4%) |
| Cm_δe | −0.0273 → −0.0266 /deg (−2.6%) |
| Gap to elevon root (y0 = 112.5 mm) | **5.9 mm** (tight: hold ±1 mm at the cut) |
| R2 hinge-line web | Ends at |y| = 96.5 mm, terminated on the notch closure. Inboard of the elevons it carries no hinge load |

A 7 in prop needs a smaller notch (2.8% of S, ΔNP −0.71 mm, 18.6 mm from the elevon root, R2 web untouched). There is no wind-tunnel data for 7 in electric props, though, and the 8 in props are the measured ones. Proposed params keys (design-hash change, for MBSE to merge): `prop_notch_x` 195.0, `prop_notch_halfspan` 106.6, `prop_dia_in` 8.0.

**Ground strike:** the prop tip reaches about 100 mm below the belly. A stopped prop that ends up vertical will strike on a belly landing. This is accepted as an expected event (FHA #7, D-17 spares): three props are on the buy list. A folding prop is the later upgrade, but there is no measured data for one yet.

## 4. Method

**Propeller.** Measured CT(J) and CP(J) from the UIUC Propeller Data Site vol. 1 (Brandt & Selig): static runs plus the ~4000 rpm wind-tunnel runs. Files are cited in `scripts/motor_trade.py`. For each flight point the script solves for the rpm that gives T = D (or the climb thrust).

**Motor.** Drela three-constant model: Q = (I − Io)/Kv, V = ω/Kv + I·(Rm + R_wire).

**ESC and battery.** ESC efficiency 0.95 and wiring 0.02 Ω (ASSUMED). Pack 0.06 Ω (ASSUMED). Full-throttle cases are run at 12.6 V and 11.1 V.

**No-load current Io.** Vendor Io is measured at 10 V no-load (~14,000 rpm). Cruise runs at 3–4k rpm, where iron loss is lower. Results are shown two ways: Io constant (conservative) and Io scaled with √rpm (best estimate). The bench test closes the gap (§8).

**Why the 7040 3-blade was wrong.** A 3-blade quad prop at low J has poor efficiency, and needs about 2× the torque per unit thrust of an 8 in 2-blade at our cruise speeds. That torque is what drove the over-current on every small motor tried.

## 5. Results (Suppo 2204/14 1400kv)

**Cruise and climb, by prop:**

| Prop | Point | rpm | J | η_prop | I (A) | P_elec (W) | η_total (Io const / scaled) | Twin assumed η | Throttle |
|---|---|---|---|---|---|---|---|---|---|
| **8x6SF** | Endurance 7.05 m/s | 2876 | 0.72 | 0.72 | 1.45 | 4.38 | **0.39 / 0.45** | 0.35 | 26% |
| **8x6SF** | Range 10.45 m/s | 3993 | 0.77 | 0.70 | 2.26 | 9.88 | **0.40 / 0.43** | 0.54 | 37% |
| **8x6SF** | Climb | 4556 | 0.65 | 0.72 | 3.58 | 19.94 | 0.39 / 0.41 | 0.55 | 48% |
| 8x6E | Range 10.45 m/s | 4241 | 0.73 | 0.66 | 2.27 | 10.34 | 0.38 / 0.41 | 0.54 | 39% |
| 8x4E | Range 10.45 m/s | 5635 | 0.55 | 0.55 | 2.06 | 11.26 | 0.35 / 0.37 | 0.54 | 47% |
| 8x3.8SF | Range 10.45 m/s | 5661 | 0.55 | 0.42 | 2.61 | 15.19 | 0.26 / 0.27 | 0.54 | 50% |

**Full throttle, static, 12.6 V:**

| Case | rpm | Thrust | T/W | Motor I | vs 7.5 A rating |
|---|---|---|---|---|---|
| 8x6SF, unlimited | 6855 (SF limit 8125) | 4.28 N | 2.04 | 12.2 A | **1.63× — not allowed** |
| **8x6SF, THR_MAX 65%** | — | **2.45 N** | **1.17** | **7.0 A** | 0.93× |
| 8x6SF, THR_MAX 65%, at 10 m/s | — | 1.67 N (climb needs 0.77 N) | — | — | — |

**Motor losses.** In cruise the motor runs at 57–62% efficiency. Copper loss (I²·Rm, with Rm = 0.55 Ω) and no-load loss dominate at 1.5–2.3 A. That is physics for a 20 g motor, not a poor choice.

**Mass vs efficiency.** A 30 g motor (HobbyStar 2204-27, motor constant 1.4× higher) gains about 3 points of η_total. Its +10 g sits 60 mm behind the CG and costs about 1.3 points of static margin, which is not a good trade.

## 6. Mass, CG and static margin (stacked, `scripts/mass_rollup.py`)

Pick: motor 20 g, prop 7.1 g, adapter 5.1 g, notch for 8 in, battery 3 mm forward, ESC at 95 mm.

| Step | Mass (g) | CG (mm) | SM |
|---|---|---|---|
| … SA-01 R2–R5, DR-01 fins | 219.7 | 131.10 | 5.24% |
| DR-14 notch (foam out, closure in) | 218.7 | 130.67 | 5.46% |
| Prop 7.1 g (vs 7.9 g) | 217.9 | 130.39 | 5.59% |
| Prop adapter 5.1 g | 223.0 | 131.99 | 4.80% |
| Motor 20 g (vs 10 g) | 233.0 | 134.56 | 3.51% |
| Battery 3 mm forward, ESC to 95 mm | **233.0** | **132.41** | **4.58%** — below the 5% floor and the 5.5% rule |

**The CG has to come forward by 1.84 mm (≈ 430 g·mm) to reach SM 5.5%.** Ways to do it, any one of which closes it:

| Lever | Amount for SM 5.5% | Amount for the 5.0% floor | Cost |
|---|---|---|---|
| FC (23 g) moved forward | 18.6 mm | 8.5 mm | Layout (MBSE): FC tray in R5 / hatch |
| Battery further forward (beyond the 3 mm) | +6.9 mm (total 9.9 mm) | +3.2 mm | Hatch / tray geometry; pack protrudes more below the skin |
| Nose ballast at x ≈ 5 mm | 3.4 g (AUW 236.4 g) | 1.5 g | Mass only; last resort per the rule |

**CEO decision (2026-10-14, 15:55 PT): option 1, layout only, no ballast.** I checked it in real CadQuery 2.8.0 (`cad/build_all.py --params cad/params.json`).

**FC +10 mm does not fit.** At its outboard corners the FC hits the swept spar tube (clearance −1.4 mm, CLASH). A sweep of feasible pairs found:

| FC forward | Battery forward (total) | FC–spar clearance | Clash check | Moment gained | SM |
|---|---|---|---|---|---|
| 10 mm | 7 mm | **−1.42 mm (CLASH)** | 3 CLASH | 478 g·mm | — |
| 6 mm | 8 mm | 2.03 mm | 0 / 0 | 448 g·mm | ≈5.56% |
| **5 mm** | **9 mm** | **2.94 mm** | **0 CLASH / 0 TIGHT** | **487 g·mm** | **5.63%** |
| 4 mm | 10 mm | 3.84 mm | 0 / 0 | 464 g·mm | ≈5.60% |

**Implemented (proposed baseline change at CE-01):** FC 5 mm forward (`build_systems.py` FC u 0.475 → 0.450) and battery 9 mm forward (`params.json` `battery_u` 0.205 → 0.160; design hash 9d4f5b2e493a). The XT30 pigtail (w2) is re-routed to exit above the tray wall.

- Full `build_all.py`: CAD-basis CG 128.5 → 125.2 mm; 0 CLASH / 0 TIGHT; `verify_params` and `verify_cad` all pass; all parts watertight.
- Stacked roll-up (`mass_rollup.py --battery-fwd-mm 9 --fc-fwd-mm 5 --esc-to-mm 95`, full R-07 power train + notch): **233.0 g, CG 130.32 mm, SM 5.63%**. Meets the ≥ 5.5% rule.

**Side effects:**
- **Pack sits 4.4 mm lower.** The airfoil is thinner further forward, so the tray bottom moves from z −15.7 to −20.0 mm. The lid is therefore a deeper belly bump: a little more drag, and the first ground contact on landing.
- **SA-01 hatch-FE to re-run** at the new aperture (u 0.075–0.245, was 0.12–0.29). The aperture aft edge is now 11 mm ahead of the spar (was 2 mm), which is a likely improvement. Bearing-lid landing case to re-check. ECD Oct 16, GM.
- The twin's record CG (128.5 mm) is unchanged until MBSE re-baselines at CE-01. The SM above comes from the roll-up.

**AUW.** 233.0 g planning (236.4 g with ballast), against the 250 g limit. The weigh-as-you-go rule (R-05) stays in force. The powertrain parts are **weighed at receipt** and the roll-up re-run before any CG change is built.

## 7. Performance with this hardware (physics model, stacked 233 g)

| Cruise | Range | Endurance | Battery power |
|---|---|---|---|
| **7.0 m/s** | **26.0–29.3 km** | **62–70 min** | 4.7–5.3 W |
| 10.45 m/s (the twin's range point) | 19.6–21.2 km | 31–34 min | 10–11 W |

The twin's own η model gives 26.2 km / 57 min at the same mass.

**Reading:**
- The investor numbers (26 km / 59 min) are supported, but at about **7 m/s cruise**, not 10.5 m/s.
- The twin's ASSUMED derate η = min(0.55, 0.20 + 0.0875·P) has the wrong shape for a real 20 g motor and 8 in prop. It is too pessimistic at 7 m/s (0.35 vs 0.39–0.45) and too optimistic at 10.5 m/s (0.54 vs 0.40–0.43).
- Proposal to MBSE: after the bench test, replace the derate with this physics model (`motor_trade.prop_point` + `motor_point`), calibrated by the measured Rm and Io. That is a twin assumption change and is MBSE's call.
- Operating effect: in a headwind, cruise faster and accept the range loss. The flight cards should carry cruise at 7–8 m/s in calm air.

## 8. Verification (bench session Oct 26–27, wattmeter + 0.1 g scale)

| # | Test | Accept |
|---|---|---|
| VC-R07-1 | Weigh motor, prop, adapter, ESC at receipt | Re-run `mass_rollup.py`; SM ≥ 5.5% after the chosen lever |
| VC-R07-2 | THR_MAX = 65%, fresh pack (≥ 12.5 V), static full stick in **every mode including MANUAL** | Motor current ≤ 7.5 A (target 7.0 A) on the wattmeter |
| VC-R07-3 | Static thrust at THR_MAX (motor on a lever on the scale) | ≥ 1.6 N (prediction 2.45 N) |
| VC-R07-4 | 60 s at THR_MAX, then motor can temperature | < 70 °C |
| VC-R07-5 | Measure Io (no prop, 10 V) and Rm (loaded points at 20–50% throttle) | Within ±25% of vendor values (0.30 A / 0.55 Ω). Then feed them into the model and re-issue §7 |
| VC-R07-6 | Thrust direction and prop retention (pusher: lettered face forward, motor direction set in BLHeli) | Air blows aft. Adapter nut torqued and marked; no slip after 60 s at THR_MAX |
| VC-R07-7 | Prop vs notch clearance (all angles, motor bell and hub included) | ≥ 5 mm everywhere |

## 9. Buy list (CEO places the order; GM authority $500, D-23)

| # | Item | Qty | Shop | Unit (USD) | Stock (checked 2026-10-14) |
|---|---|---|---|---|---|
| 11 | Suppo 2204/14 1400kv motor | 2 | [Altitude Hobbies](https://www.altitudehobbies.com/products/suppo-2204-14-1400kv-brushless-motor-park-300-equiv) | 17.59 | In stock |
| 12 | EMAX Bullet 30A ESC (EMX-SC-1774) | 1 | [Pyrodrone](https://pyrodrone.com/products/emx-sc-1774-d-shot-bullet-series-30a-escblheli_s) (same order as battery and wattmeter) | 22.80 | In stock |
| 13 | APC 8x6SF prop | 3 | [ReadyMadeRC](https://www.readymaderc.com/products/details/apc-8x6-sf-prop) (same order as servos) | 2.78 | "Only 3 left" |
| 13b | APC 8x3.8SF prop (alternate if 8x6SF sells out; η about 25% worse) | 2 | [ReadyMadeRC](https://www.readymaderc.com/products/details/apc-8x3-8-sf-prop) | ~2.8 | Check at checkout |
| 14 | Scorpion 3 mm threaded prop adapter (M5) | 2 | [Scorpion](https://www.scorpionsystem.com/catalog/aeroplane/accessories_3/prop_adapter/PropAdapter3/) | 3.09 | In stock |
| | **R-07 subtotal** | | | **~$80** (with alternates) | Plus one extra shipment (Altitude Hobbies, Scorpion) |

**Cancelled from the cart:** Specter 1404 4800KV, EMAX Bullet 20A, Gemfan 7040-3.

APC SF props ship with adapter rings. Check for a ring that fits the M5 adapter thread at receipt; if none, buy the APC LPAR06E ring set (about $2).

## 10. Open items and ECDs

| # | Item | ECD | Owner |
|---|---|---|---|
| 1 | MBSE review of DR-14 notch, CG lever, ESC (30 A floor met) | CE-01, Oct 16 | Oubi |
| 2 | Dimensioned drawing of the notch, motor mount (31 × 31 mm X-mount on the R5 centre section) and closure | Oct 16 12:00 PT (with the R2–R5 drawings) | Claude |
| 3 | Prop-disc clash check in `build_systems.py` | Oct 16 | MBSE (Claude can draft) |
| 4 | Replace the twin η derate with the physics model, after VC-R07-5 | Oct 28 (CDR) | MBSE |
| 5 | Folding-prop option (strike mitigation) | After the first flights | Claude |

Sources: [UIUC Propeller Data Site vol. 1](https://m-selig.ae.illinois.edu/props/volume-1/propDB-volume-1.html); [Suppo 2204/14 (Altitude Hobbies)](https://www.altitudehobbies.com/products/suppo-2204-14-1400kv-brushless-motor-park-300-equiv); [EMAX Bullet 30A specs (GetFPV)](https://www.getfpv.com/emax-d-shot-bullet-series-30a-esc-blheli-s.html); [Pyrodrone listing](https://pyrodrone.com/products/emx-sc-1774-d-shot-bullet-series-30a-escblheli_s); [APC 8x6SF (ReadyMadeRC)](https://www.readymaderc.com/products/details/apc-8x6-sf-prop); [APC 8x6SF (Motion RC)](https://motionrc.com/products/apc-8x6-slow-flyer-electric-propeller-lp08060sf); [Scorpion 3 mm adapter](https://www.scorpionsystem.com/catalog/aeroplane/accessories_3/prop_adapter/PropAdapter3/); [HobbyStar 2204 (RCJuice)](https://rcjuice.com/products/hobbystar-2204-2822-brushless-outrunner-motor); [Scorpion SII-2205-1490KV](https://www.scorpionsystem.com/catalog/aeroplane/motors_1/s-22_v2/SII-2205-1490KV).
