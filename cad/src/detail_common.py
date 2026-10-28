"""ReflowEconomy detailed parts shared by both concept options (kit 1.9, detail level D3).

The building shell (two 40 ft containers side by side with the seam fit-out), the intake scale, sorting
tables and bins, the safety station, the electrical board on its backboard, the export cage, racking and
the passport desk. Option modules (detail_a.py, detail_b.py) place them and add their own process line.
Every function appends cad_parts.part() dicts to a PartList. Units mm; frame as cad/src/model.py.
"""
from __future__ import annotations

from build123d import Cylinder, Plane, Pos, Rot
import cad_parts as cp
from cad_parts import part
from rfe_parts import (brk, plate, angle_member, bolt_set, bx, box, corrugated, cyl, drill, hollow, ibeam, member, mesh_xz, mesh_yz,
                       on_axis, post_foot_welds, ring, screw, shell_box, weld)

STEEL, GALV, BRIGHT, ZINC, PLY, HDPE = "painted_steel", "galvanised", "mild_steel", "zinc_plated", "plywood", "hdpe_black"


class PartList(list):
    """List of part dicts with helpers for the zone builders."""

    def add(self, name, shape, material, kind="made", bom=None, group="internal", explode=(0, 0, 0), color=None, key=None):
        p = part(name, shape, material, kind=kind, bom=bom, group=group, explode=explode, color=color)
        p["key"] = key
        self.append(p)
        return p

    def fix(self, items, explode=(0, 0, 0), key=None):
        for p in items:
            p["explode"] = explode
            p["key"] = key
            p["group"] = p.get("group") if p.get("group") not in ("fixings", "welds") else "internal"
            self.append(p)
        return items


def holes(parts, origin, direction, d):
    """Drill a clearance hole of diameter d through every listed part along a line."""
    for p in parts:
        p["shape"] = drill(p["shape"], origin, direction, d)


def coach_down(L, x, y, z, plate=None, d=10, length=60, bom=None, ex=(0, 0, 0), key=None):
    """Coach screw through a base plate into the container floor (pilot hole in the floor, clearance hole
    in the plate)."""
    if plate is not None:
        holes([plate], (x, y, z), (0, 0, -1), d + 1.0)
    return L.fix([screw(d, length, (x, y, z), (0, 0, -1), name=f"M{d} x {length} coach screw into the floor", bom=bom)], ex, key)


# ---------------------------------------------------------------------------------------------------------
# 13 Building shell: two 40 ft containers side by side, adjoining side walls removed (structural engineer)
# ---------------------------------------------------------------------------------------------------------
def shell(L, P, bom=13):
    fx, fy, t, h_in = P["FL_X"], P["FL_Y"], P["WALL_T"], P["ROOF_IN"]
    sy = P["SEAM_Y"]
    g = "shell"
    # floors (28 mm plywood on the container cross members, which are not drawn)
    L.add("Container floor A (28 mm plywood)", bx(t, fx - t, t, sy - 80, -28, 0, 2), PLY, "bought", bom, g, key="shell")
    L.add("Container floor B (28 mm plywood)", bx(t, fx - t, sy + 80, fy - t, -28, 0, 2), PLY, "bought", bom, g, key="shell")
    # bottom and top side rails (four lines: front, seam A, seam B, back), end rails
    for nm, yc in (("front", t / 2), ("seam A", sy - 40), ("seam B", sy + 40), ("back", fy - t / 2)):
        L.add(f"Bottom side rail, {nm}", member("rhs", "x", t, fx - t, yc, -80, 80, 160, 4.5), STEEL, "bought", bom, g, key="shell")
        L.add(f"Top side rail, {nm}", member("rhs", "x", t, fx - t, yc, h_in + 98.5, 80, 197, 4.0), STEEL, "bought", bom, g, key="shell")
    for xc, nm in ((t / 2, "intake end"), (fx - t / 2, "far end")):
        for y0, y1, c in ((t, sy - 80, "A"), (sy + 80, fy - t, "B")):
            L.add(f"Bottom end rail, {nm} {c}", member("rhs", "y", y0, y1, -80, xc, 160, 80, 4.5), STEEL, "bought", bom, g, key="shell")
            L.add(f"Top end rail, {nm} {c}", member("rhs", "y", y0, y1, h_in + 98.5, xc, 197, 80, 4.0), STEEL, "bought", bom, g, key="shell")
    # corner posts (eight; the four at the seam carry the seam beam)
    posts = {}
    for xc in (t / 2, fx - t / 2):
        for yc in (t / 2, sy - 40, sy + 40, fy - t / 2):
            p = L.add(f"Corner post x{int(xc)} y{int(yc)}", member("shs", "z", -160, h_in + 197, xc, yc, 80, 6), STEEL, "bought", bom, g, key="shell")
            posts[(xc, yc)] = p
    # corrugated walls: front and back full length, far end with the personnel exit, intake end headers over the doors
    front = corrugated("x", t, fx - t, 0, 0, h_in, s2=-1)
    L.add("Front wall (corrugated, left out of the renders)", Pos(0, t, 0) * front, STEEL, "bought", bom, "front_wall", key="shell")
    back = Pos(0, fy - t, 0) * corrugated("x", t, fx - t, 0, 0, h_in, s2=1)
    back = drill(back, (P["DUCT_X"], fy - t / 2, P["DUCT_Z"]), (0, 1, 0), P["DUCT_D"] + 20)
    L.add("Back wall (corrugated)", back, STEEL, "bought", bom, g, key="shell")
    for y0, y1, c in ((t, sy - 80, "A"), (sy + 80, fy - t, "B")):
        w = corrugated("y", y0, y1, 0, 0, h_in)                      # x 0..38 (outward +x)
        far = Pos(fx - t, 0, 0) * w
        if c == "A":
            e0, e1 = P["EXIT"]
            far = far - box(fx - t - 1, fx + 1, e0, e1, -1, 2000)
        L.add(f"Far end wall {c} (corrugated)", far, STEEL, "bought", bom, g, key="shell")
        hdr = Pos(t, 0, 0) * w.mirror(Plane.YZ)  # x 42..80 (outward -x)
        hdr = hdr - box(-1, t + 1, y0 - 1, y1 + 1, -1, P["DOOR_H"])
        L.add(f"Intake end door header {c} (doors open)", hdr, STEEL, "bought", bom, g, key="shell")
    return posts


def seam_fitout(L, P, posts, bom=13):
    """Seam beam (UB 305 x 165 x 40 in the reserved space) on cleats bolted to the seam corner posts, and the
    floor seam cover plate in four lengths screwed along one edge."""
    fx, t, sy, h_in = P["FL_X"], P["WALL_T"], P["SEAM_Y"], P["ROOF_IN"]
    g, ex = "shell", (0, 0, 900)
    hb, bb, tw, tf = 303.4, 165.0, 6.0, 10.2
    zc = h_in - hb / 2
    beam = L.add("Seam beam UB 305 x 165 x 40 (structural engineer's design)", ibeam("x", t, fx - t, sy, zc, hb, bb, tw, tf),
                 STEEL, "made", bom, g, ex, key="seam_beam")
    for xe, sx in ((t, 1), (fx - t, -1)):
        for sw in (1, -1):
            y_web = sy + sw * tw / 2
            cl = L.add(f"Seam beam end cleat L 90 x 90 x 8 ({'intake' if sx > 0 else 'far'} end)",
                       angle_member("z", h_in - 280, h_in - 20, xe, y_web, sx, sw, 90, 8), STEEL, "made", bom, g, ex, key="seam_beam")
            post = posts[(t / 2 if sx > 0 else fx - t / 2, sy + sw * 40)]
            for zb in (h_in - 220, h_in - 80):
                # through the cleat leg and the post wall, nut inside the hollow post
                xo = xe + sx * 8
                holes([cl, post], (xo, sy + sw * 50, zb), (-sx, 0, 0), 18)
                L.fix(bolt_set(16, 8 + 6, (xo, sy + sw * 50, zb), (-sx, 0, 0), bom=bom), ex, "seam_beam")
        for zb in (h_in - 220, h_in - 80):
            xb = xe + sx * 55
            yo = sy + tw / 2 + 8
            holes([beam] + [p for p in L if p["name"].startswith("Seam beam end cleat") and abs(p["shape"].bounding_box().center().X - (xe + sx * 45)) < 60],
                  (xb, yo, zb), (0, -1, 0), 18)
            L.fix(bolt_set(16, 8 + tw + 8, (xb, yo, zb), (0, -1, 0), bom=bom), ex, "seam_beam")
    # floor seam cover plate: 4 lengths of 4.5 mm tread plate, 4 mm gaps, screwed along the intake-side edge only
    w, th = P["SEAM_PLATE"]
    x0, x1, n, gap = t, fx - t, 4, 4.0
    Lp = (x1 - x0 - (n - 1) * gap) / n
    for i in range(n):
        xa = x0 + i * (Lp + gap)
        hs = [(-Lp / 2 + 150 + 300 * k, -w / 2 + 30, 6.5) for k in range(10)]
        pl = Pos(xa + Lp / 2, sy, 0) * plate(Lp, w, th, holes=hs, r_corner=2, edge=1.0)
        L.add(f"Floor seam cover plate {i + 1} of 4 (4.5 mm tread plate)", pl, "aluminium", "made", bom, g, (0, -300, 500), key="seam_plate")
        for k in range(10):
            L.fix([screw(6, 40, (xa + 150 + 300 * k, sy - w / 2 + 30, th), (0, 0, -1), name="M6 x 40 countersunk wood screw into the floor", bom=bom)], (0, -300, 500), "seam_plate")


# ---------------------------------------------------------------------------------------------------------
# 1 Intake: platform scale, sorting table, bins
# ---------------------------------------------------------------------------------------------------------
def platform_scale(L, x0, y0, bom=1, ex=(0, -1300, 0)):
    k = "scale"
    L.add("Platform scale deck (6 mm chequer plate)", Pos(x0 + 500, y0 + 500, 94) * plate(1000, 1000, 6, r_corner=4, edge=1.5),
          STEEL, "bought", bom, explode=ex, key=k)
    for yc in (y0 + 30, y0 + 970):
        L.add("Scale frame rail RHS 60 x 40", member("rhs", "x", x0, x0 + 1000, yc, 74, 60, 40, 3), STEEL, "bought", bom, explode=ex, key=k)
    for xc in (x0 + 30, x0 + 970):
        L.add("Scale frame cross rail RHS 60 x 40", member("rhs", "y", y0 + 60, y0 + 940, 74, xc, 40, 60, 3), STEEL, "bought", bom, explode=ex, key=k)
    for xc in (x0 + 60, x0 + 940):
        for yc in (y0 + 120, y0 + 880):
            L.add("Scale load cell foot", cyl("z", 0, 54, xc, yc, 25), "stainless", "bought", bom, explode=ex, key=k)
    base = L.add("Indicator post base plate", Pos(x0 - 60, y0 + 500, 0) * plate(120, 160, 8, r_corner=4), STEEL, "bought", bom, explode=ex, key=k)
    L.add("Indicator post (tube 40 x 2)", member("tube", "z", 8, 1000, x0 - 60, y0 + 500, 40, 2), STEEL, "bought", bom, explode=ex, key=k)
    L.add("Scale indicator", bx(x0 - 120, x0 - 0.5, y0 + 430, y0 + 570, 1000, 1150, 6), "matte_black", "bought", bom, explode=ex, key=k)
    for yy in (y0 + 450, y0 + 550):
        coach_down(L, x0 - 60, yy, 8, base, 8, 50, bom, ex, k)


def sorting_table(L, x0, x1, y0, y1, h=900, bom=1, ex=(0, -1300, 0), label="Sorting table"):
    k = "table"
    L.add(f"{label} top (3 mm sheet)", Pos((x0 + x1) / 2, (y0 + y1) / 2, h - 3) * plate(x1 - x0, y1 - y0, 3, r_corner=8, edge=1.0),
          STEEL, "made", bom, explode=ex, key=k)
    zf = h - 23
    for yc in (y0 + 70, y1 - 70):
        L.add(f"{label} frame rail SHS 40 x 3", member("shs", "x", x0 + 45, x1 - 45, yc, zf, 40, 3), STEEL, "made", bom, explode=ex, key=k)
    for xc in (x0 + 70, x1 - 70):
        L.add(f"{label} frame cross rail SHS 40 x 3", member("shs", "y", y0 + 90, y1 - 90, zf, xc, 40, 3), STEEL, "made", bom, explode=ex, key=k)
    legs = [(x0 + 70, y0 + 70), (x1 - 70, y0 + 70), (x0 + 70, y1 - 70), (x1 - 70, y1 - 70)]
    for xc, yc in legs:
        ft = L.add(f"{label} foot plate", Pos(xc, yc, 0) * plate(110, 110, 6, r_corner=3), STEEL, "made", bom, explode=ex, key=k)
        L.add(f"{label} leg SHS 50 x 3", member("shs", "z", 6, zf - 20, xc, yc, 50, 3), STEEL, "made", bom, explode=ex, key=k)
        L.fix(post_foot_welds(xc, yc, 6, 50, bom), ex, k)
        coach_down(L, xc + 42, yc + 42, 6, ft, 8, 50, bom, ex, k)
    for yc in (y0 + 70, y1 - 70):
        L.add(f"{label} lower rail SHS 40 x 3", member("shs", "x", x0 + 95, x1 - 95, yc, 200, 40, 3), STEEL, "made", bom, explode=ex, key=k)


def bin_(L, x0, y0, w, d, h, name, color, bom=1, ex=(0, -1300, 0)):
    L.add(name, shell_box(x0, x0 + w, y0, y0 + d, 0, h, 6, r=2.0), HDPE, "bought", bom, explode=ex, color=color, key="bins")


# ---------------------------------------------------------------------------------------------------------
# 10 Safety station and 11 electrical board (back wall)
# ---------------------------------------------------------------------------------------------------------
def ppe_cabinet(L, x0, x1, y0, y1, h, bom=10, ex=(0, 1600, 0)):
    k = "ppe"
    car = box(x0, x1, y0 + 20, y1, 0, h) - box(x0 + 1.5, x1 - 1.5, y0 + 19, y1 - 1.5, 1.5, h - 1.5)
    carcass = L.add("PPE and first aid cabinet carcass", brk(car, 0.5), "safety_yellow", "bought", bom, explode=ex, color="#2E7D32", key=k)
    xm = (x0 + x1) / 2
    for a, b in ((x0 + 2, xm - 1), (xm + 1, x1 - 2)):
        L.add("PPE cabinet door (folded 1 mm sheet)", hollow(a, b, y0 + 1, y0 + 19, 30, h - 30, 1.0, 0.3), "safety_yellow", "bought", bom, explode=ex, color="#2E7D32", key=k)
        L.add("PPE cabinet handle", member("bar", "z", h * 0.45, h * 0.6, b - 40 if a < xm else a + 40, y0 - 9, 12), "stainless", "bought", bom, explode=ex, key=k)
    for xc in (x0 + 100, x1 - 100):
        br = L.add("Cabinet wall bracket L 40 x 40 x 4", angle_member("x", xc - 40, xc + 40, y1, h, -1, 1, 40, 4), STEEL, "bought", bom, explode=ex, key=k)
        L.fix([screw(6, 30, (xc, y1 - 20, h + 4), (0, 0, -1), name="M6 cabinet screw into the carcass top", bom=bom)], ex, k)
        holes([br], (xc, y1 - 20, h + 4), (0, 0, -1), 7)
        holes([carcass], (xc, y1 - 20, h + 4), (0, 0, -1), 6.5)
        holes([br], (xc, y1, h + 25), (0, 1, 0), 7)
        L.fix([screw(6, 30, (xc, y1 - 4, h + 25), (0, 1, 0), name="M6 wall screw into the back wall", bom=bom)], ex, k)


def extinguisher(L, x, y, n, bom=10, ex=(0, 1600, 0)):
    k = f"extinguisher_{n}"
    body = brk(Pos(x, y, 290) * Cylinder(90, 560), 40)
    L.add(f"Fire extinguisher {n} (9 kg dry powder)", body, "safety_red", "bought", bom, explode=ex, key=k)
    L.add(f"Extinguisher {n} valve head", bx(x - 25, x + 25, y - 30, y + 30, 570, 640, 5), "brass", "bought", bom, explode=ex, key=k)
    L.add(f"Extinguisher {n} lever", bx(x - 15, x + 15, y - 110, y - 30, 630, 645, 3), "matte_black", "bought", bom, explode=ex, key=k)
    L.add(f"Extinguisher {n} hose", cp.rope([(x + 34, y, 615), (x + 110, y, 595), (x + 110, y, 260), (x + 100, y, 232)], 16), "epdm", "bought", bom, explode=ex, key=k)


def backboard(L, P, x0=3350, x1=4650, z0=600, z1=2150, bom=11, ex=(0, 1600, 1400)):
    fy, t = P["FL_Y"], P["WALL_T"]
    yb = fy - t
    bb = bx(x0, x1, yb - 18, yb, z0, z1, 2)
    pts = [(x, z) for x in (x0 + 100, (x0 + x1) / 2, x1 - 100) for z in (z0 + 100, z1 - 50)]
    for x, z in pts:
        bb = drill(bb, (x, yb - 9, z), (0, 1, 0), 9)
    p = L.add("Backboard (18 mm fire-retardant plywood)", bb, PLY, "made", bom, explode=ex, key="backboard")
    for x, z in pts:
        L.fix([screw(8, 40, (x, yb - 18, z), (0, 1, 0), name="M8 wall screw into a rivet nut in the back wall", bom=bom)], ex, "backboard")
    return p


def board(L, P, x0, x1, z0, z1, bom=11, ex=(0, 1600, 1400)):
    fy, t = P["FL_Y"], P["WALL_T"]
    yb = fy - t - 18
    k = "board"
    car = box(x0, x1, yb - 200, yb, z0, z1) - box(x0 + 1.5, x1 - 1.5, yb - 201, yb - 1.5, z0 + 1.5, z1 - 1.5)
    L.add("Electrical board enclosure (IP54 steel)", brk(car, 0.5), "insulated_white", "bought", bom, explode=ex, color="#D9D9D2", key=k)
    L.add("Board door", bx(x0 + 2, x1 - 2, yb - 220, yb - 201, z0 + 2, z1 - 2, 0.6), "insulated_white", "bought", bom, explode=ex, color="#E2E2DA", key=k)
    L.add("Board door handle", member("bar", "z", (z0 + z1) / 2 - 60, (z0 + z1) / 2 + 60, x1 - 40, yb - 232, 14), "matte_black", "bought", bom, explode=ex, key=k)
    L.add("Emergency stop at the board", cyl("y", yb - 252, yb - 221, x0 + 80, z1 - 120, 22), "safety_red", "bought", bom, explode=ex, key=k)
    L.add("Energy meter window", bx(x0 + 60, x0 + 200, yb - 222.5, yb - 220, z0 + 60, z0 + 160, 0.5), "glass", "bought", bom, explode=ex, key=k)
    for xg in (x0 + 120, (x0 + x1) / 2, x1 - 120):
        L.add("Cable gland M32", cyl("z", z1, z1 + 25, xg, yb - 100, 20), "matte_black", "bought", bom, explode=ex, key=k)
    encl = [p for p in L if p["name"] == "Electrical board enclosure (IP54 steel)"][-1]
    for x in (x0 + 60, x1 - 60):
        for z in (z0 + 60, z1 - 60):
            holes([encl], (x, yb - 1, z), (0, 1, 0), 6.6)
            L.fix([screw(6, 18, (x, yb - 1.5, z), (0, 1, 0), name="M6 board screw into the backboard", bom=bom)], ex, k)


def cable_tray_x(L, x0, x1, yc, z0, name, bom=11, ex=(0, 1600, 1400)):
    s = on_axis(cp.bent_channel_sheet(100, 50, 1.5, x1 - x0), "x", (x0, yc, z0))
    return L.add(name, s, GALV, "bought", bom, explode=ex, key="tray")


def cable_tray_y(L, y0, y1, xc, z0, name, bom=11, ex=(0, 1600, 1400)):
    s = Pos(xc, y0, 0) * Rot(0, 0, 90) * on_axis(cp.bent_channel_sheet(100, 50, 1.5, y1 - y0), "x", (0, 0, z0))
    return L.add(name, s, GALV, "bought", bom, explode=ex, key="tray")


# ---------------------------------------------------------------------------------------------------------
# 12 Export and residue cage (angle frame, welded mesh, double gate on the aisle face)
# ---------------------------------------------------------------------------------------------------------
def cage(L, x0, x1, y0, y1, h, g0, g1, bom=12, ex=(0, 1500, 0)):
    k = "cage"
    A = 40.0
    for xc, s1 in ((x0, 1), (x1, -1)):
        for yc, s2 in ((y0, 1), (y1, -1)):
            L.add("Cage corner post L 40 x 40 x 4", angle_member("z", 0, h, xc, yc, s1, s2, A, 4), GALV, "made", bom, explode=ex, key=k)
    for xc, s1 in ((g0, -1), (g1, 1)):
        L.add("Cage gate post L 40 x 40 x 4", angle_member("z", 0, h - A, xc, y0, s1, 1, A, 4), GALV, "made", bom, explode=ex, key=k)
    # top rails (legs inward and down), bottom rails (legs inward and up, screwed to the floor)
    L.add("Cage top rail, front", angle_member("x", x0 + A, x1 - A, y0, h, 1, -1, A, 4), GALV, "made", bom, explode=ex, key=k)
    L.add("Cage top rail, back", angle_member("x", x0 + A, x1 - A, y1, h, -1, -1, A, 4), GALV, "made", bom, explode=ex, key=k)
    L.add("Cage top rail, intake end", angle_member("y", y0 + A, y1 - A, h, x0, -1, 1, A, 4), GALV, "made", bom, explode=ex, key=k)
    L.add("Cage top rail, far end", angle_member("y", y0 + A, y1 - A, h, x1, -1, -1, A, 4), GALV, "made", bom, explode=ex, key=k)
    bots = [("front left", angle_member("x", x0 + A, g0 - A, y0, 0, 1, 1, A, 4), (x0 + A + g0 - A) / 2, y0 + 20),
            ("front right", angle_member("x", g1 + A, x1 - A, y0, 0, 1, 1, A, 4), (g1 + A + x1 - A) / 2, y0 + 20),
            ("back", angle_member("x", x0 + A, x1 - A, y1, 0, -1, 1, A, 4), (x0 + x1) / 2, y1 - 20),
            ("intake end", angle_member("y", y0 + A, y1 - A, 0, x0, 1, 1, A, 4), x0 + 20, (y0 + y1) / 2),
            ("far end", angle_member("y", y0 + A, y1 - A, 0, x1, 1, -1, A, 4), x1 - 20, (y0 + y1) / 2)]
    for nm, s, xs, ys in bots:
        b = L.add(f"Cage bottom rail, {nm}", s, GALV, "made", bom, explode=ex, key=k)
        coach_down(L, xs, ys, 4, b, 8, 50, bom, ex, k)
    i = 4.5
    L.add("Cage mesh panel, front left", mesh_xz(x0 + A + i, g0 - A - i, A + i, h - A - i, y0 + 2), GALV, "made", bom, explode=ex, key=k)
    L.add("Cage mesh panel, front right", mesh_xz(g1 + A + i, x1 - A - i, A + i, h - A - i, y0 + 2), GALV, "made", bom, explode=ex, key=k)
    L.add("Cage mesh panel, back", mesh_xz(x0 + A + i, x1 - A - i, A + i, h - A - i, y1 - 10), GALV, "made", bom, explode=ex, key=k)
    L.add("Cage mesh panel, intake end", mesh_yz(y0 + A + i, y1 - A - i, A + i, h - A - i, x0 + 2), GALV, "made", bom, explode=ex, key=k)
    L.add("Cage mesh panel, far end", mesh_yz(y0 + A + i, y1 - A - i, A + i, h - A - i, x1 - 10), GALV, "made", bom, explode=ex, key=k)
    # gate leaves: RHS 30 x 30 frames with mesh, hung on self-closing hinges at the outer posts
    mid = (g0 + g1) / 2
    for a, b, side in ((g0 + 5, mid - 5, "left"), (mid + 5, g1 - 5, "right")):
        yl = y0 + 25
        L.add(f"Cage gate leaf {side}, stile", member("rhs", "z", 20, h - 10, a + 15, yl, 30, 30, 2), GALV, "made", bom, explode=ex, key="cage_gates")
        L.add(f"Cage gate leaf {side}, stile", member("rhs", "z", 20, h - 10, b - 15, yl, 30, 30, 2), GALV, "made", bom, explode=ex, key="cage_gates")
        L.add(f"Cage gate leaf {side}, bottom rail", member("rhs", "x", a + 30, b - 30, yl, 35, 30, 30, 2), GALV, "made", bom, explode=ex, key="cage_gates")
        L.add(f"Cage gate leaf {side}, top rail", member("rhs", "x", a + 30, b - 30, yl, h - 25, 30, 30, 2), GALV, "made", bom, explode=ex, key="cage_gates")
        L.add(f"Cage gate leaf {side}, mesh", mesh_xz(a + 34, b - 34, 54, h - 44, yl - 2, pitch=75), GALV, "made", bom, explode=ex, key="cage_gates")
        hx = g0 if side == "left" else g1
        for zc in (300, h - 300):
            kn, pin = cp.butt_hinge(120, 40, 3, 10, open_deg=180)
            L.add("Self-closing gate hinge", Pos(hx, y0 - 10, zc - 60) * kn, "zinc_plated", "bought", bom, explode=ex, key="gate_hinges")
    L.add("Gate hasp and padlock", bx(mid - 30, mid + 30, y0 + 2, y0 + 8, h / 2 - 60, h / 2 + 60, 1), "brass", "bought", bom, explode=ex, key="cage_gates")


# ---------------------------------------------------------------------------------------------------------
# 8 Racking bay (pallet racking 1.35 x 1.0 x 2.0 m, three levels)
# ---------------------------------------------------------------------------------------------------------
def racking_bay(L, x0, x1, y0, y1, h, n, bom=8, ex=(1600, 0, 0), levels=(150, 700, 1350)):
    k = f"rack{n}"
    up_w, up_d, e = 80, 60, 50
    for xc in (x0 + e, x1 - e):
        for yc in (y0 + e, y1 - e):
            bp = L.add(f"Racking {n} upright base plate", Pos(xc, yc, 0) * plate(100, 100, 6, r_corner=3), STEEL, "bought", bom, explode=ex, key=k)
            L.add(f"Racking {n} upright 80 x 60", member("rhs", "z", 6, h, xc, yc, up_w, up_d, 2), "safety_yellow", "bought", bom, explode=ex, color="#1F5F8B", key=k)
            for sy_ in (-40, 40):
                coach_down(L, xc, yc + sy_, 6, bp, 8, 60, bom, ex, k)
        for z in (300, h - 300):
            L.add(f"Racking {n} frame brace", member("rhs", "y", y0 + e + up_d / 2, y1 - e - up_d / 2, z, xc, 30, 30, 2),
                  "safety_yellow", "bought", bom, explode=ex, color="#1F5F8B", key=k)
    for z in levels:
        for yc in (y0 + e, y1 - e):
            L.add(f"Racking {n} beam 100 x 50", member("rhs", "x", x0 + e + up_w / 2, x1 - e - up_w / 2, yc, z - 50, 50, 100, 2), "safety_red",
                  "bought", bom, explode=ex, color="#D35400", key=k)
        L.add(f"Racking {n} deck (18 mm plywood)", bx(x0 + e + up_w / 2, x1 - e - up_w / 2, y0 + 20, y1 - 20, z, z + 18, 2), PLY, "bought", bom, explode=ex, key=k)


def desk(L, x0, x1, y0, y1, h=750, bom=9, ex=(1600, -1600, 0)):
    k = "desk"
    L.add("Passport desk top (25 mm laminated board)", bx(x0, x1, y0, y1, h - 25, h, 3), "plywood", "bought", bom, explode=ex, color="#E7E2D6", key=k)
    for xc in (x0 + 40, x1 - 40):
        for yc in (y0 + 40, y1 - 40):
            L.add("Desk leg SHS 40 x 2", member("shs", "z", 0, h - 25, xc, yc, 40, 2), STEEL, "bought", bom, explode=ex, color="#3A3A3A", key=k)
        L.add("Desk side rail SHS 40 x 2", member("shs", "y", y0 + 60, y1 - 60, h - 45, xc, 40, 2), STEEL, "bought", bom, explode=ex, color="#3A3A3A", key=k)
    L.add("Thermal label printer", bx(x0 + 100, x0 + 300, y0 + 150, y0 + 400, h, h + 160, 12), "matte_black", "bought", bom, explode=ex, key="desk_kit")
    L.add("Bench scale 30 kg (platform)", bx(x0 + 450, x0 + 800, y0 + 150, y0 + 500, h, h + 45, 6), "stainless", "bought", bom, explode=ex, key="desk_kit")
    L.add("Bench scale display", bx(x0 + 560, x0 + 690, y0 + 100, y0 + 150, h, h + 90, 5), "matte_black", "bought", bom, explode=ex, key="desk_kit")
    L.add("Laptop", bx(x0 + 850, x1 - 40, y0 + 250, y0 + 480, h, h + 18, 4), "aluminium", "bought", bom, explode=ex, key="desk_kit")
    L.add("Laptop screen", bx(x0 + 850, x1 - 40, y0 + 480, y0 + 490, h + 18, h + 230, 3), "matte_black", "bought", bom, explode=ex, key="desk_kit")
    L.add("Moisture meter", bx(x0 + 330, x0 + 410, y0 + 450, y0 + 600, h, h + 30, 6), "safety_yellow", "bought", bom, explode=ex, key="desk_kit")
