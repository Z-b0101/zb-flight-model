# Inherited-Baseline Audit — Day 1–2
**Date:** 2026-10-13  
**Author:** [CE — Y3k]  
**Decision served:** Is the current configuration coherent enough to proceed into CE-01/CE-02 closure work?  
**Sources consumed:** DEV_TRACKER.md, WEIGHT_BUDGET.md, cad/cg_report.json, cad/clash_report.json, cad/params.json, ITERATION_LOG.md, RISK_REGISTER.md, TDR_RECORD.md (plus orientation set).

---

## 1. Confirmed

| Item | Evidence | Notes |
|------|----------|-------|
| Geometry winner | ITERATION_LOG Cycle 4 | 6° linear washout, 25° sweep, taper 1.0, rectangular, 8 ribs, MH60 locked as A2 winner at SM6%: 32.40 km / 77.1 min, δe = −3.55° |
| params.json schema | cad/params.json | Already carries explicit `design` + `derived` sections (MBSE format present). Geometry parameters match winner. |
| Battery hatch | cad/clash_report.json + params.json | Hatch geometry present (hatch_rect, tray, lid). All hatch-fit and battery clearances report OK. |
| Clash status (current) | clash_report.json | n_clash = 0, n_tight = 0. All LRU-skin, LRU-spar, hatch-fit, wire-hatch, wire-rib verdicts OK. |
| Regulatory mass cap | RQ-01 / WEIGHT_BUDGET | 250 g hard. Current designs sit 41–46 g under. |
| PoC payload | RQ-06 | 0 g locked. ≥30 g applies only to family instances. |
| Airfoil | D-06 / RISK R-16 | MH60 selected; PW75 retired. |
| L1 honesty line | Onboarding + TDR | Twin remains L1 validated model. L2 requires measured data. |

---

## 2. Contradictory (must be closed before freeze)

| Item | Narrative / Older | Current CAD / Loop | Delta / Finding |
|------|-------------------|--------------------|-----------------|
| AUW | WEIGHT_BUDGET 204.3 g (margin 46 g) | cg_report.json 209.0 g (margin 41 g) | +4.7 g. Explained primarily by hatch_tray 1.0 g + hatch_lid 0.7 g + wiring 3.0 g that the narrative rollup did not carry at the same fidelity. Not a hard conflict with 250 g, but the two numbers must be reconciled into one controlled rollup. |
| CG position | Onboarding cited 129.9 mm; RISK R-15 cites 120.3 mm | cg_report.json 128.5 mm aft root LE | Target remains 116.0 mm. Current delta +12.5 mm aft. Static margin therefore sits near the lower edge of the 5–8% band. |
| CG datum | Optimization loop: x_cg = 83.0 mm @ SM6% (x_ac = 95.0 mm) | CAD: 128.5 mm aft root LE | Different coordinate conventions. Confirmed by GM 2026-10-13. Must not be mixed. Reconciliation is CE-02 scope. |
| R-17 status | RISK_REGISTER still lists “OPEN — battery vs skins clash” | clash_report.json shows battery clearance OK and hatch-fit OK | Register is stale relative to current CAD. Risk can be retired or re-scoped once hatch structural continuity and retention are verified. |

---

## 3. Unknown / provisional

| Item | Basis tag | Impact |
|------|-----------|--------|
| Absolute range / endurance numbers | Model outputs (L1) | Trade-ranking only until propulsion, hotel-load, and battery discharge are measured. |
| 1 W hotel load | Assumption | Affects endurance predictions; HOTEL_LOAD_PLAN exists but no measured data. |
| 3S reference discharge curve | Reference, not measured | Required for credible energy truth before release decisions. |
| Propulsion pairing (1404 + 7040-3) | Provisional | R-07 remains open; wattmeter + thrust data required. |
| Wiring mass 3.0 g | ESTIMATED | Acceptable for now; must be tagged and eventually measured. |
| Hatch mass 1.7 g total | ESTIMATED | Acceptable; verify on first printed tray/lid. |
| Actual Depron + glue mass | Modeled | Coupon test is the retirement path (R-01 / R-03 / airframe model). |

---

## 4. Blocked / open actions required for freeze readiness

1. **CE-01 Mass/CG reconciliation**  
   - Produce one authoritative mass rollup that absorbs hatch + wiring.  
   - Decide CG recovery method (component relocation preferred; ballast last resort).  
   - Confirm static-margin band after relocation (target remain 5–8%).

2. **CE-02 Coordinate convention + digital thread**  
   - Document the single aircraft coordinate system.  
   - Map optimization 83.0 mm datum onto CAD root-LE datum (or vice-versa).  
   - Confirm all consumers (CAD, JSBSim, mission model, interactive twin) read the same params source.  
   - Note: params.json already has design/derived structure — divergence check still required.

3. **Risk register hygiene**  
   - Update R-17 status against current clash_report (hatch appears closed).  
   - Confirm R-15 CG wording matches the latest 128.5 mm figure.

4. **Physical evidence path** (not blocking digital freeze, but required before prototype authorization)  
   - Coupon / fairing test for 6° washout (R-01 gate).  
   - Measured component masses, hotel load, propulsion bench data.

---

## 5. Executive finding

The inherited baseline is **technically coherent enough to enter detailed closure work**. The largest previous show-stopper (battery–skin clash) has already been addressed in the current CAD by the hatch geometry; the clash report is clean. Remaining contradictions are quantitative (mass rollup fidelity, CG datum, CG offset) and are exactly the scope of CE-01 and CE-02.

**Recommendation to GM:**  
Proceed with CE-01 (mass + CG closure) and CE-02 (coordinate convention + single-source thread) in parallel. No architecture change required at this time. Gate 1 freeze remains contingent on successful reconciliation of the items in Section 2 and a clean divergence check.

**Next action from this seat:**  
Begin CE-01 line-by-line mass reconciliation and CG recovery options analysis. Will file the CE-01 evidence packet when the four-pass review is complete.

---

*Audit produced from controlled artifacts delivered 2026-10-13 11:29 PDT. No numbers invented.*
