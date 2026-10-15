# Provisional-values register (D-32)

| | |
|---|---|
| Owner | Claude (GM/DE). **MBSE approves each entry** (Oubi, D-32 condition A) |
| Rule | Every unmeasured input used in simulation is listed here, with a low / best / high band, its source, and the checkpoint that replaces it with a measured value. Entries stay tagged **PROVISIONAL**. **They never land in `cad/params.json` without a CE item** (rule C). This register is scenario input, not design intent |
| Baseline | Frozen CE-01, hash `479399d88b60`, 233.0 g, CG 130.32 mm, SM 5.66% |
| Tool | `scripts/sensitivity.py`: each input is set alone to its band ends and checked against seven program decisions and claims. Results: `program/sensitivity_results.json` |

## 1. Register

| ID | Input | Low / **best** / high | Source | Checkpoint | Flips a decision? |
|---|---|---|---|---|---|
| P-01 | Overall propulsion efficiency η | 0.36 / **0.42** / 0.45 | `mfg/MOTOR_TRADE.md`: UIUC APC 8x6SF CT/CP + Suppo 2204/14 Kv/Rm/Io; band = Io constant vs Io ∝ √rpm, plus the low-Re penalty | Bench VC-R07-5 (Oct 26–27) | **YES**: low end gives range 24.3 km / 57.9 min (C1, C2) |
| P-02 | Hotel (electronics) power | 1.7 / **1.0** / 0.8 W | `HOTEL_LOAD_PLAN.md` budget; CE-02 link adds +0.3–0.5 W (ELRS) | Bench M-series + VC-L3 | **YES**: 1.7 W gives 24.4 km / 58.0 min. **With the CE-02 link at +0.4 W, the best estimate is 25.7 km** |
| P-03 | Usable battery fraction | 0.75 / **0.80** / 0.85 | GNB 3S 650 mAh spec; LiPo practice | Bench discharge curve (CDR entry criterion) | **YES**: 0.75 gives 25.9 km (C1) |
| P-04 | Misc. drag `cd_misc` | 0.018 / **0.012** / 0.008 | `zb_model/drag.py` flat placeholder; Hoerner build-up TODO | First flight (glide/power-off segments) + live twin estimator (CE-02) | **YES**: 0.018 gives 25.1 km (C1) |
| P-05 | Plain-flap effectiveness knockdown | 0.65 / **0.75** / 0.85 | Literature 0.7–0.8 (MBSE steelman); twin ASSUMPTIONS | Bench throw (VC-29) + flight trim vs speed | No. Slow-flight trim −7.1° at the low end (12° available) |
| P-06 | Fin endplate factor | 1.30 / **1.55** / 1.80 | `twin/lateral.py` ASSUMED (DATCOM/Helmbold build-up) | Flight VC-38 (yaw damping, spiral) | No. Cn-β 0.0011–0.0014 /deg |
| P-07 | Fin sidewash factor | 0.80 / **1.00** / 1.20 | `twin/lateral.py` ASSUMED | Flight VC-38 | **Marginal**: the low end gives Cn-β 0.0010, exactly the 0.001 target |
| P-08 | Aft-mass growth vs estimate (motor, prop, adapter, fins; ~200 mm) | +4 / **0** / −1 g | Vendor and catalogue weights; fins estimated at 1.0 g each | **Weigh at receipt (B-01)** | **YES**: +4 g gives SM 5.07% (C3 rule 5.5%) |
| P-09 | Motor Io and Rm vs vendor | ×1.25 / **×1.00** / ×0.85 | altitudehobbies.com Suppo spec | Bench VC-R07-5 | No. Static thrust at THR_MAX 2.10–2.71 N (≥ 1.6 N) |
| P-10 | Depron compression (crush) strength | 0.10 / **0.13** / 0.17 MPa | Independent CE audit; SA-01 | Coupons Oct 21–22 | **YES** (already mitigated): landing RF 0.98 at 0.10 MPa, so the bearing lid is mandatory (SA-01 R4) |
| P-11 | Spar tube flexural modulus / strength | Spec ≥ 100 GPa / ≥ 1 GPa (bought to spec, R1) | SA-01 R1 | 3-point-bend coupon (Oct 21–22) | YES if bought off-spec: gust RF 0.88 at the low grade. Mitigated by the spec |
| P-12 | Link receiver + antenna mass (CE-02) | 2.5 / **1.8** / 1.3 g | RadioMaster XR3 page (1.3 g bare) + antenna est. | Weigh at receipt (VC-L3) | Feeds C3. Receiver must sit at x ≈ 40–50 mm (MBSE condition) |

## 2. What the sweep says (single-factor, frozen baseline)

**Watch closely (any one of these, alone, at its pessimistic end, breaks a claim or rule):**
- **The investor range claim (26–29 km at 7 m/s) is fragile.** η, hotel power, usable energy and misc. drag each, alone, take range below 26 km. All four at the pessimistic end together give **18.7 km / 44.5 min**; all four optimistic give 34.6 km / 82.5 min. **Adding the CE-02 live link (+0.4 W) puts the best estimate at 25.7 km.**
- **Static margin vs aft-mass growth:** +4 g of unplanned mass near the tail takes SM to 5.07%. Weigh the motor, prop and adapter first on arrival.

**Safe to defer (no flip anywhere in the band):** flap knockdown (P-05), fin endplate (P-06), motor constants for launch thrust (P-09). Fin sidewash (P-07) sits exactly at the limit at its low end, so it is confirmed in flight.

**Bench priority order (Oct 26–27), from the sweep:**
1. η: P-01, P-09
2. hotel power including the link: P-02
3. usable energy: P-03
4. weights of the aft items: P-08 / P-12, done at receipt

Misc. drag (P-04) needs flight. The CE-02 live estimator is what retires it.

## 3. Recommendation for external figures

Quote range and endurance as **"about 25–29 km / 60–70 min at 7 m/s (modelled; bench-confirmed Oct 27)"** rather than 26–29 km. That keeps the low end honest once the live-link power is included. CEO decision.
