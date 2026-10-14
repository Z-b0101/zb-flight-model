# Z!B Design Philosophy

**Standing:** CEO-set (established 2026-10-12/13, Gate 1 review). Changes only by CEO directive.
**Owner:** GM (holds and applies; does not amend).

## Preamble

The design philosophy is the decision filter for every trade study, optimization, and build choice in the Z!B program. When two options compete and the numbers are close, the philosophy breaks the tie. It is not decoration — each principle below has already decided a real program question. Every trade study cites the principle it applied; a recommendation that contradicts a principle must say so explicitly and name the CEO authority that permits the exception.

## The eight principles

**1. Regulatory freedom first.**
The 250 g cap is a hard design constraint, not a number to negotiate after the fact (RQ-01). Staying under it keeps the aircraft in the recreational regime — no FAA registration, no Remote ID — which is the foundation the whole program is built on. Program example: the PoC flies 0 g payload (D-05) and budgets 204 g AUW against the cap, preserving ~46 g of margin rather than spending it [VERIFY: Y3k's audit flagged the CAD rollup at 209.0 g vs the 204.3 g budget — CE-01 closure open].

**2. Energy over mass.**
Range comes from stored energy, not from shaving grams past the point of diminishing returns. Once under the regulatory cap with margin, the next kilometer is bought with battery and efficiency, not with structural starvation. Program example: D-05's rationale — the PoC is energy-limited, not weight-limited — and D-11, which cleared the 3S 750 mAh upsize as low-risk specifically because the 46 g margin made it an energy decision, not a mass decision.

**3. Experience over peak numbers.**
A forgiving, quiet, easy-to-fly aircraft beats a faster one that punishes its pilot. Peak range and speed are quoted; what gets flown is handling. Program example: D-03 "Sweet spot G" — ~9% of peak range was deliberately traded for a forgiving stall speed, quieter cruise, one-rib simplicity, and weight margin against weight-creep risk (R-05).

**4. Simplicity as reliability.**
Every part removed is a failure mode removed. The design that wins is the simplest one that meets the requirement. Program example: the A2 optimization loop rejected taper 0.85/0.70 — a +0.02–0.03 km range gain did not justify losing eight-identical-rib construction simplicity; the rectangular wing stands.

**5. Margin is a feature.**
Design margin is not waste; it is the budget that absorbs every estimate that was optimistic. A program with no margin has no room to be wrong. Program example: 46 g of mass margin under the 250 g cap; the 4 mm carbon spar carries a 3.3× bending margin (MATERIALS.md, corrected 2026-10-12); the washout decision carries a priced 5° fallback behind the 6° winner.

**6. Stable from flight one.**
The maiden flight happens in angle mode on a configuration that is already stable, already trims cleanly, and already has benign stall behavior. Heroics in flight test are a design failure. Program example: RQ-23 — ArduPlane angle mode from the maiden; MH60 chosen partly for its gentle stall and −6° elevon trim on our planform (D-06); the A2 loop ran on a 5–8% static-margin basis throughout.

**7. Cheap to crash.**
The prototype is a test article, not a trophy. Its cost must be low enough that losing one teaches instead of bankrupting the program. Program example: the all-in prototype estimate is ~$361 against $10,000 funding (BUDGET.md) — roughly 28 airframes of learning per program; the spares line (e.g., a second 1404 motor on the $34 line, D-17) prices pusher belly landings as expected events, not disasters.

**8. Honest numbers.**
State the number, its basis, its limits, and what would change it — in the same breath. A model result is a model result; a measurement is a measurement. Program example: the 30 km/72 min range claim carries the hotel-power asterisk (1 W hotel → 24.9 km/59 min sensitivity case, disclosed in the deck, not footnoted away); the program holds the L1 honesty line — a validated digital model, not a "twin" — until flight data earns L2.

---
*Filed 2026-10-13. Changes only by CEO directive, logged in DEV_TRACKER.md.*
