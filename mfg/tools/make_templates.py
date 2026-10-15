"""1:1 printable cutting templates from cad/params.json (SCM/MFG seat, 2026-10-14).

Sheet 1: DR-14 prop notch + elevon root cut lines on the centre trailing edge (planform, top view).
Sheet 2: DR-01 tip fins (x2) with the mounting station on the tip chord.
Every dimension is read from params.json; the design hash is printed on each sheet.
Print at 100 % ("actual size"), then measure the 100 mm check bar before cutting.
Usage: python3 mfg/tools/make_templates.py  -> mfg/templates/ZB-MFG-TPL-001.pdf
"""
import hashlib, json, math, os, sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "scripts"))
from divergence_check import design_hash          # the program's own hash convention
P = json.load(open(os.path.join(REPO, "cad", "params.json")))
D = P["design"]
HASH = design_hash(D)
FROZEN = "479399d88b60"                           # CE-01 freeze (D-31)
if HASH != FROZEN and "--allow-unfrozen" not in sys.argv:
    sys.exit(f"REFUSED: params.json hash {HASH} is not the frozen baseline {FROZEN}. Templates are only issued from the controlled design.")

C, SW = D["chord"], math.tan(math.radians(D["sweep_deg"]))
XN, HY = D["prop_notch_x"], D["prop_notch_halfspan"]
R_PROP = D["prop_dia_in"] * 25.4 / 2
Y0E, HINGE = D["elevon_y0"], D["hinge_x_frac"] * C
xle = lambda y: abs(y) * SW
xte = lambda y: xle(y) + C

OUT = os.path.join(REPO, "mfg", "templates"); os.makedirs(OUT, exist_ok=True)
PW, PH = landscape(letter)

def header(cv, title, lines):
    cv.setFont("Helvetica-Bold", 11); cv.drawString(12 * mm, PH - 12 * mm, title)
    cv.setFont("Helvetica", 7.5)
    for i, s in enumerate(lines):
        cv.drawString(12 * mm, PH - (17 + 3.6 * i) * mm, s)
    cv.setFont("Helvetica", 6.5)
    cv.drawRightString(PW - 12 * mm, 8 * mm, f"ZB-MFG-TPL-001  |  design hash {HASH}  |  source cad/params.json  |  SCM/MFG (Claude)  |  MODELLED geometry: verify against the as-built wing")

def check_bar(cv, x0, y0):
    cv.setLineWidth(0.6); cv.line(x0, y0, x0 + 100 * mm, y0)
    for k in range(0, 101, 10):
        h = 3 if k % 50 else 5
        cv.line(x0 + k * mm, y0, x0 + k * mm, y0 + h * mm)
    cv.setFont("Helvetica-Bold", 7); cv.drawString(x0, y0 - 4 * mm, "CHECK BAR = 100.0 mm. Reject the print if it measures outside 99.5-100.5 mm.")

def sheet_notch(cv):
    header(cv, "Sheet 1 of 2: DR-14 prop notch and elevon root cuts (centre trailing edge, TOP VIEW, 1:1)", [
        f"Cut the skins and fixed trailing edge aft of x = {XN:.1f} mm (from the root LE) for |y| <= {HY:.1f} mm. Tolerance on the side edges: +/-0.5 mm (prop clearance is exactly 5.0 mm, VC-R07-7).",
        f"Elevon root at |y| = {Y0E:.1f} mm, hinge line at x = LE + {HINGE:.0f} mm. Web of foam between notch edge and elevon root: {Y0E - HY:.1f} mm (hold +/-1 mm).",
        "Locate: lay the sheet on the bottom skin, align the two printed trailing-edge lines with the real trailing edge and the centreline with the root rib. Tape, then cut on the solid line.",
        "Dashed = +/-0.5 mm band. Grey dotted = prop tip path (r = 101.6 mm) projected on the wing. Measure the cut with a caliper and log it on the receiving / build card.",
    ])
    # page mapping: wing y -> page x (centred), wing x (aft) -> page y (down)
    ox, oy = PW / 2, PH - 48 * mm
    xr0 = XN - 15.0                                   # top of drawing (wing x)
    X = lambda y: ox + y * mm
    Y = lambda x: oy - (x - xr0) * mm
    ymax = 125.0
    cv.setLineWidth(0.4)
    cv.setDash(2, 2); cv.line(X(0), Y(xr0), X(0), Y(xte(ymax) + 2)); cv.setDash()
    cv.setFont("Helvetica", 6.5); cv.drawString(X(1), Y(xr0) - 3 * mm, "centreline y = 0 (root rib)")
    # trailing edge
    cv.setLineWidth(0.9)
    cv.line(X(-ymax), Y(xte(ymax)), X(0), Y(xte(0))); cv.line(X(0), Y(xte(0)), X(ymax), Y(xte(ymax)))
    cv.setFont("Helvetica", 6.5); cv.drawString(X(ymax - 30), Y(xte(ymax)) - 4 * mm, "wing trailing edge (25 deg sweep)")
    # x reference ticks every 10 mm along the centreline
    for xv in range(int(xr0 // 10 * 10 + 10), int(xte(ymax)) + 1, 10):
        cv.line(X(-2), Y(xv), X(2), Y(xv)); cv.drawString(X(-12), Y(xv) - 0.8 * mm, f"x{xv}")
    # notch cut outline (solid, heavy)
    cv.setLineWidth(1.4)
    pts = [(-HY, xte(HY)), (-HY, XN), (HY, XN), (HY, xte(HY))]
    for (y1, x1), (y2, x2) in zip(pts, pts[1:]):
        cv.line(X(y1), Y(x1), X(y2), Y(x2))
    # tolerance band on the side edges and the cut line
    cv.setLineWidth(0.3); cv.setDash(1.5, 1.5)
    for s in (-1, 1):
        for d in (-0.5, 0.5):
            yy = s * HY + d
            cv.line(X(yy), Y(XN), X(yy), Y(xte(yy)))
    cv.setDash()
    # hatching inside the notch (material removed)
    cv.setLineWidth(0.2)
    k = -HY + 4
    while k < HY:                                   # vertical hatch: from the cut line to the trailing edge
        if abs(k) > 3:
            cv.line(X(k), Y(XN), X(k), Y(xte(k)))
        k += 4
    cv.setFont("Helvetica-Bold", 7)
    for s in (-1, 1):
        cv.setFillColorRGB(1, 1, 1); cv.rect(X(s * 62) - 15 * mm, Y(XN + 16) - 1.2 * mm, 30 * mm, 4 * mm, stroke=0, fill=1)
        cv.setFillColorRGB(0, 0, 0); cv.drawCentredString(X(s * 62), Y(XN + 16), "REMOVE")
    cv.setFont("Helvetica", 6.5)
    cv.drawString(X(8), Y(XN - 9), "KEEP: wing forward of the cut line and outboard of the notch edges")
    # elevon root cuts and hinge lines
    cv.setLineWidth(0.9)
    for s in (-1, 1):
        y = s * Y0E
        cv.line(X(y), Y(xle(y) + HINGE), X(y), Y(xte(y)))
        cv.setDash(3, 1.5); cv.line(X(y), Y(xle(y) + HINGE), X(s * ymax), Y(xle(ymax) + HINGE)); cv.setDash()
    cv.setFont("Helvetica", 6.5)
    cv.drawString(X(Y0E + 1), Y(xle(Y0E) + HINGE) + 1.5 * mm, f"elevon root y = {Y0E:.1f}")
    cv.drawString(X(Y0E + 6), Y(xle(Y0E) + HINGE + 6), "hinge line (dashed)")
    cv.drawRightString(X(-HY - 1.5), Y(XN + 30), f"notch edge y = -{HY:.1f}")
    cv.drawString(X(HY + 1.5), Y(XN + 30), f"{Y0E - HY:.1f} mm")
    # prop tip path
    cv.setLineWidth(0.3); cv.setStrokeGray(0.55); cv.setDash(0.5, 1.2)
    for s in (-1, 1):
        cv.line(X(s * R_PROP), Y(XN), X(s * R_PROP), Y(xte(R_PROP)))
    cv.setDash(); cv.setStrokeGray(0)
    check_bar(cv, 14 * mm, 18 * mm)
    # dimension table
    cv.setFont("Helvetica", 7)
    tab = [("Notch x (from root LE)", f"{XN:.1f} mm"), ("Notch half-span", f"{HY:.1f} mm  (+/-0.5)"),
           ("Notch depth at centreline", f"{xte(0) - XN:.1f} mm"), ("Notch depth at the side edge", f"{xte(HY) - XN:.1f} mm"),
           ("Prop radius / clearance", f"{R_PROP:.1f} mm / {HY - R_PROP:.1f} mm"), ("Elevon root y", f"{Y0E:.1f} mm")]
    for i, (k, v) in enumerate(tab):
        cv.drawString(PW - 82 * mm, 34 * mm - i * 3.6 * mm, k); cv.drawRightString(PW - 14 * mm, 34 * mm - i * 3.6 * mm, v)
    cv.showPage()

def sheet_fins(cv):
    H, Cf, xf, t = D["fin_height"], D["fin_chord"], D["fin_x_frac"], D["fin_t"]
    header(cv, "Sheet 2 of 2: DR-01 tip fins, cut 2 (1:1)", [
        f"Fin: {Cf:.0f} mm chord x {H:.0f} mm high, {t:.0f} mm Depron, upright. Planform is the rectangle in params.json; corners are not specified, so cut them square.",
        f"Mount: fin leading edge at {xf * 100:.0f}% of the tip chord = {xf * C:.0f} mm aft of the tip LE; fin trailing edge then sits at {xf * C + Cf:.0f} mm, flush with the tip TE.",
        f"Mass target {D['fin_mass_g']:.1f} g per fin including glue. Weigh each fin: the design tolerates only about 0.4 g of unplanned mass at the tips (CG_TOLERANCE).",
        "Mark the inboard face of each fin before gluing so both are bonded the same way round.",
    ])
    cv.setLineWidth(1.2)
    for i, x0 in enumerate((40 * mm, 150 * mm)):
        y0 = 40 * mm
        cv.rect(x0, y0, Cf * mm, H * mm)
        cv.setFont("Helvetica-Bold", 8); cv.drawCentredString(x0 + Cf / 2 * mm, y0 + H / 2 * mm, f"FIN {'L' if i == 0 else 'R'}")
        cv.setFont("Helvetica", 6.5)
        cv.drawString(x0, y0 - 4 * mm, "LE (forward)" if i == 0 else "TE (aft)")
        cv.drawRightString(x0 + Cf * mm, y0 - 4 * mm, "TE (aft)" if i == 0 else "LE (forward)")
        cv.drawString(x0 + 1 * mm, y0 + 1.5 * mm, "root edge: glue to the tip")
    # tip chord locator strip (1:1, 200 mm)
    x0, y0 = 40 * mm, 172 * mm
    cv.setLineWidth(0.8); cv.line(x0, y0, x0 + C * mm, y0)
    for k in range(0, int(C) + 1, 10):
        cv.line(x0 + k * mm, y0, x0 + k * mm, y0 + (4 if k % 50 == 0 else 2) * mm)
    cv.setLineWidth(1.6); cv.line(x0 + xf * C * mm, y0 - 3 * mm, x0 + (xf * C + Cf) * mm, y0 - 3 * mm)
    cv.setFont("Helvetica", 6.5)
    cv.drawString(x0, y0 + 5.5 * mm, "Tip chord locator (lay along the wing tip, 0 = tip LE):  heavy bar = fin footprint")
    cv.drawString(x0 - 2 * mm, y0 - 7 * mm, "LE 0"); cv.drawRightString(x0 + C * mm + 2 * mm, y0 - 7 * mm, f"TE {C:.0f}")
    check_bar(cv, 150 * mm, 18 * mm)
    cv.showPage()

path = os.path.join(OUT, "ZB-MFG-TPL-001.pdf")
cv = canvas.Canvas(path, pagesize=(PW, PH)); cv.setTitle("Z!B cutting templates ZB-MFG-TPL-001")
sheet_notch(cv); sheet_fins(cv); cv.save()
print("wrote", os.path.relpath(path, REPO), "hash", HASH)
