# Material Claims — Substantiation Audit
Every material number used in this project, checked against sources and first-principles math. 2026-10-12.

## Verdicts

### 1. Depron 3mm ≈ 100 g/m² — CONFIRMED (with band)
- FliteTest forum ("Foam board weight" thread), measured by a builder: **"3 mm depron — 33 kg/m³ — about 100 grams for a 1 m² sheet."**
- SLEC (UK Depron distributor): Depron "as light as 28 kg/m³", consistent sheet-to-sheet density.
- A second spec sheet lists 3mm Depron at 33–40 kg/m³ depending on variant (classic vs Aero).
- **Refinement:** real band is **84–120 g/m²**. The weight model uses 100 g/m² (skins = 36g); true value could be 30–43g. The coupon test + weigh-in will nail it. Uncertainty is ±7g on AUW — survivable inside the margin.

### 2. Paper-faced foamboard rejected — CONFIRMED (conclusion holds)
- FliteTest forum, measured: Dollar Tree sheet (20"×30" = 0.387 m²) = **114g → 295 g/m²**; Elmer's = 227g → 587 g/m².
- My earlier 177g figure reconstructs as: 0.44 m² skins (1m design) × ~400 g/m² (Adams Readi-Board) ≈ 176g. Consistent.
- Current 0.9m design: 0.36 m² × 295 g/m² (cheapest DT board) = **106g skins vs 36g Depron** — a 70g penalty that single-handedly breaks the 250g cap.
- Supporting: rc-help forum — "foam to foam, depron is stronger" (foamboard's strength comes from its paper skins, which is exactly the dead weight we can't afford).

### 3. Vase-mode printed ribs ~1.5g each — CONFIRMED (conservative)
- Hackaday (2017): "single-wall vase in the shape of a wing rib" bonded to foam-board covering with Gorilla Glue — the exact hybrid technique. Their hybrid plane: 312g vs 468g fully printed, same electronics.
- First principles: rib outline perimeter ≈ 0.45m × 0.45mm wall × 3mm tall = 0.61 cm³ × 1.24 g/cm³ (PLA) ≈ **0.75g**. My 1.5g budget is 2× conservative. Holds.

### 4. Fully-printed 1m airframe rejected — CONFIRMED (range corrected upward)
- First principles (lower bound): hollow shell, top+bottom = 0.88 m² × 0.45mm wall = 396 cm³ × 0.6–0.75 g/cm³ (foamed LW-PLA) = **238–297g for skins alone**, before ribs/spar.
- **Correction:** my earlier "150–210g" was the optimistic end; realistic is **~200–300g**. The rejection is stronger than I stated: a 200g+ airframe leaves nothing for systems under 250g.
- Supporting: proven sub-250g printed aircraft are all ≤600mm span (PolyMAV Lynx 500mm); 1m-class printed planes (Eclipson etc.) run 400g+ airframes.

### 5. Carbon spar — CORRECTED: 5mm → 4mm tube
- **Error found:** I budgeted "5mm carbon tube, ~7 g/m." Real pultruded 5mm OD tube (5×3mm or 5×4mm, density 1.6 g/cm³) weighs **11–20 g/m**. My figure was wrong.
- **Fix:** 4mm OD × 3mm ID tube = π×(4−2.25) = 5.5 mm² × 1.6 g/cm³ = **8.8 g/m → 7.9g per 0.9m spar** (was 6.3g; +1.6g on AUW).
- Strength check (conservative 600 MPa flexural): Z = π(256−81)/(32×4) = 4.29 mm³ → M_allow = 2.57 N·m vs 0.77 N·m required at 3g → **margin 3.3×**. Still a comfortable spar, still the assembly backbone.
- The earlier "6× margin" claim assumed a 5mm tube that doesn't weigh what I said. The 4mm pick is the weight-honest version.

### 6. Depron shatters on crash (first airframe = test article) — CONFIRMED
- rc-help: "if you crash, depron shatters."
- RCGroups: "depron is more brittle, so it may have less give in a hard landing or soft crash and snap instead of bending."
- Mitigation stands: budget foam for two airframes; printed ribs/motor survive; rebuild ≈ $10.

### 7. Depron skin spans 120mm between ribs at cruise q — CONFIRMED (order of magnitude)
- Plate calc: q ≈ 90 Pa at 12 m/s, 120×200mm panel, E ≈ 10–15 MPa (XPS) → deflection **0.2–0.3mm**. Sub-millimeter pillowing — cosmetically irrelevant, aerodynamically invisible.
- The rib's real job is holding airfoil shape during handling, not carrying air loads (the spar does that). Coupon test will confirm feel.

### 8. Adhesives (foam-safe CA, 3M-77) — CONFIRMED
- Depron tech sheet: 3M-77 is "foam friendly and ideal for laminating" Depron; UHU Por named as the Depron-to-Depron adhesive. Foam-safe CA is community standard (rc-help repair threads).

## Net effect on the weight budget
- Spar correction: +1.6g → AUW ≈ 234g, margin 16g (was 17g). Immaterial.
- Depron density band: ±7g uncertainty until the coupon test weighs a real sheet.

## Still open (physical tests, not browser)
1. Weigh one real Depron sheet → locks skins at 30–43g.
2. Print one rib → locks 0.75g vs 1.5g.
3. Glue-joint test: Depron-to-Depron and Depron-to-PLA peel strength.

*Audit method: every numeric claim re-derived from a measured source or closed-form calc; corrections logged above, none hidden.*
