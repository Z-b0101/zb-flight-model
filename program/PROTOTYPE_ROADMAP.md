# Prototype roadmap: from frozen design to a flying, sub-250 g prototype

**Owner:** Claude (GM). **Reviewer:** Oubi (MBSE). **Decision authority:** CEO.  
**Status:** DRAFT v0.1, 2026-10-14, for MBSE feedback.  
**Asked for by:** CEO, 09:28 PT 2026-10-14, after the investor meeting ("investors are waiting for a prototype").  
**Configuration:** `cad/params.json` design hash `7be168427b4d`; twin frozen at `freeze/report-2026-10-14` @1883c1c.  
**Ground rules from the CEO (2026-10-14):** no date was given by investors, so this plans to the fastest *credible* date and shows what each week buys. **Gate 4 stays as is:** no flight article is built before Gate 4 authorization.  

---

## 1. The answer in one paragraph

A flying prototype is about **four weeks** away if three things happen this week: the CEO approves a **$246 calibration buy** (bench and coupon hardware the gates themselves require), names **who does the physical work**, and closes the **TDR**. On that basis:

- Gate 4 (build authorization) lands **Fri Oct 30**.
- The prototype is built and weighed under 250 g by **Fri Nov 6**.
- First flight is targeted for **Nov 10–13**, weather permitting.
- Ten autonomous flights with a flight-calibrated twin follow by about **Fri Nov 20**.

Money is not the constraint. The whole prototype is about $361 against a $10,000 budget. The schedule is set by parts lead time, physical hands, and the gate evidence.

## 2. Why Gate 4 needs hardware before Gate 4

The gate register (DEV_TRACKER §6) says *no major prototype spend before Gate 4*. But reaching Gate 4 requires evidence that only hardware can produce:

| Gate | What it requires | Needs hardware? |
|---|---|---|
| CDR | TDR closed + **measured 3S discharge curve** + **measured hotel load** (HOTEL_LOAD_PLAN) | Yes: battery, charger, wattmeter, avionics |
| Gate 2 | Model credibility: traceability, independent checks, sensitivity | No (digital) |
| Gate 3 | **Coupon, rib/bond tests, component weights, bench data** | Yes: Depron, carbon, filament, glue, scale, power train |
| Gate 4 | Closed interfaces, mass margin, CG range, control authority, test plan | Uses Gate 3 data |

So this roadmap separates two kinds of spend:

- **Calibration buy (before Gate 4):** test articles that retire named uncertainties ("model before money", D-15). The bench avionics are reused in the flight article, so nothing is wasted.
- **Flight-article commitment (Gate 4):** the decision to build and fly. Gate 4 is unchanged.

The calibration buy is a **CEO money decision**. This roadmap recommends it and does not assume it.

## 3. Costed buy list (prices verified 2026-10-12 in BUDGET.md; re-verify at order)

| Buy | Items | Cost | When |
|---|---|---|---|
| **A. Calibration buy** (needs CEO approval) | Airframe materials: Depron ×4, 4 mm carbon tube, filament, CA + hot glue, hinge tape, linkages ($53) · 1× 1404 motor, Bullet 20A ESC, Flash 7040 props ($36) · 1× 3S 650 mAh pack ($15) · balance charger ($28, skip if on hand) · wattmeter ($17) · 0.1 g scale ($12, skip if on hand) · FC SpeedyBee F405 WING MINI, M100-5883 GPS, PPM encoder, 2× ES9051 servos ($85) | **$246** (−$40 if charger and scale are on hand) | Order **by Fri Oct 16** |
| **B. Flight-article top-up** (at Gate 4) | Spare motor ($17, pushers eat motors on belly landings) · second 3S pack ($15) | **$32** | Order **Fri Oct 30** |
| Deferred | Payload placeholder ($50): PoC flies 0 g (D-05) | $0 now | Family-instance decision |
| | **Total to a flying prototype** | **$278 + 10% contingency ≈ $306** | |

Buy from reputable shops: there is one DOA report on the F405 WING MINI in the wild (BUDGET.md).

## 4. Phased plan with dates

Dates assume the calibration buy is ordered by Fri Oct 16 and arrives in 3–5 days (domestic shipping; **assumption**, to be confirmed at order). They also assume a builder with about 2 bench days a week in Phase 1 and 4 days in the build week.

### Phase 0: Close the design and decide (Wed Oct 14 – Sat Oct 17), digital
| Item | Owner | Due | Output |
|---|---|---|---|
| CE-01 (mass/CG) + CE-02 (coordinate convention) closure | Claude; Oubi reviews | Fri Oct 16 EOD | Reconciled mass/CG; drag basis |
| **Gate 1 baseline freeze** (WS-22) | Claude; Oubi signs | Fri Oct 16 | `params_GATE1_v1.0` |
| MfgE desk pack M1–M5: DFM review, **spar root joiner**, washout jig drawing, **coupon test card**, as-built mass sheet | MfgE (agent, option A) | Fri Oct 16 | `mfg/` procedures a builder can follow |
| Order the calibration buy | CEO approves; Claude prepares the cart | Fri Oct 16 | Order confirmations |
| WS-25 airframe recommendation | Claude + Oubi | Sat Oct 17 | Investor-visible, with stated caveats |
| **ArduPlane SITL closed loop** on the twin (Plane-4.7.1, JSBSim backend) | Claude | starts Oct 15, done Fri Oct 23 | Autonomous mission flown in simulation: takeoff, waypoints, RTL |

### Phase 1: Calibrate (Mon Oct 19 – Fri Oct 30), physical + digital in parallel
| Item | Owner | Target | Output |
|---|---|---|---|
| Parts arrive; weigh every part on receipt (R-05, R-06) | Builder | Tue–Wed Oct 20–21 | As-built mass sheet, first real rows |
| **Coupon test** (RQ-04): Depron sheet weight, test rib print + fit (R-03), glue-joint peel, carbon bend coupon, **one joiner sample** | Builder runs the card; Claude reduces the data | Wed–Thu Oct 21–22 (overnight cure) | MATERIALS.md + twin ledger: E, allowable, glue, rib mass become `measured` |
| Gate 2 credibility package | Oubi leads; Claude supports | Fri Oct 23 | Traceability, independent checks, sensitivity |
| **Bench session B3:** motor/prop wattmeter (R-07), **hotel load M5**, **3S discharge curve**, 5 V rail (R-10), compass EMI (R-11), pusher cooling (R-08), RC link via encoder (R-09), servo throw vs ±8° | Builder runs; Claude writes the cards and reduces the data | Mon–Tue Oct 26–27 | The three biggest unknowns (η, hotel load, usable energy) become measured |
| **Twin re-run on measured values**; range/endurance re-issued; L1→L2 promotion begins | Claude; Oubi verifies | Tue Oct 27 | New range numbers, labeled measured vs assumed |
| CDR | CEO go/no-go; package by Claude + Oubi | Wed Oct 28 | CDR record |
| Gate 3 package | Oubi leads | Thu Oct 29 | Calibrated parameters |
| **Gate 4: prototype authorization** | **CEO** | **Fri Oct 30** | Build authorization (Class D); order buy B |

### Phase 2: Build (Mon Nov 2 – Fri Nov 6), physical
| Item | Target | Notes |
|---|---|---|
| Print 8 ribs + joiner + hatch parts | Mon Nov 2 | Plain PLA unless the coupon says otherwise (R-04) |
| Skin on the washout jig; bond the spar with the root joiner | Tue–Wed Nov 3–4 | Jig mandatory: 6° washout is at the Depron limit (R-01) |
| Install the bench-proven power train and avionics; hatch and battery retention (R-17) | Wed–Thu Nov 4–5 | Bench hardware reused |
| **Weigh-in and CG balance** | **Thu Nov 5** | **No-fly above 250 g**; review below 10 g margin; CG to 128.5 mm with the battery as trim weight (R-15) |
| Ground checks: control throws and direction, failsafe, GPS/compass health, range check, ArduPlane params from the SITL tune | Fri Nov 6 | Test cards written in Phase 1 |

### Phase 3: Fly (Mon Nov 9 – Fri Nov 20), physical
| Item | Target | Notes |
|---|---|---|
| Gate 5 readiness review: test cards, site, weather, crash plan | Mon Nov 9 | Foam for two airframes is in buy A (R-02); a rebuild takes about 1–2 days |
| **Maiden flight**: hand launch, FBWA, manual landing | **Tue–Fri Nov 10–13** | Weather window; angle mode from the maiden (RQ-23) |
| Flight campaign: 10 autonomous flights incl. RTL; logs ingested | through Fri Nov 20 | Twin calibrated against flight data (**L2**); range claim confirmed or corrected |

## 5. What investors see, and when

| Date | Milestone | Evidence |
|---|---|---|
| Sat Oct 17 | Airframe recommendation + design frozen | WS-25 note; Gate 1 freeze |
| Thu Oct 22 | First physical parts tested | Coupon photos + measured numbers |
| Fri Oct 23 | **Autonomous mission flown in simulation** on the real autopilot firmware | SITL video/track |
| Tue Oct 27 | **Power train and electronics proven on the bench**; range re-issued on measured data | Bench data sheet; updated range |
| Fri Oct 30 | Build authorized (Gate 4) | Gate record |
| Thu Nov 5 | **Prototype on the scale, under 250 g** | Photo on the scale |
| Nov 10–13 | **First flight** | Flight video + log |
| ~Fri Nov 20 | **10 autonomous flights; twin calibrated against flight** | Flight logs; measured vs predicted range |

## 6. Decisions needed from the CEO (this week)

1. **Approve the $246 calibration buy** (or the $206 version if the charger and scale are on hand), ordered by Fri Oct 16. Every day it slips moves the whole roadmap a day.
2. **Name who does the physical work.** AI agents can write procedures and reduce data, but cannot weigh, print, glue or fly. The coupon test is already the CEO's open action (RQ-25). Options from mfg/ONBOARDING.md:
    - A: the CEO executes with agent-written cards.
    - B: hire a human technician. A local RC-club builder or a hobby-shop technician for about 2 weeks of part-time work is the fastest route; cost is not estimated here.

    The dates above need roughly **2 bench days/week in Phase 1 and 4 days in the build week**.

3. **Close the TDR (P-13)**: it is a CDR entry criterion. The recommendation on record is "proceed with actions".
4. Confirm **who flies the maiden** and where (a field and an experienced RC pilot reduce R-02 risk).

## 7. What could move the dates

| Risk | Effect | Mitigation |
|---|---|---|
| Parts arrive later than 5 days, or a DOA flight controller | Day for day on everything | Order Fri Oct 16 from reputable domestic shops; check stock at order |
| Physical work at less than the assumed pace | Phase 1 and the build stretch, up to 2× | Decision 2 above |
| **Coupon fails**: hybrid Depron/printed construction not viable (RQ-04 still "to be studied") | +1 to 2 weeks | **No construction fallback is on record today** (AIRFRAME_ARCHITECTURES' fallback is a configuration, the conventional tail, not a construction). MfgE to name one in M1 by Oct 16. The coupon runs first precisely to find this early |
| Hotel load > 2 W or efficiency far below the fit | Energy budget re-opened at CDR (HOTEL_LOAD_PLAN rule) | 750 mAh upsize (+10 g) is the best trade on record and fits the 38 g margin |
| Weigh-in above 250 g | No-fly | 38 g modeled margin; weigh-as-you-go from parts arrival |
| Maiden crash | +1 to 2 days rebuild | Spare foam, motor and pack in the plan |
| Weather | Maiden slips | Window spans 4 days; flight campaign has slack to Nov 20 |

## 8. What this roadmap does not change

- The 250 g cap (RQ-01) is inviolable.
- Gate 4 governs the build/fly decision.
- No gate consumes a model above its maturity: the twin is L1 until the bench data, L2 after flight.
- Every number traces to params.json or the assumption ledger.
