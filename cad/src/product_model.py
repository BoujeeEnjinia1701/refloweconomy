"""ReflowEconomy appearance model for photoreal scene renders (STANDARDS sections 12 and 24), TRL 3.

ReflowEconomy is a scene repository: the product is the reference micro-factory, so the hero is the whole
fitted-out floor in its real site rather than a product close-up. Every product part is components(CHOSEN)
from cad/src/model.py as it is (option A at detail level D3: the container frame and corrugated walls, the
seam beam and cleats, every machine, panel, angle, mesh, fastener and weld bead), so no dimension is typed
in again. Only appearance and site are added:

* the whole model is lifted 160 mm so the yard outside is at z = 0 (photoreal --ground-z=0) and the
  container floors stand on their bottom rails at 160 mm;
* the front wall and the roof are left out so the floor can be seen (as in the concept media);
* site context: a concrete yard slab, a concrete ramp up to the intake doors and the fan pad, all reaching
  below the ground; three 1.75 m mannequins for scale, two standing on the container floor (one at the
  shredder feed slot, one walking in the aisle) and one on the yard at the doors.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (container parts and floor markings), "internal" (the fit-out), "context" (site and people).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Plane, Polygon, Pos, Rot, extrude  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
from rfe_parts import box  # noqa: E402

P = M.PARAMS
LIFT = 160.0          # the yard is 160 mm below the container floor
TITLE = "ReflowEconomy: local micro-factory for recovered plastics"

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=48,-80", "--lens=35"]
_SITE_HOT = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=42,-125", "--lens=35"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -62, "args": _SITE,
     "note": "Site render in a concrete yard, from the front above the intake end (about 30 deg elevation), front wall "
             "and roof left out: intake and sorting, washing, the enclosed shredder with its feed hood, drying, racking "
             "and the desk in the front row; the export cage, safety station, board, extruder and press booth in the "
             "back row; two workers inside and one at the doors for scale"},
    {"name": "hot-zone", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": -118, "args": _SITE_HOT,
     "note": "Site render from the product end, above the front corner (about 24 deg elevation), front wall and roof "
             "left out: the press booth with its sliding sash, the extruder under hood B, the duct, the padded cable "
             "tray crossing over the aisle, and the fan, filter box and stack outside the back wall"},
    {"name": "studio", "groups": ["internal"], "explode": False, "el": 32, "az": -55, "args": ["--ground-z=0"],
     "note": "Studio render of the fit-out alone (no container), from the front right and above (about 32 deg "
             "elevation): every machine, enclosure, booth, rack, cage and the duct, at the positions of the layout"},
]


def _lift(shape):
    return Pos(0, 0, LIFT) * shape


def site():
    """Concrete yard, ramp to the intake doors, mannequins. Ground level is z = 0; every site part reaches below it."""
    out = []
    ctx = lambda n, sh, mat: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))
    fx, fy = P["FL_X"], P["FL_Y"]
    ctx("Concrete yard slab", box(-4000, fx + 4000, -3500, fy + 3500, -250, 0), "concrete")
    ramp = Plane.XZ * Polygon((-1400, -100), (0, -100), (0, LIFT), (-40, LIFT), (-1400, 0), align=None)
    r = extrude(ramp, amount=-(fy - 2 * P["WALL_T"] - 80))
    bb = r.bounding_box()
    r = Pos(0, P["WALL_T"] + 40 - bb.min.Y, 0) * r
    ctx("Concrete ramp to the intake doors", break_edges(r, 4), "concrete")
    try:
        import context_parts
        a_mid = P["AISLE_Y0"] + P["AISLE_W"] / 2
        feeder = Pos(6600, P["CHUTE_MOUTH_Y"] + 520, LIFT) * context_parts.mannequin(1750, "reach")
        walker = Pos(9300, a_mid - 300, LIFT) * Rot(0, 0, 90) * context_parts.mannequin(1750, "walk")
        yard = Pos(-2300, 1300, 0) * Rot(0, 0, -70) * context_parts.mannequin(1750, "stand")
        for n, s in (("Worker at the feed slot, 1.75 m (scale)", feeder), ("Worker in the aisle, 1.75 m (scale)", walker),
                     ("Person in the yard, 1.75 m (scale)", yard)):
            out.append(part(n, s, "skin", kind="context", group="context"))
    except Exception as e:  # the mannequins are for scale only; never block the product parts
        print("mannequins not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["group"] == "front_wall":
            continue
        q = dict(p)
        q["shape"] = _lift(p["shape"])
        q["group"] = "shell" if (p["bom"] == 13 or p["kind"] == "context") else "internal"
        out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    import collections
    print(len(ps), "parts;", dict(collections.Counter(p["group"] for p in ps)))
    for p in ps:
        if p["group"] == "context":
            bb = p["shape"].bounding_box()
            print(f'{p["name"]:<48} z {bb.min.Z:.0f} to {bb.max.Z:.0f}')
