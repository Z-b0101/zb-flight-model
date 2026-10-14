# CE item: DR-01 tip fins and DR-02 elevon throw (closure package)

| | |
|---|---|
| Raised by | Claude (GM/DE), 2026-10-14, from ZB-ER-001 design review |
| MBSE position | DR-01 fins **recommended**, DR-02 **concurred** (Oubi, 13:27 and 13:57 PT); closure package delegated to GM for implementation |
| Branch | `ce/dr01-dr02` (from `twin/v0.1`). **Proposed** baseline hash `752301fb9dc8`; the controlled baseline stays `7be168427b4d` until MBSE merges at CE-01 |
| Decision | CE-01 freeze, Fri Oct 16 (DR-01 and DR-02 decided together: coupled through CG) |

## What changes in `cad/params.json` (design block)

| Key | Value | Meaning |
|---|---|---|
| `fin_height` | 120.0 mm | Upright tip fin, above the wing only (no ground contact on belly landings) |
| `fin_chord` | 60.0 mm | |
| `fin_x_frac` | 0.70 | Fin leading edge at 70% of the tip chord (fin spans 70–100%) |
| `fin_t` | 3.0 mm | 3 mm Depron |
| `fin_mass_g` | 1.0 g each | Including glue (estimate; weigh at build) |
| `elevon_up_deg` | 12.0° | DR-02: minimum up-elevon (TE up) via servo arm / horn geometry |
| `elevon_down_deg` | 8.0° | Unchanged |

`DESIGN_KEYS` in `cad/parametric.py` is extended to match (schema change, MBSE-owned, made at MBSE's delegation). `verify_params.py`: all checks pass. Washout stays locked at 6°.

**Not in params.json, by design:** Cn-beta. It is derived from the fin geometry in code (`twin/lateral.py`) so it cannot drift from the geometry the way the old typed value did.

## DR-01: yaw-stability build-up (`twin/lateral.py`)

Cn-beta = wing alone (USAF DATCOM sweep / CL² term) + two fins (Helmbold low-AR lift slope × volume). CG 130.9 mm (fins on), NP 142.6 mm.

| CL | Wing alone (/deg) | Fins (/deg) | Total (/deg) | Target |
|---|---|---|---|---|
| 0.17 (cruise, 10.5 m/s) | +0.000017 | +0.00124 | **+0.00126** | ≥ 0.001 |
| 0.37 (A2 cruise) | +0.000082 | +0.00124 | **+0.00132** | ≥ 0.001 |
| 0.60 (slow flight) | +0.00022 | +0.00124 | **+0.00146** | ≥ 0.001 |

Fin numbers: area 72 cm² each, geometric AR 2.0, effective AR 3.1 (endplate factor 1.55, **assumed**), lift slope 3.42 /rad, arm 0.234 m (fin quarter-chord 364.8 mm aft of root LE).

**Orientation matters (found in the build-up):** the same 60 × 120 mm fin laid long (60 high × 120 chord) gives effective AR 0.8 and only about +0.0006 /deg total. The upright orientation is required. This is pinned by `tests/test_lateral.py::test_fin_orientation_matters`.

The JSBSim model now takes Cn-beta, the fin side-force (CY-beta −0.0048 /deg), the fin contribution to Cl-beta (−0.0003 /deg) and yaw damping (Cnr −0.15 → −0.187) from this derivation. The typed-in +0.0012 /deg and CY-beta −0.004 /deg are retired.

## Mass, CG and the five checks (re-issued; MBSE O-01 gate (b))

The twin now runs on the single planning mass basis of 211.9 g. Fins add 2 g at about 380 mm (`twin/perf.py::mass_props`).

| Check | Design record | Twin, 211.9 g, no fins | Twin, 213.9 g, fins on | Tolerance |
|---|---|---|---|---|
| Neutral point | 145.0 mm | 142.6 mm | 142.6 mm | ±5 mm |
| Static margin | 8.3% | 7.03% | **5.85%** | ±2.5 pt |
| Trim at A2 cruise (7.09 m/s) | −4.60° | −4.70° | −4.08° | ±1° |
| Range, no electronics load | 31.9 km | 30.1 km | 30.3 km | ±10% |
| Endurance, no electronics load | 75.8 min | 71.0 min | 71.2 min | ±10% |

Other effects with fins on: stall speed 4.25 → 4.27 m/s; trim at 1.3 Vs −7.2° → −6.1° (the aft CG relieves DR-02 by about 1.1°); CG 128.5 → 130.85 mm (+2.35 mm, matching MBSE's figure).

### Static-margin acceptance (for the CE-01 freeze record; no silent use of the tolerance band)
With fins, SM = 5.85%. That is inside the 5–8% design band, but 2.45 points below the design record of 8.3%, using 0.05 of the ±2.5-point check tolerance.

**Proposed record line:** "CE-01 accepts SM 5.85% (fins on, 213.9 g, CG 130.85 mm) as the design static margin. The 8.3% record is superseded. The five-check SM row is re-baselined to 5.85% ± 2.5 pt. The R-07 motor pick must not move the CG aft of 131.6 mm (SM 5.5%) without a new acceptance."

This is MBSE's decision. The line above is a proposal.

## DR-02: elevon throw

- `elevon_up_deg` 12, `elevon_down_deg` 8, set by linkage geometry (servo arm length / horn height ratio), not by changing the servo or the elevon.
- Twin: the JSBSim elevon map is now asymmetric (−1 → −12°, +1 → +8°). Flight checks and the circuit are re-trimmed. The launch-to-landing circuit still flies: 55.5 s, touchdown 5.8 m/s, 0.5 m/s sink.
- **VC-29 (updated criterion):** measured throw ≥ 12° up and ≥ 8° down each side, symmetric within 1°, with servo hinge-moment margin shown (no stall or buzz at full throw under hand load). Inclinometer at the bench before any flight. Closed only by measurement, not by the design value.

## Yaw verification criteria (L1 → L2)

| Level | Criterion | Evidence |
|---|---|---|
| L1 (model) | Cn-beta ≥ +0.001 /deg at CL 0.17, 0.37 and 0.60 | `tests/test_lateral.py` (automated) |
| L2 (flight) | Yaw damping: after a roll doublet at cruise in FBWA, sideslip and yaw-rate oscillation decays to half amplitude within 2 cycles. Spiral: wings-level hands-off in manual for 5 s gives bank change < 15° | Flight log (.bin) from flights 2–5; Claude reduces |
| L2 (flight) | Turn coordination: sideslip in a 30° bank turn is not visibly persistent | Same logs |

## Open (placeholders)
- **[DATA PENDING]** CAD/STL geometry for the fins (ZB-107) and the linkage card. The CAD toolchain (cadquery) is not in this session; generated at the CAD update after adoption. ECD Oct 16. Owner Claude.
- **[DATA PENDING]** Measured fin mass (1.0 g each estimated). Weigh at build step B-11. ECD Nov 4.
- Endplate factor 1.55 and sidewash factor 1.0 are assumed (see `twin/lateral.py::ASSUMED`). Flight closes them.
