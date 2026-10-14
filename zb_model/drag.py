"""Drag buildup — CD = Cd_airfoil(CL) + C_misc + CL^2 / (pi * AR * e).

Section data: MH60 XFoil polar, Ncrit 9, Re ~100k, via airfoiltools.com
(xf-mh60-il-100000). Cd values at CL 0.4/0.5/0.6/0.7 from the program record
(AIRFOIL_TRADE.md §2). Real wing Cd runs ~10-20% above XFoil (roughness, rib
steps); rankings are comparative, absolutes set by flight test.
"""

# MH60 section Cd vs CL (XFoil Ncrit 9, Re 100k — measured polar table values)
_CD_TABLE = [
    (0.40, 0.0155),
    (0.50, 0.0155),
    (0.60, 0.0157),
    (0.70, 0.0163),
]
CLMAX = 1.16  # MH60, gentle trailing-edge stall (CL falls 1.16 -> 1.06)

ASPECT_RATIO = 4.5  # 0.90 m span / 0.20 m chord, rectangular

# Z!B-ESTIMATED: Oswald efficiency 0.78 is a hand estimate, not a repo/VLM
# output (traceability row B2b). Calibrate against flightlab/VLM or flight test.
OSWALD_E = 0.78

# Z!B-ESTIMATED: flat misc-drag term. No reference repo uses a flat 0.012;
# AeroSandbox models misc drag per-component (Hoerner CDA models). This is a
# placeholder — replace with a Hoerner component buildup (TODO).
C_MISC = 0.012


def cd_airfoil(cl: float) -> float:
    """Section Cd by linear interpolation of the MH60 polar table."""
    if cl <= _CD_TABLE[0][0]:
        return _CD_TABLE[0][1]
    for (cl0, cd0), (cl1, cd1) in zip(_CD_TABLE, _CD_TABLE[1:]):
        if cl0 <= cl <= cl1:
            t = (cl - cl0) / (cl1 - cl0)
            return cd0 + t * (cd1 - cd0)
    # Extrapolate gently past 0.7 (cruise band is 0.37-0.5; keep it bounded)
    cl0, cd0 = _CD_TABLE[-2]
    cl1, cd1 = _CD_TABLE[-1]
    return cd1 + (cl - cl1) * (cd1 - cd0) / (cl1 - cl0)


def cd_induced(cl: float) -> float:
    """Induced drag CL^2 / (pi * AR * e)."""
    import math

    return cl**2 / (math.pi * ASPECT_RATIO * OSWALD_E)


def total_cd(cl: float) -> float:
    """Full wing CD buildup (trim drag added separately by the caller)."""
    return cd_airfoil(cl) + C_MISC + cd_induced(cl)
