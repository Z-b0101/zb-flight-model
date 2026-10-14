# Z!B proof-of-concept: where we stand (2026-10-14, 06:00 PT)

## The aircraft
A 0.90 m flying wing that weighs about 212 g, under the 250 g line. Below that line, recreational flight needs no FAA registration and no Remote ID. It is built from foam skins, a carbon spar and 3D-printed ribs, and flies an off-the-shelf ArduPlane autopilot.

## Does it work?
Not yet in the air: no hardware has been built. In simulation, yes. Tonight the team stood up a **digital twin**: a flight simulator generated directly from the controlled design file. It flies the complete mission and reproduces the design team's baseline numbers within tolerance on all five checks.

| What investors usually ask | Answer today | How solid |
|---|---|---|
| Is it under 250 g? | 212 g planned (incl. new spar joint), **38 g margin** | Modeled; confirmed only at weigh-in |
| Is it stable? | Yes: 7% static margin; pitch and roll disturbances die out in 6-DOF simulation | Modeled, cross-checked (roll terms still estimates) |
| How far / how long? | **About 26 km, or about 60 min** on one 650 mAh pack | Modeled; depends on two untested numbers |
| What's the upside? | Battery upsize to 750 mAh (+10 g) is the best trade on record, about +15% range | Modeled |

## What's proven vs what isn't
- **Checked by two independent calculations (design loop and twin), not yet by hardware:** geometry, stability, trim and range on a like-for-like basis. Spar strength is 2.8× margin at 4 g on literature material values that the coupon test will confirm.
- **Not yet proven, because they need hardware:** real airframe weight (coupon test), motor/propeller efficiency and electronics power draw (bench test), and flying qualities (first flight). The electronics power draw is the biggest swing: it moves range between about 26 and 31 km.
- **Found and being fixed:** the swept wing's spar has no designed centre joint. A first sizing says a printed sleeve of about 2–3 g solves it, well inside the margin.

## What's next, with dates
| Date | Milestone |
|---|---|
| Oct 16 | Close the remaining weight/CG and drag reconciliations (CE-01/CE-02) |
| Oct 17 | Airframe recommendation, investor-visible; ships with stated caveats rather than slipping |
| Next | Coupon test, then avionics bench test, then Gate 4 prototype authorization (no major hardware spend before it) |

## How we work
One controlled design file; every number in the report traces to it, or is labeled as an assumption with its status. The twin's two calculation errors found tonight were caught by our own verification and disclosed, not hidden.
