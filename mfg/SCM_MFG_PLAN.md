# Supply chain and manufacturing plan, Z!B PoC

| | |
|---|---|
| Seat | **Supply Chain & Manufacturing (SCM/MFG), Claude**. Appointed by the CEO, 2026-10-14 21:25 PT ("own every aspect of it as you would be made accountable for") |
| Baseline | CE-01 freeze, design hash **`479399d88b60`**, 233.0 g, CG 130.32 mm, SM 5.66% (D-31). Reproduced tonight with `scripts/mass_rollup.py` on `main` @86936d4 |
| Status | v1.1, 2026-10-14 22:30 PT (v1.1: CE-02/CE-03 purchasing impact from PR #22; spare ESC traded for the CE-02 receiver). v1.0 22:00 PT. Every number is **modelled** until a part is on the scale. Prices and stock are labelled with who checked them and when |
| Supersedes for buying | `program/BUDGET.md` (Oct 12, pre-R-07 parts), the buy list in `program/PROTOTYPE_ROADMAP.md` §3 and the cart in `mfg/CALIBRATION_BUY.md`. **Buy only from `mfg/bom.csv`.** The program files stay with their owner (MBSE); this note asks only that they point here |

## 1. Decisions needed (critical only)

| # | Decision | Why it is critical | Owner | Needed by |
|---|---|---|---|---|
| **K-1** | **Spar R1: qualify a 0.156 in tube by test.** No US-stocked 4.0 × 3.0 mm tube publishes flexural data. The two US-stocked tubes in this class are 0.156 in OD (3.96 mm) with thicker walls: DragonPlate 0.156 × 0.104 in, standard-modulus UD. Proposed CE item: accept a tube that matches the R1 **section capacity** (EI and bending strength) instead of the material numbers. For this section that is **E ≥ 88 GPa and flexural strength ≥ 876 MPa** on the 3-point bend coupon, cut from the same 48 in tube as the spar | The build cannot start without a spar. The tube adds about +2.0 g at x ≈ 165 mm, so SM goes from 5.66% to **5.51%** (DragonPlate). The ACP 0.156 × 0.100 in alternative gives 5.46% and is **not** acceptable without trim | GM proposes, MBSE approves (Art. IV) | Before the coupon test, Oct 21 |
| **K-2** | **Give the build a CG trim provision.** Behind the CG the design tolerates **0.32 mm** of CG shift to the 5.5% rule, or about **1 g** of unplanned mass at the prop and **0.4 g** at the fins. The frozen hatch leaves the battery **0 mm** of fore/aft travel. As built, the aircraft therefore has no way to trim. Proposal: a printed nose ballast pocket rated for up to 4 g (+0.27 pt per g) in the R5/hatch area, empty by default, used only after the as-built weigh-in | A first build that lands 1 g heavy aft becomes a no-fly with no remedy except rework. The CEO's "no ballast" decision (D-31) was about the design; this is a build-tolerance allowance | GM proposes, MBSE approves; CEO informed | CDR, Oct 28 |
| K-2a | **Interaction with CE-03 (PR #22, STF finding).** The fixed trailing-edge parts (+1.48 g at x 186/372 mm) take the roll-up to SM 5.25% before any build error. K-2 is therefore not a tolerance nicety: it is one of the levers for the joint CE-02 + CE-03 + battery review the STF integrates | STF integrates (Art III.5 as proposed); SCM supplies the trim-range and as-built data | 09:00 sync, Oct 15 |
| **K-3** | **VC-01 internal alert (≤ 230 g) is already exceeded** by the frozen 233.0 g. Re-baseline the alert (suggest ≤ 240 g, matching the roadmap's "review below 10 g margin") so the alert stays meaningful at the weigh-ins | A verification row that fails on the design value cannot warn about growth | MBSE | Gate 3, Oct 29 |
| **K-4** | **3D-printer access (AI-07): ANSWERED 22:26 PT, no printer on hand.** Recommendation: buy a Bambu Lab A1 ($299, BOM T-05). R5 centre section, 8 ribs, hatch frame and tray, motor mount and GPS mast are all printed | No printer means no airframe. If none is on hand, a print service adds about 3–5 days | **CEO** | Tomorrow, before the order |

## 2. Order plan (CEO places the orders; GM authority $500, D-23)

Source of truth: `mfg/bom.csv` (25 lines). Check: `python3 mfg/tools/bom_check.py` (cost, frozen-mass match, battery band; exit 0).

| Wave | When | Shop | Lines | ≈ USD |
|---|---|---|---|---|
| **W0** | **Thu Oct 15, first thing** | RcDepron.com | S-02 Depron 3 mm × 4. Single US importer, price not published, the longest lead time on the list | ~18 (est.) |
| W1 | Thu Oct 15 | Pyrodrone | P-05 Bullet 30A × 1, E-01 GNB 650 × 1, T-01 WM150, **C2-01 XR3 Nano** (CE-02 bench article) | 129.77 |
| W1 | Thu Oct 15 | RaceDayQuads | A-01 F405 WING Mini, A-02 M100-5883 | 63.98 |
| W1 | Thu Oct 15 | ReadyMadeRC | P-02 8x6SF × 3 (all that is left), P-03 8x3.8SF × 2, A-03 ES9051 × 3 | 28.91 |
| W1 | Thu Oct 15 | APC (apcprop.com) | P-02 8x6SF × 3, **second source** | 8.34 |
| W1 | Thu Oct 15 | Altitude Hobbies | P-01 Suppo 2204/14 × 2 | 35.18 |
| W1 | Thu Oct 15 | Scorpion | P-04 adapter × 2 | 6.18 |
| W1 | Thu Oct 15 | DragonPlate | S-01 0.156 × 0.104 × 48 in × 2 (no-regret at $19; acceptance via K-1) | 18.84 |
| W1 | Thu Oct 15 | Amazon / local | Encoder, filament, epoxy, foam glues, tape, linkages, fasteners, wiring, scale (≥ 500 g × 0.1 g), calibration weights | ~113 (est.) |
| | | **Total** | | **$422 + shipping ≈ $457–482**, inside $500 |
| CEO | when CE-02 is decided | GetFPV + any dealer | C2-02 Nomad ($58.49, **in stock at GetFPV**, 22:20 PT), C2-03 EdgeTX handset (~$250) | outside the $500 parts authority |

Thursday rather than Friday: it buys a day of float against the roadmap's Fri Oct 16 order date, and every day of slip moves the bench, CDR, Gate 4 and the maiden day for day.

## 3. Supply risk register (SCM-owned)

| ID | Risk | Status tonight | Mitigation |
|---|---|---|---|
| SC-01 | **APC 8x6SF**: the only flight-qualified prop, and a consumable | ReadyMadeRC: "only 3 left" (checked 21:10 PT) | Buy all 3 + 3 from APC direct. 6 on hand covers the bench and about 5 belly landings. The 8x3.8SF needs a CE item before it flies |
| SC-02 | **Depron**: single US importer, no published price or stock | Unconfirmed | Order first (W0). If no ship date within 3 days, escalate to the CEO with an alternative (to be assessed in M1 by Oct 16) |
| SC-03 | **Spar tube**: no source meets R1 as written | DragonPlate found; stock not shown | K-1. Same-lot coupon from each 48 in tube |
| SC-04 | **Suppo 2204/14**: no qualified ≤ 20 g alternate | In stock (21:10 PT) | Buy 2. Any substitute is a CE item (mass and CG) |
| SC-05 | **F405 WING Mini**: one DOA report in the wild | Not re-checked | Power up on arrival (receiving card). A DOA costs about 4 days |
| SC-06 | **Receiver**: CAD models the HotRC F-04A (5 g); the owned part is the F-08A | Not weighed | Weigh on day 1. The SBUS receiver for the HT-8A would remove the encoder |
| SC-07 | **Encoder**: CAD models the JHEMCU SPP-S (3 g, est.); the old cart said "generic" | — | Buy the modelled part, or log the substitute's mass and size before install |
| SC-09 | **CE-02 needs its receiver on the bench before it can be decided** (MBSE conditions b, c): a buy-after-decision would deadlock | — | C2-01 bought in W1 as a bench article; installed only if CE-02 is approved |
| SC-10 | **850 mAh pack (CE-03 option) has no named part** and the tray envelope is unconfirmed | — | E-02 held in W2; SCM lists fitting packs once STF/ME give the envelope |
| SC-08 | Nine shops, nine shipments | — | Track every order in the shared inbox: one line per order with the confirmation number and ETA |

## 4. Build quality rules (`mfg/as_built_mass.csv`, `mfg/templates/ZB-MFG-TPL-001.pdf`)

**Receiving (every part, on arrival):** weigh it on a scale checked against the 100 g weight, compare to `bom.csv`, inspect it, and power-test electronics the same day. A part is **quarantined** (not installed) if it is outside its band. Battery band: **61.3–64.0 g**. A pack 0.8 g light breaks the 5.5% rule, because the battery sits ahead of the CG.

**Weigh-as-you-go:** every line of `as_built_mass.csv` is weighed before it is installed. The sheet carries a **stop-if-over** value per line, set by where the mass sits: **0.5 g** for anything aft of about x = 150 mm (prop, adapter, fins, webs), 1.0 g for lines just aft of the CG, and 2.0 g for lines ahead of it. Weigh the glue bottle before and after every session. Stop and re-run the roll-up when a line trips. No-fly above 250.0 g; review when the margin falls below 10 g.

**CG measurement:** finger balancing cannot resolve 0.3 mm. Use the **single-scale method**: rest the wing LE on a fixed knife edge and the TE region on the scale, both at marked stations. Then CG = L × F_scale / W. With L ≈ 150 mm, a 0.1 g scale resolves about 0.06 mm. A printed fixture and its card come with M5.

**Templates:** print ZB-MFG-TPL-001 at 100%. Reject the print if the check bar measures outside 99.5–100.5 mm. Cut the DR-14 notch to ±0.5 mm and measure it with a caliper. Each fin is 1.0 g, including glue. The generator refuses to draw from anything but hash `479399d88b60`.

## 5. What I own next (ECDs)

| # | Item | ECD |
|---|---|---|
| M1 | DFM review of every `cad/` part, plus **VC-35 construction fallback** (named, with mass and schedule impact) | Fri Oct 16, 12:00 PT |
| M3 | Washout jig drawing + skinning procedure (R-01) | Fri Oct 16, 12:00 PT |
| M4 | Coupon test card: Depron sheet weight, rib print + fit, glue peel, **spar 3-point bend to the K-1 limits**, R5 socket bond sample, hatch pull-off ≥ 9.1 N | Fri Oct 16, 18:00 PT |
| M5 | CG fixture + weigh-in card (single-scale method) | Fri Oct 16, 18:00 PT |
| — | Receiving log opened in the shared inbox; first order confirmations recorded | Thu Oct 15, as the orders go in |

## 6. Reproduce

```
python3 scripts/mass_rollup.py --motor-g 20 --prop-g 7.1 --adapter-g 5.1 --notch-dia-in 8 --battery-fwd-mm 9 --esc-to-mm 95 --fc-fwd-mm 5   # 233.0 g, 130.32 mm, 5.66%
python3 mfg/tools/cg_tolerance.py     # tolerances, trim travel, first-build scenario
python3 mfg/tools/bom_check.py        # cost, frozen-mass match, battery band (exit 0)
python3 mfg/tools/make_templates.py   # 1:1 templates, refuses an unfrozen hash
```

## Appendix A: as-built CG tolerance (output of `cg_tolerance.py`, modelled)

| Unplanned mass at | ΔSM per g (pt) | g to the 5.5% rule | g to the 5.0% floor |
|---|---|---|---|
| prop + adapter (x 200–206) | −0.155 | 1.1 | 4.3 |
| motor (x 192) | −0.132 | 1.3 | 5.1 |
| fins / tip trailing edge (x ≈ 350) | −0.469 | 0.4 | 1.5 |
| wing structure average (x ≈ 128) | +0.004 | never | never |
| FC / receiver tray (x ≈ 90) | +0.086 | never | never |
| nose / battery area (x ≈ 32) | +0.210 | never | never |

Plausible first-build growth (an assumed high-side case, not a prediction): +5 g wiring, +3 g glue, +2 g motor mount, Depron at the top of its density band (+7 g). Result: **AUW 250.0 g, SM 5.77%**. For a first build, **mass is the binding limit, not stability**. That is why every line is weighed before it goes in.

## Sources (checked 2026-10-14, 21:10–21:25 PT)

[APC 8x6SF, ReadyMadeRC](https://www.readymaderc.com/products/details/apc-8x6-sf-prop) · [APC 8x6SF, APC direct](https://www.apcprop.com/product/8x6sf/) · [Suppo 2204/14, Altitude Hobbies](https://www.altitudehobbies.com/products/suppo-2204-14-1400kv-brushless-motor-park-300-equiv) · [Bullet 30A, Pyrodrone](https://pyrodrone.com/products/emx-sc-1774-d-shot-bullet-series-30a-escblheli_s) · [DragonPlate pultruded tubes](https://tools.dragonplate.com/category/pultruded-carbon-fiber-tube) · [ACP pultruded tubing](https://acpcomposites.com/shop/tubes-rods/carbon-fiber-tubes/carbon-fiber-pultruded-tubing) · [Easy Composites 4 mm tube](https://www.easycomposites.co.uk/4mm-pultruded-carbon-fibre-tube) (publishes 28–40 GPa tensile modulus, so it is rejected for R1) · [Depron US importer](https://www.modelairplanenews.com/depron-foam-back-usa/)

## Appendix B: tagup, Thu Oct 15 09:00 PT (done / next / blocked / decisions)

| | Item | Owner | ECD | Ref |
|---|---|---|---|---|
| **Done** | Controlled BOM, mass sheet, CG tolerance, templates; votes cast on #24 (AGREE), #25 (AMEND), #27 (AGREE) | SCM/MFG | 2026-10-14 | PR #26; PR comments 22:15 PT |
| **Next 1** | Orders placed (W0 Depron first, then W1) and logged in the inbox with confirmation numbers and ETAs | CEO places; SCM logs | Thu Oct 15 EOD | `mfg/bom.csv` v1.1 |
| **Next 2** | Coupon card with the K-1 spar bend test and the R5 socket bond sample; CG fixture + weigh-in card | SCM/MFG | Fri Oct 16 18:00 PT | §5 M4, M5 |
| **Next 3** | DFM review + VC-35 construction fallback + washout jig | SCM/MFG | Fri Oct 16 12:00 PT | §5 M1, M3 |
| **Blocked** | Everything printed (R5, ribs, hatch, motor mount) until printer access is known | CEO (AI-07) | Thu Oct 15 | K-4 |
| **Decisions** | K-1 spar qualification; K-2 trim provision (joint with CE-02/CE-03); K-3 VC-01 alert | STF proposes / MBSE approves | before Oct 21 coupon; CDR | §1 |
