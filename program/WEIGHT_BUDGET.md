# Weight Budget — Sub-250g 0.9m Hybrid UAV
Cap: 250g total AUW (regulatory). All weights in grams. Real part weights where verified, modeled where noted.

## Current rollup (2026-10-12)
| Subsystem | Weight | Basis |
|---|---|---|
| Airframe | 73.6 | modeled: skins 36 + ribs 12 + spar 7.9 (4mm tube, corrected 2026-10-12) + misc 17.7 |
| Battery 3S 650mAh | 62 | verified spec (GNB) |
| Motor 1404 | 10 | verified spec |
| ESC 20A | 3.5 | verified spec (EMAX Bullet) |
| FC stack | 23 | verified (oga.global teardown) |
| GPS/compass | 7.7 | verified spec (M100-5883) |
| Servos ×2 | 8.6 | verified spec (ES9051) |
| RX + encoder | 8 | estimate |
| Prop 7×4 | 7.9 | verified spec (Flash 7040) |
| Payload (PoC) | 0 | 30g requirement applies to product/family instances, not the PoC |
| **Total** | **204.3** | **margin 46g** |

## Key insight
At this scale the design is **energy-limited, not weight-limited**: saving 9g of structure buys ~1% range; spending 10g on battery buys ~15% range. The cap makes it a **reallocation problem** — harvest low-value grams, spend them on high-value grams. Reliability also has a price in grams, and the cheapest reliability is free (fewer connectors, threadlock, jig discipline).

## Harvest list (low-value grams → recover)
| # | Action | Saves | Reliability effect |
|---|---|---|---|
| H-1 | Wiring diet: direct-solder servos/ESC, shorten all leads | ~3g | **Positive** — fewer intermittent connectors |
| H-2 | Glue/tray discipline: weigh glue, lightened equipment tray | ~4g | Neutral (verified by coupon test) |
| H-3 | FC stack audit: verify 23g; decide WiFi board stays or goes post-setup | ~2g | Neutral if removed post-config |
| H-4 | Spar 5mm → 4mm | ~2.5g | **Negative** — halves bending margin AND weakens the assembly backbone. **Rejected.** |

## Spend list (high-value grams ← invest)
| # | Action | Costs | Buys |
|---|---|---|---|
| S-1 | Battery 650 → 750mAh (~72g) | +10g | **+15% range (29.5→34km), +11% endurance (66→73min)** — best range-per-gram trade available |
| S-2 | GPS mast (compass isolation) | +2g | Directly retires R-11 (EMI-induced compass errors) |
| S-3 | Threadlock + proper servo horns | ~0g | Crash/maintenance reliability, free |
| S-4 | Conformal coat on FC | ~1g | Moisture reliability — optional, decide after maiden environment known |

## Weight requirements (allocated targets) — PoC, 0g payload
| Subsystem | Current | Target | Status |
|---|---|---|---|
| Airframe | 72 | 68 | via H-2, verified by build weigh-in |
| Battery | 62 | 72 | via S-1, low-risk at PoC margin |
| Motor/ESC/prop | 21.4 | 21 | as-is |
| FC stack | 23 | 21 | via H-3 |
| GPS | 7.7 | 10 | via S-2 |
| Servos/RX/encoder | 16.6 | 14 | via H-1 |
| Payload (PoC) | 0 | 0 | 30g requirement applies to family instances |
| **Total** | **203** | **206** | **margin 47g / 44g** |

## End states (PoC, 0g payload)
- **Bank it:** do H-1..H-3 only → ~195g, 55g margin, ~31km / 74min.
- **Spend it (recommended):** 750mAh battery + GPS mast, full harvest → ~207g, 43g margin, **~35km / 83min**. With the PoC's 46g starting margin, the ≥20g gate for the battery upsize is already cleared — no weigh-in contingency needed, though the Phase 1 weigh-in still validates the model.

## Phased decision
With 0g PoC payload the margin is 46g, so S-1 (750mAh) is low-risk from the start. Still run the Phase 1 weigh-in to validate the airframe model — the scale arbitrates, as always.

## Verification gates
1. **Coupon test:** weigh rib + skin sample + glue joint → validates airframe model.
2. **Phase 1 weigh-in:** bare airframe + power train on the scale before avionics.
3. **Pre-maiden weigh-in:** full AUW (PoC: 0g payload); no-fly if >250g, review if margin <10g.

*Last updated: 2026-10-12*
