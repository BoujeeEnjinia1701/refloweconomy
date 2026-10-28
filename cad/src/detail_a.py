"""ReflowEconomy option A, the reference micro-factory (CHOSEN), at detail level D3 (kit 1.9).

The constructable layout of RFE-DDR-003 with the approved follow-ups of 2026-10-02 and the STEM check fix of
2026-10-25 (feed slot 120 mm high, RFE-DEC-001 D3), every zone built from real stock with its fixings:
intake, washing, the enclosed shredder with its cranked feed hood, drying rack, extruder under hood B, hot
and cooling presses with the transfer bridge inside booth hood A, the duct, fan and stack, racking, desk,
safety station, electrical board and cable tray, and the export cage, in the container shell with the seam
fit-out. Positions and sizes come from PARAMS and ZONES in cad/src/model.py.
"""
from __future__ import annotations

from build123d import Plane, Pos, Rectangle, Rot, Sketch, Circle, FilletPolyline, loft, sweep
import cad_parts as cp
from detail_common import (GALV, HDPE, PLY, STEEL, PartList, backboard, bin_, board, cable_tray_x, cable_tray_y, cage,
                           coach_down, desk, extinguisher, holes, platform_scale, ppe_cabinet, racking_bay, seam_fitout,
                           shell, sorting_table)
from rfe_parts import (brk, brk_long, plate, angle_member, bolt_set, box, bx, cyl, drill, hollow, member, plain_anchor, plain_nut, mesh_xy, mesh_xz, on_axis, post_foot_welds, ring,
                       screw, shell_box, weld)

LIN = "insulated_white"


def _dims(d):
    return (d["x"][1] - d["x"][0], d["y"][1] - d["y"][0], d["z"][1] - d["z"][0])


def panel(L, name, x0, x1, y0, y1, z0, z1, outer, cuts=(), bom=None, ex=(0, 0, 0), key=None, skin=STEEL, color=None):
    """A 60 mm acoustic or booth panel: a 1.5 mm steel skin on the 'outer' face (-x, +x, -y, +y or +z) and a
    mineral-wool lining for the rest, with openings cut through both. Returns (skin, lining) part dicts."""
    t = 1.5
    ax, sgn = outer[1], outer[0]
    lo = dict(x=(x0, x1), y=(y0, y1), z=(z0, z1))
    a0, a1 = lo[ax]
    sk = dict(lo); li = dict(lo)
    if sgn == "-":
        sk[ax] = (a0, a0 + t); li[ax] = (a0 + t, a1)
    else:
        sk[ax] = (a1 - t, a1); li[ax] = (a0, a1 - t)
    s = box(*sk["x"], *sk["y"], *sk["z"])
    m = box(*li["x"], *li["y"], *li["z"])
    for c in cuts:
        s = s - box(*c)
        m = m - box(*c)
    ps = L.add(f"{name}, steel skin", brk_long(s, 0.45, _dims(sk)), skin, "made", bom, explode=ex, key=key, color=color)
    pm = L.add(f"{name}, lining", brk_long(m, 0.5, _dims(li)), LIN, "made", bom, explode=ex, key=key, color="#BDB8A8")
    return ps, pm


def panel_screw(L, targets, origin, direction, bom, ex, key, length=75):
    """Self-drilling screw through a panel's skin and lining into the frame angle behind it."""
    holes(targets, origin, direction, 5.5)
    L.fix([screw(5, length, origin, direction, name="M5 panel screw into the frame angle", bom=bom)], ex, key)


# ---------------------------------------------------------------------------------------------------------
def washing(L, P, bom=2, ex=(0, 0, 1500)):
    k = "wash"
    for x0, nm in ((3800, "pre-wash"), (4700, "float-sink rinse")):
        L.add(f"Washing tank, {nm} (500 L polyethylene)", shell_box(x0, x0 + 800, 300, 1000, 0, 900, 8, r=2.5), "pe_tank_white", "bought", bom, explode=ex, key=k)
        L.add(f"Tank rim stiffener, {nm}", bx(x0 + 8, x0 + 792, 285, 300, 860, 900, 4), "pe_tank_white", "bought", bom, explode=ex, key=k)
        L.add(f"Tank drain valve, {nm}", cyl("y", 250, 300, x0 + 400, 80, 28), "brass", "bought", bom, explode=ex, key=k)
        L.add(f"Tank drain valve handle, {nm}", bx(x0 + 385, x0 + 415, 240, 260, 108, 190, 3), "safety_red", "bought", bom, explode=ex, key=k)
    trap = shell_box(4000, 5300, 1100, 1600, 0, 450, 6, r=2.0)
    for xb in (4430, 4870):
        trap = trap + box(xb, xb + 6, 1106, 1594, 6, 400)
    L.add("Sediment trap with two baffles (polyethylene)", trap, "pe_tank_white", "bought", bom, explode=ex, key=k)
    base = L.add("Pump base plate", Pos(5410, 1300, 0) * plate(160, 300, 8, r_corner=4), STEEL, "bought", bom, explode=ex, key=k)
    L.add("Transfer pump motor 0.75 kW (splash-rated)", cyl("y", 1180, 1400, 5410, 120, 75), "painted_steel", "bought", bom, explode=ex, color="#2B5C8A", key=k)
    L.add("Transfer pump volute", cyl("y", 1400, 1440, 5410, 120, 90), "cast_aluminium", "bought", bom, explode=ex, key=k)
    for yy in (1170, 1430):
        coach_down(L, 5370, yy, 8, base, 8, 50, bom, ex, k)
        coach_down(L, 5450, yy, 8, base, 8, 50, bom, ex, k)
    L.add("Pump suction hose 32 mm (from the trap)", cp.rope([(5410, 1460, 140), (5410, 1480, 560), (5150, 1350, 560), (5150, 1350, 260)], 32), "epdm", "bought", bom, explode=ex, key=k)
    L.add("Pump delivery hose 32 mm (to the rinse tank)", cp.rope([(5410, 1172, 200), (5410, 1100, 1000), (5100, 800, 1000), (5100, 800, 700)], 32), "epdm", "bought", bom, explode=ex, key=k)


# ---------------------------------------------------------------------------------------------------------
def shredder(L, P, bom=3, ex=(0, -1700, 0)):
    """Open-design shredder (Shredder Pro class) on its stand, inside the lined acoustic enclosure, with the
    chute collar, the cranked feed hood and its interlocked flap, door, hinges and drive."""
    k = "shredder"
    # stand
    stand_plate = L.add("Shredder stand top plate (10 mm)", Pos(6600, 855, 840) * plate(500, 400, 10, r_corner=4), STEEL, "made", bom, explode=ex, key=k)
    legs = [(6380, 685), (6820, 685), (6380, 1025), (6820, 1025)]
    for xc, yc in legs:
        ft = L.add("Shredder stand foot plate", Pos(xc, yc, 0) * plate(120, 120, 8, r_corner=3), STEEL, "made", bom, explode=ex, key=k)
        L.add("Shredder stand leg SHS 50 x 3", member("shs", "z", 8, 840, xc, yc, 50, 3), STEEL, "made", bom, explode=ex, key=k)
        L.fix(post_foot_welds(xc, yc, 8, 50, bom), ex, k)
        coach_down(L, xc + (45 if xc > 6600 else -45), yc, 8, ft, 10, 60, bom, ex, k)
    for yc in (685, 1025):
        L.add("Shredder stand brace SHS 40 x 3", member("shs", "x", 6405, 6795, yc, 300, 40, 3), STEEL, "made", bom, explode=ex, key=k)
    # cutting chamber on a base flange, bolted to the stand plate
    fl = L.add("Cutting chamber base flange (15 mm)", bx(6430, 6770, 710, 1000, 850, 865, 2), STEEL, "made", bom, explode=ex, key=k)
    L.add("Cutting chamber (twin-shaft cutters inside)", bx(6450, 6750, 730, 980, 865, 1100, 6), STEEL, "made", bom, explode=ex, color="#3B3F44", key=k)
    for xb in (6440, 6760):
        for yb in (720, 990):
            holes([fl, stand_plate], (xb, yb, 865), (0, 0, -1), 11)
            L.fix(bolt_set(10, 25, (xb, yb, 865), (0, 0, -1), bom=bom), ex, k)
    L.add("Cutter shaft bearing housing, free side", cyl("x", 6430, 6450, 855, 1010, 40), "cast_aluminium", "bought", bom, explode=ex, key=k)
    L.add("Gearbox (2.2 kW gearmotor)", bx(6770, 6950, 780, 930, 900, 1050, 6), "painted_steel", "bought", bom, explode=ex, color="#2B5C8A", key=k)
    L.add("Gearmotor 2.2 kW", cyl("x", 6950, 7180, 855, 975, 78), "painted_steel", "bought", bom, explode=ex, color="#2B5C8A", key=k)
    L.add("Gearmotor fan cowl", cyl("x", 7180, 7205, 855, 975, 70), "matte_black", "bought", bom, explode=ex, key=k)
    gp = L.add("Gearbox support post SHS 50 x 3", member("shs", "z", 8, 900, 6880, 855, 50, 3), STEEL, "made", bom, explode=ex, key=k)
    gf = L.add("Gearbox post foot plate", Pos(6880, 855, 0) * plate(110, 110, 8, r_corner=3), STEEL, "made", bom, explode=ex, key=k)
    L.fix(post_foot_welds(6880, 855, 8, 50, bom), ex, k)
    coach_down(L, 6925, 900, 8, gf, 10, 60, bom, ex, k)
    # hopper from the chamber up to the collar
    lo = Plane.XY.offset(1100) * Rectangle(290, 240)
    hi = Plane.XY.offset(1512) * Rectangle(470, 380)
    lo2 = Plane.XY.offset(1099) * Rectangle(286, 236)
    hi2 = Plane.XY.offset(1513) * Rectangle(466, 376)
    hop = Pos(6600, 855, 0) * (loft([lo, hi]) - loft([lo2, hi2]))
    L.add("Shredder hopper (2 mm sheet)", hop, STEEL, "made", bom, explode=ex, key=k)
    L.add("Flake bin (polyethylene)", shell_box(6450, 6750, 750, 960, 0, 500, 5, r=2.0), HDPE, "bought", bom, explode=ex, color="#2F6F4F", key=k)
    L.add("Shredder drive, single-phase input (2.2 kW)", bx(7400, 7560, 300, 600, 1000, 1300, 5), "insulated_white", "bought", bom, explode=ex, color="#D9D9D2", key=k)
    return stand_plate


def enclosure(L, P, bom=3, ex=(0, -1700, 1900)):
    k = "shred_enc"
    x0, x1, y0, y1 = 5800, 7400, 150, 1550
    T, H = 60, 1540
    door = (6200, 7000, y1 - T - 1, y1 + 1, -1, 1450)
    front = panel(L, "Enclosure wall, front", x0, x1, y0, y0 + T, 0, H, "-y", (), bom, ex, k)
    back = panel(L, "Enclosure wall, aisle face", x0, x1, y1 - T, y1, 0, H, "+y", (door,), bom, ex, k)
    endl = panel(L, "Enclosure wall, washing end", x0, x0 + T, y0 + T, y1 - T, 0, H, "-x", (), bom, ex, k)
    endr = panel(L, "Enclosure wall, drying end", x1 - T, x1, y0 + T, y1 - T, 0, H, "+x", (), bom, ex, k)
    roof = panel(L, "Enclosure roof", x0, x1, y0, y1, H, H + T, "+z", ((6350, 6850, 650, 1060, H - 1, H + T + 1),), bom, ex, k)
    # angle frame inside: corner posts, roof rails, door frame, floor cleats
    A = 40
    xi0, xi1, yi0, yi1 = x0 + T, x1 - T, y0 + T, y1 - T
    for xc, s1 in ((xi0, 1), (xi1, -1)):
        for yc, s2 in ((yi0, 1), (yi1, -1)):
            L.add("Enclosure frame corner post L 40 x 40 x 4", angle_member("z", 0, H, xc, yc, s1, s2, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Enclosure roof rail, front", angle_member("x", xi0 + A, xi1 - A, yi0, H, 1, -1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Enclosure roof rail, aisle face", angle_member("x", xi0 + A, xi1 - A, yi1, H, -1, -1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Enclosure roof rail, washing end", angle_member("y", yi0 + A, yi1 - A, H, xi0, -1, 1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Enclosure roof rail, drying end", angle_member("y", yi0 + A, yi1 - A, H, xi1, -1, -1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Door frame jamb, hinge side", angle_member("z", 0, 1450, 6200, yi1, -1, -1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Door frame jamb, latch side", angle_member("z", 0, 1450, 7000, yi1, 1, -1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Door frame head", angle_member("x", 6200, 7000, yi1, 1450, -1, 1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    cle = [("front", angle_member("x", xi0 + A, xi1 - A, yi0, 0, 1, 1, A, 4), [(x, yi0 + 22) for x in (6000, 6600, 7200)]),
           ("aisle face, washing end", angle_member("x", xi0 + A, 6160, yi1, 0, -1, 1, A, 4), [(6000, yi1 - 22)]),
           ("aisle face, drying end", angle_member("x", 7040, xi1 - A, yi1, 0, -1, 1, A, 4), [(7200, yi1 - 22)]),
           ("washing end", angle_member("y", yi0 + A, yi1 - A, 0, xi0, 1, 1, A, 4), [(xi0 + 22, 600), (xi0 + 22, 1100)]),
           ("drying end", angle_member("y", yi0 + A, yi1 - A, 0, xi1, 1, -1, A, 4), [(xi1 - 22, 600), (xi1 - 22, 1100)])]
    for nm, s, pts in cle:
        c = L.add(f"Enclosure floor cleat, {nm}", s, STEEL, "made", bom, explode=ex, key=k)
        for x, y in pts:
            coach_down(L, x, y, 4, c, 8, 50, bom, ex, k)
    # panel screws into the corner posts (two heights, both faces of each corner)
    posts = [p for p in L if p["name"] == "Enclosure frame corner post L 40 x 40 x 4"][-4:]
    for z in (300, 1250):
        for pnl, xs, ys, d, post in ((front, xi0 + 20, y0, (0, 1, 0), posts[0]), (front, xi1 - 20, y0, (0, 1, 0), posts[2]),
                                     (back, xi0 + 20, y1, (0, -1, 0), posts[1]), (back, xi1 - 20, y1, (0, -1, 0), posts[3]),
                                     (endl, x0, yi0 + 20, (1, 0, 0), posts[0]), (endl, x0, yi1 - 20, (1, 0, 0), posts[1]),
                                     (endr, x1, yi0 + 20, (-1, 0, 0), posts[2]), (endr, x1, yi1 - 20, (-1, 0, 0), posts[3])):
            panel_screw(L, list(pnl) + [post], (xs, ys, z), d, bom, ex, k)
    # door leaf (recessed 15 mm in the opening), self-closing hinges, handle, interlock
    dsk = L.add("Enclosure door leaf, steel skin", bx(6205, 6995, y1 - 16.5, y1 - 15, 5, 1445, 0.4), STEEL, "made", bom, explode=ex, key="enc_door")
    L.add("Enclosure door leaf, lining", bx(6205, 6995, y1 - 45, y1 - 16.5, 5, 1445, 0.5), LIN, "made", bom, explode=ex, color="#BDB8A8", key="enc_door")
    L.add("Enclosure door handle", member("bar", "z", 650, 850, 6950, y1 + 8, 20), "stainless", "bought", bom, explode=ex, key="enc_door")
    L.add("Enclosure door handle standoff, lower", bx(6940, 6960, y1 - 15, y1 - 2, 640, 660, 2), "stainless", "bought", bom, explode=ex, key="enc_door")
    L.add("Door interlock switch", bx(7010, 7070, y1, y1 + 35, 900, 1000, 3), "safety_yellow", "bought", bom, explode=ex, key="enc_door")
    for zc in (200, 725, 1250):
        kn, pin = cp.butt_hinge(120, 40, 3, 10, open_deg=180)
        L.add("Self-closing spring hinge, enclosure door", Pos(6200, y1 + 8, zc - 60) * kn, "stainless", "bought", bom, explode=ex, key="door_hinges")
    # chute collar through the roof, cranked feed hood with the 120 mm slot, flap and interlock
    mz, my = P["CHUTE_MOUTH_Z"], P["CHUTE_MOUTH_Y"]
    sw, sh = P["CHUTE_SLOT"]
    top = mz + sh + 20
    col = box(6350, 6850, 650, 1060, H, mz) - box(6370, 6830, 670, 1040, H - 1, mz + 1)
    colp = L.add("Feed chute collar (lined, 20 mm walls)", brk(col, 1.0), STEEL, "made", bom, explode=ex, key="chute")
    hood = box(6350, 6850, 650, my, mz, top) - box(6600 - sw / 2, 6600 + sw / 2, 670, my + 1, mz - 1, mz + sh)
    hoodp = L.add("Cranked feed hood (closed top, 460 x 120 mm feed slot)", brk(hood, 1.0), STEEL, "made", bom, explode=ex, key="chute_hood")
    L.add("Feed hood sill on the enclosure roof (lined 2 mm sheet box)", hollow(6350, 6850, 1060, my, H + T, mz, 2.0, 0.6), STEEL, "made", bom, explode=ex, key="chute_hood")
    for xb in (6360, 6840):
        for yb in (680, 1030):
            holes([hoodp, colp], (xb, yb, top), (0, 0, -1), 9)
            L.fix(bolt_set(8, top - H, (xb, yb, top), (0, 0, -1), bom=bom), ex, "chute_hood")
    L.add("Feed slot flap (interlocked, hinged at the top)", bx(6350, 6850, my, my + 12, mz, top, 1.0), STEEL, "made", bom, explode=ex, key="chute_lid")
    L.add("Feed flap hinge pin", member("bar", "x", 6340, 6860, my + 6, top + 5, 10), "stainless", "bought", bom, explode=ex, key="chute_lid")
    L.add("Feed flap interlock switch", bx(6860, 6920, 1400, 1490, mz, mz + 80, 3), "safety_yellow", "bought", bom, explode=ex, key="chute_lid")
    L.add("Emergency stop at the feed slot", cyl("y", y1 + 8, y1 + 40, 7150, 1350, 25), "safety_red", "bought", bom, explode=ex, key="chute_lid")
    L.add("Emergency stop housing", bx(7110, 7190, y1, y1 + 8, 1300, 1400, 2), "safety_yellow", "bought", bom, explode=ex, key="chute_lid")


# ---------------------------------------------------------------------------------------------------------
def drying(L, P, bom=4, ex=(0, 0, 1300)):
    k = "rack_dry"
    for xc in (7720, 8880):
        for yc in (220, 780):
            bp = L.add("Drying rack base plate", Pos(xc, yc, 0) * plate(100, 100, 8, r_corner=3), STEEL, "made", bom, explode=ex, key=k)
            L.add("Drying rack post SHS 40 x 3", member("shs", "z", 8, 1800, xc, yc, 40, 3), STEEL, "made", bom, explode=ex, key=k)
            L.fix(post_foot_welds(xc, yc, 8, 40, bom), ex, k)
            coach_down(L, xc, yc + (38 if yc < 500 else -38), 8, bp, 8, 50, bom, ex, k)
    for i in range(10):
        zl = 200 + 160 * i
        L.add(f"Tray runner L 25 x 25 x 3, intake side, level {i + 1}", angle_member("y", 200, 800, zl, 7740, -1, 1, 25, 3), STEEL, "made", bom, explode=ex, key=k)
        L.add(f"Tray runner L 25 x 25 x 3, product side, level {i + 1}", angle_member("y", 200, 800, zl, 8860, -1, -1, 25, 3), STEEL, "made", bom, explode=ex, key=k)
        for x, s in ((7740, 1), (8860, -1)):
            for yw in (200, 760):
                L.fix([weld((x, yw, zl), (0, 1, 0), (s, 0, 0), (0, 0, 1), 40, 3, bom, name="Runner to post weld")], ex, k)
        L.add(f"Drying tray {i + 1} frame, front", angle_member("x", 7745, 8855, 245, zl, 1, 1, 25, 3), GALV, "made", bom, explode=ex, key=k)
        L.add(f"Drying tray {i + 1} frame, back", angle_member("x", 7745, 8855, 755, zl, -1, 1, 25, 3), GALV, "made", bom, explode=ex, key=k)
        L.add(f"Drying tray {i + 1} frame, intake end", angle_member("y", 270, 730, zl, 7745, 1, 1, 25, 3), GALV, "made", bom, explode=ex, key=k)
        L.add(f"Drying tray {i + 1} frame, product end", angle_member("y", 270, 730, zl, 8855, 1, -1, 25, 3), GALV, "made", bom, explode=ex, key=k)
        L.add(f"Drying tray {i + 1} mesh", mesh_xy(7775, 8825, 275, 725, zl + 3, pitch=75, wire=3), GALV, "made", bom, explode=ex, key=k)
    base = L.add("Drying fan stand base (10 mm plate)", Pos(8300, 1000, 0) * plate(500, 300, 10, r_corner=4), STEEL, "made", bom, explode=ex, key="dry_stand")
    L.add("Drying fan stand post SHS 60 x 3", member("shs", "z", 10, 600, 8300, 1000, 60, 3), STEEL, "made", bom, explode=ex, key="dry_stand")
    L.fix(post_foot_welds(8300, 1000, 10, 60, bom), ex, "dry_stand")
    for x in (8100, 8500):
        coach_down(L, x, 1000, 10, base, 8, 50, bom, ex, "dry_stand")
    L.add("Drying fan 0.4 kW, guard ring", ring("y", 900, 940, 8300, 900, 300, 286), STEEL, "bought", bom, explode=ex, color="#4A4F55", key="dry_fan")
    L.add("Drying fan motor", cyl("y", 1000, 1100, 8300, 900, 90), "painted_steel", "bought", bom, explode=ex, color="#4A4F55", key="dry_fan")
    L.add("Drying fan guard grille", mesh_xz(8040, 8560, 640, 1160, 942, pitch=60, wire=3), STEEL, "bought", bom, explode=ex, key="dry_fan")
    L.add("Drying fan yoke", bx(8270, 8330, 950, 1100, 600, 800, 3), STEEL, "bought", bom, explode=ex, key="dry_fan")


# ---------------------------------------------------------------------------------------------------------
def extruder(L, P, bom=5, ex=(0, 1500, 0)):
    k = "extruder"
    top = L.add("Extruder frame top plate (10 mm)", Pos(6350, 4250, 890) * plate(1300, 500, 10, r_corner=4), STEEL, "made", bom, explode=ex, key=k)
    for xc in (5725, 6975):
        for yc in (4025, 4475):
            ft = L.add("Extruder frame foot plate", Pos(xc, yc, 0) * plate(100, 100, 8, r_corner=3), STEEL, "made", bom, explode=ex, key=k)
            L.add("Extruder frame leg SHS 50 x 3", member("shs", "z", 8, 890, xc, yc, 50, 3), STEEL, "made", bom, explode=ex, key=k)
            L.fix(post_foot_welds(xc, yc, 8, 50, bom), ex, k)
            coach_down(L, xc + (38 if xc < 6000 else -38), yc + (38 if yc < 4250 else -38), 8, ft, 8, 50, bom, ex, k)
    for yc in (4025, 4475):
        L.add("Extruder frame rail SHS 40 x 3", member("shs", "x", 5750, 6950, yc, 300, 40, 3), STEEL, "made", bom, explode=ex, key=k)
    L.add("Extruder gearbox", bx(5720, 5900, 4120, 4380, 900, 1150, 6), "painted_steel", "bought", bom, explode=ex, color="#2B5C8A", key=k)
    L.add("Extruder motor 1.5 kW", cyl("z", 1150, 1450, 5810, 4250, 88), "painted_steel", "bought", bom, explode=ex, color="#2B5C8A", key=k)
    L.add("Extruder feed throat", bx(5900, 6000, 4170, 4330, 900, 1120, 3), STEEL, "made", bom, explode=ex, key=k)
    lo = Plane.XY.offset(1120) * Rectangle(90, 160); hi = Plane.XY.offset(1420) * Rectangle(90, 360)
    lo2 = Plane.XY.offset(1119) * Rectangle(86, 156); hi2 = Plane.XY.offset(1421) * Rectangle(86, 356)
    L.add("Extruder hopper (1.5 mm sheet)", Pos(5950, 4250, 0) * (loft([lo, hi]) - loft([lo2, hi2])), STEEL, "made", bom, explode=ex, key=k)
    L.add("Extruder barrel (100 mm, 15 mm wall)", member("tube", "x", 6000, 6975, 4250, 1050, 100, 15), "mild_steel", "made", bom, explode=ex, key=k)
    for xa in (6200, 6450, 6700):
        L.add("Barrel heater band", ring("x", xa, xa + 60, 4250, 1050, 62, 50), "stainless", "bought", bom, explode=ex, key=k)
    L.add("Extruder nozzle", cyl("x", 6975, 6992, 4250, 1050, 30), "brass", "made", bom, explode=ex, key=k)
    L.add("Barrel end support", bx(6880, 6920, 4230, 4270, 900, 1000, 2), STEEL, "made", bom, explode=ex, key=k)
    L.add("Extruder drive and temperature controllers", bx(5740, 5940, 3960, 4000, 500, 800, 4), "insulated_white", "bought", bom, explode=ex, color="#D9D9D2", key=k)
    return top


def hood_b(L, P, top, bom=7, ex=(0, 1500, 1300)):
    k = "hood_b"
    dy0, dy1 = P["DUCT_Y"]
    s = box(6000, 7000, 4000, 4500, 900, 1350) - box(6001.5, 6998.5, 4001.5, 4498.5, 899, 1348.5)
    s = s - box(6100, 6900, 3999, 4002, 920, 1320)
    s = drill(s, (6000, 4250, 1050), (1, 0, 0), 120, 10)
    s = drill(s, (6575, (dy0 + dy1) / 2, 1350), (0, 0, 1), 252, 10)
    hood = L.add("Hood B, extruder barrel enclosure (1.5 mm galvanised sheet)", brk(s, 0.4), GALV, "made", bom, explode=ex, key=k)
    angs = [L.add("Hood B base angle L 25 x 25 x 3, aisle side", angle_member("x", 6026.5, 6973.5, 4001.5, 900, 1, 1, 25, 3), GALV, "made", bom, explode=ex, key=k),
            L.add("Hood B base angle L 25 x 25 x 3, wall side", angle_member("x", 6026.5, 6973.5, 4498.5, 900, -1, 1, 25, 3), GALV, "made", bom, explode=ex, key=k),
            L.add("Hood B base angle L 25 x 25 x 3, hopper end", angle_member("y", 4001.5, 4498.5, 900, 6001.5, 1, 1, 25, 3), GALV, "made", bom, explode=ex, key=k),
            L.add("Hood B base angle L 25 x 25 x 3, nozzle end", angle_member("y", 4001.5, 4498.5, 900, 6998.5, 1, -1, 25, 3), GALV, "made", bom, explode=ex, key=k)]
    for x in (6150, 6500, 6850):
        for y, a in ((4014, angs[0]), (4486, angs[1])):
            holes([a, top], (x, y, 903), (0, 0, -1), 9)
            L.fix(bolt_set(8, 13, (x, y, 903), (0, 0, -1), bom=bom), ex, k)


# ---------------------------------------------------------------------------------------------------------
def presses(L, P, bom=6, ex=(0, 0, 500)):
    k = "press_hot"
    cols = [(7410, 3460), (8590, 3460), (7410, 4640), (8590, 4640)]
    for xc, yc in cols:
        ft = L.add("Hot press column foot plate (12 mm)", Pos(xc, yc, 0) * plate(140, 140, 12, r_corner=4), STEEL, "made", bom, explode=ex, key=k)
        L.add("Hot press column SHS 80 x 5", member("shs", "z", 12, 1490, xc, yc, 80, 5), STEEL, "made", bom, explode=ex, key=k)
        L.fix(post_foot_welds(xc, yc, 12, 80, bom, 5), ex, k)
        coach_down(L, xc + (-50 if xc < 8000 else 50), yc + (-50 if yc < 4000 else 50), 12, ft, 10, 70, bom, ex, k)
    for yc in (3460, 4640):
        L.add("Hot press top beam RHS 160 x 80", member("rhs", "x", 7370, 8630, yc, 1570, 80, 160, 5), STEEL, "made", bom, explode=ex, key=k)
        L.add("Hot press bottom beam RHS 160 x 80", member("rhs", "x", 7450, 8550, yc, 180, 80, 160, 5), STEEL, "made", bom, explode=ex, key=k)
    for xc in (7650, 8000, 8350):
        L.add("Hot press crossbeam RHS 120 x 80", member("rhs", "y", 3500, 4600, 1590, xc, 120, 80, 5), STEEL, "made", bom, explode=ex, key=k)
        for s in (1, -1):
            L.fix([weld((xc + s * 40, 3500, 1530), (0, 1, 0), (s, 0, 0), (0, 0, 1), 1100, 5, bom, name="Crossbeam to carrier weld")], ex, k)
    L.add("Upper platen carrier (15 mm plate)", bx(7450, 8550, 3500, 4600, 1515, 1530, 2), STEEL, "made", bom, explode=ex, key=k)
    L.add("Upper platen insulation (40 mm board)", bx(7450, 8550, 3500, 4600, 1475, 1515, 3), LIN, "bought", bom, explode=ex, color="#CFC8B4", key=k)
    L.add("Upper heated platen 1.1 x 1.1 m (15 mm)", bx(7450, 8550, 3500, 4600, 1460, 1475, 2), "mild_steel", "made", bom, explode=ex, key=k)
    L.add("Lower heated platen 1.1 x 1.1 m (15 mm)", bx(7450, 8550, 3500, 4600, 935, 950, 2), "mild_steel", "made", bom, explode=ex, key=k)
    L.add("Lower platen insulation (40 mm board)", bx(7450, 8550, 3500, 4600, 895, 935, 3), LIN, "bought", bom, explode=ex, color="#CFC8B4", key=k)
    L.add("Lower platen carrier (15 mm plate)", bx(7450, 8550, 3500, 4600, 880, 895, 2), STEEL, "made", bom, explode=ex, key=k)
    L.add("Jack table (15 mm plate)", bx(7450, 8550, 3420, 4680, 260, 275, 2), STEEL, "made", bom, explode=ex, key=k)
    for xc, yc in ((7700, 3750), (8300, 3750), (7700, 4350), (8300, 4350)):
        L.add("Bottle jack, body", cyl("z", 275, 575, xc, yc, 55), "safety_red", "bought", bom, explode=ex, key=k)
        L.add("Bottle jack, ram", cyl("z", 575, 650, xc, yc, 25), "mild_steel", "bought", bom, explode=ex, key=k)
        L.add("Jack spacer block", bx(xc - 60, xc + 60, yc - 60, yc + 60, 650, 880, 3), STEEL, "made", bom, explode=ex, key=k)
    L.add("Mould with a 12 mm sheet charge", bx(7500, 8500, 3550, 4550, 950, 966, 2), "hdpe_recycled", "made", bom, explode=ex, key=k)
    L.add("Press control box (heater contactors, controllers)", bx(7370, 7450, 3360, 3420, 1100, 1400, 4), "insulated_white", "bought", bom, explode=ex, color="#D9D9D2", key=k)
    # cooling press (unheated): lower table on four legs, upper plate clamped on four rods
    kc = "press_cool"
    lowp = L.add("Cooling press lower plate (20 mm)", bx(8650, 9550, 3600, 4500, 930, 950, 2), STEEL, "made", bom, explode=ex, key=kc)
    upp = L.add("Cooling press upper plate (20 mm)", bx(8650, 9550, 3600, 4500, 966, 986, 2), STEEL, "made", bom, explode=ex, key=kc)
    L.add("Mould cooling under load", bx(8690, 9510, 3640, 4460, 950, 966, 2), "hdpe_recycled", "made", bom, explode=ex, key=kc)
    for xc in (8730, 9470):
        for yc in (3680, 4420):
            ft = L.add("Cooling press foot plate", Pos(xc, yc, 0) * plate(110, 110, 8, r_corner=3), STEEL, "made", bom, explode=ex, key=kc)
            L.add("Cooling press leg SHS 60 x 4", member("shs", "z", 8, 930, xc, yc, 60, 4), STEEL, "made", bom, explode=ex, key=kc)
            L.fix(post_foot_welds(xc, yc, 8, 60, bom), ex, kc)
            coach_down(L, xc, yc + (45 if yc < 4000 else -45), 8, ft, 8, 50, bom, ex, kc)
    for yc in (3680, 4420):
        L.add("Cooling press brace SHS 40 x 3", member("shs", "x", 8760, 9440, yc, 300, 40, 3), STEEL, "made", bom, explode=ex, key=kc)
    for xc in (8730, 9470):
        L.add("Cooling press brace SHS 40 x 3", member("shs", "y", 3710, 4390, 300, xc, 40, 3), STEEL, "made", bom, explode=ex, key=kc)
    for xc, yc in ((8668, 3618), (9532, 3618), (8668, 4482), (9532, 4482)):
        holes([lowp, upp], (xc, yc, 950), (0, 0, 1), 22)
        L.add("Clamp rod M20", member("bar", "z", 895, 1030, xc, yc, 20), "zinc_plated", "fastener", bom, explode=ex, key=kc)
        L.fix([cp.part("M20 hex nut (ISO 4032)", Pos(xc, yc, 986) * plain_nut(20), "zinc_plated", kind="fastener", bom=bom),
               cp.part("M20 hex nut (ISO 4032)", Pos(xc, yc, 912) * plain_nut(20), "zinc_plated", kind="fastener", bom=bom)], ex, kc)
    L.add("Cooling press lifting handle", member("bar", "y", 3900, 4200, 1011, 9100, 20), "stainless", "bought", bom, explode=ex, key=kc)
    L.add("Handle block", bx(9080, 9120, 3880, 3920, 986, 1001, 2), "stainless", "bought", bom, explode=ex, key=kc)
    L.add("Handle block", bx(9080, 9120, 4180, 4220, 986, 1001, 2), "stainless", "bought", bom, explode=ex, key=kc)
    # transfer bridge between the presses at platen height
    kb = "bridge"
    ends = [L.add("Transfer bridge end plate", bx(8550, 8650, 3600, 3610, 900, 950, 1), STEEL, "made", bom, explode=ex, key=kb),
            L.add("Transfer bridge end plate", bx(8550, 8650, 4490, 4500, 900, 950, 1), STEEL, "made", bom, explode=ex, key=kb)]
    for xr in (8580, 8620):
        holes(ends, (xr, 4050, 930), (0, 1, 0), 12.5)
        L.add("Transfer roller (tube 40 x 2)", member("tube", "y", 3612, 4488, 930, xr, 40, 2), GALV, "made", bom, explode=ex, key=kb)
        L.add("Transfer roller axle (12 mm bar)", member("bar", "y", 3600, 4500, 930, xr, 12), "mild_steel", "made", bom, explode=ex, key=kb)
    for yc in (3580, 4520):
        bf = L.add("Transfer bridge leg foot plate", Pos(8600, yc, 0) * plate(80, 80, 6, r_corner=3), STEEL, "made", bom, explode=ex, key=kb)
        L.add("Transfer bridge leg SHS 40 x 3", member("shs", "z", 6, 900, 8600, yc, 40, 3), STEEL, "made", bom, explode=ex, key=kb)
        coach_down(L, 8630, yc, 6, bf, 6, 40, bom, ex, kb)


# ---------------------------------------------------------------------------------------------------------
def booth(L, P, bom=7, ex=(0, 0, 2400)):
    k = "booth"
    x0, x1, y0, y1, H, T = 7250, 9700, 3200, P["FL_Y"] - P["WALL_T"], 2240, 60
    dy0, dy1 = P["DUCT_Y"]
    zc = P["DUCT_Z"]
    o1 = (7330, 8530, y0 - 1, y0 + T + 1, 900, 1500)
    o2 = (8580, 9620, y0 - 1, y0 + T + 1, 900, 1500)
    front = panel(L, "Booth front panel (two sash openings)", x0, x1, y0, y0 + T, 0, H, "-y", (o1, o2), bom, ex, k)
    endl = panel(L, "Booth end panel, extruder side (duct collar)", x0, x0 + T, y0 + T, y1, 0, H, "-x",
                 ((x0 - 1, x0 + T + 1, dy0 - 10, dy1 + 10, zc - 135, zc + 135),), bom, ex, k)
    endr = panel(L, "Booth end panel, product side", x1 - T, x1, y0 + T, y1, 0, H, "+x", (), bom, ex, k)
    roof = panel(L, "Booth roof panel", x0, x1, y0, y1, H, H + T, "+z", (), bom, ex, k)
    A = 40
    xi0, xi1, yi0 = x0 + T, x1 - T, y0 + T
    posts = {}
    for xc, s1 in ((xi0, 1), (xi1, -1)):
        for yc, s2 in ((yi0, 1), (y1, -1)):
            posts[(xc, yc)] = L.add("Booth frame corner post L 40 x 40 x 4", angle_member("z", 0, H, xc, yc, s1, s2, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Booth roof rail, front", angle_member("x", xi0 + A, xi1 - A, yi0, H, 1, -1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Booth roof rail, back", angle_member("x", xi0 + A, xi1 - A, y1, H, -1, -1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Booth roof rail, extruder side", angle_member("y", yi0 + A, y1 - A, H, xi0, -1, 1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    L.add("Booth roof rail, product side", angle_member("y", yi0 + A, y1 - A, H, xi1, -1, -1, A, 4), STEEL, "made", bom, explode=ex, key=k)
    cle = [("front", angle_member("x", xi0 + A, xi1 - A, yi0, 0, 1, 1, A, 4), [(7800, yi0 + 22), (9100, yi0 + 22)]),
           ("extruder side", angle_member("y", 3600, 4500, 0, xi0, 1, 1, A, 4), [(xi0 + 22, 3700), (xi0 + 22, 4300)]),
           ("product side", angle_member("y", yi0 + A, y1 - A, 0, xi1, 1, -1, A, 4), [(xi1 - 22, 3700), (xi1 - 22, 4300)])]
    for nm, s, pts in cle:
        c = L.add(f"Booth floor cleat, {nm}", s, STEEL, "made", bom, explode=ex, key=k)
        for x, y in pts:
            coach_down(L, x, y, 4, c, 8, 50, bom, ex, k)
    for z in (400, 1900):
        for pnl, xs, ys, d, post in ((front, xi0 + 20, y0, (0, 1, 0), posts[(xi0, yi0)]), (front, xi1 - 20, y0, (0, 1, 0), posts[(xi1, yi0)]),
                                     (endl, x0, yi0 + 20, (1, 0, 0), posts[(xi0, yi0)]), (endl, x0, y1 - 20, (1, 0, 0), posts[(xi0, y1)]),
                                     (endr, x1, yi0 + 20, (-1, 0, 0), posts[(xi1, yi0)]), (endr, x1, y1 - 20, (-1, 0, 0), posts[(xi1, y1)])):
            panel_screw(L, list(pnl) + [post], (xs, ys, z), d, bom, ex, k)
    # sash rails (aluminium channel 30 x 30) and the sliding sash (one opening uncovered at a time)
    ch = cp.bent_channel_sheet(30, 30, 1.5, 9850 - 7250)
    bot = on_axis(ch, "x", (7250, y0 - 15, 845))
    tp = Pos(7250, y0 - 15, 1555) * Rot(180, 0, 0) * on_axis(ch, "x", (0, 0, 0))
    rb = L.add("Sash rail, bottom (aluminium channel 30 x 30)", bot, "aluminium", "made", bom, explode=ex, key="rails")
    rt = L.add("Sash rail, top (aluminium channel 30 x 30)", tp, "aluminium", "made", bom, explode=ex, key="rails")
    for xs in (7400, 8000, 8600, 9200, 9640):
        for z, r in ((860, rb), (1540, rt)):
            panel_screw(L, [r] + list(front), (xs, y0 - 1.5, z), (0, 1, 0), bom, ex, "rails", length=40)
    ks = "sash"
    sx0, sx1 = 8555, 9805
    L.add("Sash frame rail, bottom", member("rhs", "x", sx0, sx1, y0 - 15, 860, 20, 20, 1.5), "aluminium", "made", bom, explode=ex, key=ks)
    L.add("Sash frame rail, top", member("rhs", "x", sx0, sx1, y0 - 15, 1540, 20, 20, 1.5), "aluminium", "made", bom, explode=ex, key=ks)
    L.add("Sash frame stile", member("rhs", "z", 870, 1530, sx0 + 10, y0 - 15, 20, 20, 1.5), "aluminium", "made", bom, explode=ex, key=ks)
    L.add("Sash frame stile", member("rhs", "z", 870, 1530, sx1 - 10, y0 - 15, 20, 20, 1.5), "aluminium", "made", bom, explode=ex, key=ks)
    L.add("Sash glazing (6 mm polycarbonate)", bx(sx0 + 20, sx1 - 20, y0 - 18, y0 - 12, 870, 1530, 1), "polycarbonate", "made", bom, explode=ex, key=ks)
    L.add("Sash pull handle", member("bar", "z", 1050, 1350, sx0 + 60, y0 - 40, 16), "stainless", "bought", bom, explode=ex, key=ks)
    L.add("Sash pull handle standoff", bx(sx0 + 52, sx0 + 68, y0 - 32, y0 - 25, 1100, 1120, 1), "stainless", "bought", bom, explode=ex, key=ks)


def duct_and_fan(L, P, bom=7, ex=(0, 0, 3600)):
    k = "duct"
    fy, t = P["FL_Y"], P["WALL_T"]
    dy0, dy1 = P["DUCT_Y"]
    yc, zc, xd, r = (dy0 + dy1) / 2, P["DUCT_Z"], P["DUCT_X"], P["DUCT_D"] / 2
    path = FilletPolyline((6575, yc, 1349), (6575, yc, zc), (xd, yc, zc), (xd, fy + 80, zc), radius=250)
    prof = Plane(origin=(6575, yc, 1349), z_dir=(0, 0, 1)) * (Circle(r) - Circle(r - 0.8))
    L.add("Fume duct 250 mm (0.8 mm galvanised spiral duct, bends R 250)", sweep(prof, path=path), GALV, "bought", bom, explode=ex, key=k)
    # booth take-off with balancing damper under the bend
    to = L.add("Booth take-off 200 mm with balancing damper", member("tube", "z", zc - r - 120, zc - r, xd, 4636, 200, 1.0), GALV, "bought", bom, explode=ex, key="takeoff")
    L.add("Damper blade", ring("z", zc - r - 63, zc - r - 60, xd, 4636, 98, 6), GALV, "bought", bom, explode=ex, key="takeoff")
    # wall sleeve with a flange on the inside face
    L.add("Wall sleeve (flanged)", ring("y", fy - t, fy, xd, zc, r + 10, r) + ring("y", fy - t - 6, fy - t, xd, zc, r + 20, r), GALV, "bought", bom, explode=ex, key="sleeve")
    # duct wall brackets: arm L 40 x 40 x 4, diagonal strut, wall plate, strap over the duct
    zb = zc - r
    for xb in (6900, 7700):
        L.add("Duct bracket arm L 40 x 40 x 4", angle_member("y", dy0, fy - t - 6, zb, xb, -1, 1, 40, 4), STEEL, "made", bom, explode=ex, key="duct_brackets")
        wp = L.add("Duct bracket wall plate (60 x 6 flat)", bx(xb, xb + 60, fy - t - 6, fy - t, zb - 345, zb, 1), STEEL, "made", bom, explode=ex, key="duct_brackets")
        import math
        y_lo, z_lo, y_hi, z_hi = fy - t - 31, zb - 280, dy0 + 250, zb - 42
        Ls = math.hypot(y_lo - y_hi, z_hi - z_lo)
        ang = math.degrees(math.atan2(y_lo - y_hi, z_hi - z_lo))
        strut = Pos(xb + 8.5, (y_lo + y_hi) / 2, (z_lo + z_hi) / 2) * Rot(ang, 0, 0) * Pos(0, 0, -Ls / 2) * cp.flat_bar(5, 30, Ls)
        L.add("Duct bracket strut (30 x 5 flat)", strut, STEEL, "made", bom, explode=ex, key="duct_brackets")
        L.fix([weld((xb + 4, fy - t - 6, zb - 4), (1, 0, 0), (0, -1, 0), (0, 0, -1), 36, 4, bom, name="Arm to wall plate weld")], ex, "duct_brackets")
        for z in (zb - 300, zb - 80):
            holes([wp], (xb + 45, fy - t - 6, z), (0, 1, 0), 9)
            L.fix([screw(8, 40, (xb + 45, fy - t - 6, z), (0, 1, 0), name="M8 wall screw into a rivet nut in the back wall", bom=bom)], ex, "duct_brackets")
        strap = ring("x", xb + 4, xb + 34, yc, zc, r + 3, r) & box(xb, xb + 40, yc - r - 5, yc + r + 5, zc, zc + r + 5)
        L.add("Duct strap (half band)", strap, GALV, "bought", bom, explode=ex, key="duct_brackets")
    # fan and filter box outside the back wall on its stand, discharge stack above the roof
    kf = "fan"
    fx0, fx1, fy0, fy1, fz0, fz1 = 7650, 8650, fy + 80, fy + 780, 1600, 2700
    fb = box(fx0, fx1, fy0, fy1, fz0, fz1) - box(fx0 + 1.5, fx1 - 1.5, fy0 + 1.5, fy1 - 1.5, fz0 + 1.5, fz1 - 1.5)
    L.add("Fan and filter box (G4, F7 bag, impregnated carbon; 1.5 kW centrifugal fan)", brk(fb, 0.5), GALV, "bought", bom, explode=ex, key=kf)
    for i, (a, b) in enumerate(((fx0 + 30, fx0 + 330), (fx0 + 350, fx0 + 650), (fx0 + 670, fx1 - 30))):
        L.add(f"Filter box access door {i + 1}", bx(a, b, fy1, fy1 + 12, fz0 + 80, fz1 - 80, 1), GALV, "bought", bom, explode=ex, key=kf)
        L.add(f"Access door latch {i + 1}", bx(b - 40, b - 10, fy1 + 12, fy1 + 30, 2100, 2200, 2), "matte_black", "bought", bom, explode=ex, key=kf)
    L.add("Fan motor 1.5 kW", cyl("x", fx1, fx1 + 260, fy0 + 350, 2150, 95), "painted_steel", "bought", bom, explode=ex, color="#2B5C8A", key=kf)
    ks = "fan_stand"
    sx0, sx1, sy0, sy1 = fx0, fx1, fy0, fy1
    zg = -160
    for xc in (sx0 + 25, sx1 - 25):
        for yc in (sy0 + 25, sy1 - 25):
            bp = L.add("Fan stand base plate", Pos(xc, yc, zg) * plate(120, 120, 10, r_corner=3), STEEL, "made", bom, explode=ex, key=ks)
            L.add("Fan stand leg SHS 50 x 3", member("shs", "z", zg + 10, 1550, xc, yc, 50, 3), STEEL, "made", bom, explode=ex, key=ks)
            L.fix(post_foot_welds(xc, yc, zg + 10, 50, bom), ex, ks)
            for dx in (-45, 45):
                if (xc < 8000 and dx < 0) or (xc > 8000 and dx > 0):
                    holes([bp], (xc + dx, yc, zg + 10), (0, 0, -1), 13)
                    L.fix([cp.part("M12 concrete anchor (through-bolt) into the pad", Pos(xc + dx, yc, zg + 10) * plain_anchor(12, 80), "zinc_plated", kind="fastener", bom=bom)], ex, ks)
    for yc in (sy0 + 25, sy1 - 25):
        L.add("Fan stand top rail SHS 50 x 3", member("shs", "x", sx0, sx1, yc, 1575, 50, 3), STEEL, "made", bom, explode=ex, key=ks)
    for xc in (sx0 + 25, sx1 - 25):
        L.add("Fan stand top cross rail SHS 50 x 3", member("shs", "y", sy0 + 50, sy1 - 50, 1575, xc, 50, 3), STEEL, "made", bom, explode=ex, key=ks)
    import math
    for yb in (sy0 - 3, sy1 + 3):
        Lb = math.hypot(sx1 - sx0 - 100, 1400)
        ang = math.degrees(math.atan2(sx1 - sx0 - 100, 1400))
        br = Pos((sx0 + sx1) / 2, yb, zg + 10 + 100 + 700) * Rot(0, ang, 0) * Pos(0, 0, -Lb / 2) * cp.flat_bar(40, 6, Lb)
        L.add("Fan stand diagonal brace (40 x 6 flat)", br, STEEL, "made", bom, explode=ex, key=ks)
    L.add("Discharge stack 250 mm (1 m above the roof)", member("tube", "z", fz1, P["WALL_H"] + 1000, P["DUCT_X"], fy + 430, 250, 1.0), GALV, "bought", bom, explode=ex, key="stack")
    L.add("Stack rain band", ring("z", P["WALL_H"] + 950, P["WALL_H"] + 1000, P["DUCT_X"], fy + 430, 140, 125), GALV, "bought", bom, explode=ex, key="stack")


# ---------------------------------------------------------------------------------------------------------
def electrical(L, P, bom=11, ex=(0, 1600, 1400)):
    fy, t = P["FL_Y"], P["WALL_T"]
    z0, z1 = P["TRAY_Z"]
    c0, c1 = P["TRAY_CROSS_X"]
    backboard(L, P, bom=bom, ex=ex)
    board(L, P, 3900, 4600, 1200, 2000, bom, ex)
    L.add("Riser trunking 100 x 100 (board to tray)", member("rhs", "z", 2000, z0, 4150, fy - t - 70, 100, 100, 1.5), GALV, "bought", bom, explode=ex, key="tray")
    cable_tray_x(L, 3900, 7250, fy - t - 70, z0, "Cable tray 100 x 50, back run", bom, ex)
    cable_tray_y(L, t + 100, fy - t - 120, (c0 + c1) / 2, z0, "Cable tray 100 x 50, aisle crossing (under the seam beam)", bom, ex)
    cable_tray_x(L, 3800, 8900, t + 50, z0, "Cable tray 100 x 50, front run", bom, ex)
    for x in (5100, 6100, 7050):
        sp = L.add("Tray wall spacer", bx(x, x + 50, fy - t - 20, fy - t, z0, z1 + 45, 2), "zinc_plated", "bought", bom, explode=ex, key="tray_spacers")
        holes([sp], (x + 25, fy - t - 20, z1 + 22), (0, 1, 0), 7)
        L.fix([screw(6, 30, (x + 25, fy - t - 20, z1 + 22), (0, 1, 0), name="M6 wall screw into a rivet nut in the back wall", bom=bom)], ex, "tray_spacers")
    # padding on the crossing over the aisle: closed-cell foam in 100 mm bands of yellow and black hazard tape
    tp, ya, yb = P["TRAY_PAD"]
    n = int(round((yb - ya) / 100))
    for i in range(n):
        y0 = ya + i * (yb - ya) / n
        y1_ = y0 + (yb - ya) / n
        u = box(c0 - tp, c1 + tp, y0, y1_, z0 - tp, z1) - box(c0, c1, y0 - 1, y1_ + 1, z0, z1 + 1)
        col = "#E3B21C" if i % 2 == 0 else "#141414"
        L.add(f"Tray crossing padding band {i + 1} (15 mm foam, hazard tape)", u, "epdm", "made", bom, explode=ex, color=col, key="tray_pad")


# ---------------------------------------------------------------------------------------------------------
def build(P, Z):
    L = PartList()
    posts = shell(L, P)
    seam_fitout(L, P, posts)
    # 1 intake
    platform_scale(L, 300, 400)
    sorting_table(L, 1500, 3500, 110, 1010)
    for i, (nm, col) in enumerate([("PET", "#2563EB"), ("HDPE", "#16A34A"), ("PP", "#EAB308"), ("Metals", "#9CA3AF")]):
        bin_(L, 1500 + i * 510, 1030, 420, 600, 800, f"{nm} bin 420 x 600 x 800 (polyethylene)", col)
    washing(L, P)
    shredder(L, P)
    enclosure(L, P)
    drying(L, P)
    top = extruder(L, P)
    hood_b(L, P, top)
    presses(L, P)
    booth(L, P)
    duct_and_fan(L, P)
    # 8 racking with lots
    racking_bay(L, 10750, 12100, 3796, 4796, 2000, 1)
    racking_bay(L, 9100, 10450, 150, 1150, 2000, 2)
    for z in (168, 718):
        L.add("Product lot: 1 x 1 m HDPE sheets (10 x 12 mm)", bx(10850, 11850, 3810, 4782, z, z + 120, 3), "hdpe_recycled", "made", 8, explode=(1600, 0, 0), key="lots1")
    L.add("Product lot: HDPE and PP beams", bx(10850, 12000, 3900, 4500, 1368, 1520, 3), "hdpe_recycled", "made", 8, explode=(1600, 0, 0), color="#3A5F55", key="lots1")
    for z in (168, 718):
        for xa in (9200, 9750):
            L.add("PET flake bag 25 kg (drawn as a 24 mm skin so it weighs 25 kg)", hollow(xa, xa + 500, 250, 1050, z, z + 480, 24, 8), "canvas", "bought", 8, explode=(1600, 0, 0), key="lots2")
    desk(L, 10800, 11900, 150, 850)
    # 10 safety station
    ppe_cabinet(L, 2500, 3300, 4346, 4796, 1900)
    fy, t = P["FL_Y"], P["WALL_T"]
    ew = L.add("Eyewash station wall plate", bx(3420, 3730, fy - t - 28, fy - t - 18, 820, 1280, 2), "safety_yellow", "bought", 10, explode=(0, 1600, 0), color="#2E7D32", key="eyewash")
    for xb in (3500, 3650):
        L.add("Eyewash bottle (1 L)", cyl("z", 900, 1250, xb, fy - t - 98, 70), "polycarbonate", "bought", 10, explode=(0, 1600, 0), key="eyewash")
    L.add("Eyewash bottle shelf", bx(3425, 3725, fy - t - 170, fy - t - 28, 885, 900, 2), "safety_yellow", "bought", 10, explode=(0, 1600, 0), color="#2E7D32", key="eyewash")
    for xb in (3440, 3710):
        for z in (840, 1260):
            holes([ew], (xb, fy - t - 28, z), (0, 1, 0), 6.5)
            L.fix([screw(6, 25, (xb, fy - t - 28, z), (0, 1, 0), name="M6 eyewash screw into the backboard", bom=10)], (0, 1600, 0), "eyewash")
    for i, (x, y) in enumerate(((4800, 4650), (5300, 4650), (10600, 1500))):
        extinguisher(L, x, y, i + 1)
    electrical(L, P)
    # 12 export and residue cage with the sand container and bale bags
    cage(L, 250, 2350, 3300, 4700, 1800, 600, 1800)
    L.add("Fire-safe cell container (steel, dry sand)", shell_box(400, 1000, 4100, 4550, 0, 500, 2, r=0.6), "safety_red", "bought", 12, explode=(0, 1500, 0), color="#7A1F1A", key="cage_kit")
    L.add("Cell container lid", bx(395, 1005, 4095, 4555, 500, 512, 2), "safety_red", "bought", 12, explode=(0, 1500, 0), color="#7A1F1A", key="cage_kit")
    L.add("Dry sand fill", bx(402, 998, 4102, 4548, 2, 380, 20), "sand", "bought", 12, explode=(0, 1500, 0), key="cage_kit")
    L.add("Bale bag of export lots (drawn as a skin, about 60 kg)", hollow(1300, 2200, 3900, 4600, 0, 700, 25, 8), "canvas", "bought", 12, explode=(0, 1500, 0), key="cage_kit")
    # floor markings (paint, no BOM line)
    a0, a1 = P["AISLE_Y0"], P["AISLE_Y0"] + P["AISLE_W"]
    hx0, hx1 = P["HOT_X"]
    fx = P["FL_X"]
    m = box(t, fx - t, a0 - 50, a0, 0, 1) + box(t, fx - t, a1, a1 + 50, 0, 1)
    m = m + box(hx0, hx1, a1 + 60, a1 + 160, 0, 1) + box(hx0, hx0 + 100, a1 + 60, fy - t, 0, 1) + box(hx1 - 50, hx1, a1 + 60, fy - t, 0, 1)
    L.add("Floor markings (paint: aisle edges and hot zone boundary)", m, "safety_yellow", "context", None, "shell", key="markings")
    return L
