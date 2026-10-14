# Budget — Sub-250g 0.9m Hybrid UAV ("Sweet Spot")
Baseline: 0.9m span, 0.20m chord, rectangular Depron wing + printed details. Prices verified 2026-10-12 unless marked (est).

## Airframe (hybrid) — $53
| Item | Cost |
|---|---|
| Depron 3mm sheets ×4 (spares included) | $18 |
| Carbon tube 5mm × 1m (spar) | $7 |
| PLA/PETG filament (ribs, mount, horns — partial spool) | $8 |
| Foam-safe CA + hot glue sticks | $9 |
| Hinge tape (Blenderm or similar) | $5 |
| Micro pushrods/linkages | $6 |

## Propulsion — $53 (review-informed picks)
| Item | Pick | Reviews | Cost |
|---|---|---|---|
| Motor, 1404 4800KV (3S) | HGLRC Specter 1404 4800KV | Mixed 3.5/5 — burnout reports are all hard-throttle 4S quad use; our 5W cruise loafs. Carry a spare: pushers eat motors on belly landings | $17 ×2 = $34 |
| ESC, 20A | EMAX D-SHOT Bullet 20A (3.5g) | 4.65/5, 20 reviews; quality MOSFETs, runs cool | $10 |
| Props 7×4 3-blade ×2 | Gemfan Flash 7040-3 | 4.98/5, 341 reviews, "very efficient" | $9 |

## Avionics — $85 (review-informed picks)
| Item | Pick | Reviews | Cost |
|---|---|---|---|
| Flight controller | SpeedyBee F405 WING MINI | 5/5 (11 reviews) + ArduPilot forum endorsement ("work 100%, quality 100%"); one DOA report in the wild — buy from a reputable shop | $47 |
| GPS + compass | HGLRC M100-5883 (M10, 7.7g) | Glowing long-term review: 25–30s cold fix, 18–24 sats, "ideal for fixed-wing navigation"; M10 recommended by INAV docs | $18 |
| PWM→PPM encoder (HotRC F-08A → FC) | generic | commodity part | $4 |
| Micro servos ×2 | EMAX ES9051 (4.3g each) | 4.9/5, 227 reviews — "the reference sub-250g servo" | $16 |

## Power — $58
| Item | Pick | Reviews | Cost |
|---|---|---|---|
| 2× 3S 650mAh LiPo (~62g each, XT30) | GNB 650 3S 80C | established brand, 62g verified spec | $30 |
| Balance charger (if none on hand — unconfirmed) | | | $28 |

## Payload — $50 placeholder (type TBD: camera / FPV / sensors)

## One-time tools — $29
| Item | Cost |
|---|---|
| Wattmeter (bench power-train verification) | $17 |
| Kitchen scale 0.1g (weigh-as-you-go — unconfirmed) | $12 |

## Total
| | |
|---|---|
| Subtotal | $328 |
| Contingency 10% | $33 |
| **Project total** | **~$361** |
| Budget cap | $10,000 (funding raised 2026-10-13 — project Z!B) |
| **Headroom** | **~$9,639** |

## Phased spending (don't buy everything day one)
- **Phase 1 — airframe + bench test: ~$170.** Airframe materials, motor, ESC, props, batteries, charger, wattmeter. Proves the power train and the build before any autonomy money is spent.
- **Phase 2 — autonomy: ~$80.** FC, GPS, encoder, servos. Only after the airframe exists.
- **Phase 3 — payload: ~$50.** When the type is decided.
- Tools (~$29) whenever needed.

## Notes
- LRU picks are review-informed (2026-10-12), not cheapest-listing: every major unit carries its review basis in the tables above.
- **Weight reconciliation with real parts:** battery 62g (was 55), FC stack 23g (was 11), motor 10g (was 12), ESC 3.5g (was 8), servos 8.6g (was 8), GPS 7.7g (was 9), prop 7.9g (was 6). Net +13.7g → **AUW ≈ 233g, margin 17g** (was 31g modeled). Weigh-as-you-go is now mandatory, not advisory — R-05 tightened.
- Battery weight check 2026-10-12: real 3S 650mAh packs run 57–70g (GNB 62g, Zeee 57g, CNHL 70g) vs the 55g estimate in the weight model. Re-weigh on arrival.
- Rebuild cost after a crash: ~$10 in Depron + glue. The airframe is intentionally the cheapest part to lose.
- Biggest cost uncertainty is the payload itself — a micro FPV setup and a sensor package live in very different price bands.
- If charger and scale are already on hand: subtract ~$40.

*Last updated: 2026-10-12*
