# Airframe Architectures — Academic Literature Track

The rigorous counterpart to the skunkworks survey (`WILD_CONCEPTS.md`). Same platform constraints, different method: every claim below must trace to peer-reviewed literature, theses, textbooks, or NASA reports. Where the literature is silent, that is stated.

**Platform (non-negotiable):** sub-250g AUW · 30km-class quiet autonomous cruise/loiter at ~7 m/s, Re ≈ 90k · hybrid build (3mm Depron + carbon spar + printed ribs) · cheap to crash · platform/family, not just the 0.9m PoC · current baseline: 0.9m rectangular tailless wing, MH60, 204g AUW.

**Decision standard applied:** 4 rounds of proactive criticism per candidate (R1 naive ranking → R2 honesty filter → R3 steelman → R4 kill attempts), iterated until the ranking converged. Mind-changes between rounds are documented in §4.

---

## 1. Literature base

| # | Source | What it contributes |
|---|--------|---------------------|
| L1 | Ning & Kroo (2010), "Multidisciplinary Considerations in the Design of Wings and Wing Tip Devices," *J. Aircraft* 47(2) | Minimum-drag wing optimization under lift/weight/pitching-moment/stall constraints. For tailless aircraft, C-wings slightly beat winglets once trim + stability constraints are imposed; advantage grows for span-constrained or low-sweep designs. http://scholarsarchive.byu.edu/facpub/1629/ |
| L2 | Kroo, VKI Lecture Series on Innovative Configurations (2005) | Nonplanar wing review: horizontal tip extensions on a BWB move the aerodynamic center aft enough to trim without large sweep, opening laminar-flow drag reduction. http://innopedia.wdfiles.com/local--files/references/nonplanarwing |
| L3 | Bowers et al., "Experimental Flight Validation of the Prandtl 1933 Bell Spanload" (2021), NASA/TM (NTRS) | Flight-measured yawing-moment-due-to-aileron (Cnδa) on Prandtl-D demonstrators: positive = proverse yaw confirmed in flight, matching vortex-lattice prediction within ~15%. https://ntrs.nasa.gov/api/citations/20210014683/downloads/H3284FINAL.pdf |
| L4 | Ran & Parks (2023), "Aerodynamic Modeling of a Flying Wing Featuring Ludwig Prandtl's Bell Spanload," *Aerospace* 10, 613 | CFD + VLM of bell-spanload flying wing: proverse yaw traced entirely to the twist distribution; tip-region pressure drag near zero/negative on the deflected side. https://www.mdpi.com/2226-4310/10/7/613 |
| L5 | NASA Armstrong, Prandtl-D program briefs (2015–2019) | Subscale demonstrators (12.5–25 ft span, foam/carbon, bungee-launched, hobby-grade RC): bell twist validated in flight; program claims ~11–12% drag reduction and a path to deleting the vertical tail. https://ntts-prod.s3.amazonaws.com/t2p/prod/t2media/tops/pdf/DRC-TOPS-36.pdf |
| L6 | METU M.Sc. thesis, "Aerodynamic Design and Control of Tandem Wing UAV" (etd.lib.metu.edu.tr) | Full tandem micro-UAV design study: front-wing downwash degrades rear-wing control effectiveness and can induce rear-wing stall/instability at some AoA; interference handled via CFD database + careful control design + Monte-Carlo robustness check. Notes propulsion ≈ 60% of micro-UAV weight. http://etd.lib.metu.edu.tr/upload/12623631/index.pdf |
| L7 | "Aerodynamic Exploration for Tandem Wings with Smooth or Corrugated Surfaces at Low Reynolds Number," *Aerospace* 2023, 10, 427 | Fixed-wing tandem MAV study at low Re: gap/stagger/decalage parametric; concludes tandem can outperform with proper arrangement. https://www.mdpi.com/2226-4310/10/5/427/xml |
| L8 | Munianjanappa et al., "Design and Development of a Flying Wing Reconnaissance UAV" (ResearchGate, 2024) | Direct tandem-vs-conventional comparison (3 kg class, CFD + flight test): tandem achieved 13.5% shorter wingspan and 40% shorter takeoff roll than the conventional equivalent; tandem pays in structural weight and drag. https://www.researchgate.net/publication/376893514_DESIGN_AND_DEVELOPMENT_OF_A_FLYING_WING_RECONNAISSANCE_UAV |
| L9 | "Box Wing vs Monoplane for Small UAVs" (arXiv 2112.02872) | Head-to-head at small-UAV scale: box wing wins specifically where induced drag dominates (high lift demand, low AR). https://arxiv.org/pdf/2112.02872 |
| L10 | UPM thesis, joined-wing investigation (oa.upm.es/40383) | Prandtl–Munk theory applied to joined wings: multiplane systems beat conventional span-matched configurations on induced drag; wind-tunnel Oswald factor exceeded prediction; frames joined wing as a UAS-suitable configuration. https://oa.upm.es/40383/1/INVE_MEM_2015_216896.pdf |
| L11 | Kroo et al., joined-wing optimization (via review in Scribd-hosted Stanford paper) | VLM + beam-structures comparison: joined wing saved ~11% cruise drag vs a conventional design of equal lifting area and structural weight (joint at ~70% semispan) — but mission-wide economics (takeoff, climb) could erase the gain. https://www.scribd.com/document/97178784/19970022623-1997032389 |
| L12 | Baig et al. (2018), "A New Methodology for Aerodynamic Design and Analysis of a Small Scale Blended Wing Body," *J. Aeronaut. Aerospace Eng.* 7:206 | Small-scale BWB design method; cites Thomson et al. 5 m BWB UAV work; foam prototype flown successfully; stability handled by CG placement ahead of center of pressure plus reflex airfoils. https://www.longdom.org/open-access-pdfs/a-new-methodology-for-aerodynamic-design-and-analysis-of-a-small-scaleblended-wing-body-2168-9792-1000206.pdf |
| L13 | "Exploring the Performance Boundaries of a Small Reconfigurable Multi-Mission UAV" (Switchblade), *Aerospace* 2023, 10, 684 | BWB small UAV, CFD + wind tunnel + flight: low-speed endurance variant reached 1 h 48 min / 131 km; CFD underpredicted lift and overpredicted high-AoA drag vs tunnel; BWB aerodynamics "difficult to model analytically prior to CFD"; both variants flew off their aerodynamic optimum. https://www.mdpi.com/2226-4310/10/8/684/html |
| L14 | "Design and Flight Tests of a Small Flying Wing UAV," *Aerospace* 2026, 13, 240 | Small flying-wing design + flight test program: sweep mattered more for longitudinal stability than wingtip airfoil Cm; twist shaped the lift distribution; low-Re tip flow forced larger tip chords and high-critical-AoA sections. https://www.mdpi.com/2226-4310/13/3/240 |
| L15 | Hepperle, "Airfoil Design for Tailless Airplanes" (mh-aerotools.de) | Designer-level treatment of reflex/camber tradeoffs for tailless sections: more camber + reflex raises max lift but hardens the stall; the MH series was developed specifically for tailless model aircraft. http://www.mh-aerotools.de/airfoils/nf_7.htm |
| L16 | Univ. of Seville, Aircraft Design course slides (flying-wing section) | Pedagogical summary of the standard result: flying wings cut wetted area and interference drag vs wing+fuselage+tail, improving range/endurance for a given propulsion system — at the cost of complicating stability, control, and the design process itself. http://aero.us.es/adesign/Slides/Extra/Airplane/Flying_Wings/Airfoil Design For Flying Wing Uav.pdf |

---

## 2. Architecture cards (literature-grounded)

### A. Swept tailless flying wing — the baseline
- **Literature promise:** The all-lifting configuration minimizes parasite drag (L16); small-UAV flight-test literature confirms the configuration works at our scale with sweep + twist as the stability tools (L14). Ning & Kroo (L1) provide the optimization framework that treats trim and stability as first-class constraints rather than afterthoughts — directly applicable to our 8%-SM, elevon-trimmed design.
- **Cost:** Directional stability/control is the documented Achilles heel of tailless designs (L14, L16); stall/spin behavior needs care (L14 lost 34 m in a spin entry before recovery). Mitigations in our design: winglets, 20° sweep, ArduPlane stabilization.
- **Family fit:** Excellent — the construction system (identical ribs) is already wing-native; scaling span/chord is parametric.

### B. Prandtl-D bell-spanload twisted wing
- **Literature promise:** Proverse yaw demonstrated in flight, not just theory (L3: positive Cnδa measured on two independent flight-data teams); CFD traces the effect entirely to twist (L4); NASA program claims ~11–12% drag reduction plus a path to deleting the vertical tail (L5). US Patent 9,382,000.
- **Cost:** All flight validations are at 12.5–25 ft span — orders of magnitude above our Re and scale; the bell distribution's induced-drag benefit is thinnest exactly at our low-CL cruise; twist must be built accurately (though our printed ribs make per-station twist nearly free).
- **Family fit:** Excellent — it is a twist distribution, not a new configuration; it ports to any family span.

### C. Tandem wing
- **Literature promise:** Both surfaces produce positive lift (no tail-download penalty); compact span for a given area (L8: −13.5% span, −40% takeoff roll vs conventional); low-Re parametric studies show tandems can outperform with proper gap/stagger/decalage (L7).
- **Cost:** The literature is candid that interference is the whole problem: rear wing flies in front-wing downwash, degrading control effectiveness and risking rear-wing stall/instability (L6 — an entire thesis wrestling with this); CG placement between the wings is sensitive; two wings = more parts, more joints, more weight (L8).
- **Family fit:** The best packaging story in the trade space — a real fuselage/payload bay between two lifting surfaces, which is the family's future sensor problem, not an aero problem.

### D. Box / joined wing
- **Literature promise:** Prandtl's "best wing system" on induced drag (L10, via Prandtl–Munk theory); the one head-to-head study at small-UAV scale found the box wins where induced drag dominates (L9); Kroo et al. measured ~11% cruise-drag saving vs conventional at equal area and structural weight (L11); closed structure is inherently stiff.
- **Cost:** The win condition (induced-drag-dominated flight) is the opposite of our mission — at Cl≈0.5/Re≈90k, profile drag and propulsion dominate; the vertical joiners are weight, wetted area, and precision joints in foam; Kroo et al. themselves warn mission-wide analysis can erase the cruise gain (L11).
- **Family fit:** Poor — joint complexity scales badly in Depron; the stiffness argument matters less when a carbon spar already solves bending.

### E. Blended wing body (small-scale)
- **Literature promise:** Internal volume inside a lifting centerbody (batteries/payload without a draggy fuselage); X-48 program flew 122 flights (2007–2013); foam small-scale prototypes have flown (L12); structural efficiency of the merged shape.
- **Cost:** At 0.9 m span a BWB is geometrically almost indistinguishable from our rectangular wing with a fatter center chord — an evolution, not an architecture; small BWBs are analytically difficult (L13: "difficult to model analytically prior to CFD") and the tested variants flew off-optimum; yaw control reintroduces surfaces (X-48 used winglets/twin tails).
- **Family fit:** Good as a *variant* — when the family needs internal volume, fatten the center chord. Not a distinct PoC architecture.

### F. Conventional tail-aft
- **Literature promise:** The entire design knowledge base; textbook stability methods (tail volume coefficient); the Munianjanappa comparison (L8) is the honest baseline everything else is measured against; lowest handling-qualities development risk.
- **Cost:** Permanent taxes — tail download (the stabilizer flies at negative lift in cruise), fuselage wetted area that produces no lift; at sub-250g the empennage is a large weight fraction; our construction system is wing-native, so a fuselage + tail means new part types and joints.
- **Family fit:** Neutral — buildable, but it abandons the platform's tailless-efficiency identity for no mission gain.

### (Addressed, not ranked) Annular / ring wing
Prandtl's minimum-induced-drag work crowns the *box* wing, not the ring (L10); no serious low-Re endurance literature supports the ring for a cruise mission. Killed in the skunkworks survey on drag grounds; the academic track concurs and moves on.

---

## 3. Criticism rounds

**R1 — Naive literature ranking (brochure claims):** 1. BWB (40% endurance claims, X-48 glamour) · 2. Bell spanload (NASA 12%) · 3. Baseline wing · 4. Tandem · 5. Box/joined · 6. Conventional.

**R2 — Honesty filter (apply our operating point: Cl≈0.5, Re≈90k, profile drag + propulsion dominate):**
- BWB's big numbers are transport-scale; at 0.9 m the geometry collapses to "fat-center wing." Demoted.
- Box/joined's win condition (induced-drag-dominated) is inverted at our mission. Demoted hard.
- Bell spanload's *drag* benefit thins at our Cl — but the *parts-removal* benefit (delete winglets via proverse yaw) is operating-point-independent. Held.
- Tandem's aero case weakens (interference tax is real, L6) but its packaging case is untouched. Held.
- Conventional rises slightly: the literature's risk baseline has value. Held low.

**R3 — Steelman each (best possible case):**
- *Baseline:* the most-flown small-UAV endurance configuration in the literature; MH60 verified; Ning & Kroo's framework optimizes exactly our trim problem. Lowest technical risk, period.
- *Bell:* flight-validated physics (L3), subtraction not addition, twist free in our process. The only candidate that removes parts.
- *Tandem:* the only candidate solving the family's payload-volume problem with positive lift everywhere; L8's measured −13.5% span is real.
- *BWB:* X-48's 122 flights + foam prototypes (L12) prove buildability; volume argument is genuine.
- *Box:* Prandtl's theory + the arXiv small-UAV head-to-head + UPM's measured e-beats-prediction — the physics is the most prestigious in the trade space.
- *Conventional:* the safe harbor — if tailless handling ever defeats us, this is where we land.

**R4 — Kill attempts (strongest argument against each):**
- *Baseline:* directional stability is the documented weak point (L14, L16) — **survives**: winglets + 20° sweep + ArduPlane are specific, adequate mitigations.
- *Bell:* unvalidated at our Re/scale; twist accuracy — **survives**: the parts-removal benefit doesn't need the drag claim, and rib-printing makes twist genuinely cheap. Flagged for flight validation.
- *Tandem:* L6 is essentially a thesis-length warning about interference; Quickie history on CG sensitivity — **survives on packaging only**, explicitly not on aero merit.
- *BWB:* L13 shows small BWBs underperform their analysis and need CFD to design at all — **demoted** to evolutionary variant; it is not a separate architecture at our scale.
- *Box:* joints in Depron at 200 g; win condition inverted; L11's own authors warn the mission analysis erases the gain — **killed for the PoC**. Kept as a revisit note if a future family member ever becomes induced-drag-dominated.
- *Conventional:* permanent download + wetted-area taxes; abandons platform identity — **kept as the fallback**, not the plan.

---

## 4. Mind-changes between rounds (audit trail)

1. **BWB: 1st → 4th.** The transport-scale endurance claims evaporated at 0.9 m span; L13 (Switchblade) showed small BWBs are hard to model and fly off-optimum. It is a center-chord variant of the baseline, not an architecture. (Changed R1→R2.)
2. **Box/joined: 5th → killed.** Prandtl's "best wing system" prestige did not survive checking the win condition against our operating point (L9's own framing) plus L11's mission-economics warning. (Changed R2→R4.)
3. **Bell spanload: 2nd → 1st (aspirational).** The subtraction argument (delete winglets) survived R4 independently of the drag debate — the only candidate that removes parts rather than adding them. (Changed R3→R4.)
4. **Conventional: 6th → 5th (fallback).** Steelmanning the knowledge-base and handling-qualities arguments recovered it from "boring" to "the right lifeboat." It is kept in the trade space deliberately. (Changed R3→R4.)
5. **Tandem: held 3rd throughout**, but its *justification* changed: aero promise (R1) → packaging promise (R4). The ranking is stable; the reasoning is not what it was.

Convergence: R3 and R4 agree on the order; no candidate moved in the final pass. 11/12-equivalent consensus reached — the ranking below is the converged output.

---

## 5. Ranked top tier for Z!B

1. **Prandtl-D bell-spanload tailless wing** — the platform's target architecture. NASA flight-validated proverse yaw (L3), deletes the winglets (parts, weight, drag), twist is free in printed ribs. Next step: validate proverse yaw at our Re/scale in flight test; the drag claim is secondary.
2. **Swept tailless flying wing, MH60 (current baseline)** — the PoC pathfinder. Deepest small-scale literature support (L14), verified airfoil (L15), lowest risk. The PoC flies this; the bell twist is its documented evolution, not a redesign.
3. **Tandem wing** — the family payload carrier. Kept for the packaging problem (real fuselage volume, positive lift everywhere), with L6's interference warnings as the design constraints, not a veto. A sensor-carrying family member starts here.
4. **BWB centerbody evolution** — the near-term variant path: when the family needs internal volume, fatten the center chord of architecture #1/#2. Tracked as a variant, not a program.
5. **Conventional tail-aft** — the handling-qualities fallback, deliberately retained. If tailless directional stability ever defeats the program in flight test, this is the lifeboat — accepted costs and all.

**Explicitly not top tier:** box/joined wing (killed for the PoC on joint complexity + inverted win condition; revisit only if a family member becomes induced-drag-dominated), annular wing (no literature case for our mission).

---

## 6. Strongest literature finding

NASA Armstrong's flight measurement of positive Cnδa — proverse yaw — on the Prandtl-D demonstrators (L3), reproduced by two independent flight-data analysis teams and matched by vortex-lattice prediction within ~15%. A tailless wing yawing *into* the commanded turn, with no vertical tail, is demonstrated fact rather than theory. It converts the bell twist from a "wild concept" into the platform's highest-upside, lowest-parts-count evolution.

## 7. Biggest open question

The literature contains **no configuration-level comparison at our scale and Reynolds number** — no measured flying-wing-vs-tandem-vs-BWB study at Re 50k–150k, sub-250g, with endurance numbers. The comparisons that exist are CFD, transport-scale, or single-configuration flight tests. Concretely: bell-spanload proverse yaw has never been demonstrated below ~3 m span / above Re ~10⁶ in flight; whether the tip-region upwash physics survives at Re ≈ 90k in a foam wing is the single most valuable unknown, and only our flight test can answer it.

---

## References (verbatim URLs)

- L1: http://scholarsarchive.byu.edu/facpub/1629/ · http://flowlab.groups.et.byu.net/publications/Ning2010-Multidisciplinary-Considerations.pdf
- L2: http://innopedia.wdfiles.com/local--files/references/nonplanarwing
- L3: https://ntrs.nasa.gov/api/citations/20210014683/downloads/H3284FINAL.pdf
- L4: https://www.mdpi.com/2226-4310/10/7/613
- L5: https://ntts-prod.s3.amazonaws.com/t2p/prod/t2media/tops/pdf/DRC-TOPS-36.pdf
- L6: http://etd.lib.metu.edu.tr/upload/12623631/index.pdf
- L7: https://www.mdpi.com/2226-4310/10/5/427/xml
- L8: https://www.researchgate.net/publication/376893514_DESIGN_AND_DEVELOPMENT_OF_A_FLYING_WING_RECONNAISSANCE_UAV
- L9: https://arxiv.org/pdf/2112.02872
- L10: https://oa.upm.es/40383/1/INVE_MEM_2015_216896.pdf
- L11: https://www.scribd.com/document/97178784/19970022623-1997032389
- L12: https://www.longdom.org/open-access-pdfs/a-new-methodology-for-aerodynamic-design-and-analysis-of-a-small-scaleblended-wing-body-2168-9792-1000206.pdf
- L13: https://www.mdpi.com/2226-4310/10/8/684/html
- L14: https://www.mdpi.com/2226-4310/13/3/240
- L15: http://www.mh-aerotools.de/airfoils/nf_7.htm
- L16: http://aero.us.es/adesign/Slides/Extra/Airplane/Flying_Wings/Airfoil Design For Flying Wing Uav.pdf
