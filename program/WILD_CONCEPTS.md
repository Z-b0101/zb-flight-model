# Wild Concepts — Side Quest Survey

Exploratory survey of unconventional configurations for the sub-250g platform family. Not on the critical path; nothing here gates the PoC.

**Non-negotiable constraints applied to every concept:** sub-250g AUW; buildable in 3mm Depron + carbon spar + vase-mode printed ribs; cheap to crash; simplicity = reliability; efficient quiet cruise/loiter (~30km class); tailless preferred.

**The honesty filter up front:** our cruise flies at Cl≈0.5, Re≈90k, where profile drag and propulsion losses dominate the energy budget. Any concept whose payoff lives in *induced* drag buys less than it appears to. Concepts are judged on net mission effect, not brochure claims.

---

## Concept cards

### 1. Prandtl-D bell-spanload twisted wing
- **What:** Aggressive spanwise twist producing a bell-shaped lift distribution (Prandtl 1933). NASA Armstrong flew subscale demonstrators (Prandtl-D No. 1–3, 2013–2015+) and recorded proverse yaw — the wingtip force vector tilts forward in upwash, so roll control yaws *into* the turn, no vertical tail needed. US Patent 9,382,000.
- **Promise:** Delete the vertical tail/winglets entirely (weight + drag saving); modest induced-drag improvement; yaw stability without surfaces.
- **Cost:** Twist must be built accurately — but our printed ribs make twist nearly free (rotate rib profiles along the span at print time). Slightly higher induced drag than elliptical loading; needs validation that proverse yaw actually materializes at our Re/scale.
- **Verdict:** The wildest *credible* concept on this list. Subtraction, not addition — it removes parts. Directly serves the mission.
- Sources: [Aerotech News on Prandtl-D flights](https://www.aerotechnews.com/blog/2016/04/01/flying-wing-shaped-experimental-airplane-validating-new-wing-design-method/), [MDPI modeling paper](https://www.mdpi.com/2226-4310/10/7/613/xml), [NASA TOPS brief (PDF)](https://ntts-prod.s3.amazonaws.com/t2p/prod/t2media/tops/pdf/DRC-TOPS-36.pdf)

### 2. Ogival/ogee planform (Concorde-style)
- **What:** Ogee leading-edge curve; sharp LE generates a stable leading-edge vortex at high AoA → vortex lift + essentially stall-proof behavior.
- **Promise:** Stall safety as a design feature; the coolest-looking option by a wide margin. Low-Re research (swift-wing delta studies, low-sweep delta stall-mode work) confirms LEV systems do form and persist at Re ~10⁴–10⁵ — the physics is real at our scale.
- **Cost:** Vortex lift only exists at high AoA (10°+); at our 4–6° cruise AoA the ogee is just a low-effective-AR delta — *worse* cruise L/D than our AR 4.5 rectangular wing. More wetted area. Buildable (ribs follow any planform; skins stay flat), but the mission pays a cruise penalty for a party trick.
- **Verdict:** Viable and buildable, marginal mission benefit. Best framed as a stall-proof "sport" family member, not the endurance PoC.
- Sources: [low-sweep delta aerodynamics (PDF)](https://www.kimerius.com/app/download/5784132992/The+aerodynamics+of+low+sweep+delta+wings.pdf), [swift-wing LEV study](https://www.researchgate.net/publication/319281137_The_leading-edge_vortex_of_swift_wing-shaped_delta_wings), [low-Re wing segmentation study](https://www.mdpi.com/2226-4310/11/4/320/htm)

### 3. Tandem wing
- **What:** Two wings in line (Rutan Quickie/VariEze lineage; Mignet Flying Flea before it). Both surfaces produce positive lift — no tail download penalty. Compact span for a given area.
- **Promise:** Packaging: a real fuselage/payload bay between two lifting surfaces — the most natural answer to the family's future sensor-payload problem. Structurally efficient (fuselage supported at two points; each wing smaller). Positive lift everywhere.
- **Cost:** Interference — the rear wing flies in the front wing's downwash, needs careful decalage; CG sits between the wings and trim is touchier (the Quickie was famously sensitive to small airfoil changes). Roughly 5–10% interference drag penalty vs a clean monoplane. Two wings = more parts, more joints.
- **Verdict:** Genuinely viable, justified by *packaging* rather than efficiency. A strong candidate for a sensor-carrying family member. A METU thesis studied exactly this for tube-launched micro-UAVs.
- Sources: [Tandem wing (Wikipedia)](https://en.wikipedia.org/wiki/Tandem_wing), [Rutan Quickie (Wikipedia)](https://en.wikipedia.org/wiki/Rutan_Quickie), [tandem-wing micro-UAV thesis (PDF)](http://etd.lib.metu.edu.tr/upload/12623631/index.pdf)

### 4. Box wing / joined wing
- **What:** Two wings joined at the tips by vertical surfaces — Prandtl's "best wing system" for induced drag (1920s). An MIT-led study (arXiv 2112.02872) specifically compared box vs mono wings for *small UAVs* and found box wings win where induced drag dominates (high lift demand, low AR).
- **Promise:** Real induced-drag reduction; closed-loop structure is stiff; good gust tolerance and stall behavior.
- **Cost:** The vertical tip joiners are the whole problem at our scale: weight, wetted area, and joints that must be built precisely in foam. Our cruise is not induced-drag-dominated, so the payoff is thin while the joint complexity directly violates "simplicity = reliability." A 3D-printable Prandtl box-wing UAV has been designed (academia.edu) — as a research object, not a product.
- **Verdict:** Interesting physics, net-negative at our scale and mission. The joints kill it. Say no.
- Sources: [box vs mono wing for small UAVs (arXiv)](https://arxiv.org/pdf/2112.02872), [3D-printable Prandtl box-wing UAV](https://www.academia.edu/42893082/Towards_Design_of_a_3D_Printable_Prandtl_Box_Wing_Unmanned_Aerial_Vehicle), [UPM experimental investigation (PDF)](https://oa.upm.es/19299/1/INVE_MEM_2011_122192.pdf)

### 5. Annular / ring wing
- **What:** Closed circular wing — Lee-Richards (1913), Nemeth Umbrellaplane (1934, genuinely stall-proof STOL), SNECMA Coléoptère, FlyNano (2012), Belarusian OW-1 (2007, only crewed annular to sustain stable horizontal flight). A YouTuber recently flew a giant RC ring wing and found remarkable stability.
- **Promise:** No wingtips → no tip vortices in the conventional sense; famously docile stall (the Nemeth machine descended "almost vertically" under control); insanely stable.
- **Cost:** Effective aspect ratio is atrocious; wetted area is enormous (both faces of the ring); a structural ring in Depron is heavy and hard to make stiff. Endurance mission + ring wing = drag disaster. Everything it promises (stability, STOL) is irrelevant to a 30km cruise mission.
- **Verdict:** Cool but stupid for our mission. Said plainly, as instructed.
- Sources: [Closed wing (Wikipedia)](https://en.wikipedia.org/wiki/Closed_wing), [Lee-Richards annular monoplane](https://en.wikipedia.org/wiki/Lee-Richards_annular_monoplane), [ProjectAir giant ring wing](https://interestingengineering.com/innovation/uk-youtuber-giant-plane-ring-shaped-wings)

### 6. Blended wing body (BWB)
- **What:** Wing and body merged into one lifting shape (Boeing/NASA X-48B/C: 122 flights, 2007–2013).
- **Promise:** Internal volume — batteries and payload inside a lifting centerbody; structurally efficient; quiet.
- **Cost:** At 0.9m span, a BWB is nearly indistinguishable from "our rectangular wing with a fat center chord." The ribs already vary freely in our construction method, so this is an *evolution*, not a revolution. Yaw control needs attention (X-48 used winglets/twin tails).
- **Verdict:** Mild-wild. The most likely near-term evolution of the PoC airframe when the family needs payload volume. Not really a side quest — it's the obvious next step.
- Sources: [Boeing X-48 (Wikipedia)](https://en.wikipedia.org/wiki/Boeing_X-48), [X-48C first flight](https://www.theengineer.co.uk/content/news/blended-wing-body-research-aircraft-flies-for-the-first-time)

### 7. KFm stepped airfoil (Kline–Fogleman)
- **What:** A step in the wing section traps a vortex that acts as a rolling bearing for the airflow — stall-resistant to absurd AoA, keeps control surfaces effective. Huge foam-RC following; literally designed for sheet-foam construction.
- **Promise:** Trivially buildable — stepped Depron sheets need *no printed ribs at all*. Extremely forgiving flight characteristics; flying wings especially benefit.
- **Cost:** Draggier than a real airfoil section (wind-tunnel L/D is poor; the RC following is about handling, not efficiency). Gives up cruise performance vs MH60.
- **Verdict:** Not the efficiency answer, but the ultimate *buildability fallback*: if rib printing ever becomes the bottleneck, a KFm wing is a weekend build. Also the right section for a crash-happy trainer variant.
- Sources: [Kline–Fogleman airfoil (Wikipedia)](https://en.wikipedia.org/wiki/Kline%E2%80%93Fogleman_airfoil), [Park Pilot design notes](https://www.theparkpilot.org/kline-fogleman-airfoil-design), [FliteTest KFm discussion](https://forum.flitetest.com/index.php?threads/kline-fogleman-modified-kfm-airfoils.621/page-2)

### 8. Simple dart/delta
- **What:** The paper-dart planform. Countless RC deltas; stall-proof by geometry.
- **Promise:** Simplest possible build (fewer unique parts than even our 8-rib wing); robust; fun.
- **Cost:** Low effective AR → high induced drag at our low cruise speeds. Elevons at the tips, pitch authority meh. A step backward in efficiency from the current wing.
- **Verdict:** Fine for a "sport" family member. Not the endurance answer.

### 9. Biplane
- **What:** Two wings, one above the other. MAV wind-tunnel work shows 64–158% more lift than the equivalent monoplane at low AoA (gap/chord ≈ 0.53) — but with interference drag that makes it a worse cruiser.
- **Promise:** Compact span — the packable/backpack family member. Structurally the strut-braced box is stiff and light in carbon.
- **Cost:** Interference drag is a permanent tax; struts + rigging = parts count and failure modes; endurance suffers vs the monoplane.
- **Verdict:** Viable only where packability is the mission. Otherwise a worse wing with more parts.

### 10. Forward-swept wing
- **What:** X-29's party trick: inboard-directed spanwise flow keeps tips (and ailerons) unstalled to high AoA.
- **Promise:** Tip-stall resistance; moves the aerodynamic center forward (packaging leverage for nose-heavy layouts).
- **Cost:** Aeroelastic divergence — the X-29 needed composite aeroelastic tailoring to not tear its own wings off. Our Depron/carbon structure is torsionally soft; a forward-swept Depron wing is a divergence experiment, not an airplane. Zero cruise benefit.
- **Verdict:** No mission payoff, real structural risk. Skip.
- Sources: [Grumman X-29 (Wikipedia)](https://en.wikipedia.org/wiki/Grumman_X-29)

### 11. Oblique / skew wing
- **What:** One wing pivoted asymmetrically (NASA AD-1, 79 flights, 1979–82, R.T. Jones's concept). Transonic/supersonic wave-drag play.
- **Promise:** At Mach 1+, enormous. At 7 m/s: nothing.
- **Cost:** A pivot mechanism in a 200g airplane; cross-coupling handling quirks the AD-1 never solved below 60° skew.
- **Verdict:** Maximally wild, completely stupid for our mission. Included for the joy of it.
- Sources: [AD-1 flight test retrospective](https://www.slashgear.com/1351054/ad-1-strange-nasa-aircraft-pivoting-wing/), [Rutan AD-1 program summary (PDF)](http://burtrutan.com/downloads/AD1ProjectSummary.pdf)

### 12. Morphing / variable sweep
- **What:** Wings that change shape in flight — RoboSwift (<100g, 50cm span, Delft/Wageningen) proved sub-100g sweep morphing flies; UCSD demonstrated variable sweep on a small UAV; passive/active twist-morphing wings exist in the literature.
- **Promise:** Multi-point optimization: spread wings for loiter, sweep for dash. Genuinely demonstrated at our weight class.
- **Cost:** Our mission is *steady-state cruise* — morphing optimizes across flight phases we don't have. Actuators, hinges, and slop eat grams and add failure modes to a platform whose philosophy is simplicity.
- **Verdict:** Demonstrated but pointless for the PoC. A far-future family member with a dash requirement could revisit. Not this decade's problem.
- Sources: [RoboSwift (New Scientist)](https://www.newscientist.com/article/1906268-morphing-aircraft-mimics-a-bird-on-the-wing/), [polymorphing wing for small UAVs (MDPI)](https://mdpi.com/2226-4310/9/4/205/htm)

---

## Ranked: top 3 wildest-but-viable

**1. Prandtl-D bell-spanload twist** — the only concept here that *removes* parts: delete the winglets via proverse yaw, keep the efficiency. Twist is free in our construction method (rotate rib profiles at print time), NASA already flew the demonstrators, and it deepens the flying-wing identity instead of fighting it. The single most compelling reason: subtraction beats addition, and this is the only wild idea that subtracts.

**2. Ogival/ogee planform** — Concorde looks with a genuine low-Re story: leading-edge vortices demonstrably form at Re~10⁵, making the wing essentially stall-proof. The single most compelling reason: stall safety as a designed-in feature (not a hope), at a build cost of zero — printed ribs follow any planform for free. Cruise penalty is real and must be priced honestly.

**3. Tandem wing** — the only concept that solves a *family* problem rather than an aero problem: real internal volume and a natural sensor-bay layout between two positively-lifting surfaces, in a compact span. The single most compelling reason: when the family grows a payload, the tandem is waiting with the packaging answer — and both wings can stay MH60 in our existing construction system.

**Honorable mentions:** BWB center-body (the obvious near-term evolution, barely wild); KFm section (the buildability escape hatch); box wing (killed on joint complexity — the honest no).

---

## Proposal: Airframe Design Model extensions

Target: the `airframe-design-model` web artifact. These extensions let it evaluate concepts 1–3 (and kill 4–5, 9–12 with numbers instead of adjectives). Ordered by value.

### E1. Parameterized planform + twist module (highest value)
Replaces/augments the single taper-ratio input.
- **New inputs:** `planform_type` ∈ {rectangular, tapered, elliptical, ogee, double-delta}; ogee parameters (apex position η_apex, leading-edge fullness exponent); crank position/chord for double-delta; `twist_preset` ∈ {linear washout, Prandtl-D bell} plus a per-station twist table override (8 stations, matching our 8-rib build).
- **New physics:** 20-station lifting-line (Weissinger-style) over the actual chord distribution → spanwise lift distribution plot, true induced-drag factor e (replacing the fixed 0.78 assumption), local Re(η) for the low-Re drag adder.
- **New outputs:** spanload shape visualization with elliptical/bell reference overlay; trim elevon deflection from the twist distribution; proverse/adverse yaw hint flag (tip-region upwash check for bell loadings).
- **Why first:** unlocks quantitative evaluation of winners #1 (twist) and #2 (ogee) inside the existing model. Kills or confirms with numbers.

### E2. Multi-surface configuration mode
- **New inputs:** `config` ∈ {monoplane, tandem, box}; tandem: front/rear span, chord, gap, stagger, decalage; box: joiner height h, joiner chord.
- **New physics:** tandem — rear-wing dynamic-pressure ratio (≈0.9 default, editable), downwash angle from front wing, decalage trim solution, combined neutral point (area × lift-curve-slope weighted), CG envelope between the surfaces; box — Prandtl/Munk interference factor as a function of h/b applied to induced drag, joiner wetted-area drag adder, joiner structural weight estimate (foam + carbon cap).
- **New outputs:** per-surface lift share, trim state, combined NP/CG with the CG-envelope plot, interference-drag delta vs monoplane.
- **Why second:** evaluates winner #3 (tandem) and lets the model honestly kill the box wing (E1+E2 together show the joint weight erasing the induced-drag gain).

### E3. Side-by-side mission compare mode
- **What:** run the full mission (range, endurance, AUW, stall speed, part count) on up to 3 saved configurations and render a comparison table + bar view.
- **Why third:** the trade-study view. Every concept card above becomes a saved config; the ranking stops being prose and starts being a table. This is the feature that makes the model a *decision* tool rather than a calculator.

### Secondary (do after E1–E3)
- **S1. Vortex-lift correction** (Polhamus suction analogy) for sharp-LE ogee/delta — hard-gated to α > 12° with a prominent "post-stall/high-AoA only, irrelevant to cruise" warning. Prevents the model from laundering a party trick into cruise performance.
- **S2. Low-Re aero pack:** laminar-separation-bubble drag adder for Re < 150k (flagged estimate), KFm step option (ΔCd + ΔClmax, stall character → gentle).
- **S3. Buildability/simplicity index:** parts count, unique-rib count, joint count, skin-curvature flag → a single "complexity score" that penalizes configurations per the design philosophy (cheap to crash, simplicity = reliability). Lets the model kill pretty-but-fragile ideas on philosophy grounds, quantitatively.

**Suggested build order:** E1 → E3 (compare needs something to compare; E1 gives it two new configs immediately) → E2 → S1/S2/S3. E1+E3 alone make the model dangerous in the best way.
