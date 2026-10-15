# CE-03 (finding): fixed trailing-edge parts are not in the mass budget

| | |
|---|---|
| Owner | Claude (GM/DE), 2026-10-14 evening |
| Trigger | CE-01 open item 3 (`te_tip` CAD part) and MBSE nit: "confirm it does not move the mass basis" |
| Status | **Finding, raised for MBSE review.** No params or roll-up change; the frozen baseline stands until CE review (rule C) |

## 1. Geometry added (CAD only)

| Part | Region | Volume | Mass at 40 kg/m³ Depron | Centroid x (aft of root LE) |
|---|---|---|---|---|
| `te_centre` (added at the freeze) | Hinge to TE, \|y\| < 112 mm, minus the DR-14 notch | 22.5 cm³ | 0.90 g | 186 mm |
| `te_tip_left` / `te_tip_right` (new) | Hinge to TE, y 405.5–450 mm | 2 × 7.3 cm³ | 2 × 0.29 g | 372 mm |
| **Total** | | **37.1 cm³** | **1.48 g** | — |

Results:
- CAD: `build_all.py` is clean (0 CLASH / 0 TIGHT; `verify_params` and `verify_cad` all pass).
- **CAD-basis mass is unchanged at 223.3 g.** The CAD uses budget masses (airframe 73.6 g), not part volumes. The CAD CG list is also unchanged, by design.

## 2. The finding

- **The airframe budget's "skins 36 g" covers skins + elevons only.** Measured from the CAD: skins 32.4 g + elevons 3.8 g = 36.2 g. The two fixed trailing-edge regions were never modelled, so they are **not in the budget**.
- When built, they add **+1.48 g, all aft of the CG.**
- Frozen roll-up 233.0 g / CG 130.32 mm / SM 5.66% becomes **234.5 g / CG 131.13 mm / SM 5.25%**. That is **below the 5.5% rule** (still above the 5.0% floor).

## 3. Combined with CE-02, and the options

| Case | AUW | CG | SM |
|---|---|---|---|
| Frozen CE-01 | 233.0 g | 130.32 mm | 5.66% |
| + TE parts | 234.5 g | 131.13 mm | **5.25%** |
| + TE parts + CE-02 link (receiver at 45 mm) | 228.3 g | 131.33 mm | **5.16%** |
| + TE + link + **battery 2.5 mm further forward** (`battery_u` ≈ 0.147) | 228.3 g | ≈130.64 mm | 5.50% (on the line; tray fit to check) |
| + TE + link + **850 mAh battery** (+12 g at x ≈ 32 mm, est.) | 240.3 g | 126.37 mm | **7.64%** |

**Reading:**
- The TE parts and the CE-02 link both push the CG aft.
- The **850 mAh battery fixes the static margin with room to spare** and adds about 27% range. AUW is 240.3 g, a 9.7 g margin.
- That makes the joint CE-02 + battery review, already agreed with MBSE, the natural place to close this.

**Fallbacks if the 850 mAh pack does not fit the tray:**
- battery about 2.5 mm further forward, or
- lighter TE construction: a single 3 mm Depron strip instead of solid fill, about half the mass.

## 4. Ask

MBSE to review at the 09:00 sync:
1. Accept the finding that the airframe budget omits the fixed TE.
2. Close it jointly with CE-02 + the 850 mAh battery decision, after the parts are weighed.

Until then the frozen numbers stand, and the external SM is quoted as 5.66% (frozen roll-up) with this finding noted.
