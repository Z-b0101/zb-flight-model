# Airfoil Trade Study — Sub-250g Flying-Wing PoC

**Date:** 2026-10-13 · **Status:** complete, recommendation issued
**Baseline it feeds:** 0.90 m span / 0.20 m chord / AR 4.5 / 20° sweep / 2° washout / 204 g AUW / 3S 650 mAh (5.77 Wh)

---

## 1. Selection criteria (the physics first)

**Why a flying wing needs reflex or sweep+washout.** A stable aircraft needs the CG ahead of the neutral point *and* zero net pitching moment at cruise CL. A conventional layout gets its nose-up trim moment from the tail's download. A tailless wing must generate that moment with the wing itself. Two paths:

1. **Reflexed airfoil (positive Cm0)** — trailing edge kicks up; aft loading gives a nose-up zero-lift moment. The plank solution (unswept).
2. **Sweep + washout** — on an aft-swept wing the tips sit behind the CG. Washing the tips out (lower incidence) downloads them; aft download = nose-up moment. Lifting-line estimate for our planform: **≈ +0.0075 of wing Cm0 per degree of washout** (2° washout ≈ +0.015).

**The three-way trim trade.** Required moment at the wing AC for trim: `Cm_ac = CL × SM` (with SM = static margin as a fraction). At CL 0.5 / 8 % SM that's +0.040, supplied by the sum of airfoil Cm + washout effect + elevon deflection. A "better L/D" airfoil with strongly negative Cm0 can lose *net* to a draggier airfoil that trims clean — up-elevon costs trim drag (≈ 1.3e-4 × δ² in wing CD for our 25 %-chord, ~65 %-span elevons, stated assumption) and eats pitch authority. There is no free lunch; this trade is the heart of the study.

**Re ≈ 90k reality.** At our Reynolds number the boundary layer forms laminar separation bubbles — XFoil (Ncrit 9, clean environment) is typically 10–20 % optimistic on drag and stall vs. a real foam/printed wing. Treat all polars below as *comparative*, not absolute. Absolute numbers get verified in flight test (Gate 2).

**What makes a good section for *this* aircraft:** (a) low Cd in *our* CL band (0.37–0.5, not the brochure max-L/D point); (b) gentle stall; (c) Cm compatible with 20° sweep + 2° washout trim budget; (d) ≥ 9 % thickness for the spar.

---

## 2. Candidate data (Re ≈ 100k)

| | **MH60** | **S3021** | **HS130** | **E387** | **PW75** (incumbent) |
|---|---|---|---|---|---|
| Provenance | XFoil Ncrit 9, airfoiltools, full table extracted | XFoil Ncrit 5, airfoiltools, full table extracted ⚠️ | Published Cm0 (Nurflügel airfoil DB, Scribd) | UIUC wind-tunnel literature + XFoil Re 500k snippet | Designer notes only — **no polar found anywhere** |
| Cd @ CL 0.4 / 0.5 / 0.6 / 0.7 | .0155 / .0155 / .0157 / .0163 | .0126 / .0131 / .0137 / .0144 | — (no data) | — (no Re-100k polar retrieved) | — |
| Cm @ CL≈0.5 (Cm0) | −0.022 (−0.037 @ CL 0) | −0.062 (−0.061 @ CL 0) | +0.0157 (Cm0) | ≈ −0.080 | ? (reflexed ⇒ positive, per designer) |
| Clmax | 1.16 | 1.16 | ? | ≈ 1.0 | ? |
| Stall character | Gentle trailing-edge (CL falls 1.16→1.06 gradually) | Very gentle (1.16→1.01 over 6°) | ? | Gentle (documented) | ? |
| (CL/CD)max | 45 @ α 6.5° | 55 @ α 6.25° | ? | ~50–55 (lit.) | ? |
| Thickness | 10.1 % ✓ | 9.5 % ✓ | ~8–9 % ✓ | 9.1 % ✓ | ? |

⚠️ S3021's polar is Ncrit 5 (rougher environment) vs MH60's Ncrit 9 — slightly pessimistic for S3021; does not affect the verdict (Section 4).

**PW75 research note:** genuine search (RC forums, airfoil databases, designer references) turned up only that it is "a modified PW51 with more reflex, giving a higher pitching moment" — a reflexed plank section by designer intent (Peter Wick). No coordinates, no polar, no test data. This *is* risk R-16, confirmed unresolvable by research.

**HS130 research note:** Hartmut Siegmann section, "very popular in Germany for very fast planks… less drag and very fast… optimized for use of elevons (25 % chord)". Minimum chord 150 mm (we are 200 mm ✓). It is a *speed* section — designed for low CL (fast flight), the opposite corner from our 7 m/s efficient-cruise mission. No Re-100k polar found.

---

## 3. Mission model results

Model: `CD = Cd_airfoil(CL) + 0.012 + CL²/(π·4.5·0.78)`; W = 2.00 N; `V = √(2W/ρSCL)`; `P_shaft = ½ρV³S·CD`; `η = min(0.55, 0.20+0.0875·P_shaft)`; endurance = 5.77/P_elec h; range = endurance·V·3.6. Constraints: V ≥ max(1.5·Vstall, 7.0), Re ≥ 80k. CL optimized per airfoil.

| Airfoil | CL* | V* (m/s) | P_elec (W) | Endurance | Range | L/D |
|---|---|---|---|---|---|---|
| MH60 (aero only) | 0.370 | 7.00 | 4.54 | 76 min | **32.0 km** | 9.3 |
| MH60 **with trim drag** (−6° elevon, ΔCD 0.0045) | 0.370 | 7.00 | 4.84 | 72 min | **30.0 km** | 8.3 |
| MH60, 3° washout refinement (ΔCD 0.0018) | 0.370 | 7.00 | 4.67 | 74 min | **31.2 km** | 8.9 |
| S3021 (aero only — trim-excluded, see §4) | 0.370 | 7.00 | 4.34 | 80 min | 33.5 km | 10.0 |

Notes:
- The V ≥ 7.0 m/s floor is essentially non-binding: unconstrained optimum sits at CL 0.40 / V 6.7 m/s with identical range (prop-efficiency derate at low power flattens the curve). The 7 m/s cruise costs nothing.
- Vstall ≈ 3.95 m/s for both (Clmax 1.16) → 1.5 × Vstall = 5.9 < 7.0, so the 7.0 m/s floor governs.
- **MH60 with real polar + trim drag lands at 30.0 km / 72 min — within 3 % of the Gate 1 claim (30.8 km / 73 min), which was built on assumed aero. The baseline performance survives contact with real data.**

---

## 4. Trim assessment (20° sweep + 2° washout, CL 0.5, 8 % SM)

Required: Cm_ac = +0.040. Washout credit: +0.015. Elevon effectiveness assumed −0.008/° (25 % chord, ~65 % span; ±2° sensitivity).

| Airfoil | Wing Cm0 | Elevon for trim | Trim-drag ΔCD | Verdict |
|---|---|---|---|---|
| MH60 | −0.007 | **−5.9°** (up) | 0.0045 | ✅ Acceptable — normal flying-wing practice |
| HS130 | +0.031 | **−1.2°** (up) | ~0.0002 | ✅✅ Trims essentially faired — but aero unverified |
| PW75 | ? (≈ +0.02…+0.04 if designer intent holds) | ≈ 0…+2° (assumed) | ? | ❓ Unverifiable |
| S3021 | −0.046 | **−10.9°** | 0.0150 | ❌ Excluded — deflection likely separates elevon flow; eats all pitch authority |
| E387 | −0.065 | **−13.1°** | 0.0246 | ❌ Excluded — needs a different planform, not this one |

The instructive near-miss: S3021 has the best profile L/D of the field (15 % less drag than MH60 in the cruise band) and the gentlest stall — and it still loses, because −11° of trim elevon costs more drag than its airfoil advantage and leaves no control margin. **For a tailless aircraft, trim compatibility dominates profile drag.** E387 fails the same way, harder.

**Free refinement:** 3° washout (built into the rib stack at zero cost/weight) + 5–6 % SM → MH60 trims at −3…−4° elevon, recovering to 31.2 km / 74 min. Recommend adopting at Gate 2 geometry freeze.

---

## 5. Ranked summary & recommendation

| Rank | Airfoil | Range / endurance (trim-included) | Why here |
|---|---|---|---|
| **1** | **MH60** | **30.0 km / 72 min** (31.2 / 74 with 3° washout) | Only candidate with verified Re-100k polar + documented gentle stall that trims on our planform |
| 2 | HS130 | n/a (no polar) | Perfect trim (−1°) but unverifiable aero and a speed-section mission mismatch |
| 3 | PW75 | n/a (no data) | Incumbent; literally cannot be evaluated — R-16 |
| — | S3021 | 33.5 / 80 aero-only, trim-excluded | Best L/D in field, disqualified on trim (−11° elevon) |
| — | E387 | trim-excluded | Superb low-Re section, wrong planform (−13° elevon) |

### Recommendation: switch PW75 → MH60

1. **Verifiability.** MH60 is the only candidate with a real Re≈100k polar and documented stall behavior. PW75 has no obtainable data — the "margin over PW75 in km" is uncomputable, and that *is* the finding (R-16).
2. **Trim works.** −6° elevon at baseline geometry; −3…−4° with the zero-cost 3°-washout refinement. Sane, flyable, quantified.
3. **Baseline confirmed.** 30.0 km / 72 min with real data vs 30.8 / 73 assumed at Gate 1 — the performance claim stands.
4. **Purpose-designed.** Hepperle's MH series is designed for tailless aircraft; 10.1 % thickness fits the 4 mm spar; gentle trailing-edge stall suits a first-flight-stable PoC.
5. **Resolves R-16 by replacement**, not by hoping the data turns up.

---

## 6. Caveats & Gate 2 verification musts

- **XFoil optimism:** real wing Cd likely 10–20 % above these polars (surface roughness, rib steps, laminar bubbles); Clmax likely lower. All rankings are comparative. Absolute performance gets set by flight test.
- **Ncrit mismatch:** S3021 polar is Ncrit 5 vs MH60's Ncrit 9 — comparison slightly understates S3021; verdict unaffected (trim excludes it regardless).
- **Trim math is approximate:** washout ΔCm (+0.0075/°) is a lifting-line estimate; elevon effectiveness (−0.008/°) is thin-airfoil-based. Flight test calibrates both; carry ±2° elevon uncertainty into control sizing.
- **Stall character must be verified in flight:** XFoil says gentle, but tip-stall behavior with washout on *our* construction is a flight-test item (high-α handling checks in the Gate 2 test plan).
- **PW75/HS130 data scarcity stands:** if a future family instance wants the plank philosophy (unswept), HS130 deserves its own polar effort — out of scope for this PoC.
- **E387/S3021 are not "bad"** — they are excellent sections for tailed or higher-sweep tailless planforms. They are wrong *for this planform*.

*Model script: `/tmp/airfoil_model.py`, `/tmp/sens.py` (re-runnable). Polar sources: airfoiltools.com (xf-mh60-il-100000, xf-s3021-il-100000-n5); Nurflügel airfoil database (HS130 Cm0 +0.0157); UIUC LSATs literature (E387).*
