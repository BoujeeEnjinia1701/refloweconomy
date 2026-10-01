"""ReflowEconomy reference micro-factory: parametric floor layout (build123d), TRL 3, constructable.

Run from the repo root:
    python cad/src/model.py            export STEP and STL of the layout, shell and equipment
    python cad/src/model.py --check    run the constructability checks (overlaps, contacts, headroom)

Massing-plus level of detail: correct zone footprints, aisle, doors, hoods, duct, cable tray and
the made fit-out parts (booth, sash, hood B, shredder enclosure, drying rack, cage, brackets and
stands) at the sizes the build plan RFE-BLD-001 gives. Bought machines are envelopes. Units mm,
Z up, floor at Z = 0. X runs along the line from the intake end (X = 0) to the product end; Y runs
from the front wall (Y = 0) to the back wall; material flows in +X.

Layout (decided by Amish, 2026-09-25, RFE-DDR-001 items 1, 2 and 5): a plastics line on two
40 ft container footprints side by side with the adjoining side walls removed, one 1.2 m
central aisle along the container seam, a front row (intake, washing, shredding, drying,
flake store, passport desk) and a back row (export cage, safety station, electrical board,
hot zone, product racking). The sheet press, its cooling press and the extruder sit under
enclosing hoods in one hot zone.

Design for construction (RFE-DDR-003, 2026-09-30, made under Amish's 2026-09-30 instruction to
make the design physically buildable; open for his review): seam beam and floor seam plate for
the container option; hood B sits on the extruder frame; duct lowered under the booth roof and
joined to a booth take-off inside the booth; sliding sash with two openings so the cooling press
can be reached; transfer bridge between the presses; shredder enclosure roof lowered so the
feed chute is at 1.70 m, its access door moved to the aisle face and its floor plate removed;
drying fan on a stand; backboard for the board and eyewash; cable tray; duct brackets, fan stand
and stack outside; cage gate on the aisle face; sorting table and bins clear of the aisle line.

Every zone is an axis-aligned envelope in ZONES so that RFE-CAL-001
(docs/04-calcs/sizing.py) can check the aisle width, the hot zone clearance and the
floor area from the same numbers that draw the model.
"""
import sys
from pathlib import Path

from build123d import Box, Compound, Cylinder, Pos, Rot, export_step, export_stl

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 13 building shell: two 40 ft ISO containers side by side (external 12 192 x 2 438 each)
    "FL_X": 12192.0, "FL_Y": 4876.0,
    "WALL_T": 80.0,             # corrugated wall, modelled solid
    "WALL_H": 2590.0,           # external height of a standard container; roof not modelled
    "ROOF_IN": 2393.0,          # inside clear height of a standard container, under the roof
    "SEAM_Y": 2438.0,           # container seam, side walls removed along it
    "SEAM_BEAM": (165.0, 305.0),  # space reserved for the seam beam (width, depth); section by the structural engineer
    "SEAM_PLATE": (300.0, 4.5),   # floor seam cover plate (width, thickness)
    # circulation
    "AISLE_Y0": 1700.0, "AISLE_W": 1200.0,   # central aisle along X
    "DOOR_A": (160.0, 2280.0),  # container A end doors at X = 0 (intake)
    "DOOR_B": (2598.0, 4716.0), # container B end doors at X = 0 (export and residue collection)
    "EXIT": (1300.0, 2200.0),   # personnel exit cut in the far end wall of container A
    "DOOR_H": 2200.0,
    "HEADROOM": 2000.0,         # least clear height over the aisle
    # hot zone boundary (painted line) and required clearance to stock
    "HOT_X": (5400.0, 9750.0),
    "HOT_CLEAR": 1000.0,
    # fume extraction: 250 mm main duct, fan and filter outside the back wall
    "DUCT_D": 250.0, "DUCT_Z": 2050.0, "DUCT_X": 8150.0, "DUCT_Y": (4225.0, 4475.0),
    # cable tray 100 x 50 mm: back run, aisle crossing (under the seam beam), front run
    "TRAY_Z": (2038.0, 2088.0), "TRAY_CROSS_X": (5550.0, 5650.0),
    # hood openings (m), used by RFE-CAL-001
    "HOOD_A_OPEN": (1.2, 0.6),  # press booth sliding sash, one opening uncovered at a time
    "HOOD_B_OPEN": (0.8, 0.4),  # extruder barrel enclosure, open face on the aisle side
}
P = PARAMS

# Zone envelopes: key -> (BOM line, name, x0, x1, y0, y1, height, row)
ZONES = {
    "scale":   (1, "Platform scale 1 x 1 m", 300, 1300, 400, 1400, 100, "front"),
    "table":   (1, "Sorting table 2.0 x 0.9 m", 1500, 3500, 110, 1010, 900, "front"),
    "bins":    (1, "Four material bins", 1500, 3480, 1030, 1630, 800, "front"),
    "wash":    (2, "Washing tanks and sediment trap", 3800, 5500, 300, 1600, 900, "front"),
    "shred":   (3, "Shredder in acoustic enclosure", 5800, 7400, 150, 1550, 1700, "front"),
    "dry":     (4, "Drying rack and fan", 7700, 8900, 200, 1200, 1800, "front"),
    "store2":  (8, "Racking bay 2 (flake bags)", 9100, 10450, 150, 1150, 2000, "front"),
    "desk":    (9, "Passport and quality desk", 10800, 11900, 150, 850, 900, "front"),
    "cage":    (12, "Export and residue cage", 250, 2350, 3300, 4700, 1800, "back"),
    "ppe":     (10, "Safety and PPE station", 2500, 3750, 4346, 4796, 1900, "back"),
    "board":   (11, "Electrical board", 3900, 4600, 4576, 4776, 2000, "back"),
    "extr":    (5, "Extruder in barrel enclosure", 5700, 7000, 4000, 4500, 1550, "back"),
    "press":   (6, "Sheet press and cooling press in booth", 7250, 9700, 3200, 4796, 2300, "back"),
    "store1":  (8, "Racking bay 1 (products)", 10750, 12100, 3796, 4796, 2000, "back"),
}


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def cyl_y(x, z, y0, y1, r):
    """Cylinder along Y."""
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def cyl_x(y, z, x0, x1, r):
    """Cylinder along X."""
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def cyl_z(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def zbox(key, z0=0.0, h=None, inset=0.0):
    _, _, x0, x1, y0, y1, zh, _ = ZONES[key]
    return box(x0 + inset, x1 - inset, y0 + inset, y1 - inset, z0, z0 + (zh if h is None else h))


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# ---------------------------------------------------------------- shell
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
    # duct penetration in the back wall, 10 mm round the duct for the flanged sleeve
    far_back = back - cyl_y(p["DUCT_X"], p["DUCT_Z"], fy - t - 1, fy + 1, p["DUCT_D"] / 2 + 10)
    return slab + front + far_back + intake_end + far_end


def seam_beam(p=PARAMS):
    """Space reserved for the seam beam under the roof, carried by the container corner posts at both ends."""
    w, d = p["SEAM_BEAM"]
    return box(p["WALL_T"], p["FL_X"] - p["WALL_T"], p["SEAM_Y"] - w / 2, p["SEAM_Y"] + w / 2, p["ROOF_IN"] - d, p["ROOF_IN"])


def seam_plates(p=PARAMS):
    """Floor seam cover plate in four lengths with 4 mm gaps, screwed along one edge only."""
    w, th = p["SEAM_PLATE"]
    x0, x1 = p["WALL_T"], p["FL_X"] - p["WALL_T"]
    n, gap = 4, 4.0
    L = (x1 - x0 - (n - 1) * gap) / n
    out = []
    for i in range(n):
        xa = x0 + i * (L + gap)
        pl = box(xa, xa + L, p["SEAM_Y"] - w / 2, p["SEAM_Y"] + w / 2, 0, th)
        for k in range(10):          # screw holes along the intake-side edge only, 30 mm in, 300 pitch
            pl = pl - cyl_z(xa + 150 + 300 * k, p["SEAM_Y"] - w / 2 + 30, -1, th + 1, 3.25)
        out.append(pl)
    return _fuse(out)


def floor_markings(p=PARAMS):
    """Painted aisle edges and hot zone boundary (10 mm high strips, 50 mm wide)."""
    x0, x1 = p["HOT_X"]
    a0, a1 = p["AISLE_Y0"], p["AISLE_Y0"] + p["AISLE_W"]
    fx, t = p["FL_X"], p["WALL_T"]
    m = box(t, fx - t, a0 - 50, a0, 0, 10) + box(t, fx - t, a1, a1 + 50, 0, 10)
    m = m + box(x0, x1, a1 + 60, a1 + 160, 0, 10) + box(x0, x0 + 100, a1 + 60, p["FL_Y"] - t, 0, 10)
    m = m + box(x1 - 50, x1, a1 + 60, p["FL_Y"] - t, 0, 10)
    return m


# ---------------------------------------------------------------- made fit-out parts
def press_booth(p=PARAMS):
    """Booth A: 60 mm framed panels, open at the back against the container wall, two sash openings
    in the front and a sealed hole for the duct in the left end wall."""
    _, _, x0, x1, y0, y1, h, _ = ZONES["press"]
    b = box(x0, x1, y0, y1, 0, h) - box(x0 + 60, x1 - 60, y0 + 60, y1 + 1, -1, h - 60)
    b = b - box(7330, 8530, y0 - 1, y0 + 61, 900, 1500)      # opening 1, hot press, 1.2 x 0.6 m
    b = b - box(8580, 9620, y0 - 1, y0 + 61, 900, 1500)      # opening 2, cooling press, 1.04 x 0.6 m
    dy0, dy1 = p["DUCT_Y"]
    b = b - box(x0 - 1, x0 + 61, dy0 - 10, dy1 + 10, p["DUCT_Z"] - 135, p["DUCT_Z"] + 135)
    return b


def sash_rails():
    """Top and bottom rails (aluminium channel 30 x 30) screwed to the booth front."""
    y0 = ZONES["press"][4]
    return box(7250, 9850, y0 - 30, y0, 845, 875) + box(7250, 9850, y0 - 30, y0, 1525, 1555)


def sash_panel(pos="cooling"):
    """One sliding sash panel 1.25 x 0.65 m; it covers one opening, so only one is ever open.
    Drawn over opening 2 (the pressing position: opening 1 open)."""
    y0 = ZONES["press"][4]
    x0 = 8555 if pos == "cooling" else 7305
    return box(x0, x0 + 1250, y0 - 25, y0 - 5, 875, 1525)


def transfer_bridge():
    """Roller bridge between the hot press and the cooling press at platen height."""
    return box(8600, 8650, 3600, 4500, 900, 950)


def hood_b(p=PARAMS):
    """Hood B: 20 mm framed sheet enclosure over the barrel, standing on the extruder frame (z 900),
    open face 0.8 x 0.4 m on the aisle side, barrel hole in the hopper end, spigot hole in the top."""
    h = box(6000, 7000, 4000, 4500, 900, 1350) - box(6020, 6980, 4020, 4480, 899, 1330)
    h = h - box(6100, 6900, 3999, 4021, 920, 1320)
    h = h - cyl_x(4250, 1050, 5999, 6021, 60)
    dy0, dy1 = p["DUCT_Y"]
    h = h - box(6460, 6690, dy0 + 10, dy1 - 10, 1329, 1351)
    return h


def duct(p=PARAMS):
    """250 mm galvanised duct (drawn square): riser from hood B, run along the back row into the booth,
    elbow to the back wall; booth take-off with a balancing damper below the elbow."""
    dy0, dy1 = p["DUCT_Y"]
    zc, r = p["DUCT_Z"], p["DUCT_D"] / 2
    fy, t = p["FL_Y"], p["WALL_T"]
    d = box(6450, 6700, dy0, dy1, 1350, zc + r)                       # riser
    d = d + box(6700, p["DUCT_X"] + r, dy0, dy1, zc - r, zc + r)       # run
    d = d + box(p["DUCT_X"] - r, p["DUCT_X"] + r, dy1, fy - t, zc - r, zc + r)   # elbow leg to the wall
    d = d + cyl_y(p["DUCT_X"], zc, fy - t, fy + t, r)                  # through the wall to the fan box
    return d


def booth_takeoff(p=PARAMS):
    zc, r = p["DUCT_Z"], p["DUCT_D"] / 2
    return cyl_z(p["DUCT_X"], 4636, zc - r - 120, zc - r, 100)


def wall_sleeve(p=PARAMS):
    fy, t = p["FL_Y"], p["WALL_T"]
    r = p["DUCT_D"] / 2
    return cyl_y(p["DUCT_X"], p["DUCT_Z"], fy - t, fy, r + 10) - cyl_y(p["DUCT_X"], p["DUCT_Z"], fy - t - 1, fy + 1, r)


def duct_brackets(p=PARAMS):
    """Two wall shelf brackets (40 x 40 x 4 angle) under the duct run, one outside and one inside the booth."""
    dy0 = p["DUCT_Y"][0]
    zb = p["DUCT_Z"] - p["DUCT_D"] / 2
    fy, t = p["FL_Y"], p["WALL_T"]
    return _fuse([box(x, x + 50, dy0, fy - t, zb - 40, zb) for x in (6775, 7700)])


def fan_box(p=PARAMS):
    fy = p["FL_Y"]
    return box(7650, 8650, fy + 80, fy + 780, 1600, 2700)


def fan_stand(p=PARAMS):
    """Four 50 x 50 x 3 SHS legs on base plates, a top frame of the same tube; bolted to a pad outside."""
    fy = p["FL_Y"]
    x0, x1, y0, y1 = 7650, 8650, fy + 80, fy + 780
    legs = [box(x, x + 50, y, y + 50, -150, 1550) for x in (x0, x1 - 50) for y in (y0, y1 - 50)]
    frame = [box(x0, x1, y0, y0 + 50, 1550, 1600), box(x0, x1, y1 - 50, y1, 1550, 1600),
             box(x0, x0 + 50, y0 + 50, y1 - 50, 1550, 1600), box(x1 - 50, x1, y0 + 50, y1 - 50, 1550, 1600)]
    import math
    L, ang = math.hypot(x1 - x0 - 100, 1600), math.degrees(math.atan2(1600, x1 - x0 - 100))
    braces = [Pos((x0 + x1) / 2, y, 700) * Rot(0, -ang, 0) * Box(L, 30, 30) for y in (y0 - 15, y1 + 15)]
    return _fuse(legs + frame + braces)


def stack(p=PARAMS):
    fy = p["FL_Y"]
    return cyl_z(p["DUCT_X"], fy + 430, 2700, p["WALL_H"] + 1000, p["DUCT_D"] / 2)


def backboard():
    """18 mm fire-retardant plywood (drawn 20) on the back wall, carrying the board and the eyewash."""
    b = box(3350, 4650, 4776, 4796, 600, 2150)
    for x in (3450, 4000, 4550):
        for z in (700, 2050):
            b = b - cyl_y(x, z, 4775, 4797, 4.5)
    return b


def cable_tray(p=PARAMS):
    """100 x 50 perforated tray: back run on the backboard and spacers, crossing clamped under the seam beam,
    front run on the front wall; riser trunking from the board top."""
    z0, z1 = p["TRAY_Z"]
    c0, c1 = p["TRAY_CROSS_X"]
    t, fy = p["WALL_T"], p["FL_Y"]
    back = box(3900, ZONES["press"][2], fy - t - 120, fy - t - 20, z0, z1)
    cross = box(c0, c1, t + 100, fy - t - 120, z0, z1)
    front = box(3800, 8900, t, t + 100, z0, z1)
    riser = box(4200, 4300, fy - t - 120, fy - t - 20, 2000, z0)
    return back + cross + front + riser


def tray_spacers(p=PARAMS):
    t, fy = p["WALL_T"], p["FL_Y"]
    z0, z1 = p["TRAY_Z"]
    return _fuse([box(x, x + 50, fy - t - 20, fy - t, z0, z1) for x in (5100, 6100, 7050)])


def shredder_enclosure():
    """Lined acoustic enclosure: 60 mm panels on an angle frame, no floor, roof at 1.60 m, access door
    opening in the aisle face, chute hole in the roof."""
    _, _, x0, x1, y0, y1, _, _ = ZONES["shred"]
    enc = box(x0, x1, y0, y1, 0, 1600) - box(x0 + 60, x1 - 60, y0 + 60, y1 - 60, -1, 1540)
    enc = enc - box(6200, 7000, y1 - 61, y1 + 1, -1, 1450)          # access door opening
    enc = enc - box(6350, 6850, 650, 1060, 1539, 1601)             # chute collar hole
    return enc


def enclosure_door():
    y1 = ZONES["shred"][5]
    return box(6205, 6995, y1 - 45, y1 - 15, 5, 1445)


def feed_chute():
    """Chute collar through the roof, 20 mm walls, 1.54 to 1.70 m; interlocked lid on top."""
    c = box(6350, 6850, 650, 1060, 1540, 1700) - box(6370, 6830, 670, 1040, 1539, 1701)
    lid = box(6350, 6850, 650, 1060, 1700, 1712)
    return c, lid


def drying_rack():
    """Four 40 x 40 SHS posts and ten 1.2 x 0.6 m mesh trays at 160 mm pitch."""
    posts = [box(x, x + 40, y, y + 40, 0, 1800) for x in (7700, 8860) for y in (200, 760)]
    trays = [box(7740, 8860, 200, 800, z, z + 20) for z in range(200, 1800, 160)]
    return _fuse(posts + trays)


def fan_stand_dry():
    return box(8050, 8550, 850, 1150, 0, 10) + box(8270, 8330, 970, 1030, 10, 600)


def dry_fan():
    return cyl_y(8300, 900, 900, 1100, 300)


def cage():
    """Welded mesh panels on 40 x 40 angle frames (60 mm overall), no floor, double gate in the aisle face."""
    _, _, x0, x1, y0, y1, h, _ = ZONES["cage"]
    c = box(x0, x1, y0, y1, 0, h) - box(x0 + 60, x1 - 60, y0 + 60, y1 - 60, -1, h + 1)
    c = c - box(600, 1800, y0 - 1, y0 + 61, -1, h + 1)
    return c


def cage_gates():
    y0 = ZONES["cage"][4]
    return box(605, 1195, y0 + 10, y0 + 50, 20, 1790) + box(1205, 1795, y0 + 10, y0 + 50, 20, 1790)


# ---------------------------------------------------------------- components
def components(p=PARAMS):
    """Ordered {key: (bom, name, shape, colour)}. BOM numbers match bom/bom.csv (0 = floor markings)."""
    C = {}

    def add(key, bom, name, shape, colour):
        C[key] = (bom, name, shape, colour)

    # 13 shell and the parts that make the container option buildable
    add("shell", 13, "Building shell (two 40 ft containers)", shell(p), "#D6D3CE")
    add("seam_beam", 13, "Seam beam (structural engineer's design)", seam_beam(p), "#78716C")
    add("seam_plate", 13, "Floor seam cover plate", seam_plates(p), "#A8A29E")
    add("markings", 0, "Floor markings (aisle and hot zone)", floor_markings(p), "#0F766E")

    # 1 intake: scale, table (top and legs) and four bins
    add("scale", 1, "Platform scale", zbox("scale"), "#8B5E34")
    _, _, x0, x1, y0, y1, h, _ = ZONES["table"]
    table = box(x0, x1, y0, y1, h - 50, h)
    for x in (x0 + 50, x1 - 100):
        for y in (y0 + 50, y1 - 100):
            table = table + box(x, x + 50, y, y + 50, 0, h - 50)
    add("table", 1, "Sorting table", table, "#8B5E34")
    for i, (nm, col) in enumerate([("PET", "#2563EB"), ("HDPE", "#16A34A"), ("PP", "#EAB308"), ("Metals", "#9CA3AF")]):
        bx = 1500 + i * 510
        add(f"bin_{nm.lower()}", 1, f"{nm} bin", box(bx, bx + 420, 1030, 1630, 0, 800), col)

    # 2 washing: pre-wash tank, float-sink rinse tank, trap and pump skid
    add("wash", 2, "Washing tanks and sediment trap",
        box(3800, 4600, 300, 1000, 0, 900) + box(4700, 5500, 300, 1000, 0, 900) + box(4000, 5300, 1100, 1600, 0, 450), "#38BDF8")

    # 3 shredder (Shredder Pro envelope 1205 x 550 x 1512) inside a lined acoustic enclosure
    add("shred_enc", 3, "Acoustic enclosure (lined)", shredder_enclosure(), "#4B5563")
    add("shredder", 3, "Shredder", box(6000, 7205, 580, 1130, 0, 1512), "#1F2937")
    add("enc_door", 3, "Enclosure access door (interlocked)", enclosure_door(), "#6B7280")
    chute, lid = feed_chute()
    add("chute", 3, "Feed chute collar", chute, "#374151")
    add("chute_lid", 3, "Chute lid (interlocked)", lid, "#9CA3AF")

    # 4 drying rack and fan on its stand
    add("rack_dry", 4, "Drying rack", drying_rack(), "#A3A3A3")
    add("dry_stand", 4, "Drying fan stand", fan_stand_dry(), "#525252")
    add("dry_fan", 4, "Drying fan", dry_fan(), "#737373")

    # 5 extruder: frame, drive, hopper, barrel; hood B on the frame
    ext = box(5700, 7000, 4000, 4500, 0, 900) + box(5700, 6000, 4100, 4400, 900, 1100) + box(5800, 6000, 4150, 4350, 1100, 1550)
    ext = ext + cyl_x(4250, 1050, 6000, 6950, 50) + box(6880, 6920, 4225, 4275, 900, 1000)
    add("extruder", 5, "Extruder", ext, "#C2410C")
    add("hood_b", 7, "Extruder enclosure (hood B)", hood_b(p), "#6B7280")

    # 6 sheet press (1 x 1 m), cooling press and the transfer bridge between them
    add("press_hot", 6, "Sheet press, 1 x 1 m", box(7400, 8600, 3500, 4600, 0, 1650), "#9A3412")
    add("press_cool", 6, "Cooling press", box(8650, 9550, 3600, 4500, 0, 1200), "#7C2D12")
    add("bridge", 6, "Transfer bridge", transfer_bridge(), "#57534E")

    # 7 booth, sash, duct and fan
    add("booth", 7, "Press booth (hood A)", press_booth(p), "#6B7280")
    add("rails", 7, "Sash rails", sash_rails(), "#9CA3AF")
    add("sash", 7, "Sliding sash", sash_panel(), "#64748B")
    add("duct", 7, "Duct 250 mm", duct(p), "#9CA3AF")
    add("takeoff", 7, "Booth take-off with damper", booth_takeoff(p), "#9CA3AF")
    add("sleeve", 7, "Wall sleeve", wall_sleeve(p), "#4B5563")
    add("duct_brackets", 7, "Duct wall brackets", duct_brackets(p), "#374151")
    add("fan_stand", 7, "Fan stand (outside)", fan_stand(p), "#374151")
    add("fan", 7, "Fan and filter box (outside)", fan_box(p), "#6B7280")
    add("stack", 7, "Discharge stack", stack(p), "#9CA3AF")

    # 8 racking: bay 1 (products, back row), bay 2 (flake bags, front row)
    for key in ("store1", "store2"):
        _, _, x0, x1, y0, y1, h, _ = ZONES[key]
        r = box(x0, x1, y0, y1, 0, h) - box(x0 + 60, x1 - 60, y0 - 1, y1 + 1, 150, h - 50)
        for z in (700, 1350):
            r = r + box(x0 + 60, x1 - 60, y0, y1, z, z + 40)
        add(f"rack{key[-1]}", 8, f"Racking {key[-1]}", r, "#0F766E")
    add("lots1", 8, "Product lots", box(10850, 11600, 3900, 4650, 150, 650) + box(10850, 11600, 3900, 4650, 740, 1150), "#99F6E4")
    add("lots2", 8, "Flake bags", box(9200, 10300, 250, 1050, 150, 690) + box(9200, 10300, 250, 1050, 740, 1300), "#99F6E4")

    # 9 passport desk with printer and bench scale
    add("desk", 9, "Passport and quality desk", zbox("desk", h=750) - box(10900, 11800, 149, 750, -1, 700), "#E5E7EB")
    add("desk_kit", 9, "Label printer and bench scale", box(10900, 11150, 300, 550, 750, 900) + box(11300, 11700, 300, 700, 750, 820), "#111827")

    # 10 safety station: cabinet, eyewash on the backboard, extinguishers (entrance, hot zone, product end)
    add("ppe", 10, "PPE and first aid cabinet", box(2500, 3300, 4346, 4796, 0, 1900), "#15803D")
    add("eyewash", 10, "Eyewash", box(3400, 3750, 4476, 4776, 800, 1300), "#22C55E")
    for i, (x, y) in enumerate(((4800, 4650), (5300, 4650), (10600, 1500))):
        add(f"extinguisher_{i + 1}", 10, "Fire extinguishers" if i == 0 else f"Fire extinguisher {i + 1}", cyl_z(x, y, 0, 600, 90), "#DC2626")

    # 11 electrical board on its backboard, cable tray
    add("backboard", 11, "Backboard (plywood)", backboard(), "#D6B98C")
    add("board", 11, "Electrical board", box(3900, 4600, 4576, 4776, 1200, 2000), "#D4A017")
    add("tray", 11, "Cable tray", cable_tray(p), "#A3A3A3")
    add("tray_spacers", 11, "Tray wall spacers", tray_spacers(p), "#525252")

    # 12 export and residue cage by door B, gate on the aisle face
    add("cage", 12, "Export and residue cage", cage(), "#78716C")
    add("cage_gates", 12, "Cage gates", cage_gates(), "#57534E")
    _, _, x0, x1, y0, y1, h, _ = ZONES["cage"]
    add("cage_kit", 12, "Sand container and bale bags",
        box(x0 + 150, x0 + 900, y0 + 150, y1 - 150, 0, 900) + box(x0 + 1100, x1 - 150, y0 + 150, y1 - 150, 0, 700), "#A8A29E")
    return C


def build_parts(p=PARAMS):
    """Return {bom: [(name, shape, colour)]} for the layout. BOM numbers match bom/bom.csv."""
    out = {}
    for bom, name, shape, colour in components(p).values():
        out.setdefault(bom, []).append((name, shape, colour))
    return out


def assembly(parts=None):
    parts = parts or build_parts()
    return Compound(children=[s for items in parts.values() for _, s, _ in items])


def equipment(parts=None):
    """Everything except the shell and markings (used for the exploded view and drawings)."""
    parts = parts or build_parts()
    return Compound(children=[s for k, items in parts.items() if k not in (0, 13) for _, s, _ in items])


# ---------------------------------------------------------------- constructability checks
# Pairs that must touch (share a face, edge or point): (a, b, what holds them)
CONTACTS = [
    ("seam_beam", "shell", "beam ends on the container corner posts at both end walls"),
    ("table", "shell", "sorting table legs on the floor"),
    ("tray", "seam_beam", "tray crossing clamped under the seam beam"),
    ("tray", "backboard", "back run screwed to the backboard"),
    ("tray", "tray_spacers", "back run on the wall spacers"),
    ("tray_spacers", "shell", "spacers riveted to the back wall"),
    ("tray", "shell", "front run on the front wall"),
    ("tray", "board", "riser trunking on the board top"),
    ("tray", "booth", "back run stops at the booth end wall gland"),
    ("backboard", "shell", "backboard on rivet nuts in the back wall"),
    ("board", "backboard", "board screwed to the backboard"),
    ("eyewash", "backboard", "eyewash bracket screwed to the backboard"),
    ("ppe", "shell", "cabinet against the back wall, two wall brackets"),
    ("booth", "shell", "booth panels on the floor and against the back wall"),
    ("rails", "booth", "rails screwed to the booth front"),
    ("sash", "rails", "sash runs between the rails"),
    ("bridge", "press_hot", "bridge against the hot press platen side"),
    ("bridge", "press_cool", "bridge against the cooling press platen side"),
    ("hood_b", "extruder", "hood B bolted to the extruder frame top"),
    ("duct", "hood_b", "riser on the hood B spigot"),
    ("duct", "duct_brackets", "duct strapped to the wall brackets"),
    ("duct_brackets", "shell", "brackets bolted to the back wall"),
    ("duct", "takeoff", "booth take-off below the elbow"),
    ("sleeve", "shell", "sleeve flanged to the back wall"),
    ("duct", "fan", "duct into the fan box inlet"),
    ("fan", "fan_stand", "fan box bolted to the stand top frame"),
    ("stack", "fan", "stack on the fan outlet"),
    ("shred_enc", "shell", "enclosure panels cleated to the floor"),
    ("chute", "shred_enc", "chute collar through the roof hole"),
    ("chute_lid", "chute", "lid hinged on the collar"),
    ("rack_dry", "shell", "rack posts on the floor"),
    ("dry_stand", "shell", "fan stand on the floor"),
    ("dry_fan", "dry_stand", "fan bolted to the stand post"),
    ("cage", "shell", "cage panels bolted to the floor"),
    ("rack1", "shell", "racking anchored to the floor"),
    ("rack2", "shell", "racking anchored to the floor"),
    ("seam_plate", "shell", "seam plate screwed to one container floor"),
]
CLEAR = [("seam_beam", 2000.0), ("tray", 2000.0)]   # least height over the aisle


def check(p=PARAMS, verbose=True):
    """Constructability checks: no two parts overlap; every listed pair touches; every part inside the
    building is under the roof; the aisle keeps its headroom; nothing stands in the painted aisle."""
    C = components(p)
    keys = list(C)
    fails, n = [], 0
    bbs = {k: C[k][2].bounding_box() for k in keys}

    def bb_overlap(a, b, tol=0.5):
        A, B = bbs[a], bbs[b]
        return (A.min.X < B.max.X - tol and B.min.X < A.max.X - tol and A.min.Y < B.max.Y - tol
                and B.min.Y < A.max.Y - tol and A.min.Z < B.max.Z - tol and B.min.Z < A.max.Z - tol)

    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            n += 1
            if not bb_overlap(a, b):
                continue
            v = (C[a][2] & C[b][2]).volume
            if v > 1.0:
                fails.append(f"overlap {a} / {b}: {v / 1e3:.1f} cm3")
    for a, b, why in CONTACTS:
        n += 1
        d = C[a][2].distance_to(C[b][2])
        if d > 0.5:
            fails.append(f"no contact {a} / {b} ({why}): gap {d:.1f} mm")
    inside = [k for k in keys if k not in ("shell", "fan", "fan_stand", "stack", "duct", "sleeve", "markings")]
    for k in inside:
        n += 1
        if bbs[k].max.Z > p["ROOF_IN"] + 0.5:
            fails.append(f"{k} above the roof underside: {bbs[k].max.Z:.0f} mm")
    a0, a1 = p["AISLE_Y0"], p["AISLE_Y0"] + p["AISLE_W"]
    for k in keys:
        if k in ("shell", "seam_beam", "seam_plate", "markings", "tray"):
            continue
        n += 1
        if bbs[k].min.Y < a1 and bbs[k].max.Y > a0 and bbs[k].min.Z < p["HEADROOM"]:
            fails.append(f"{k} stands in the painted aisle")
    for k, hmin in CLEAR:
        n += 1
        piece = C[k][2] & box(0, p["FL_X"], a0, a1, -1, p["ROOF_IN"])
        if piece.volume > 0 and piece.bounding_box().min.Z < hmin - 0.5:
            fails.append(f"{k} leaves {piece.bounding_box().min.Z:.0f} mm headroom over the aisle")
    if verbose:
        for f in fails:
            print("FAIL", f)
        print(f"{n} constructability checks, {len(fails)} failed")
    return fails


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if check() else 0)
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True)
    (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    asm = assembly(parts)
    for name, shp in (("refloweconomy-layout", asm), ("refloweconomy-shell", shell()),
                      ("refloweconomy-equipment", equipment(parts))):
        export_step(shp, str(root / "step" / f"{name}.step"))
        export_stl(shp, str(root / "stl" / f"{name}.stl"))
    bb = asm.bounding_box()
    print(f"layout bounding box {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (fan box and stack outside the back wall)")
    print("wrote cad/step/refloweconomy-{layout,shell,equipment}.step and cad/stl/*.stl")
