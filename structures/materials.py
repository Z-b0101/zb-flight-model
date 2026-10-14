"""Material property sets for the Z!B structural analysis.

Every value carries its basis. Nothing here is measured on our parts yet: the
coupon test (RQ-04 / VC-06 / VC-27) replaces these with measured values.
Three spar grades bracket the published spread for pultruded carbon tube.
"""

# Pultruded carbon tube (spar). E, G in Pa; allowables in Pa (flexural, as the spar works in bending).
SPAR_GRADES = {
    "low": dict(E=30e9, G=3.0e9, sigma_allow=250e6, rho=1400.0,
                basis="EasyComposites TDS (pultrusions): tensile modulus 28-40 GPa, flexural strength 250-400 MPa; low end used"),
    "nominal": dict(E=120e9, G=4.0e9, sigma_allow=600e6, rho=1600.0,
                    basis="Program assumption since 2026-10-12 (MATERIALS.md #5): 120 GPa, 600 MPa with knockdown"),
    "premium": dict(E=131e9, G=4.5e9, sigma_allow=1000e6, rho=1550.0,
                    basis="Rock West 47316 minimum properties: flexural modulus 131 GPa, flexural strength 1.83 GPa; allowable taken as 1.0 GPa (~0.55x) for a tube vs a rod"),
}

# Depron 3 mm (extruded polystyrene sheet). Literature band; ASSUMED until coupon.
DEPRON = dict(
    E=12e6,             # Pa, XPS sheet in-plane modulus, band 8-20 MPa (MATERIALS.md #7 uses 10-15)
    G=5e6,              # Pa, in-plane shear modulus, band 3-8 MPa (assumed)
    sigma_t=0.40e6,     # Pa, tensile strength, band 0.3-0.5 MPa (assumed; Foamular 250 flexural min 75 psi = 0.52 MPa)
    sigma_c=0.17e6,     # Pa, compressive strength at yield (Foamular 250 min 25 psi, ASTM D1621)
    tau=0.20e6,         # Pa, shear strength (assumed)
    nu=0.3,
    rho=36.0,           # kg/m3, Depron 33-40 (MATERIALS.md #1)
    t=0.003,            # m
    basis="XPS literature band (Owens Corning FOAMULAR 250 data sheet minimums; MATERIALS.md); ASSUMED until coupon",
)

# Printed PLA (ribs, joiner sleeve, hatch frame).
PLA = dict(
    E=3.0e9,
    sigma_xy=45e6,      # Pa, in-layer tensile (FDM, along filament), typical 40-55 MPa
    sigma_z=15e6,       # Pa, interlayer (Z) tensile, typical 10-25 MPa
    rho=1240.0,
    basis="Typical FDM PLA literature values; print orientation governs (in-layer vs interlayer); ASSUMED until coupon",
)

# Ultimate factor of safety on limit loads (proposed; MBSE to ratify).
FOS = 1.5
