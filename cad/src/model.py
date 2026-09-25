"""ReflowEconomy reference micro-factory: parametric floor layout (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL of the layout assembly and the building shell into cad/step and cad/stl.

Massing-plus level of detail: correct zone footprints, aisle, doors, hood and duct
positions, and main equipment envelopes. Not fabrication detail. Units mm, Z up, floor at
Z = 0. X runs along the line from the intake end (X = 0) to the product end; Y runs from the
front wall (Y = 0) to the back wall; material flows in +X.

Layout (decided by Amish, 2026-09-25, RFE-DDR-001 items 1, 2 and 5): a plastics line on two
40 ft container footprints side by side with the adjoining side walls removed, one 1.2 m
central aisle along the container seam, a front row (intake, washing, shredding, drying,
flake store, passport desk) and a back row (export cage, safety station, electrical board,
hot zone, product racking). The sheet press, its cooling press and the extruder sit under
enclosing hoods in one hot zone.

Every zone is an axis-aligned envelope in ZONES so that RFE-CAL-001
(docs/04-calcs/sizing.py) can check the aisle width, the hot zone clearance and the
floor area from the same numbers that draw the model.
"""
from pathlib import Path

from build123d import Box, Compound, Cylinder, Pos, Rot, export_step, export_stl

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 13 building shell: two 40 ft ISO containers side by side (external 12 192 x 2 438 each)
    "FL_X": 12192.0, "FL_Y": 4876.0,
    "WALL_T": 80.0,             # corrugated wall, modelled solid
    "WALL_H": 2590.0,           # external height of a standard container; roof not modelled
    "SEAM_Y": 2438.0,           # container seam, side walls removed along it
    # circulation
    "AISLE_Y0": 1700.0, "AISLE_W": 1200.0,   # central aisle along X
    "DOOR_A": (160.0, 2280.0),  # container A end doors at X = 0 (intake)
    "DOOR_B": (2598.0, 4716.0), # container B end doors at X = 0 (export and residue collection)
    "EXIT": (1300.0, 2200.0),   # personnel exit cut in the far end wall of container A
    "DOOR_H": 2200.0,
    # hot zone boundary (painted line) and required clearance to stock
    "HOT_X": (5400.0, 9750.0),
    "HOT_CLEAR": 1000.0,
    # fume extraction: 250 mm main duct, fan and filter outside the back wall
    "DUCT_D": 250.0, "DUCT_Z": 2150.0, "DUCT_X": 8150.0,
    # hood openings (m), used by RFE-CAL-001
    "HOOD_A_OPEN": (1.2, 0.6),  # press booth sliding sash
    "HOOD_B_OPEN": (0.8, 0.4),  # extruder barrel enclosure, nozzle and mould end
}
P = PARAMS

# Zone envelopes: key -> (BOM line, name, x0, x1, y0, y1, height, row)
ZONES = {
    "scale":   (1, "Platform scale 1 x 1 m", 300, 1300, 400, 1400, 100, "front"),
    "table":   (1, "Sorting table 2.0 x 0.9 m", 1500, 3500, 150, 1050, 900, "front"),
    "bins":    (1, "Four material bins", 1500, 3480, 1080, 1680, 800, "front"),
    "wash":    (2, "Washing tanks and sediment trap", 3800, 5500, 300, 1600, 900, "front"),
    "shred":   (3, "Shredder in acoustic enclosure", 5800, 7400, 150, 1550, 2100, "front"),
    "dry":     (4, "Drying rack and fan", 7700, 8900, 200, 1200, 1800, "front"),
    "store2":  (8, "Racking bay 2 (flake bags)", 9100, 10450, 150, 1150, 2000, "front"),
    "desk":    (9, "Passport and quality desk", 10800, 11900, 150, 850, 900, "front"),
    "cage":    (12, "Export and residue cage", 250, 2350, 3300, 4700, 1800, "back"),
    "ppe":     (10, "Safety and PPE station", 2500, 3750, 4346, 4796, 1900, "back"),
    "board":   (11, "Electrical board", 3900, 4600, 4596, 4796, 2000, "back"),
    "extr":    (5, "Extruder in barrel enclosure", 5600, 7100, 3900, 4600, 1550, "back"),
    "press":   (6, "Sheet press and cooling press in booth", 7250, 9700, 3200, 4796, 2300, "back"),
    "store1":  (8, "Racking bay 1 (products)", 10750, 12100, 3796, 4796, 2000, "back"),
}


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def zbox(key, z0=0.0, h=None, inset=0.0):
    _, _, x0, x1, y0, y1, zh, _ = ZONES[key]
    return box(x0 + inset, x1 - inset, y0 + inset, y1 - inset, z0, z0 + (zh if h is None else h))


def shell(p=PARAMS):
    """13 Building shell: slab, side walls and end walls with door openings. Roof omitted."""
    fx, fy, t, h = p["FL_X"], p["FL_Y"], p["WALL_T"], p["WALL_H"]
    slab = box(0, fx, 0, fy, -150, 0)
    front = box(0, fx, 0, t, 0, h)
    back = box(0, fx, fy - t, fy, 0, h)
    intake_end = box(0, t, 0, fy, 0, h)
    for y0, y1 in (p["DOOR_A"], p["DOOR_B"]):
        intake_end = intake_end - box(-1, t + 1, y0, y1, 0, p["DOOR_H"])
    far_end = box(fx - t, fx, 0, fy, 0, h) - box(fx - t - 1, fx + 1, *p["EXIT"], 0, 2000)
    # duct penetration in the back wall
    far_back = back - (Pos(p["DUCT_X"], fy - t / 2, p["DUCT_Z"]) * Rot(90, 0, 0) * Cylinder(p["DUCT_D"] / 2 + 10, t + 2))
    return slab + front + far_back + intake_end + far_end


def floor_markings(p=PARAMS):
    """Painted aisle edges and hot zone boundary (10 mm high strips)."""
    x0, x1 = p["HOT_X"]
    a0, a1 = p["AISLE_Y0"], p["AISLE_Y0"] + p["AISLE_W"]
    fx, t = p["FL_X"], p["WALL_T"]
    m = box(t, fx - t, a0 - 50, a0, 0, 10) + box(t, fx - t, a1, a1 + 50, 0, 10)
    m = m + box(x0, x1, a1 + 60, a1 + 160, 0, 10) + box(x0, x0 + 100, a1 + 60, p["FL_Y"] - t, 0, 10)
    m = m + box(x1 - 100, x1, a1 + 60, p["FL_Y"] - t, 0, 10)
    return m


def build_parts(p=PARAMS):
    """Return {bom: [(name, shape, colour)]} for the layout. BOM numbers match bom/bom.csv."""
    out = {}

    def add(bom, name, shape, colour):
        out.setdefault(bom, []).append((name, shape, colour))

    # 1 intake: scale, table (top and legs) and four bins
    add(1, "Platform scale", zbox("scale"), "#8B5E34")
    _, _, x0, x1, y0, y1, h, _ = ZONES["table"]
    table = box(x0, x1, y0, y1, h - 50, h)
    for x in (x0 + 50, x1 - 100):
        for y in (y0 + 50, y1 - 100):
            table = table + box(x, x + 50, y, y + 50, 0, h - 50)
    add(1, "Sorting table", table, "#8B5E34")
    for i, (nm, col) in enumerate([("PET", "#2563EB"), ("HDPE", "#16A34A"), ("PP", "#EAB308"), ("Metals", "#9CA3AF")]):
        bx = 1500 + i * 510
        add(1, f"{nm} bin", box(bx, bx + 420, 1080, 1680, 0, 800), col)

    # 2 washing: float-sink tank, rinse tank, trap and pump skid
    wash = box(3800, 4600, 300, 1000, 0, 900) + box(4700, 5500, 300, 1000, 0, 900)
    wash = wash + box(4000, 5300, 1100, 1600, 0, 450)
    add(2, "Washing tanks and sediment trap", wash, "#38BDF8")

    # 3 shredder (Shredder Pro envelope 1205 x 550 x 1512) inside a lined acoustic enclosure
    enc = zbox("shred", h=1900) - box(5860, 7340, 210, 1490, 60, 1840)
    enc = enc - box(5750, 5900, 500, 1200, 0, 1700)          # open end facing the washing zone, closed by a door
    enc = enc + box(6300, 6900, 600, 1100, 1900, 2100)        # interlocked feed chute through the roof
    add(3, "Acoustic enclosure (lined)", enc, "#4B5563")
    add(3, "Shredder", box(6000, 7205, 580, 1130, 0, 1512), "#1F2937")

    # 4 drying rack and fan
    dry = box(7700, 8900, 200, 800, 0, 1800) + Pos(8300, 1000, 900) * Rot(90, 0, 0) * Cylinder(300, 200)
    add(4, "Drying rack and fan", dry, "#A3A3A3")

    # 5 extruder with barrel enclosure (hood B) on its frame
    add(5, "Extruder", box(5700, 7000, 4000, 4500, 0, 1100) + box(5750, 6000, 4100, 4400, 1100, 1550), "#C2410C")
    hood_b = box(6000, 7100, 3900, 4600, 1000, 1500) - box(6040, 7101, 3940, 4560, 1000, 1460)
    add(7, "Extruder enclosure (hood B)", hood_b, "#6B7280")

    # 6 sheet press (1 x 1 m) and cooling press inside booth A
    add(6, "Sheet press, 1 x 1 m", box(7400, 8600, 3500, 4600, 0, 1650), "#9A3412")
    add(6, "Cooling press", box(8700, 9600, 3600, 4500, 0, 1200), "#7C2D12")
    booth = zbox("press") - box(7310, 9640, 3260, 4797, -1, 2240)
    booth = booth - box(7400, 8600, 3150, 3300, 900, 1500)    # hood A sash opening, 1.2 x 0.6 m
    add(7, "Press booth (hood A)", booth, "#6B7280")

    # 7 duct: booth and extruder enclosure to the back wall, fan and filter outside
    duct = box(6500, p["DUCT_X"] + 125, 4300, 4550, p["DUCT_Z"] - 125, p["DUCT_Z"] + 125)
    duct = duct + box(6450, 6700, 4300, 4550, 1500, p["DUCT_Z"] + 125)
    duct = duct + Pos(p["DUCT_X"], p["FL_Y"] - 120, p["DUCT_Z"]) * Rot(90, 0, 0) * Cylinder(p["DUCT_D"] / 2, 400)
    add(7, "Duct 250 mm", duct, "#9CA3AF")
    add(7, "Fan and filter box (outside)", box(7650, 8650, p["FL_Y"] + 80, p["FL_Y"] + 780, 1600, 2700), "#6B7280")

    # 8 racking: bay 1 (products, back row), bay 2 (flake bags, front row)
    for key in ("store1", "store2"):
        _, _, x0, x1, y0, y1, h, _ = ZONES[key]
        r = box(x0, x1, y0, y1, 0, h) - box(x0 + 60, x1 - 60, y0 - 1, y1 + 1, 150, h - 50)
        for z in (700, 1350):
            r = r + box(x0 + 60, x1 - 60, y0, y1, z, z + 40)
        add(8, f"Racking {key[-1]}", r, "#0F766E")
    add(8, "Product lots", box(10850, 11600, 3900, 4650, 190, 650) + box(9200, 10300, 250, 1050, 190, 1100), "#99F6E4")

    # 9 passport desk with printer and bench scale
    add(9, "Passport and quality desk", zbox("desk", h=750) - box(10900, 11800, 149, 750, 0, 700), "#E5E7EB")
    add(9, "Label printer and bench scale", box(10900, 11150, 300, 550, 750, 900) + box(11300, 11700, 300, 700, 750, 820), "#111827")

    # 10 safety station: cabinet, eyewash, extinguishers (entrance, hot zone, product end)
    add(10, "PPE and first aid cabinet", box(2500, 3300, 4346, 4796, 0, 1900), "#15803D")
    add(10, "Eyewash", box(3400, 3750, 4496, 4796, 800, 1300), "#22C55E")
    ext = Pos(4800, 4650, 300) * Cylinder(90, 600) + Pos(5300, 4650, 300) * Cylinder(90, 600)
    ext = ext + Pos(10600, 1500, 300) * Cylinder(90, 600)
    add(10, "Fire extinguishers", ext, "#DC2626")

    # 11 electrical board (heater interlock and E-stop circuit)
    add(11, "Electrical board", box(3900, 4600, 4596, 4796, 1200, 2000), "#D4A017")

    # 12 export and residue cage by door B
    _, _, x0, x1, y0, y1, h, _ = ZONES["cage"]
    cage = box(x0, x1, y0, y1, 0, h) - box(x0 + 60, x1 - 60, y0 + 60, y1 - 60, 60, h + 1)
    cage = cage + box(x0 + 150, x0 + 900, y0 + 150, y1 - 150, 60, 900) + box(x0 + 1100, x1 - 150, y0 + 150, y1 - 150, 60, 700)
    add(12, "Export and residue cage", cage, "#78716C")

    # 13 shell and floor markings
    add(13, "Building shell (two 40 ft containers)", shell(p), "#D6D3CE")
    add(0, "Floor markings (aisle and hot zone)", floor_markings(p), "#0F766E")
    return out


def assembly(parts=None):
    parts = parts or build_parts()
    return Compound(children=[s for items in parts.values() for _, s, _ in items])


def equipment(parts=None):
    """Everything except the shell and markings (used for the exploded view and drawings)."""
    parts = parts or build_parts()
    return Compound(children=[s for k, items in parts.items() if k not in (0, 13) for _, s, _ in items])


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    asm = assembly(build_parts())
    for name, shp in (("refloweconomy-layout", asm), ("refloweconomy-shell", shell()),
                      ("refloweconomy-equipment", equipment(build_parts()))):
        export_step(shp, str(root / "step" / f"{name}.step"))
        export_stl(shp, str(root / "stl" / f"{name}.stl"))
    bb = asm.bounding_box()
    print(f"layout bounding box {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (fan box outside the back wall)")
    print("wrote cad/step/refloweconomy-{layout,shell,equipment}.step and cad/stl/*.stl")
