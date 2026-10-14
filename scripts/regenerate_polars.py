#!/usr/bin/env python3
"""Regenerate MH60 polar tables reproducibly.

TODO: needs an XFoil binary on PATH.
  - Input:  zb_model/data/polars/mh60.dat (Selig format; add per README)
  - Runs:   XFoil, Ncrit 9 (matches the airfoiltools xf-mh60-il-100000
            provenance used in the trade study), Re 100k sweep
  - Output: zb_model/data/polars/mh60_polar.csv + pins the Cd/CL table in
            zb_model/drag.py

Until this runs, drag.py carries the extracted table values directly
(source: airfoiltools.com full-table extraction, AIRFOIL_TRADE.md §2).
"""

import shutil
import subprocess
import sys
from pathlib import Path

POLAR_DIR = Path(__file__).resolve().parent.parent / "zb_model" / "data" / "polars"
N_CRIT = 9
REYNOLDS = 100_000


def main() -> int:
    xfoil = shutil.which("xfoil")
    if xfoil is None:
        print("TODO: install an XFoil binary and put it on PATH, then re-run.",
              file=sys.stderr)
        return 1
    dat = POLAR_DIR / "mh60.dat"
    if not dat.exists():
        print(f"TODO: add {dat} (see zb_model/data/polars/README.md).",
              file=sys.stderr)
        return 1
    # XFoil batch script: load, set Ncrit, Re sweep, dump polar.
    # Kept as a scaffold — validate the polar against the extracted table
    # in drag.py before trusting regenerated values.
    print(f"XFoil found at {xfoil}; batch polar generation not yet wired.")
    print("Validate regenerated polars against drag._CD_TABLE before use.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
