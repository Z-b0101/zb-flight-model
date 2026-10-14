# Z!B structural and aeroelastic analysis (SA-01)

| | |
|---|---|
| Owner | Claude (acting GM/DE) |
| Independent check | MBSE (Oubi): requested, see section 9 |
| Design | `cad/params.json` hash `7be168427b4d`; planning mass 211.9 g |
| Status | **Modelled, not measured.** Every material value is assumed until the coupon test (Oct 21–22). Gate 4 item, due Fri Oct 16 |
| Tools | `structures/` (beam FE, hatch plane-stress FE, aeroelastics, checks); `tests/test_structures.py` |
| Date | 2026-10-14 |

## 1. Bottom line

1. **The wing is strong enough in bending with a properly specified spar.** A hard landing loads the spar more than any flight case. A 1.5 m/s sink landing gives a root moment of 0.94 N·m. The worst flight case, a 7.6 m/s gust at 12 m/s, gives 0.76 N·m. With the nominal tube, and taking no credit for the skins, the reserve factor on landing is **1.82**. The required minimum is 1.0, and it is measured on top of a 1.5 safety factor.
2. **The cheap tube must not be used.** A tube at the bottom of the published range (30 GPa, 250 MPa) **fails** the gust case (RF 0.94). It only scrapes through the 1.5 m/s landing (RF 1.02). So the spar must be bought to a specification, and the coupon must confirm it (R1).
3. **The weak links are the foam, not the carbon.**
   - The top skin buckles before a 4 g ultimate load (RF 0.94 at 4 g, 0.59 in the gust).
   - The bottom skin buckles in a 1.5 m/s landing (RF 0.47).
   - As drawn, the wing has no closed torsion box. The skins stop at the hinge line, which makes the section open and about 12 times softer in torsion. In that state the twin's static aeroelastics cannot be trusted, and a simple typical-section check puts divergence near cruise speed.
4. **About 3 g of Depron fixes the foam weak links.**
   - A web along the hinge line closes the torsion box (R2). Flutter is then about 43–45 m/s, against a 25 m/s dive speed.
   - A second web at mid-chord halves the width of the skin panels (R3). Buckling RF rises to 1.9 (landing) and 2.4 (gust).
5. **Control reversal sets the speed limit.** Even with the web, the elevons lose half their roll authority by 15 m/s and reverse at about 21 m/s. The torsion box is soft foam and the elevons sit behind the spar. This is below the 25 m/s dive case. Cruise (7–12 m/s) is unaffected. The autopilot gets an airspeed ceiling of 16 m/s (R7). Stiffening the skin alone buys little (+3 m/s for 2.5 times the GJ); bending stiffness matters as much. Classical flutter is not a risk: the screen gives about 45 m/s.
6. **Most of the integration value is in the centre bay.**
   - A single printed centre section can combine the spar V-joiner, battery tray, hatch frame, FC mount and motor mount (R5).
   - A hatch lid that bears on its frame keeps the bottom skin's load path in compression (R4).
7. **Found on the way: a sign error in the twin, now fixed.** The VLM modelled the 6° washout as wash-in. NP, SM and range did not move. Trim and spanload did. The corrected spanload unloads the tips, which lowers flight bending moments by 7–16%. All numbers below use the corrected twin (`twin/v0.1 @532559c`).

## 2. What was analysed

| Item | Method | File |
|---|---|---|
| Spanload, trim | Twin VLM (40×10 per side), trimmed for lift and pitch | `twin/vlm.py`, `structures/model.py` |
| Wing primary structure | 3-D frame FE along the swept spar axis (30 elements, clamped root): bending both ways, torsion, axial. Aero and inertia loads applied with their offsets | `structures/model.py` |
| Section properties | Pultruded tube plus Depron skin, LE to hinge (75% chord). Modulus-weighted. Torsion: Bredt for a closed box, open-section for the drawn skin | `model.section` |
| Load cases | C1 1 g at 10.5 m/s; C2 2.5 g at 12; C3 4 g at 15; C4 FAR 23.341 gust 7.6 m/s at 12 m/s (n = 6.15, stall-capped); C5 1 g at 25 m/s (dive) | `structures/analysis.py` |
| Hatch cut-out | Plane-stress CST FE of the bottom skin around the 34×72 mm aperture, with and without a printed frame | `structures/hatch_fe.py` |
| Static aeroelastics | FE twist fed back into the VLM, re-trimmed each pass; roll effectiveness (antisymmetric) | `structures/aeroelastic.py` |
| Flutter / divergence screen | Theodorsen typical section, k-method, at 75% semispan, using FE uncoupled bending and torsion frequencies; swept by 1/cos Λ | `structures/aeroelastic.py` |
| Landing | Centre body stops in the crush stroke; wing response by modal superposition (6 modes, impulse limit, SRSS) | `structures/checks.py` |
| Launch, motor mount, joiner, bonds, skin buckling, cap option | Closed-form checks on FE loads | `structures/checks.py` |

**Margins convention.** Loads are limit loads. The ultimate factor is **1.5** (proposed, for MBSE to ratify). Reserve factor RF = allowable / (1.5 × limit stress). **RF ≥ 1 passes.**

## 3. Verification of the tools

| Test | Result |
|---|---|
| Tip load on cantilever, 0° and 25° sweep | Tip deflection and root moment exact (to 1e-9) |
| Tip torque | Twist = TL/GJ exact |
| Uniform load, 40 elements | Tip deflection within 0.2% of wL⁴/8EI |
| Hatch FE: small circular hole | Kt 3.07–3.10 against Peterson 3.05; the drawn hatch converges (3.41 / 3.48 / 3.46 as the mesh refines) |
| Flutter solver, Hodges & Pierce typical section | U_F/(bω_α) = 2.18 against the textbook 2.17 |
| VLM washout sign | Washout must lower CL and raise Cm0 (new test: this is the bug found today) |

These are pinned in `tests/test_structures.py`; all pass.

## 4. Results: flight load cases (nominal tube, with the hinge-line web)

| Case | n | Root M (N·m) | Root T (N·m) | Spar alone, limit (MPa) | Top skin (kPa) | Tip deflection (mm) | Tip twist (°, + nose-up) |
|---|---|---|---|---|---|---|---|
| C1 cruise | 1.0 | 0.098 | 0.015 | 23 | 7 | 2.5 | +0.02 |
| C2 pull-up | 2.5 | 0.293 | 0.041 | 68 | 21 | 8.6 | −0.01 |
| C3 manoeuvre | 4.0 | 0.479 | 0.059 | 112 | 34 | 14.3 | −0.15 |
| C4 gust | 6.15 | 0.759 | 0.124 | 177 | 54 | 23.5 | +0.19 |
| C5 dive | 1.0 | 0.010 | 0.071 | 2 | 1 | −2.0 | −1.06 |

Inertia relief is real. The wing carries 73 g of its own mass, and that cuts the root moment by about a third compared with a lift-only hand calculation.

**Spar alone (design basis: skins assumed buckled), RF at ultimate:**

| Tube grade | Allowable | C3 4 g | C4 gust | Landing 1.5 m/s | Landing 2.5 m/s (abuse) |
|---|---|---|---|---|---|
| Low (30 GPa, 250 MPa) | 250 MPa | 1.49 | **0.94** | **1.02** | **0.61** |
| Nominal (120 GPa, 600 MPa) | 600 MPa | 3.58 | 2.26 | **1.82** | 1.09 |
| Premium (131 GPa, 1.83 GPa flexural; 1.0 GPa used) | 1.0 GPa | 5.97 | 3.77 | 2.96 | 1.77 |

## 5. Results: the foam

**Skin buckling.** The top skin panel between the spar (30%) and the hinge (75%) is 90 mm wide and nearly flat (radius 589 mm), so curvature adds nothing. The flat-plate buckling stress is 48 kPa.

| Case | Skin stress (kPa) | Buckling RF as drawn | With mid-chord web (R3) | Crush RF (0.17 MPa) |
|---|---|---|---|---|
| C3 4 g, top | 34 | **0.94** | 3.75 | 3.31 |
| C4 gust, top | 54 | **0.59** | 2.37 | 2.09 |
| Landing 1.5 m/s, bottom | 68 | **0.47** | 1.88 | 1.66 |

**Torsion box.**
- As drawn, the skins stop at the hinge and the section is open, with GJ = 0.08 N·m². Almost all of it is the spar tube.
- Closing the box with a 3 mm Depron web at the hinge line gives GJ = 1.02 N·m², 12 times stiffer.
- The open section's linear twist predictions run to +19° in the gust. That is not credible, because the model ignores warping restraint by the ribs. What it does show is that the open wing is soft enough that its static aeroelastics cannot be bounded.

**Hatch cut-out (bottom skin, root bay).**

| Configuration | Kt (foam) | Gust tension RF (0.40 MPa) | Landing compression RF (crush 0.17 MPa) |
|---|---|---|---|
| As drawn, r = 4 mm | 3.46 | 1.40 | **0.48** |
| r = 8 mm + PLA frame 6 × 1.2 mm | 2.10 | 2.31 | **0.79** (passes at limit: 143 < 170 kPa) |
| + lid bearing on the frame spanwise (R4) | → about 1 in compression | 2.31 | ≥ 1.1 (to confirm by the bench compression test) |

The PLA frame stress is about 20 × the far-field skin stress × 3/1.2. That is a few MPa, against 45 MPa in-layer, so the frame itself is fine.

## 6. Results: aeroelastics (corrected twin)

**Static coupled trim** (the FE twist is fed back into the VLM, then lift and pitch are re-trimmed):

| Configuration | 1 g, 10.5 m/s | 4 g, 15 m/s | 1 g, 25 m/s |
|---|---|---|---|
| Nominal tube, with web | tip +0.08°, elevon 1.10 → 1.07°, converged in 3 passes | tip +0.56°, converged | tip −0.57°, elevon 2.19 → 2.37°, converged |
| Low tube, with web | tip −0.03° | tip −0.02° | tip −0.27° |
| Nominal tube, **no web (as drawn)** | tip +4.8°, trim moves by 2° of alpha | **does not converge** (tip +46°) | **does not converge** |
| Low tube, **no web** | tip +7.6° | **diverges** | **diverges** |

With the web, aeroelastic twist is small: the trim, drag and range numbers stand. Without it they do not.

**Elevon roll effectiveness** (flexible roll moment ÷ rigid; antisymmetric twist, coupled):

| Configuration | 10 m/s | 15 m/s | 20 m/s | 25 m/s | Reversal speed |
|---|---|---|---|---|---|
| Nominal tube, with web | 0.75 | 0.48 | 0.08 | **−0.43** | **≈ 20.8 m/s** |
| Low tube, with web | 0.62 | 0.23 | −0.37 | −1.14 | ≈ 17 m/s |
| Nominal tube, no web | −0.48 | −2.0 | −4.4 | −7.5 | **reversed at all speeds** |

Sensitivity (nominal tube, with web). Making the skin 2.5 times stiffer in shear (GJ 1.02 → 2.44 N·m²) only moves reversal from about 20.8 to about 24.2 m/s (effectiveness 0.61 / 0.31 / −0.08 at 15 / 20 / 25 m/s). So torsion is only half the story. The other half is **bending–torsion coupling through the 25° sweep**: when the spar bends up, the streamwise sections wash out. That is why the low-grade tube reverses earlier (17 m/s) than the nominal one (21 m/s). `structures/reversal_gj.json`

**This is the most important aeroelastic finding.** The elevons sit at 75% chord, behind the spar (30%), so deflecting them twists the soft foam box against themselves. The sweep then adds bending washout. Even with the web, roll authority halves by 15 m/s and **reverses at about 21 m/s**, below the 25 m/s dive case.

The result depends on the assumed Depron shear modulus (5 MPa; the published band is 3–8) and on the spar's bending stiffness. Two things follow:
- an airspeed limit in the autopilot (R7);
- a torsion-stiffness test on the built wing (section 9).

**Flutter and divergence screen** (Theodorsen typical section at 75% semispan, uncoupled FE frequencies):

| Configuration | 1st bending | 1st torsion | Flutter (swept) | Typical-section divergence (unswept, conservative) |
|---|---|---|---|---|
| Nominal tube, with web | 11.0 Hz | 32.2 Hz | **44.6 m/s** (1.8 × the 25 m/s dive) | 33 m/s |
| Low tube, with web | 8.1 Hz | 31.9 Hz | 42.8 m/s | 33 m/s |
| Nominal tube, no web | 11.0 Hz | 9.1 Hz | no classical flutter found | **9.4 m/s** (below cruise) |

The mass ratio is very low (μ = 1.9), and with the web the frequencies are well separated (σ = 0.34). Classical flutter is not the risk; control reversal is.

## 7. Results: other checks

| Check | Load (limit) | Result |
|---|---|---|
| Landing, centre body | 1.5 m/s sink, 3 mm crush stroke (assumed): 38 g pulse, 4 ms | Battery pushes 23 N into the hatch, in compression against the ground |
| Hatch retention | Inverted or cartwheel impact, 10 g (assumed): 6.1 N outward | **Requirement: pull-off ≥ 9.1 N** (VC-31). Two 6×3 mm N52 magnets or a latch; pull-test on the bench |
| Hand launch | 9 m/s over 0.7 m: 5.9 g aft | Battery 3.6 N aft into the tray stop. Grip 20 N over two thumb pads: 44 kPa, crush RF 2.55 |
| Motor mount (pusher) | Thrust ≤ 6 N (R-07 placeholder), torque 0.08 N·m, landing 9.4 N | Needs ≥ 70 mm² of bond if on foam only (peel needs about 4× that). **Tie it into the printed centre section** (needs only 5 mm² of PLA bond) |
| Spar V-joiner (root) | M 0.76 + T 0.12 → 0.77 N·m limit, 1.15 N·m ultimate | 12 × 12 mm PLA block, two 40 mm sockets: block 4.0 MPa (RF 11 in-layer, **3.7 even interlayer**); socket bearing 1.1 MPa. The joiner sees the gust moment; the landing moment (0.94) still leaves RF 3.0 interlayer |
| Spar–rib bond (torque through 4.2 mm slot, 3 mm rib) | Open section: the spar carries 85% of torque | 0.70 MPa, RF 2.9 on 3 MPa CA. **With the web: 0.06 MPa, RF 36** |
| Rib–skin bond (peel under suction) | Peak suction about 3× mean at gust: 213 Pa | 24 N/m per rib line, 8 kPa peel on a 3 mm land: RF 33 |
| Carbon cap strips (3 × 0.5 mm, option) | Gust and landing | Not recommended (see R-option below) |

## 8. Recommended design changes (ranked), with integration notes

| # | Change | Mass | Cost | What it buys | Integration |
|---|---|---|---|---|---|
| **R1** | **Buy the spar to a specification**: 4.0 mm OD pultruded tube from a vendor publishing flexural modulus ≥ 100 GPa and strength ≥ 1 GPa. Coupon 3-point bend before Gate 4; reject if E < 80 GPa or strength < 600 MPa | 0 | about the same as cart line 7 | Removes the only flight-case FAIL (low grade, gust RF 0.94) | Cart line 7 gets a spec; coupon card gets a bend test (fixture in the MfgE pack) |
| **R2** | **Hinge-line web**: 3 mm Depron, full span, bonded between top and bottom skin at 75% chord | ~0.8 g + glue | ~0 | Closes the torsion box: GJ ×12; flutter about 45 m/s vs 25 m/s dive; spar–rib bond RF 2.9 → 36; makes the twin's aeroelastics valid | **It is also the elevon hinge line and the servo-horn reaction point**: hinge tape goes on a solid edge, not on loose skin edges |
| **R3** | **Mid-chord web** at 52.5% chord, 3 mm Depron, at least over the inboard 60% | ~1.5 g full span | ~0 | Skin buckling RF to ≥ 1.9 everywhere, so crush now governs. Second torsion cell | Servo bay sits between the webs; servo lead passes through one 6 mm hole (low-stressed) |
| **R4** | **Hatch**: 8 mm corner radius; a 6 × 1.2 mm PLA frame printed **as one part with the battery tray**; a PLA lid that bears spanwise on the frame; retention ≥ 9.1 N | ~+1.5 g net (frame + tray replace foam) | filament | Kt 3.46 → 2.1 (→ about 1 in compression with lid contact); landing RF 0.48 → ≥ 1 | The tray gives the battery a launch stop (3.6 N) and a positive CG location (the CG is the program's tightest number) |
| **R5** | **Integrated printed centre section** (root bay, ±56 mm): V-joiner (12 × 12 mm, 40 mm sockets, printed with the tube axes in the layer plane) + tray/frame (R4) + FC mount + **motor mount tied into it** | replaces the planned ~2 g sleeve; net ~+1–2 g | filament | One part carries every hard-point load: joiner RF ≥ 3.7, motor mount on PLA not foam, launch grip on PLA | One print instead of four parts and four bonds; fixes the CG stack-up; one more CAD part for the MfgE pack (M2) |
| R6 | **Washout 6° → 3–4°** (MBSE decision, CE item) | 0 | 0 | Corrected twin: range 26.6 → 27.0 km, cruise trim near 0°, better span efficiency; eases R-01 (6° is at the Depron limit) | Stall behaviour is not in the VLM: needs MBSE judgement and the flight test card |
| **R7** | **Airspeed ceiling 16 m/s in the autopilot** (ArduPlane `AIRSPEED_MAX` / FBWA and TECS limits); maiden-flight card says the same; dive case C5 removed from the envelope | 0 | 0 | Keeps roll effectiveness ≥ 0.4 (reversal ≈ 21 m/s nominal, 17 m/s low-grade tube) | One parameter; a flight-test card line; VC-29 control authority evaluated inside the limit |
| — | Carbon cap strips (option, **not recommended**) | +2.9 g inboard | ~$10 | Skin stress ÷5 | Stiffer wing attracts twice the landing moment (2.0 N·m), loads the joiner; caps need a spar-line web to stay stable, and even then landing RF is ~1.0 on cap buckling. Hold as a fallback only if the Depron coupon comes in weak |

**Mass:** R1–R5 add about +4 to +5 g. The margin is 38 g today. R-07 (motor) may take 5–15 g. That leaves about 18 g or more.

## 9. Assumed versus measured inputs (what the coupon and bench must close)

| Input | Assumed | Basis | Closed by |
|---|---|---|---|
| Spar E, strength, ID | 120 GPa, 600 MPa, ID 3 mm | Program assumption; TDS spread 30–131 GPa | Coupon: 3-point bend + caliper (add to the card) |
| Depron E, crush, tension, shear | 12 MPa, 0.17, 0.40, 0.20 MPa | XPS data-sheet minimums | Coupon: strip tension + flat compression (add) |
| PLA in-layer and interlayer | 45 / 15 MPa | Typical FDM | Joiner sample, printed as the real part, bend to failure (already on the card) |
| CA bond carbon–PLA | 3 MPa | Conservative | Joiner sample (same test) |
| Landing sink and stroke | 1.5 m/s, 3 mm | Typical belly landing on grass | First flights: video of touchdown; inspect for skin creases at the hatch |
| Gust | 7.6 m/s (FAR 23.341) | Regulation basis; stall-capped | — |
| Wing GJ and EI (built wing) | GJ 1.02 N·m², EI 1.69 N·m² | Section model | **Bench: tip-torque and tip-load test on the built wing** (lever + known weight + phone inclinometer; 15 min). Sets the reversal speed and the R7 limit |
| Ultimate factor | 1.5 | Proposed | MBSE to ratify |

## 10. Requests to MBSE (Oubi)

1. Ratify the 1.5 ultimate factor and the RF convention.
2. Add a `structure` block to `params.json`: tube grade and spec, web positions (R2, R3), hatch radius and frame, centre-section part. This keeps the twin and CAD on one source (RQ-09).
3. An independent check of one number. The suggested check: the gust root moment, 0.76 N·m, by your own strip theory.
4. Decide R6 (washout).
5. Add the coupon-card items in section 9 (spar bend, Depron strip and compression, hatch-lid compression and pull-off).
6. Agree the 16 m/s airspeed ceiling (R7) as an envelope requirement, and add the built-wing GJ/EI test to the bench card.

## 11. Limits of this analysis

- **Linear throughout.** There is no post-buckling, no material non-linearity and no large deflection.
- **Open-section results are qualitative.** Without the web, the twist numbers are not credible (no warping restraint).
- **Flutter is a typical-section screen** at one station, with assumed section CG (40% chord) and radius of gyration. It is a screen, not a flutter clearance. The ground vibration test of the built wing is the check: tap test with a phone accelerometer for the bending and torsion frequencies, for 15 minutes on the bench.
- **The landing is impulse-limit, SRSS:** conservative against a measured pulse.
- **Every material number is assumed** until the coupon (Oct 21–22).
