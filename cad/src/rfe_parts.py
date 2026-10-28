"""ReflowEconomy modelling helpers for the kit 1.9 detailed model (repo-specific; the kit's parts library
is .kit/cad_parts.py and is used for every stock section and fastener here).

Every helper returns build123d solids in millimetres in the model frame of cad/src/model.py (X along the
line from the intake end, Y from the front wall to the back wall, Z up, finished floor at Z = 0), or lists
of cad_parts.part() dicts. Members are placed by axis and end coordinates so that the geometry reads like
a cutting list: "SHS 40 x 3 along Z from 0 to 1800 at x 7720, y 220".
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Circle, Compound, Cylinder, Location, Plane, Polygon, Pos, Rectangle,  # noqa: E402
                       RectangleRounded, RegularPolygon, Rot, Sketch, extrude)
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402

AX = {"x": ((0, 1, 0), (1, 0, 0)), "y": ((0, 0, 1), (0, 1, 0)), "z": ((1, 0, 0), (0, 0, 1))}


def on_axis(shape, axis, origin):
    """Place a shape built along +Z (profile in XY) so that its +Z runs along the global axis.
    Local (u, v, w) map to: axis x -> (Y, Z, X); axis y -> (Z, X, Y); axis z -> (X, Y, Z)."""
    xd, zd = AX[axis]
    return Plane(origin=origin, x_dir=xd, z_dir=zd).location * shape


def _uvw(axis, a, c1, c2):
    """Global point from (along-axis coordinate a, first cross coordinate c1, second c2)."""
    if axis == "x":
        return (a, c1, c2)
    if axis == "y":
        return (c2, a, c1)
    return (c1, c2, a)


def brk(shape, r=1.0):
    """Break every edge by r mm with a chamfer (a fillet where a chamfer fails). Chamfers keep the faces planar,
    which keeps the STEP files of a 1,000-part layout small; a sawn or folded edge is broken this way anyway."""
    from build123d import chamfer, fillet
    for op in (chamfer, fillet):
        try:
            out = op(shape.edges(), r)
            ok = out.is_valid() if callable(out.is_valid) else out.is_valid
            if ok:
                return out
        except Exception:
            pass
    return shape


def brk_long(shape, r, dims):
    """Chamfer only the edges that run along the longest of dims (dx, dy, dz): the four long edges of a
    block, the arrises a saw or folder leaves. Fewer faces than breaking every edge, so the 1,000-part
    assembly STEP stays under the size limit."""
    from build123d import Axis, chamfer
    ax = (Axis.X, Axis.Y, Axis.Z)[max(range(3), key=lambda i: dims[i])]
    try:
        out = chamfer(shape.edges().filter_by(ax), r)
        ok = out.is_valid() if callable(out.is_valid) else out.is_valid
        if ok:
            return out
    except Exception:
        pass
    return brk(shape, r)


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def bx(x0, x1, y0, y1, z0, z1, r=1.0):
    """Axis-aligned block with broken edges (a real sawn, folded or moulded part, never a bare box)."""
    t = min(x1 - x0, y1 - y0, z1 - z0)
    return brk_long(box(x0, x1, y0, y1, z0, z1), min(r, t / 3.0), (x1 - x0, y1 - y0, z1 - z0))


def shell_box(x0, x1, y0, y1, z0, z1, wall, open_top=True, r=2.0):
    """Moulded or fabricated open-top tub: walls and floor of thickness 'wall', edges broken."""
    outer = box(x0, x1, y0, y1, z0, z1)
    inner = box(x0 + wall, x1 - wall, y0 + wall, y1 - wall, z0 + wall, z1 + (1 if open_top else -wall))
    return brk_long(outer - inner, min(r, wall / 3.0), (x1 - x0, y1 - y0, z1 - z0))


def member(kind, axis, a0, a1, c1, c2, *dims):
    """A stock member along an axis from a0 to a1, profile centred on (c1, c2) in the cross plane
    (for axis x the cross plane is (y, z); for y it is (z, x); for z it is (x, y)).
    kind: shs (a, t), rhs (w, h, t) with w along the first cross axis, tube (od, t), bar (d), flat (w, t)."""
    L = a1 - a0
    if kind == "shs":
        s = cp.shs(dims[0], dims[1], L)
    elif kind == "rhs":
        s = cp.rhs(dims[0], dims[1], dims[2], L)
    elif kind == "tube":
        s = cp.round_tube(dims[0], dims[1], L)
    elif kind == "bar":
        s = cp.round_bar(dims[0], L)
    elif kind == "flat":
        s = cp.flat_bar(dims[0], dims[1], L)
    else:
        raise ValueError(kind)
    return on_axis(s, axis, _uvw(axis, a0, c1, c2))


def angle_member(axis, a0, a1, c1, c2, s1=1, s2=1, a=40.0, t=4.0, b=None):
    """Equal or unequal angle along an axis, heel at (c1, c2) in the cross plane, legs running in the s1
    direction of the first cross axis and the s2 direction of the second (s = +1 or -1)."""
    b = a if b is None else b
    pts = [(0, 0), (a, 0), (a, t), (t, t), (t, b), (0, b)]
    pts = [(s1 * u, s2 * v) for u, v in pts]
    if s1 * s2 < 0:
        pts = pts[::-1]
    prof = Polygon(*pts, align=None)
    return on_axis(extrude(prof, a1 - a0), axis, _uvw(axis, a0, c1, c2))


def channel_member(axis, a0, a1, c1, c2, h, b, t, s1=1, s2=1, tf=None):
    """Parallel-flange channel: web along the second cross axis (height h, centred on c2), flanges of width
    b running in the s1 direction of the first cross axis from the web's back face at c1."""
    tf = tf or t * 1.4
    pts = [(0, -h / 2), (b, -h / 2), (b, -h / 2 + tf), (t, -h / 2 + tf), (t, h / 2 - tf), (b, h / 2 - tf), (b, h / 2), (0, h / 2)]
    pts = [(s1 * u, s2 * v) for u, v in pts]
    if s1 * s2 < 0:
        pts = pts[::-1]
    return on_axis(extrude(Polygon(*pts, align=None), a1 - a0), axis, _uvw(axis, a0, c1, c2))


def ibeam(axis, a0, a1, c1, c2, h, b, tw, tf, r=8.9):
    """Universal beam (I section) along an axis, depth h along the second cross axis, flange width b along
    the first, centred on (c1, c2)."""
    pts = [(-b / 2, -h / 2), (b / 2, -h / 2), (b / 2, -h / 2 + tf), (tw / 2, -h / 2 + tf), (tw / 2, h / 2 - tf),
           (b / 2, h / 2 - tf), (b / 2, h / 2), (-b / 2, h / 2), (-b / 2, h / 2 - tf), (-tw / 2, h / 2 - tf),
           (-tw / 2, -h / 2 + tf), (-b / 2, -h / 2 + tf)]
    s = extrude(Polygon(*pts, align=None), a1 - a0)
    try:
        from build123d import Axis, fillet
        inner = [e for e in s.edges().filter_by(Axis.Z) if abs(abs(e.center().X) - tw / 2) < 0.01]
        s = fillet(inner, r)
    except Exception:
        pass
    return on_axis(s, axis, _uvw(axis, a0, c1, c2))


def corrugated(axis, a0, a1, c1, c2, height, depth=36.0, pitch=278.0, t=2.0, s2=1):
    """Corrugated container wall sheet (trapezoidal profile) running along 'axis' from a0 to a1, from c2 up
    'height' along Z, the corrugations standing out in the s2 direction of the first cross axis from c1.
    The profile repeats every 'pitch' mm of the wall length."""
    # profile in the plane (along-wall, outward) extruded up the height; build in local XY then place
    n = max(1, int((a1 - a0) // pitch))
    p = (a1 - a0) / n
    flat, slope = 0.36 * p, 0.14 * p
    top = []
    for i in range(n):
        x = i * p
        top += [(x, 0), (x + flat, 0), (x + flat + slope, depth), (x + 2 * flat + slope, depth), (x + p, 0)]
    pts = []
    for q in top:
        if not pts or pts[-1] != q:
            pts.append(q)
    outer = pts
    inner = [(x, y + t) for x, y in reversed(outer)]
    prof = Polygon(*(outer + inner), align=None)
    s = extrude(prof, height)                         # local x along the wall, y outward, z up
    s = s.mirror(Plane.XZ) if s2 < 0 else s
    if axis == "x":
        return Pos(a0, c1, c2) * s
    return Pos(c1, a0, c2) * Rot(0, 0, 90) * s.mirror(Plane.XZ)


def drill(shape, origin, direction, d, depth=4000.0):
    """Subtract a round hole of diameter d from origin along direction (both ways by depth/2)."""
    ax = max(range(3), key=lambda i: abs(direction[i]))
    axis = "xyz"[ax]
    o = list(origin)
    o[ax] -= depth / 2
    return shape - on_axis(Pos(0, 0, depth / 2) * Cylinder(d / 2, depth), axis, tuple(o))


def _frame(origin, direction):
    """Plane whose local -Z runs along 'direction' (a unit axis vector) and whose origin is 'origin'."""
    dx, dy, dz = direction
    z = (-dx, -dy, -dz)
    x = (1, 0, 0) if abs(dx) < 0.9 else (0, 1, 0)
    return Plane(origin=origin, x_dir=x, z_dir=z)


# Fasteners and welds are drawn with plain solids at their ISO dimensions (cad_parts.ISO): hex prisms without
# the 30 degree chamfer and beads without the rounded crown, so the assembly STEP files stay under the size
# limit (a chamfered kit fastener is about 44 kB of STEP each; this repo has about 300 of them).
def _hex_plain(s_af, h):
    return extrude(RegularPolygon(s_af / math.sqrt(3), 6), h)


def plain_bolt(d, length):
    s_af, k = cp.ISO[d][0], cp.ISO[d][1]
    return _hex_plain(s_af, k) + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def plain_nut(d):
    s_af, m = cp.ISO[d][0], cp.ISO[d][2]
    return _hex_plain(s_af, m) - Pos(0, 0, m / 2) * Cylinder(d / 2, m)


def plain_washer(d):
    d2, h = cp.ISO[d][3], cp.ISO[d][4]
    return Pos(0, 0, h / 2) * (Cylinder(d2 / 2, h) - Cylinder(d * 0.54, h))


def plain_bolt_set(d, grip):
    """As cad_parts.hex_bolt_set (same lengths and positions), in plain solids."""
    s_af, k, m, d2, h, pt = cp.ISO[d]
    L = math.ceil((grip + 2 * h + m + 2.5 * pt) / 5) * 5
    return [(f"M{d}x{L} hex bolt (ISO 4017)", Pos(0, 0, h) * plain_bolt(d, L)),
            (f"M{d} washer (ISO 7089)", plain_washer(d)),
            (f"M{d} washer (ISO 7089)", Pos(0, 0, -grip - h) * plain_washer(d)),
            (f"M{d} hex nut (ISO 4032)", Pos(0, 0, -grip - h - m) * plain_nut(d))]


def plain_anchor(d, embed):
    s_af, k, m, d2, h, pt = cp.ISO[d]
    stud = Pos(0, 0, (m + h + 2 * pt - embed) / 2) * Cylinder(d / 2, embed + m + h + 2 * pt)
    return stud + plain_washer(d) + Pos(0, 0, h) * plain_nut(d)


def bolt_set(d, grip, origin, direction, bom=None, group="fixings", note=""):
    """ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut clamping a joint 'grip' thick. The head sits
    on the joint face at 'origin' and the bolt points along 'direction' (unit axis vector) into the joint."""
    loc = _frame(origin, direction).location
    return [part(n, loc * s, "zinc_plated", kind="fastener", bom=bom, group=group, note=note)
            for n, s in plain_bolt_set(d, grip)]


def screw(d, length, origin, direction, name="screw", bom=None, group="fixings", material="zinc_plated"):
    """Hex head screw or coach screw (no nut): head on the face at origin, shank along direction."""
    loc = _frame(origin, direction).location
    s = plain_bolt(d, length)
    return part(name, loc * s, material, kind="fastener", bom=bom, group=group)


def weld(origin, run, leg1, leg2, length, size=4.0, bom=None, group="welds", name="Fillet weld"):
    """Fillet weld bead of leg 'size' along 'run' from origin for 'length', its legs lying along leg1 and
    leg2 (unit axis vectors pointing away from the two joined faces into the corner's open side)."""
    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
    o = tuple(origin)
    if tuple(round(c) for c in cross(leg2, run)) != tuple(leg1):
        o = tuple(o[i] + run[i] * length for i in range(3))
        run = tuple(-c for c in run)
    pl = Plane(origin=o, x_dir=run, z_dir=leg2)
    bead = Rot(90, 0, 0) * Rot(0, 90, 0) * extrude(Polygon((0, 0), (size, 0), (0, size), align=None), length)
    return part(name, pl.location * bead, "mild_steel", kind="weld", bom=bom, group=group)


def post_foot_welds(x, y, z, a, bom=None, size=4.0, name="Post foot weld"):
    """Four fillet beads round the foot of a square post of side a centred at (x, y), on a plate top at z."""
    h = a / 2
    return [weld((x - h, y - h, z), (1, 0, 0), (0, -1, 0), (0, 0, 1), a, size, bom, name=name),
            weld((x - h, y + h, z), (1, 0, 0), (0, 1, 0), (0, 0, 1), a, size, bom, name=name),
            weld((x - h, y - h, z), (0, 1, 0), (-1, 0, 0), (0, 0, 1), a, size, bom, name=name),
            weld((x + h, y - h, z), (0, 1, 0), (1, 0, 0), (0, 0, 1), a, size, bom, name=name)]


def mesh_xz(x0, x1, z0, z1, y, pitch=75.0, wire=4.0):
    """Welded wire mesh in a plane of constant y (wires along X and Z), as one part."""
    rods = []
    nx = max(1, int(round((x1 - x0) / pitch)))
    nz = max(1, int(round((z1 - z0) / pitch)))
    for i in range(nx + 1):
        x = x0 + (x1 - x0) * i / nx
        rods.append(Pos(x, y, (z0 + z1) / 2) * Cylinder(wire / 2, z1 - z0))
    for j in range(nz + 1):
        z = z0 + (z1 - z0) * j / nz
        rods.append(Pos((x0 + x1) / 2, y + wire, z) * Rot(0, 90, 0) * Cylinder(wire / 2, x1 - x0))
    return Compound(rods)


def mesh_yz(y0, y1, z0, z1, x, pitch=75.0, wire=4.0):
    """Welded wire mesh in a plane of constant x (wires along Y and Z), as one part."""
    rods = []
    ny = max(1, int(round((y1 - y0) / pitch)))
    nz = max(1, int(round((z1 - z0) / pitch)))
    for i in range(ny + 1):
        y = y0 + (y1 - y0) * i / ny
        rods.append(Pos(x, y, (z0 + z1) / 2) * Cylinder(wire / 2, z1 - z0))
    for j in range(nz + 1):
        z = z0 + (z1 - z0) * j / nz
        rods.append(Pos(x + wire, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(wire / 2, y1 - y0))
    return Compound(rods)


def mesh_xy(x0, x1, y0, y1, z, pitch=60.0, wire=3.0):
    """Welded wire mesh in a plane of constant z (a tray bottom), as one part."""
    rods = []
    nx = max(1, int(round((x1 - x0) / pitch)))
    ny = max(1, int(round((y1 - y0) / pitch)))
    for i in range(nx + 1):
        x = x0 + (x1 - x0) * i / nx
        rods.append(Pos(x, (y0 + y1) / 2, z + wire / 2) * Rot(90, 0, 0) * Cylinder(wire / 2, y1 - y0))
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        rods.append(Pos((x0 + x1) / 2, y, z + 1.5 * wire) * Rot(0, 90, 0) * Cylinder(wire / 2, x1 - x0))
    return Compound(rods)


def frustum_hopper(x0, x1, y0, y1, z0, z1, top_grow, t=2.0):
    """Sheet hopper: a hollow frustum whose bottom is the rectangle x0..x1, y0..y1 at z0 and whose top is
    that rectangle grown by top_grow on every side at z1."""
    from build123d import loft, Plane as Pl
    g = top_grow
    lo = Pl.XY.offset(z0) * Rectangle(x1 - x0, y1 - y0)
    hi = Pl.XY.offset(z1) * Rectangle(x1 - x0 + 2 * g, y1 - y0 + 2 * g)
    outer = loft([lo, hi])
    lo2 = Pl.XY.offset(z0 - 1) * Rectangle(x1 - x0 - 2 * t, y1 - y0 - 2 * t)
    hi2 = Pl.XY.offset(z1 + 1) * Rectangle(x1 - x0 + 2 * g - 2 * t, y1 - y0 + 2 * g - 2 * t)
    inner = loft([lo2, hi2])
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, 0) * (outer - inner)


def cyl(axis, a0, a1, c1, c2, r):
    """Solid cylinder along an axis (for discs, platens, motors); edges broken so it is a real part.
    c1, c2 are the other two coordinates in x, y, z order (for axis y: x then z)."""
    if axis == "y":
        c1, c2 = c2, c1
    return brk(on_axis(Pos(0, 0, (a1 - a0) / 2) * Cylinder(r, a1 - a0), axis, _uvw(axis, a0, c1, c2)), 1.5)


def ring(axis, a0, a1, c1, c2, ro, ri):
    """Ring along an axis; c1, c2 as in cyl()."""
    if axis == "y":
        c1, c2 = c2, c1
    s = Pos(0, 0, (a1 - a0) / 2) * (Cylinder(ro, a1 - a0) - Cylinder(ri, a1 - a0))
    return brk(on_axis(s, axis, _uvw(axis, a0, c1, c2)), 0.8)


def hollow(x0, x1, y0, y1, z0, z1, t, r=2.0):
    """Closed hollow block (a bag or bale drawn as its skin) with broken edges; t is chosen so the part's
    mass is the real mass of the bag or bale."""
    outer = box(x0, x1, y0, y1, z0, z1)
    inner = box(x0 + t, x1 - t, y0 + t, y1 - t, z0 + t, z1 - t)
    return brk_long(outer - inner, min(r, t / 3.0), (x1 - x0, y1 - y0, z1 - z0))


def plate(w, h, t, holes=(), r_corner=3.0, edge=0.4):
    """Flat plate w (X) x h (Y) x t (Z from 0) centred on the origin, holes [(x, y, d), ...] from the centre,
    every edge chamfered (corner cut r_corner, edges min(1, t/3)). Same call as cad_parts.sheet, but with
    planar breaks so the many foot and base plates keep the assembly STEP small."""
    s_ = Pos(0, 0, t / 2) * Box(w, h, t)
    for x, y, d in holes:
        s_ = s_ - Pos(x, y, t / 2) * Cylinder(d / 2, t + 2)
    return brk_long(s_, min(1.0, t / 3.0), (0, 0, 1))   # the four corner edges of the plate
