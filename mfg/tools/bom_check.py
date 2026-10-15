"""BOM consistency check (SCM/MFG seat). Reads mfg/bom.csv and checks it against the CE-01 freeze.

1. Order cost, by wave and in total, against the GM parts authority ($500, D-23).
2. Installed LRU masses vs the frozen LRU set used in the CE-01 roll-up (must match line by line).
3. Battery acceptance band: lightest pack that keeps SM >= 5.5 % (pack sits ahead of the CG).
Usage: python3 mfg/tools/bom_check.py   (exit code = number of failed checks)
"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import cg_tolerance as T

FROZEN_LRU_G = {"P-01": 20.0, "P-02": 7.1, "P-04": 5.1, "P-05": 3.5, "A-01": 23.0, "A-02": 7.7,
                "A-03": 4.3, "A-04": 5.0, "A-05": 3.0, "E-01": 62.0}       # CE-01 freeze / build_systems.py
AUTHORITY = 500.0
SHIPPING_EST = (35.0, 60.0)                                                   # est. for 8-9 shops

rows = list(csv.DictReader(open(os.path.join(REPO, "mfg", "bom.csv"))))
fails = 0
cost = {}
for r in rows:
    q = float(r["qty_order"] or 0); u = float(r["unit_usd"] or 0)
    cost[r["order_wave"]] = cost.get(r["order_wave"], 0.0) + q * u
tot = sum(cost.values())
print("Order cost by wave (USD, ex shipping):", {k: round(v, 2) for k, v in sorted(cost.items())})
print(f"Total {tot:.2f}; with shipping {tot + SHIPPING_EST[0]:.0f}-{tot + SHIPPING_EST[1]:.0f} vs ${AUTHORITY:.0f} authority")
if tot + SHIPPING_EST[1] > AUTHORITY:
    print("FAIL: cart may exceed the GM parts authority"); fails += 1

print("\nInstalled LRU masses vs CE-01 freeze:")
inst = 0.0
for r in rows:
    if r["id"] in FROZEN_LRU_G:
        m = float(r["unit_mass_g"]) * float(r["qty_installed"])
        exp = FROZEN_LRU_G[r["id"]] * float(r["qty_installed"])
        ok = abs(m - exp) < 0.05
        fails += 0 if ok else 1
        inst += m
        print(f"  {r['id']} {r['item']:<22} {m:6.1f} g  frozen {exp:6.1f} g  {'OK' if ok else 'MISMATCH'}")
print(f"  LRUs installed: {inst:.1f} g; airframe + structure + wiring by difference: {233.0 - inst:.1f} g")

np_mm, m0, cg0 = T.frozen()
xb = 32.0                                   # battery centre, x = battery_u 0.160 x 200 mm
dm = 0.0
while (np_mm - T.add(m0, cg0, dm, xb)[1]) / 200 >= 0.055 and dm > -20: dm -= 0.1
print(f"\nBattery: SM falls below 5.5% if the pack is {abs(dm):.1f} g lighter than 62.0 g "
      f"(accept >= {62.0 + dm + 0.1:.1f} g); mass cap allows up to {62.0 + 250 - m0:.1f} g")
sys.exit(fails)
