"""ReflowEconomy general arrangement drawing RFE-DWG-001 (Rev P2): micro-factory floor plan.

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/RFE-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py. The concept sheet in media/ uses RFE-DWG-010. Figures quoted in the
notes come from RFE-CAL-001 (python docs/04-calcs/sizing.py).

The plan is a horizontal section at 1.45 m above the floor seen from above, so walls are
cut and the equipment below shows; hoods, the duct and the fan box above the cut are drawn
dashed. The front elevation below it is a plain view from the front (Y = 0 side) with the
front wall removed.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Compound, ExportSVG, LineType, Unit  # noqa: E402
from drawing import Sheet, INK, MUTED, ACCENT, _t, _viewbox  # noqa: E402
from model import PARAMS as P, ZONES, box, build_parts  # noqa: E402

K = 1 / 50                      # sheet scale
CUT_Z = 1450.0
WORK = ROOT / "cad/drawings/_views"
WORK.mkdir(parents=True, exist_ok=True)
parts = build_parts()


def collect(pred):
    return Compound(children=[s for k, items in parts.items() for n, s, _ in items if pred(k, n)])


def project(shape, name, origin, up, look, hidden=False, dashed=False):
    vis, hid = shape.project_to_viewport(origin, up, look)
    ex = ExportSVG(unit=Unit.MM, line_weight=0.35)
    ex.add_layer("Visible", line_color=0x111827, line_type=LineType.ISO_DASH if dashed else LineType.CONTINUOUS,
                 line_weight=0.25 if dashed else 0.35)
    ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=0.18)
    ex.add_shape(vis, layer="Visible")
    if hidden:
        ex.add_shape(hid, layer="Hidden")
    p = WORK / f"{name}.svg"
    ex.write(str(p))
    return p


# frame of reference for the plan: the full model extents (shell plus the fan box outside)
full = collect(lambda k, n: True)
bb = full.bounding_box()
cx, cy, cz = bb.center().X, bb.center().Y, bb.center().Z
D = 1e5
cutter = box(-1000, P["FL_X"] + 1000, -1000, P["FL_Y"] + 2000, -200, CUT_Z)

# plan: section below the cut, plus overhead items (hoods, duct, fan box) dashed
below = Compound(children=[(s & cutter) for k, items in parts.items() for n, s, _ in items
                           if not (k == 7 and ("Duct" in n or "Fan" in n))])
over = collect(lambda k, n: k == 7)
plan_top = project(below, "plan", (cx, cy, cz + D), (0, 1, 0), (cx, cy, cz))
plan_over = project(over, "plan_over", (cx, cy, cz + D), (0, 1, 0), (cx, cy, cz), dashed=True)
# front elevation without the front wall
no_front = Compound(children=[s for k, items in parts.items() for n, s, _ in items if k not in (0, 13)]
                    + [box(0, P["FL_X"], P["FL_Y"] - P["WALL_T"], P["FL_Y"], 0, P["WALL_H"]),
                       box(0, P["FL_X"], 0, P["FL_Y"], -150, 0)])
elev = project(no_front, "front", (cx, cy - D, cz), (0, 0, 1), (cx, cy, cz))

s = Sheet(project="ReflowEconomy", title="Reference micro-factory, floor plan GA", dwg_no="RFE-DWG-001",
          rev="P2", author="Amish Chadha", date="2026-09-25", scale=K, concept=True,
          material="Layout only; equipment envelopes. See bom/bom.csv and RFE-CAL-001",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (RFE-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Notes: 1.5 kW fan, 38 A demand, shed preferred (RFE-DDR-002)", "2026-09-25", "AC")])

# placement: plan at top left, elevation below, both at 1:50
PX, PY = 20.0, 24.0
pw, ph = bb.size.X * K, bb.size.Y * K


def place(svg, x_of, y_of):
    """Place a projection so model coordinates land exactly: x_of(vx) and y_of(vy) give the sheet corner."""
    vx, vy, vw, vh = _viewbox(Path(svg).read_text())
    s.add_svg(svg, x_of(vx), y_of(vy), vw * K, vh * K, scale=K)


place(plan_top, lambda vx: PX + (cx + vx - bb.min.X) * K, lambda vy: PY + (bb.max.Y - (cy - vy)) * K)
place(plan_over, lambda vx: PX + (cx + vx - bb.min.X) * K, lambda vy: PY + (bb.max.Y - (cy - vy)) * K)
s._layers.append(_t(PX + pw / 2, PY + ph + 11, "PLAN, SECTION AT 1.45 M", 2.8, 600, INK, "middle"))
s._layers.append(_t(PX + pw / 2, PY + ph + 15, "Scale 1:50; dashed: hoods, duct and fan above the cut", 2.2, 400, MUTED, "middle"))

nb = no_front.bounding_box()
EX, EY = PX, PY + ph + 18
place(elev, lambda vx: EX + (cx + vx - bb.min.X) * K, lambda vy: EY + (nb.max.Z - (cz - vy)) * K)
s._layers.append(_t(PX + pw / 2, EY + nb.size.Z * K + 6, "FRONT ELEVATION (FRONT WALL REMOVED)", 2.8, 600, INK, "middle"))
s._layers.append(_t(PX + pw / 2, EY + nb.size.Z * K + 10, "Scale 1:50", 2.2, 400, MUTED, "middle"))


def sx(x):
    return PX + (x - bb.min.X) * K


def sy(y):
    return PY + (bb.max.Y - y) * K


def line(x1, y1, x2, y2, w=0.18, color=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    s._layers.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{w}"{d}/>')


def dim_h(x1, x2, y, text, off=0):
    line(x1, y, x2, y)
    for x in (x1, x2):
        line(x, y - 1.5, x, y + 1.5)
    s._layers.append(_t((x1 + x2) / 2, y - 1.2 + off, text, 2.2, 400, INK, "middle", mono=True))


def dim_v(x, y1, y2, text):
    line(x, y1, x, y2)
    for y in (y1, y2):
        line(x - 1.5, y, x + 1.5, y)
    s._layers.append(f'<text x="{x - 1.2:.2f}" y="{(y1 + y2) / 2:.2f}" font-family="IBM Plex Mono, Menlo, monospace" '
                     f'font-size="2.2" fill="{INK}" text-anchor="middle" transform="rotate(-90 {x - 1.2:.2f} {(y1 + y2) / 2:.2f})">{text}</text>')


# overall dimensions and aisle
dim_h(sx(0), sx(P["FL_X"]), sy(0) + 6, f"{P['FL_X']:.0f}")
dim_v(sx(0) - 5, sy(P["FL_Y"]), sy(0), f"{P['FL_Y']:.0f}")
a0, a1 = P["AISLE_Y0"], P["AISLE_Y0"] + P["AISLE_W"]
dim_v(sx(P["FL_X"]) + 4, sy(a1), sy(a0), f"{P['AISLE_W']:.0f} AISLE")
line(sx(P["WALL_T"]), sy(P["SEAM_Y"]), sx(P["FL_X"] - P["WALL_T"]), sy(P["SEAM_Y"]), 0.18, MUTED, "3 1 0.6 1")
s._layers.append(_t(sx(600), sy(P["SEAM_Y"]) - 0.8, "container seam (container option only)", 1.9, 400, MUTED))
# hot zone boundary
hx0, hx1 = P["HOT_X"]
s._layers.append(f'<rect x="{sx(hx0):.2f}" y="{sy(P["FL_Y"] - P["WALL_T"]):.2f}" width="{(hx1 - hx0) * K:.2f}" '
                 f'height="{(P["FL_Y"] - P["WALL_T"] - a1) * K:.2f}" fill="none" stroke="#B45309" stroke-width="0.35" stroke-dasharray="2 1"/>')
s._layers.append(_t(sx(hx0) + 3, sy(P["FL_Y"] - P["WALL_T"]) + 21, "HOT ZONE", 2.0, 600, "#B45309"))
# doors and flow arrow
s._layers.append(_t(sx(0) + 1.5, sy(1550) + 0.8, "INTAKE DOOR", 1.9, 600, ACCENT))
s._layers.append(_t(sx(0) + 1.5, sy(3000) - 0.8, "EXPORT DOOR", 1.9, 600, ACCENT))
s._layers.append(_t(sx(P["FL_X"]) - 1.5, sy(sum(P["EXIT"]) / 2) - 0.8, "EXIT", 2.0, 600, ACCENT, "end"))
ay = sy(a0 + P["AISLE_W"] / 2)
line(sx(1500), ay, sx(10200), ay, 0.35, ACCENT)
s._layers.append(f'<path d="M{sx(10200):.2f} {ay - 1.4:.2f} L{sx(10200) + 3:.2f} {ay:.2f} L{sx(10200):.2f} {ay + 1.4:.2f} Z" fill="{ACCENT}"/>')
s._layers.append(_t(sx(5600), ay + 3.6, "MATERIAL FLOW", 2.0, 600, ACCENT, "middle"))
# zone balloons (BOM numbers)
seen = set()
for key, (bom, name, x0, x1, y0, y1, h, row) in ZONES.items():
    if key in ("bins",):
        continue
    bxp, byp = sx((x0 + x1) / 2), sy((y0 + y1) / 2)
    s._layers.append(f'<circle cx="{bxp:.2f}" cy="{byp:.2f}" r="2.3" fill="#FFFFFF" stroke="{ACCENT}" stroke-width="0.35"/>')
    s._layers.append(_t(bxp, byp + 0.9, str(bom), 2.4, 600, ACCENT, "middle"))
bxp, byp = sx(8150), sy(P["FL_Y"] + 430)
s._layers.append(f'<circle cx="{bxp:.2f}" cy="{byp:.2f}" r="2.3" fill="#FFFFFF" stroke="{ACCENT}" stroke-width="0.35"/>')
s._layers.append(_t(bxp, byp + 0.9, "7", 2.4, 600, ACCENT, "middle"))

s.add_notes("Zones (numbers match bom/bom.csv)", [
    "1  Intake scale, sorting table, four bins",
    "2  Wash tanks, float-sink, sediment trap",
    "3  Shredder in lined acoustic enclosure",
    "4  Drying rack (7.2 m2 trays) and fan",
    "5  Extruder with barrel enclosure (hood B)",
    "6  Sheet press and cooling press (booth A)",
    "7  Hoods, 250 mm duct, 1.5 kW fan, filter outside",
    "8  Racking: bay 1 products, bay 2 flake",
    "9  Passport and quality desk",
    "10 PPE cabinet, eyewash, extinguishers",
    "11 Electrical board, 230 V 40 A, interlock",
    "12 Export and residue cage by export door",
    "13 Shed preferred, or two 40 ft boxes 12 192 x 4 876",
], x=276, y=34, width=140)
s.add_notes("Key data (RFE-CAL-001)", [
    "59.4 m2 footprint; clear aisle 1.52 m (1.20 m painted)",
    "Hot zone 1.0 m from stock; exits at both ends",
    "100 kg input/shift: 32.3 kg products, 19.3 kg flake",
    "Max demand 8.75 kW (38 A) with heater interlock",
    "Hoods 0.5 m/s face: 0.57 m3/s at about 815 Pa",
    "Shredder LEX 79 dB(A) enclosed (sound power assumed)",
    "Not met: R1, R4, R8. At risk: R6, R12",
    "Container side walls: structural engineer only",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=113, width=140)
s.save(ROOT / "cad/drawings/RFE-DWG-001")
shutil.rmtree(WORK, ignore_errors=True)
print("wrote cad/drawings/RFE-DWG-001.svg, .pdf, .png")
