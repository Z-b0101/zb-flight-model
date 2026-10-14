# Calibration buy: parts cart (draft for order by Fri Oct 16)

**Owner:** Claude (GM). **Spend authority:** GM up to $500 (D-23); the CEO places the orders (agents cannot pay).
**Prices checked:** 2026-10-14 on the shop pages linked below. Stock was not always shown; check at checkout.

## One finding first: hold the motor, ESC and propeller (R-07)
The planned **HGLRC Specter 1404 4800KV** is rated by its seller for **2.5–4 inch props, 15.1 A max** ([WREKD](https://wrekd.com/products/hglrc-specter-1404-4800kv-micro-motor)). The design swings a **7-inch** prop. R-07 has questioned this pairing since Oct 12.

A first estimate (assumed prop and motor constants, to be confirmed on the bench) gives:

| Motor class (all on 7040-3, 3S) | Cruise 4 W shaft | Climb 15 W shaft | Full throttle |
|---|---|---|---|
| 1404 4800KV (planned, 10 g) | 4.7 A, motor eff. ~0.60 | 11.5 A, ~0.49 | **~66 A: burns out the motor and the 20 A ESC** |
| 1404 2750KV (10 g) | 2.7 A, ~0.75 | 6.6 A, ~0.66 | ~33 A |
| ~1804 2000KV (~15–18 g) | 2.0 A, ~0.84 | 4.8 A, ~0.77 | ~22 A |
| ~2204 1400KV (~25 g) | 1.4 A, ~0.93 | 3.3 A, ~0.90 | ~14 A |

**What this means:** the planned motor would cruise but cannot be given full throttle without burning out. A lower-KV motor runs cooler and more efficiently, and could *raise* range. It costs 5–15 g of the 38 g weight margin.

**Plan:** I pick the motor/ESC/prop set by **Thu Oct 15 EOD**, with Oubi reviewing the mass and CG effect. The rest of the cart can be ordered now. The power-train items follow by Fri Oct 16, so the bench session (Oct 26–27) is unaffected.

## Cart: order now
| # | Item | Shop | Price (USD) | Note |
|---|---|---|---|---|
| 1 | SpeedyBee F405 WING APP Mini (flight controller) | [RaceDayQuads](https://racedayquads.com/products/speedybee-f405-wing-mini-2-6s-fixed-wing-flight-controller) | 43.49 | One DOA report in the wild: power it on the day it arrives |
| 2 | HGLRC M100-5883 GPS + compass | [RaceDayQuads](https://racedayquads.com/products/hglrc-m100-5883-gps-module-10th-gen) | 20.49 | Same shop as #1 (one shipment) |
| 3 | EMAX ES9051 servo ×2 | [ReadyMadeRC](https://www.readymaderc.com/products/details/emax-es9051-4-3g-digital-mini-servo) | 9.98 | In stock, $4.99 each |
| 4 | GNB 3S 650 mAh 80C XT30 LiPo ×1 | [Pyrodrone](https://pyrodrone.com/collections/3s-batteries/products/gaoneng-gnb-3s-11-1v-650mah-80c-lipo-battery-xt30) | 15.99 | In stock, 62 g, 20×28×64 mm (fits the hatch) |
| 5 | ToolkitRC WM150 watt meter | [Pyrodrone](https://pyrodrone.com/products/toolkitrc-wm150-advanced-watt-power-meter) | 51.99 | In stock; 10 mA precision, needed to measure the ~1 W electronics draw. Same shop as #4 |
| 6 | Depron 3 mm sheets (4) | [RcDepron.com](https://www.modelairplanenews.com/depron-foam-back-usa/) (US importer) | ~18 (est.) | Price not published; confirm at order |
| 7 | 4 mm OD carbon tube, 1 m (×2, one spare) | US hobby shop or Amazon | ~14 (est.) | Must be 4.0 mm OD to fit the 4.2 mm rib slot |
| 8 | PWM→PPM encoder | Amazon | ~4 (est.) | Only if the radio receiver has PWM outputs (R-09) |
| 9 | PLA filament, foam-safe CA, hot glue, hinge tape, pushrods | Amazon / local | ~28 (est.) | Commodity |
| 10 | 0.1 g kitchen scale | Amazon | ~12 (est.) | Skip if on hand |
| | **Subtotal, order now** | | **~$218** | Plus shipping from ~4 shops (est. $25–35) |

## Cart: order by Fri Oct 16 (after the R-07 decision)
| # | Item | Price (USD) | Note |
|---|---|---|---|
| 11 | Motor (choice from the table above) | ~17–25 | The planned Specter 1404 4800KV is also sold out at WREKD |
| 12 | 20 A ESC | ~12 | The EMAX Bullet 20A is **out of stock** at [GetFPV](https://www.getfpv.com/emax-d-shot-bullet-series-20a-esc-blheli-s.html); the substitute is chosen with the motor |
| 13 | Gemfan Flash 7040 3-blade, 4-pack | 5.49 | [GetFPV](https://www.getfpv.com/propellers/mini-quad-propellers/gemfan-flash-7040-durable-3-blade-propeller-set-of-4-clear.html), in stock, 7.9 g, 5 mm hub; confirm the hub fits the chosen motor shaft |
| | **Subtotal** | **~$35–43** | |

**Expected total: about $255–260 plus shipping (~$290 all-in), inside the $500 authority.**

## CEO answers (2026-10-14, 10:43 PT)
1. **No 0.1 g scale on hand:** #10 stays in the cart.
2. **RC transmitter and receiver on hand:** the CEO is sending a photo. Once the model is identified, #8 (the PWM→PPM encoder) is kept or dropped, depending on whether the receiver outputs PWM or a serial protocol (R-09).
