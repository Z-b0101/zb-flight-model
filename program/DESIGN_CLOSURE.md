# Z!B Phase A · Workstream WS-20 — Design Closure Record

**Date:** 2026-10-13 · **Owner:** GM (subagent) · **System of record:** DEV_TRACKER.md
**Starting geometry:** A2 winner — 6° linear washout, 25° quarter-chord sweep,
rectangular (taper 1.0), MH60, 8 ribs (`aero_opt/cad_loop/cyc4_wash6/params.json`).
All CAD regenerated from this geometry (the pre-existing `cad/params.json` was
still the 2°/20° baseline — first regen brought it to the winner).

---

## ITEM 1 — Battery hatch H1 (R-17) — CLOSED

### Starting point (honest)
Regenerating the CAD at the winner geometry gave:
- **Clash 1 (known):** battery-vs-skins, 14.1 mm interference (20 mm pack in a
  ~20 mm wing at u=22%, chordwise).
- **Clash 2 (found 2026-10-13, this work):** battery-vs-**spar** — the 4 mm spar
  tube passes straight through the battery box (spar apex (10, 0, 3.6) is
  10 mm inside the pack). The old vertex-sampling clash check had a false
  negative: a tube through a box interior has no close *vertices*.
  Fixed by replacing it with an analytic segment-vs-box test (§ below).

### Options considered
| ID | Concept | Verdict |
|---|---|---|
| H1 | Bottom aperture + printed tray + Depron lid (fwd tape hinge, 2 aft snap-latches) | **ADOPTED** |
| H2 | Top hatch (pack protrudes above wing) | Rejected: suction-side aero, GPS-mast conflict |
| H3 | Blister fairings top+bottom, pack stays | Rejected: drag, complexity, still clashes spar |
| H4 | External chin pod (no skin cut) | Rejected: belly-landing strikes the pod first = battery impact |
| H5 | Spanwise side-load through rib bay | Rejected: cuts rib structure |

### 4-round criticism of H1
- **R1 — Real need?** Yes: two independent interferences (skin 14.1 mm,
  spar tube through box). No placement of the 64 mm pack at u=0.22 chordwise
  clears the spar; the pack *must* move.
- **R2 — Steelman H4 (chin pod):** no skin cut → trivially watertight; easiest
  battery swap. Counter: PoC belly-lands; a chin pod is the first thing to hit.
  H1 keeps the pack inside the OML (1.1 mm protrusion + shallow lid pan).
- **R3 — Break H1:** (i) aperture weakens center-section skin → tray is bonded
  to ribs + skin frame and becomes a structural member (documented);
  (ii) lid departs in flight → positive latch + hinge + pre-flight check item;
  (iii) swap wear on Depron → wear surfaces are printed (tray/latch), not foam;
  (iv) water ingress → tray flange + lid close the aperture (gasket line is a
  shop detail).
- **R4 — Reconcile:** hatch mass (1.7 g) is in the CG rollup; clash check is
  hatch-aware and reads ZERO; w2 re-routed (bend ≥4 mm, no skin breach);
  aperture + battery placement are derived params (Item 3).

### Final design (all numbers from `cad/params.json` design+derived)
- **Battery:** GNB 3S 650 mAh, **spanwise** (64 mm along y) at **u=0.205**
  (x=41.0 mm aft of root LE), zc=−4.15 mm (2 mm top-clearance rule,
  sweep-aware: box corners sample shifted sections on the swept wing).
  Spar clearance 3.0 mm; LE clearance 27 mm; top-corner clearance 2.0 mm.
- **Aperture** (bottom skin, real hole in the mesh): u 0.120–0.290
  (x −26…+8), y ±36. Skin is one (u,y) grid with aperture quads skipped and
  explicit wall caps — watertight **with** the hole (edge-manifold check).
- **Tray:** 4 printed walls (1.2 mm, volumetric corner overlaps), bonded to
  skin frame; **lid:** Depron 3 mm panel (44×82); retention: fwd fiber-tape
  hinge + 2 aft printed snap-latches (positive, field-swappable).
- **Wiring:** w2 (FC→XT30) re-routed to the pack's +y end; min bend 6.0 mm;
  no undocumented skin breaches.

### Result
`clash_report.json`: **0 CLASH, 0 TIGHT** (was 1 CLASH + 1 undetected).
All 10 mesh groups watertight. `verify_cad.py` + `verify_systems.py`: all PASS.

---

## ITEM 2 — CG resolution (R-15) — DECIDED

### The starting number was stale
The task cited CG 120.3 mm (SM 5.9%) — that was the **20°-sweep** geometry.
Regenerating at the **winner (25° sweep)** moves the airframe CG aft
(190.6 mm; swept area centroid + elevons) → **CG = 128.5 mm** (209.0 g,
margin 41.0 g). The 120.3/5.9% framing is retired.

### The neutral-point reconciliation (defect filed, not buried)
- **Derived:** VLM neutral point for the winner = **144.98 mm** aft of root LE
  (x_ac=94.98 mm aft of root QC, `sim_SM6.json`; invariant under x_ref;
  mesh-converged loop). → SM = (144.98−128.5)/200 = **8.26%**.
- **Stipulated:** the 116 mm target implies NP=132 (JSBSim alpha: −0.08 slope
  "by construction", CG "tuned… by construction" — pre-A2, never derived for
  this geometry). No model produces 132; nothing physical (prop is
  stabilizing → moves NP *aft*, wrong sign) bridges the 13 mm gap.
- **Standing:** the derived VLM number is the authority. The 116 mm target is
  **retired as stale** (it was set pre-sweep-change). Filed as a
  reconciliation defect for CDR adjudication; R-15 bench-balance remains the
  physical backstop.

### Ballast vs layout vs accept — with numbers (12-angle analysis converged)
| Option | Math | Verdict |
|---|---|---|
| (a) Ballast to 116 | Δ=−12.5 mm → **25 g** at the nose (12% mass penalty) | **REJECTED** — absurd at winner geometry; would also push VLM-SM to 14.5% (δe≈−7.3°, near the 8° authority limit) |
| (b) Battery fwd to 116 | Needs −42 mm → pack past the LE | **REJECTED** — geometrically impossible |
| (b2) RX/encoder fwd | −2.8 mm for new clash risks in the thin nose | **REJECTED** — poor trade |
| (c) Accept | SM **8.26%** (VLM): in/edge of 5–8% band, δe=−4.60° (3.4° authority margin), tip margin OK | **ADOPTED** |

The 12 angles (provenance, physics sign, mission-sim consistency, risk
asymmetry, bench backstop, VLM error magnitude, NP invariance check,
116-unachievability, ballast absurdity, aeroelastic bound, flight-test
calibration path, band semantics) converge ≥11/12: **trust the derived NP,
accept the as-designed CG, no ballast.**

### Honest performance at the as-designed CG
Mission re-run (same `mission.evaluate`, winner wing):
- Loop claim @SM6% (CG assumed 133): **32.40 km / 77.1 min**, δe=−3.55°
- **As-designed @SM8.26% (CG 128.5): 31.86 km / 75.8 min**, δe=−4.60°, feasible
- Delta: **−0.54 km (−1.7%)** — the cost of the real layout vs the sim's
  CG assumption. Still +1.86 km over the 30 km trade-study baseline.

---

## ITEM 3 — params.json refactor (MBSE §4.2) — DONE

`cad/params.json` is now the split single source of truth (same path):
- **`design`** (29 keys, hand-edited): wing (span/chord/taper/sweep/washout/
  twist_stations/airfoil), spar, ribs + lightening holes, skin, elevons,
  **battery** (u/y/orientation/mass/dims — CG-critical, hatch-coupled),
  **hatch** (margins, top clearance). Updated to the winner: sweep 25°,
  washout 6°.
- **`derived`** (recomputed, never hand-edited): rib_stations_y,
  spar_centre_uv, holes_uvd, hatch_rect, battery_zc_mm, battery_box.
- **`meta`**: format tag + `aero_basis` (VLM NP 144.98 mm with source and
  geometry).

**Generator updates:** `parametric.py` (`load_params` reads split *or* flat;
`compute_derived` is the single source used by builders and verifier);
`build_cad.py` writes the split record; `build_systems.py` consumes derived
hatch/battery; `verify_cad.py` reads the split (and its 20°-era hardcoded
checks were fixed); `verify_systems.py` updated (209.0 g, VLM SM readout).

**Verify step:** new `cad/verify_params.py`, run at the end of every
`build_all.py` (fails the build on divergence). Current result:
**all 6 checks PASS** — derived == compute_derived(design); aero basis
matches design geometry (this check would have caught the 116/132 staleness).

**Backward compatibility (aero_opt loop):** the `--params` variant pattern is
unchanged — variant files stay **flat overrides** over DEFAULTS
(`params_in.json` needs no edits). `load_params` was synced into
`aero_opt/cad_loop/parametric.py` and `aero_opt/cad_interface.py` so both
also accept the split record. Documented in `cad/README.md`.

---

## Risk / tracker deltas for the GM
- **R-17 (battery clash):** → **CLOSED**. Hatch H1 designed; clash 0/0;
  plus fixed the clash checker's false negative (analytic spar-vs-box).
- **R-15 (CG):** CG 128.5 mm → SM 8.26% (VLM). In/edge of band; no ballast.
  116 mm target retired as stale (defect filed for CDR).
- **New defect:** VLM NP (144.98) vs program-stipulated NP (132) — 13 mm
  unreconciled; VLM trusted, JSBSim alpha needs re-derivation at the winner
  geometry (blocks Twin v2 fidelity claim, not the PoC).
- LRU table migration into design params: documented follow-up (mechanical).

## Files
- `~/workspace/uav-sub250g/cad/params.json` — split single truth
- `~/workspace/uav-sub250g/cad/verify_params.py` — new
- `~/workspace/uav-sub250g/DESIGN_CLOSURE.md` — this file
- CAD: `~/workspace/uav-sub250g/cad/` (`clash_report.json`: 0/0;
  `cg_report.json`: 128.5 mm / 209.0 g)
