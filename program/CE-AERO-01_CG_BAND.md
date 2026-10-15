# CE-AERO-01: CG band from the frozen NP, and up-elevon throw 12° → 14° (proposed)

| | |
|---|---|
| Raised by | AERO seat (`[AERO — Claude]`), 2026-10-14 |
| Status | **PROPOSED**, for MBSE review (Oubi). CE number to be assigned by MBSE |
| Baseline | `cad/params.json` @ hash `479399d88b60` (main @86936d4). Nothing in this item edits `params.json` |
| Evidence | `scripts/cg_band.py`, `tests/test_cg_band.py` (6 guards), output `reports/cg_band.json` |
| Fidelity (STF 5 checks) | Traceable ✓ · Labelled ✓ · Reproducible ✓ (35/35 tests) · **Verified: partly** · **Bounded: no**. Risk brief below |

## Risk brief (read first)

**PROBLEM.** The CG window the aircraft can fly in is narrow. The aft limit is set by stability (static margin 5.5%), and the forward limit by how much up-elevon the trim at low speed uses. With the frozen 12° up-throw, the window is **3.3 mm wide** (127.3–130.6 mm) at the low end of the cited flap-effectiveness band, and **0.9 mm** at a pessimistic value. The record's CG target (VC-30 and the roadmap's Nov 5 weigh-in, "128.5 mm") comes from the superseded 8.3% basis and gives no forward limit.

**GAP.** *Bounded* fails: the forward limit depends on `flap_knockdown`, which `twin/perf.py` itself marks **CRITICAL, UNCALIBRATED** (0.7–0.8 assumed). The bench can measure throw but not effectiveness; only flight trim-vs-speed closes it. *Verified* is partial: the throw criterion (2/3 of up-throw used at 1.3 Vs) is an AERO engineering-judgement value, PROVISIONAL until MBSE approves it, and servo hinge-moment margin at 14° is unmeasured.

**RISK.** A CG that is too far forward (for example, the 850 mAh battery option, about SM 7.6% on the PR #22 branch) could leave too little up-elevon to flare or pull up at landing speed. That would mean a hard landing or a mushing stall-in near the pilot, in the FHA phase #7 (and #1 at launch). Likelihood: moderate if the CG is set by "more SM is safer" alone. Severity: airframe damage, low injury risk (FHA). Touches safety floor: **SM ≥ 5.5%** on the aft side only. The forward limit is not a constitutional floor today; this item proposes adding it to VC-30.

**DEPENDENCIES.**
- MBSE approval of the forward-limit criterion (Oubi). ECD: Oct 15, 12:00 PT review.
- Servo arm and horn geometry for 14° up (ME seat / STF linkage card, DR-02 open item). ECD Oct 16.
- Bench throw and hinge-moment check at 14° under VC-29 (Oct 26–27, already scheduled).
- Flight trim-vs-speed on flights 1–2 to calibrate `flap_knockdown`.

**OPTIONS.**
- (a) Keep 12°, accept the narrow band, set the CG mid-window (about 129 mm, SM ≈ 6.3%). Cost $0, 0 days. Window 3.3 mm at knockdown 0.7; nearly zero at 0.6.
- (b) **Raise up-throw to 14° by linkage geometry** (servo arm hole or horn height; no new parts, no mass change) and set the CG band by the table below. Cost about $0, under half a day of linkage work, verified inside the existing VC-29 bench session. Window grows to 6.1 mm at knockdown 0.7 and 3.3 mm at 0.6.
- (c) Wait for flight calibration of `flap_knockdown`. That cannot happen before the maiden, so it is not a real option for the first flight.

**RECOMMENDATION: (b).** It is the only option that gives a usable CG window across the whole flap-effectiveness uncertainty, at no mass or dollar cost. It also centres the maiden CG with ±1.6 mm of build tolerance on both sides, even in the stress case.

## Results (all modelled; `python scripts/cg_band.py`)

Frozen record: NP 141.64 mm, MAC 200 mm, CG 130.32 mm, SM 5.66%, Vs 4.54 m/s.

| Limit | CG (mm) | SM | Basis |
|---|---|---|---|
| Aft, design floor | **130.64** | 5.50% | Constitution Art V.6 |
| Aft, absolute floor | 131.64 | 5.00% | Constitution Art V.6 |

Forward limit: trim at 1.3 Vs uses at most 2/3 of the up-throw (PROVISIONAL criterion).

| flap_knockdown | Up 12° (frozen) | Up 14° (proposed) | Up 15° |
|---|---|---|---|
| 0.80 | 124.92 mm (SM 8.36%) | 121.71 (9.96%) | 120.10 (10.77%) |
| 0.75 | 126.12 (7.76%) | 123.11 (9.26%) | 121.61 (10.01%) |
| 0.70 | **127.33 (7.16%)**, window 3.3 mm | **124.52 (8.56%)**, window 6.1 mm | 123.11 (9.26%) |
| 0.60 (stress) | **129.73 (5.95%)**, window 0.9 mm | **127.33 (7.16%)**, window 3.3 mm | 126.12 (7.76%) |

Trim elevon at 1.3 Vs at the frozen CG: −5.8° to −7.7° across knockdown 0.8–0.6.

Note: trim CL at 1.3 Vs is fixed by CLmax, so the forward limit in mm does not depend on all-up mass. A heavier battery moves the CG; it does not move the limit.

## Proposed record changes (for MBSE to approve; none made here)

1. **VC-30** acceptance: replace "CG within the agreed SM band (design 128.5 mm, R-15)" with "as-built CG between the forward limit (CE-AERO-01 table, at the up-throw measured under VC-29) and the aft limit 130.64 mm (SM 5.5%)".
2. **Roadmap Nov 5 line**: replace "CG to 128.5 mm" with the CE-AERO-01 band. Proposed maiden target, if (b) is adopted: **CG 129.0 mm (SM ≈ 6.3%), ±1.5 mm**. That is the centre of the stress-case window (127.33–130.64 mm at knockdown 0.6, 14° up), so it stays inside the band across the whole knockdown range.
3. **DR-02**: `elevon_up_deg` 12 → 14 through a CE item, once the linkage card shows the geometry and VC-29 shows hinge-moment margin. `elevon_down_deg` unchanged at 8°.
4. **Joint CE-02 / CE-03 / 850 mAh decision** (STF, MBSE): check the resulting CG against this band before adopting. With 12° up, the 850 mAh option's CG (about SM 7.6%, PR #22 branch, not on main) is ahead of the forward limit for knockdown below about 0.74 (the limit is SM 7.76% at 0.75 and 7.16% at 0.70). At the cited 0.70 it fails; at 0.75 it passes with 0.24 mm to spare.

## Correction (Law 1)

Earlier tonight I recommended flying the maiden at about SM 7–8% without checking elevon authority. With the frozen 12° up-throw that is unsafe at the low end of the knockdown band: SM 7.16% is the forward limit at 0.7, and 5.95% at 0.6. I withdraw it. The right target is the centre of the CG window, not the highest SM: about SM 6.3% (CG 129.0 mm) with option (b). Higher SM is not automatically safer on a flying wing with limited elevon authority.
