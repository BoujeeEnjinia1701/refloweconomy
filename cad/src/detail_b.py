"""ReflowEconomy option B, the sort-and-bale hub (alternative concept, not carried to the drawing, BOM or
build plan), at detail level D3 (kit 1.9).

Working principle: mechanical densification only. Collected material is weighed, hand-sorted by polymer and
colour at two sorting tables into eight bins and three bulk bags, and pressed into bales of about 120 kg in a
10 t electro-hydraulic vertical baler for a regional reprocessor. Nothing is washed, shredded or melted on site,
so there is no wet area, no hot zone and no fume extraction. Same container shell, seam fit-out, intake scale,
safety station, electrical board, export cage, racking and passport desk as option A, so the two options are
compared on one footprint. Units mm; frame as cad/src/model.py.
"""
from __future__ import annotations

from build123d import Pos
import cad_parts as cp
from detail_common import (GALV, PLY, STEEL, PartList, backboard, bin_, board, cable_tray_x, cage, coach_down, desk,
                           extinguisher, holes, platform_scale, ppe_cabinet, racking_bay, seam_fitout, shell, sorting_table)
from rfe_parts import brk, plate, angle_member, bx, box, cyl, hollow, member, mesh_xz, post_foot_welds, screw, shell_box, weld


def bag_stand(L, x0, y0, n, ex=(0, -1300, 0)):
    """Bulk-bag stand: four SHS 40 x 3 posts, a top frame the bag loops hang on, foot plates screwed down."""
    k = f"bag_stand_{n}"
    x1, y1, h = x0 + 900, y0 + 900, 1400
    for xc in (x0 + 20, x1 - 20):
        for yc in (y0 + 20, y1 - 20):
            ft = L.add("Bag stand foot plate", Pos(xc, yc, 0) * plate(90, 90, 6, r_corner=3), STEEL, "made", None, explode=ex, key=k)
            L.add("Bag stand post SHS 40 x 3", member("shs", "z", 6, h - 40, xc, yc, 40, 3), STEEL, "made", None, explode=ex, key=k)
            L.fix(post_foot_welds(xc, yc, 6, 40), ex, k)
            coach_down(L, xc + (32 if xc > x0 + 450 else -32), yc + (32 if yc > y0 + 450 else -32), 6, ft, 6, 40, None, ex, k)
    for yc in (y0 + 20, y1 - 20):
        L.add("Bag stand top rail SHS 40 x 3", member("shs", "x", x0, x1, yc, h - 20, 40, 3), STEEL, "made", None, explode=ex, key=k)
    for xc in (x0 + 20, x1 - 20):
        L.add("Bag stand top cross rail SHS 40 x 3", member("shs", "y", y0 + 40, y1 - 40, h - 20, xc, 40, 3), STEEL, "made", None, explode=ex, key=k)
    L.add("Bulk bag 850 x 850 mm (woven polypropylene)", shell_box(x0 + 45, x1 - 45, y0 + 45, y1 - 45, 120, h - 45, 3, r=1.0), "canvas", "bought", None, explode=ex, key=k)


def baler(L, ex=(0, 1500, 0)):
    """10 t electro-hydraulic vertical baler (bought): posts, chamber walls with stiffeners, crosshead, cylinder,
    ram platen, lower door on hinges with its latch, loading gate with interlock, power pack and controls."""
    k = "baler"
    x0, x1, y0, y1 = 5000, 6100, 4000, 4750
    base = L.add("Baler base plate (12 mm)", bx(x0, x1, y0, y1, 148, 160, 2), STEEL, "bought", None, explode=ex, key=k)
    rails = [L.add("Baler base rail RHS 148 x 80", member("rhs", "x", x0, x1, yc, 74, 80, 148, 5), STEEL, "bought", None, explode=ex, key=k)
             for yc in (y0 + 50, y1 - 50)]
    for xs in (x0 + 150, x1 - 150):
        for r, yc in zip(rails, (y0 + 50, y1 - 50)):
            holes([base, r], (xs, yc, 160), (0, 0, -1), 13)
            L.fix([screw(12, 200, (xs, yc, 160), (0, 0, -1), name="M12 x 200 coach screw into the floor")], ex, k)
    for xc in (x0 + 40, x1 - 40):
        for yc in (y0 + 40, y1 - 40):
            L.add("Baler corner post SHS 80 x 5", member("shs", "z", 160, 2100, xc, yc, 80, 5), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
            w4 = post_foot_welds(xc, yc, 160, 80, None, 5)
            L.fix(w4[:3] if xc < 5500 else w4[:2] + w4[3:], ex, k)   # no bead on the face the chamber wall closes
    L.add("Chamber side wall, left (6 mm)", bx(x0 + 80, x0 + 86, y0, y1, 160, 2100, 1), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    L.add("Chamber side wall, right (6 mm)", bx(x1 - 86, x1 - 80, y0, y1, 160, 2100, 1), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    L.add("Chamber back wall (6 mm)", bx(x0 + 86, x1 - 86, y1 - 6, y1, 160, 2100, 1), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    L.add("Upper front plate (6 mm)", bx(x0 + 86, x1 - 86, y0 - 6, y0, 1500, 2100, 1), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    for z in (500, 900, 1300, 1700):
        L.add("Side wall stiffener 60 x 10, left", member("flat", "y", y0 + 80, y1 - 80, z, x0 + 75, 60, 10), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
        L.add("Side wall stiffener 60 x 10, right", member("flat", "y", y0 + 80, y1 - 80, z, x1 - 75, 60, 10), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
        L.add("Back wall stiffener 10 x 60", member("flat", "x", x0 + 86, x1 - 86, y1 + 5, z, 10, 60), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    for yc in (y0 - 10 + 50, y1 + 10 - 50):
        L.add("Crosshead RHS 200 x 100", member("rhs", "x", x0, x1, yc, 2200, 100, 200, 6), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    L.add("Cylinder mounting plate (20 mm)", bx(5250, 5850, y0 + 90, y1 - 90, 2180, 2200, 2), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    xm, ym = 5550, (y0 + y1) / 2
    L.add("Hydraulic cylinder barrel 160 mm", member("tube", "z", 1720, 2180, xm, ym, 160, 12), "painted_steel", "bought", None, explode=ex, color="#B3261E", key=k)
    L.add("Hydraulic cylinder end cap", cyl("z", 1700, 1720, xm, ym, 85), "painted_steel", "bought", None, explode=ex, color="#B3261E", key=k)
    L.add("Piston rod 70 mm (chromed)", member("bar", "z", 1580, 1700, xm, ym, 70), "stainless", "bought", None, explode=ex, key=k)
    L.add("Ram platen (20 mm plate)", bx(x0 + 100, x1 - 100, y0 + 20, y1 - 20, 1520, 1540, 2), STEEL, "bought", None, explode=ex, key=k)
    for xr in (5250, 5850):
        L.add("Platen rib 40 x 10", member("flat", "y", y0 + 40, y1 - 40, 1560, xr, 40, 10), STEEL, "bought", None, explode=ex, key=k)
    L.add("Platen rod boss", bx(xm - 60, xm + 60, ym - 60, ym + 60, 1540, 1580, 3), STEEL, "bought", None, explode=ex, key=k)
    # lower door with stiffeners on hinges, latch lever; loading gate with interlock
    L.add("Lower door (6 mm plate)", bx(x0 + 90, x1 - 90, y0 - 12, y0 - 6, 170, 990, 1), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    for z in (350, 650, 900):
        L.add("Door stiffener 50 x 8", member("flat", "x", x0 + 120, x1 - 120, y0 - 16, z, 8, 50), STEEL, "bought", None, explode=ex, color="#1F5F8B", key=k)
    for z in (300, 800):
        kn, pin = cp.butt_hinge(120, 40, 4, 16, open_deg=180)
        L.add("Lower door hinge", Pos(x0 + 80, y0 - 30, z - 60) * kn, "zinc_plated", "bought", None, explode=ex, key=k)
    L.add("Door latch lever", member("tube", "z", 450, 850, x1 - 60, y0 - 40, 30, 3), "safety_red", "bought", None, explode=ex, key=k)
    L.add("Door latch keeper", bx(x1 - 80, x1 - 40, y0 - 20, y0 - 12, 600, 700, 2), STEEL, "bought", None, explode=ex, key=k)
    L.add("Loading gate frame, bottom", member("rhs", "x", x0 + 100, x1 - 100, y0 - 25, 1015, 20, 30, 2), STEEL, "bought", None, explode=ex, key=k)
    L.add("Loading gate frame, top", member("rhs", "x", x0 + 100, x1 - 100, y0 - 25, 1480, 20, 30, 2), STEEL, "bought", None, explode=ex, key=k)
    L.add("Loading gate mesh", mesh_xz(x0 + 110, x1 - 110, 1034, 1461, y0 - 27, pitch=60, wire=4), STEEL, "bought", None, explode=ex, key=k)
    L.add("Loading gate interlock switch", bx(x1 - 80, x1 - 20, y0 - 60, y0 - 20, 1520, 1600, 3), "safety_yellow", "bought", None, explode=ex, key=k)
    L.add("Baler control box (start, stop, emergency stop)", bx(x1, x1 + 60, y0 + 150, y0 + 350, 1000, 1250, 4), "insulated_white", "bought", None, explode=ex, color="#D9D9D2", key=k)
    L.add("Baler emergency stop", cyl("x", x1 + 60, x1 + 90, y0 + 250, 1180, 25), "safety_red", "bought", None, explode=ex, key=k)
    # power pack beside the baler
    L.add("Power pack oil tank (60 L, 3 mm sheet)", hollow(6150, 6650, 4350, 4700, 0, 300, 3, 1.0), "painted_steel", "bought", None, explode=ex, color="#1F5F8B", key=k)
    L.add("Power pack motor 2.2 kW (single-phase)", cyl("z", 300, 620, 6400, 4525, 90), "painted_steel", "bought", None, explode=ex, color="#2B5C8A", key=k)
    L.add("Power pack pump and valve block", bx(6500, 6640, 4450, 4600, 300, 420, 4), "cast_aluminium", "bought", None, explode=ex, key=k)
    L.add("Hydraulic hose, pressure", cp.rope([(6550, 4560, 420), (6550, 4560, 2340), (5600, 4410, 2340), (5600, 4410, 2210)], 20), "epdm", "bought", None, explode=ex, key=k)
    L.add("Hydraulic hose, return", cp.rope([(6590, 4500, 420), (6590, 4500, 2360), (5500, 4340, 2360), (5500, 4340, 2210)], 20), "epdm", "bought", None, explode=ex, key=k)


def pallet(L, x0, y0, n, ex=(0, 0, 0)):
    k = f"pallet_{n}"
    for yc in (y0 + 50, y0 + 500, y0 + 950):
        L.add("Pallet stringer 100 x 100", bx(x0, x0 + 1200, yc - 50, yc + 50, 0, 100, 3), "hardwood", "bought", None, explode=ex, key=k)
    for i in range(7):
        xa = x0 + 15 + i * 170
        L.add("Pallet deck board 22 mm", bx(xa, xa + 140, y0, y0 + 1000, 100, 122, 2), "hardwood", "bought", None, explode=ex, key=k)


def bale(L, x0, y0, z0, n, ex=(0, 0, 0)):
    k = f"bale_{n}"
    x1, y1, z1 = x0 + 1000, y0 + 700, z0 + 750
    L.add("Bale of sorted PET bottles (about 120 kg; drawn as a 32 mm skin so it weighs that)", hollow(x0, x1, y0, y1, z0, z1, 32, 10), "pe_tank_silver", "bought", None, explode=ex, color="#7FA7B8", key=k)
    for xs in (x0 + 180, x0 + 490, x0 + 800):
        st = box(xs, xs + 19, y0 - 1, y1 + 1, z0 - 1, z1 + 1) - box(xs - 1, xs + 20, y0, y1, z0, z1)
        L.add("Bale strap (19 mm steel band)", st, GALV, "bought", None, explode=ex, key=k)


def pallet_truck(L, x0, y0, ex=(0, 0, 0)):
    k = "pallet_truck"
    for yc in (y0 + 110, y0 + 450):
        L.add("Pallet truck fork (4 mm pressed channel)", hollow(x0, x0 + 1150, yc - 80, yc + 80, 15, 85, 4, 1.2), "safety_red", "bought", None, explode=ex, key=k)
        L.add("Fork roller", member("tube", "y", yc - 90, yc - 81, 40, x0 + 80, 50, 6), "rubber_belt", "bought", None, explode=ex, key=k)
    L.add("Pallet truck chassis (4 mm plate)", hollow(x0 + 1150, x0 + 1350, y0 + 20, y0 + 540, 15, 300, 4, 1.2), "safety_red", "bought", None, explode=ex, key=k)
    L.add("Pallet truck pump", cyl("z", 300, 520, x0 + 1250, y0 + 280, 45), "safety_red", "bought", None, explode=ex, key=k)
    L.add("Steer wheel", member("tube", "y", y0 + 230, y0 + 330, 100, x0 + 1450, 180, 40), "rubber_belt", "bought", None, explode=ex, key=k)
    L.add("Pallet truck handle", member("tube", "z", 520, 1200, x0 + 1250, y0 + 280, 30, 3), "safety_red", "bought", None, explode=ex, key=k)


def build(P, Z):
    L = PartList()
    posts = shell(L, P)
    seam_fitout(L, P, posts)
    fy, t = P["FL_Y"], P["WALL_T"]
    # intake and sorting: scale, two tables, eight bins, three bulk-bag stands
    platform_scale(L, 300, 400, bom=None)
    sorting_table(L, 1500, 3500, 110, 1010, bom=None, label="Sorting table 1")
    sorting_table(L, 3800, 5800, 110, 1010, bom=None, label="Sorting table 2")
    names = [("PET clear", "#7FB3D5"), ("PET coloured", "#2E86C1"), ("HDPE natural", "#D5D8DC"), ("HDPE coloured", "#16A34A"),
             ("PP", "#EAB308"), ("Aluminium cans", "#9CA3AF"), ("Steel cans", "#6B7280"), ("Paper and card", "#A9784A")]
    for i, (nm, col) in enumerate(names):
        x = (1500 if i < 4 else 3800) + (i % 4) * 510
        bin_(L, x, 1030, 420, 600, 800, f"{nm} bin 420 x 600 x 800 (polyethylene)", col, bom=None)
    for n, x in enumerate((6100, 7150, 8200)):
        bag_stand(L, x, 200, n + 1)
    racking_bay(L, 9250, 10600, 150, 1150, 2000, 2, bom=None)
    for z in (168, 718):
        for xa in (9370, 9920):
            L.add("Sorted film bag 25 kg (drawn as a 24 mm skin)", hollow(xa, xa + 500, 250, 1050, z, z + 480, 24, 8), "canvas", "bought", None, explode=(1600, 0, 0), key="lots2")
    desk(L, 10800, 11900, 150, 850, bom=None)
    # back row: cage, safety station, board, baler with its power pack, bale store, racking
    cage(L, 250, 2350, 3300, 4700, 1800, 600, 1800, bom=None)
    L.add("Fire-safe cell container (steel, dry sand)", shell_box(400, 1000, 4100, 4550, 0, 500, 2, r=0.6), "safety_red", "bought", None, explode=(0, 1500, 0), color="#7A1F1A", key="cage_kit")
    L.add("Cell container lid", bx(395, 1005, 4095, 4555, 500, 512, 2), "safety_red", "bought", None, explode=(0, 1500, 0), color="#7A1F1A", key="cage_kit")
    ppe_cabinet(L, 2500, 3300, 4346, 4796, 1900, bom=None)
    backboard(L, P, bom=None)
    board(L, P, 3900, 4600, 1200, 2000, bom=None)
    ew = L.add("Eyewash station wall plate", bx(3420, 3730, fy - t - 28, fy - t - 18, 820, 1280, 2), "safety_yellow", "bought", None, explode=(0, 1600, 0), color="#2E7D32", key="eyewash")
    for xb in (3500, 3650):
        L.add("Eyewash bottle (1 L)", cyl("z", 900, 1250, xb, fy - t - 98, 70), "polycarbonate", "bought", None, explode=(0, 1600, 0), key="eyewash")
    L.add("Eyewash bottle shelf", bx(3425, 3725, fy - t - 170, fy - t - 28, 885, 900, 2), "safety_yellow", "bought", None, explode=(0, 1600, 0), color="#2E7D32", key="eyewash")
    for xb in (3440, 3710):
        for z in (840, 1260):
            holes([ew], (xb, fy - t - 28, z), (0, 1, 0), 6.5)
            L.fix([screw(6, 25, (xb, fy - t - 28, z), (0, 1, 0), name="M6 eyewash screw into the backboard")], (0, 1600, 0), "eyewash")
    L.add("Riser trunking 100 x 100 (board to tray)", member("rhs", "z", 2000, P["TRAY_Z"][0], 4150, fy - t - 70, 100, 100, 1.5), GALV, "bought", None, explode=(0, 1600, 1400), key="tray")
    cable_tray_x(L, 3900, 5000, fy - t - 70, P["TRAY_Z"][0], "Cable tray 100 x 50 (board to baler)", bom=None)
    for i, (x, y) in enumerate(((4800, 4650), (9700, 4650), (10600, 1500))):
        extinguisher(L, x, y, i + 1, bom=None)
    baler(L)
    for n, x in enumerate((6800, 8100)):
        pallet(L, x, 3700, n + 1)
        bale(L, x + 100, 3850, 123, 2 * n + 1)
        bale(L, x + 100, 3850, 123 + 752, 2 * n + 2)
    pallet_truck(L, 9300, 3720)
    racking_bay(L, 10750, 12100, 3796, 4796, 2000, 1, bom=None)
    for z in (168, 718):
        for xa in (10870, 11420):
            L.add("Sorted PP bag 25 kg (drawn as a 24 mm skin)", hollow(xa, xa + 500, 3900, 4700, z, z + 480, 24, 8), "canvas", "bought", None, explode=(1600, 0, 0), key="lots1")
    a0, a1 = P["AISLE_Y0"], P["AISLE_Y0"] + P["AISLE_W"]
    m = box(t, P["FL_X"] - t, a0 - 50, a0, 0, 1) + box(t, P["FL_X"] - t, a1, a1 + 50, 0, 1)
    L.add("Floor markings (paint: aisle edges)", m, "safety_yellow", "context", None, "shell", key="markings")
    return L
