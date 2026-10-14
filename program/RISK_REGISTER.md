# Risk Register — Sub-250g UAV
Baseline: 0.90m MH60 flying wing, hybrid Depron/printed construction ("to be studied" — gated on coupon test, D-10), ≤250g AUW, PoC 0g payload (≥30g requirement applies to product/family instances, D-05), ArduPlane angle-mode autonomy.
Maintained by Oubi. Updated whenever a risk opens, closes, or changes. Deltas reported at each development stage.

## Airframe
- **R-01 Wing twist during skinning** → untrimmable wing, efficiency loss. *Mitigation:* flat jig + washout shims mandatory; test rib + skin sample first. *Status:* OPEN
- **R-02 Depron shatters on crash** → airframe loss. *Mitigation:* first airframe is a test article; budget foam for two; printed ribs are reusable. *Status:* OPEN
- **R-03 Printed rib fit / Depron bend-radius mismatch** → gaps, weak bonds. *Mitigation:* print one test rib and check fit before batch printing. *Status:* OPEN
- **R-04 LW-PLA foaming slicer sensitivity** → weak or overweight printed parts. *Mitigation:* use plain PLA for small rib parts (simpler, weight acceptable); calibrate foaming on test pieces only if LW-PLA is chosen. *Status:* OPEN
- **R-16 PW75 polar never verified** → incumbent airfoil had no obtainable coordinates, polar, or test data (confirmed by dedicated search 2026-10-13); flying it meant unknown stall/trim behavior on the maiden. *Resolution:* airfoil trade study (AIRFOIL_TRADE.md) evaluated PW75 / MH60 / HS130 / E387 / S3021 at Re≈100k with mission model + trim analysis → **airfoil switched to MH60** (verified polar, gentle stall, trims with −6° elevon at 2° washout). *Status:* RETIRED 2026-10-13 — closed by replacement, not by finding the data

## Weight (master constraint: 250g total AUW)
- **R-05 Weight creep** → exceeds 250g → loses the entire regulatory advantage. *Mitigation:* weigh-as-you-go on a kitchen scale; every subsystem weighed before install; any line-item overage must be offset elsewhere before install. *Status:* OPEN — PoC margin is 46g (204.3g AUW, WEIGHT_BUDGET.md); the margin is armor against creep, discipline mandatory
- **R-06 Battery actual weight vs 55g estimate** → budget break. *Mitigation:* weigh the chosen pack before committing; size the bay for alternatives. *Status:* OPEN

## Propulsion
- **R-07 Prop/motor mismatch** → excess current, poor efficiency, or excess noise. *Mitigation:* wattmeter bench test of the full power train before first flight. *Status:* OPEN
- **R-08 Pusher cooling/airflow** → motor or ESC overheat in the buried installation. *Mitigation:* verify airflow and temperatures on the bench at full throttle. *Status:* OPEN

## Avionics / integration
- **R-09 Receiver interface: F-08A parallel PWM vs FC serial RC input** → no RC link to autopilot. *Mitigation:* PWM→PPM encoder in the buy list; verify the interface before hardware freeze. *Status:* OPEN — flagged 2026-10-13 for reassessment vs the clean-sheet design (DEV_TRACKER.md §8); encoder still in buy list per BUDGET.md
- **R-10 5V rail capacity (FC + GPS + RX + 2 servos)** → brownouts, FC resets. *Mitigation:* SpeedyBee PDB servo BEC (4.9V/4.5A) covers servos; verify total rail budget on the bench. *Status:* OPEN
- **R-11 GPS/compass EMI from motor and ESC wiring** → poor position hold, bad RTL. *Mitigation:* GPS on a mast clear of power wiring; verify HDOP and compass health on the bench. *Status:* OPEN

## Operations / program
- **R-17 Battery vs skins clash** → 20mm pack in a ~20mm wing: CAD clash check found 14.1mm interference; battery needs a hatch. Geometry flagged as follow-up, not faked. *Mitigation:* design battery hatch into the center section; re-run clash check. *Status:* OPEN — hatch designed and CAD clash re-run is CLEAN (clash_report.json n_clash = 0, battery clearance + hatch-fit OK, 2026-10-13). Re-scoped per CE's Day 1–2 audit: the remaining concern is hatch structural continuity and battery retention (vibration/landing loads), not clearance. Verification path: coupon/hatch pull test in the physical evidence sequence.
- **R-12 Video link range < battery range** (on payload-bearing instances) → practical range limited by the link, not energy. *Mitigation:* when the payload type is decided (family-instance decision, AI-06), run a link-budget check before that instance's hardware freeze. *Status:* OPEN — parked until a family-instance payload is defined (D-05: PoC flies 0g)
- **R-13 No LiPo charger on hand** → can't fly. *Mitigation:* confirm ownership; buy if missing. *Status:* OPEN
- **R-14 Payload type undefined for family instances** → late layout and power-budget changes when the first payload-bearing instance is defined. *Mitigation:* decide payload type (AI-06) before that instance's Gate 2 freeze. PoC flies 0g (D-05), so this no longer blocks the PoC path. *Status:* OPEN
- **R-15 CG out of range on maiden** → instability or crash. *Mitigation:* bench-balance at ~18% MAC with the battery as the trim weight; verify before launch. *Status:* OPEN — CAD full-vehicle model (2026-10-13) reports CG at 128.5mm aft root LE (datum per cg_report.json) vs 116mm target → delta +12.5mm aft, SM near the lower edge of the 5–8% band; battery already moved, needs ballast or layout revision (sensitivity 0.30mm/mm). Datum caution: the optimization loop's 83.0mm figure (x_cg at SM6%) is a different coordinate convention, NOT the CAD datum — do not mix (CE-02 scope). Full reconciliation is CE-01 work per CE's Day 1–2 audit.

## Retired
- **R-16** (2026-10-13): PW75 polar unverifiable → airfoil switched to MH60 per AIRFOIL_TRADE.md.

---
*Last updated: 2026-10-13 (airfoil trade study: R-16 opened and retired, MH60 selected; reconciled with D-05/D-10: PoC 0g payload, 46g margin, payload = family-instance decision)*
