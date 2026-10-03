"""ReflowEconomy appearance model for scene renders (build123d), TRL 3.

ReflowEconomy is a scene repository (STANDARDS section 12): the product is the reference
micro-factory, not a single machine, so the hero is a scene render of the whole fitted-out floor
rather than a product close-up. Every part is taken directly from cad/src/model.py (components),
so every dimension, position and the 2026-10-02 changes (feed hood on the shredder chute,
self-closing door and gate hinges, padded and taped tray crossing) come from the constructable
design and are never typed in again. Only appearance is added here: a surface material per part,
the front wall left out so the floor can be seen (as in the concept media), and two posed
mannequins for scale, standing on the floor.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Axes as model.py: X along the line from the intake end, Y from the front wall to the back wall,
Z up, mm, floor at Z = 0.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Pos, Rot  # noqa: E402
from context_parts import mannequin  # noqa: E402
from model import PARAMS as P, box, components  # noqa: E402

TITLE = "ReflowEconomy: local micro-factory for recovered plastics"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -62,
     "note": "Scene render from the front, above the intake end (about 30 deg elevation), front wall left out: "
             "intake and sorting, washing, the enclosed shredder with its feed hood, drying, racking and the desk "
             "in the front row; the export cage, safety station, board, extruder and press booth in the back row; "
             "workers for scale"},
    {"name": "hot-zone", "groups": ["shell", "internal", "context"], "explode": False, "el": 24, "az": -118,
     "note": "Scene render from the product end, above the front corner (about 24 deg elevation), front wall left "
             "out: the press booth with its sliding sash, the extruder under hood B, the duct and the padded cable "
             "tray crossing over the aisle"},
]

# Surface materials by component key (photoreal.py classes); colours stay those of model.py
MATERIAL = {
    "shell": "painted", "seam_beam": "painted", "seam_plate": "metal", "markings": "painted",
    "scale": "painted", "table": "metal", "wash": "plastic", "shred_enc": "painted", "shredder": "painted",
    "enc_door": "painted", "door_hinges": "metal", "chute": "painted", "chute_hood": "painted", "chute_lid": "painted",
    "rack_dry": "metal", "dry_stand": "painted", "dry_fan": "painted", "extruder": "painted", "hood_b": "metal",
    "press_hot": "painted", "press_cool": "painted", "bridge": "metal", "booth": "painted", "rails": "metal",
    "sash": "clear", "duct": "metal", "takeoff": "metal", "sleeve": "metal", "duct_brackets": "metal",
    "fan_stand": "painted", "fan": "painted", "stack": "metal", "rack1": "painted", "rack2": "painted",
    "lots1": "plastic", "lots2": "fabric", "desk": "wood", "desk_kit": "plastic", "ppe": "painted",
    "eyewash": "plastic", "backboard": "wood", "board": "painted", "tray": "metal", "tray_spacers": "metal",
    "tray_pad": "rubber", "tray_tape": "rubber", "cage": "metal", "cage_gates": "metal", "gate_hinges": "metal",
    "cage_kit": "fabric",
}
SHELL_KEYS = ("shell", "seam_beam", "seam_plate", "markings")
FRONT_WALL = box(-1, P["FL_X"] + 1, -1, P["WALL_T"] + 0.5, 0, P["WALL_H"] + 1)


def _people():
    """Two workers for scale, standing on the floor: one at the shredder feed slot facing it, one
    walking along the aisle toward the product end. Positions come from model.py."""
    a_mid = P["AISLE_Y0"] + P["AISLE_W"] / 2
    feeder = Pos(6600, P["CHUTE_MOUTH_Y"] + 520, 1) * mannequin(1750, "reach")          # faces -Y, toward the slot
    walker = Pos(9300, a_mid - 300, 1) * Rot(0, 0, 90) * mannequin(1750, "walk")          # faces +X along the aisle
    return [("Worker at the feed slot (1.75 m, scale)", feeder), ("Worker in the aisle (1.75 m, scale)", walker)]


def product_parts():
    """Named parts for the renders: dicts with name, shape, color, material, group and bom."""
    out = []
    for key, (bom, name, shape, colour) in components(P).items():
        if key == "shell":
            shape = shape - FRONT_WALL
            name = "Building shell (front wall left out)"
        out.append(dict(name=name, shape=shape, color=colour, material=MATERIAL.get(key, "plastic"),
                        group="shell" if key in SHELL_KEYS else "internal", bom=bom or None))
    for name, shape in _people():
        out.append(dict(name=name, shape=shape, color="#B8B2A7", material="clay", group="context", bom=None))
    return out


if __name__ == "__main__":
    for p in product_parts():
        bb = p["shape"].bounding_box()
        print(f'{p["name"]:<48} {p["group"]:<9} {p["material"]:<8} z {bb.min.Z:.0f} to {bb.max.Z:.0f}')
