"""ReflowEconomy prototype build plan pictures (RFE-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/RFE-DWG-101 to 111        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
A single picture can be drawn with e.g. "sheets:105" or "joints:3" or "steps:7" to save memory.
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, box, components  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
C = components(P)
FY, T = P["FL_Y"], P["WALL_T"]
FRONT_WALL = box(-1, P["FL_X"] + 1, -1, T + 0.5, -200, P["WALL_H"] + 1)


def sh(*keys):
    out = None
    for k in keys:
        s = C[k][2]
        out = s if out is None else out + s
    return out


def col(key):
    return C[key][3]


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    """The piece of a shape inside a window box (for close-ups and local context)."""
    return shape & box(x0, x1, y0, y1, z0, z1)


def shell_open():
    """The shell with its front wall left out, so the inside can be seen."""
    return C["shell"][2] - FRONT_WALL


def ctx(x0, x1, y0=-1, y1=None, z0=-200, z1=None):
    """Local piece of the open shell for orientation."""
    return part("Building", win(shell_open(), x0, x1, y0, FY + 1 if y1 is None else y1, z0, P["WALL_H"] + 1 if z1 is None else z1), "#E7E5E4")


# ----------------------------------------------------------------- named components, in build order
ORDER = [
    ("shell", "Building shell (front wall left out)", ["shell"], (0, 0, 0)),
    ("seam_beam", "Seam beam (engineer's design)", ["seam_beam"], (0, -400, 1500)),
    ("seam_plate", "Floor seam cover plate", ["seam_plate"], (0, -300, 500)),
    ("markings", "Floor markings", ["markings"], (0, 0, 250)),
    ("safety", "Safety station: cabinet, eyewash, extinguishers", ["ppe", "eyewash", "extinguisher_1", "extinguisher_2", "extinguisher_3"], (0, 0, 900)),
    ("backboard", "Backboard", ["backboard"], (0, 0, 1500)),
    ("board", "Electrical board", ["board"], (0, -500, 1500)),
    ("tray", "Cable tray and spacers", ["tray", "tray_spacers"], (0, 0, 1900)),
    ("tray_pad", "Tray crossing padding and hazard tape", ["tray_pad", "tray_tape"], (0, 0, 2500)),
    ("extruder", "Extruder", ["extruder"], (0, 0, 600)),
    ("hood_b", "Hood B", ["hood_b"], (0, 0, 1300)),
    ("presses", "Sheet press and cooling press", ["press_hot", "press_cool"], (0, 0, 500)),
    ("bridge", "Transfer bridge", ["bridge"], (0, -700, 900)),
    ("booth", "Press booth (hood A)", ["booth"], (0, 0, 2400)),
    ("sash", "Sash rails and sliding sash", ["rails", "sash"], (0, -1100, 2400)),
    ("duct", "Duct, brackets, take-off, sleeve", ["duct", "takeoff", "sleeve", "duct_brackets"], (0, 0, 3600)),
    ("fan", "Fan stand, fan and filter box, stack", ["fan_stand", "fan", "stack"], (0, 900, 0)),
    ("shredder", "Shredder", ["shredder"], (0, -2300, 0)),
    ("enclosure", "Acoustic enclosure, door and hinges, chute, feed hood", ["shred_enc", "enc_door", "door_hinges", "chute", "chute_hood", "chute_lid"], (0, -2300, 1900)),
    ("wash", "Washing tanks and trap", ["wash"], (0, -2300, 0)),
    ("dryer", "Drying rack and fan on its stand", ["rack_dry", "dry_stand", "dry_fan"], (0, -2300, 0)),
    ("intake", "Intake: scale, sorting table, bins", ["scale", "table", "bin_pet", "bin_hdpe", "bin_pp", "bin_metals"], (0, -2300, 0)),
    ("racking", "Racking with flake bags and products", ["rack1", "rack2", "lots1", "lots2"], (0, 0, 0)),
    ("desk", "Passport and quality desk", ["desk", "desk_kit"], (0, -2300, 0)),
    ("cage", "Export cage, gates, sand container", ["cage", "cage_gates", "gate_hinges", "cage_kit"], (0, 0, 700)),
]


def named(key):
    for k, name, keys, off in ORDER:
        if k == key:
            s = shell_open() if k == "shell" else sh(*keys)
            return part(name, s, col(keys[0]), off)
    raise KeyError(key)


# ----------------------------------------------------------------- overview
def overview():
    parts = [named(k) for k, *_ in ORDER]
    parts[0].color = "#E7E5E4"
    return bv.overview(parts, OUT / "overview.png", "ReflowEconomy reference micro-factory: every component, pulled apart",
                       subtitle="Numbered in build order. Front row pulled toward you, wall and overhead parts lifted. Seen from the front right and above",
                       elev=32, azim=-68, size=(15, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    base = dict(project="ReflowEconomy", date=DATE)
    out = []

    def make(no, *a, **k):
        if only is None or only == no:
            out.append(bv.component_sheet(*a, dwg_no=f"RFE-DWG-{no}", **{**base, **k}))

    # 101 floor seam cover plate (one of four lengths)
    one = C["seam_plate"][2].solids()[0]
    make(101, part("Floor seam cover plate", one, col("seam_plate")),
         [ctx(0, 3300, 1500, 3400), part("Seam beam", win(C["seam_beam"][2], 0, 3300, 0, FY, 0, 3000), GH)],
         title="ReflowEconomy floor seam cover plate (make 4): making sketch",
         material="Aluminium tread plate 4.5 mm, 5754 class", view_shape=one, inset_view=(30, -60),
         notes=["Container option only; a rented shed needs none.",
                "Make four lengths, each 3005 x 300 mm, from 4.5 mm tread plate.",
                "Laid end to end along the seam with 4 mm gaps; the four lengths",
                "  run the full 12,032 mm between the end walls.",
                "Chamfer both long edges 2 mm at 45 degrees so trolleys roll over.",
                "Drill and countersink 6.5 mm holes along ONE long edge only, 30 mm",
                "  in from the edge, 150 mm from each end and at 300 mm pitch.",
                "Fit: centre on the seam, screw down with M6 x 40 countersunk wood",
                "  screws into the floor of the intake-side container only, so the",
                "  two containers can move a little without tearing the plate.",
                "Check: the plate lies flat with no edge more than 1 mm proud."])

    # 102 backboard
    make(102, part("Backboard", C["backboard"][2], col("backboard")),
         [ctx(3000, 5000, 4000), part("Electrical board", C["board"][2], GH), part("Eyewash", C["eyewash"][2], GH),
          part("Cabinet", C["ppe"][2], GH)],
         title="ReflowEconomy backboard: making sketch", material="Fire-retardant plywood 18 mm",
         inset_view=(25, -70),
         notes=["One 1300 x 1550 mm sheet of 18 mm fire-retardant plywood.",
                "Seal both faces and all edges with two coats of paint.",
                "Drill six 9 mm holes: 100, 650 and 1200 mm from the left edge,",
                "  in two rows 100 and 1450 mm up from the bottom edge. Move each",
                "  hole sideways up to 40 mm so it lands on a corrugation crest.",
                "Fit: bottom edge 600 mm above the floor, left edge 3350 mm from the",
                "  outside of the intake end, on the back wall; M8 rivet nuts in crests,",
                "  M8 x 30 screws with large washers.",
                "Board area: 550 to 1250 mm from the left edge, 600 to 1400 mm up.",
                "Eyewash: 50 to 400 mm from the left edge, 200 to 700 mm up.",
                "Cable tray runs along the front face at the top, 1438 mm up.",
                "Check: the board is flat and does not rock on the corrugations."])

    # 103 hood B
    make(103, part("Hood B", C["hood_b"][2], col("hood_b")),
         [part("Extruder", C["extruder"][2], GH), part("Duct riser", win(C["duct"][2], 6400, 6750, 4100, 4600, 1300, 1700), GH)],
         title="ReflowEconomy hood B (extruder barrel enclosure): making sketch",
         material="Galvanised steel sheet 1.5 mm on 20 x 20 x 3 angle frame", view_shape=C["hood_b"][2],
         inset_view=(25, -60),
         notes=["Open-bottomed box 1000 long, 500 deep, 450 high, 20 mm walls:",
                "  1.5 mm galvanised sheet riveted to a 20 x 20 x 3 angle frame.",
                "Front (aisle) face: opening 800 x 400, 100 in from each end,",
                "  20 above the bottom edge. Fold the opening edges back 15 mm.",
                "Hopper end: 120 mm hole for the barrel, centre 250 from the front",
                "  face and 150 above the bottom edge (10 mm clear of the barrel).",
                "Top: cut-out for a 250 mm duct spigot, centre 575 from the hopper",
                "  end and 350 from the front face; rivet the spigot on.",
                "Bottom flange: 20 x 20 angle, six 9 mm holes for M8 bolts.",
                "Fit: stands on the extruder frame top (900 mm up), bolted down;",
                "  the hopper stays outside, against the hopper end.",
                "Check: the barrel turns clear of the hole all round."])

    # 104 transfer bridge
    make(104, part("Transfer bridge", C["bridge"][2], col("bridge")),
         [part("Sheet press", C["press_hot"][2], GH), part("Cooling press", C["press_cool"][2], GH)],
         title="ReflowEconomy transfer bridge: making sketch", material="Steel angle 30 x 30 x 3 and one 40 mm roller",
         inset_view=(75, -60),
         notes=["A 50 x 900 mm frame of 30 x 30 x 3 angle, 50 mm deep overall.",
                "One 40 mm steel roller, 880 mm long, on two sealed bearings in",
                "  the frame ends; roller top 950 mm above the floor, level with",
                "  both platens. Check your presses and set this height to suit.",
                "Two 9 mm holes in the end that meets the hot press frame.",
                "Fit: bolted to the side of the hot press frame with two M8 bolts;",
                "  the other edge rests against the cooling press frame.",
                "The mould slides from the hot press over the roller onto the",
                "  cooling press without being lifted.",
                "Check: a straight edge laid across both platens and the roller",
                "  touches all three; nothing steps up by more than 1 mm."])

    # 105 press booth
    make(105, part("Press booth", C["booth"][2], col("booth")),
         [ctx(6800, 10200, 2800), part("Presses", sh("press_hot", "press_cool"), GH), part("Hood B", C["hood_b"][2], GH)],
         title="ReflowEconomy press booth (hood A): making sketch",
         material="Galvanised sheet 1.5 mm on 40 x 40 x 4 angle frame, 60 mm panels", inset_view=(25, -60),
         notes=["Front 2450 x 2300, two ends 1596 x 2300, roof 2450 x 1596: panels",
                "  of 1.5 mm galvanised sheet on 40 x 40 x 4 angle, 60 mm overall.",
                "  No back panel: the container wall closes the booth.",
                "Front: opening 1, 1200 x 600, 80 to 1280 from the left end;",
                "  opening 2, 1040 x 600, 1330 to 2370 from the left end; both",
                "  900 to 1500 mm above the floor. Frame every opening.",
                "Left end: 270 x 270 hole for the duct, 1015 to 1285 from the",
                "  front face, 1915 to 2185 up; seal the duct with a rubber collar.",
                "Roof: one rafter of the same angle at mid-length.",
                "Bolt the panels together through the frames with M8 bolts.",
                "Fit: cleats of 40 x 40 angle screwed to the floor at 600 pitch;",
                "  back edges on rivet nuts in the wall, closed-cell foam strip",
                "  cut to the corrugations. Put the presses in first.",
                "Check: no gap wider than 5 mm round the panels with the fan off."])

    # 106 sash and rails
    make(106, part("Sliding sash and rails", sh("rails", "sash"), col("sash")),
         [part("Press booth", win(C["booth"][2], 7000, 10000, 3100, 3400, 0, 2400), GH)],
         title="ReflowEconomy sliding sash and rails: making sketch",
         material="Galvanised sheet 1.5 mm; aluminium channel 30 x 30 x 2", inset_view=(15, -60),
         notes=["Rails: two 2600 mm lengths of 30 x 30 x 2 aluminium channel,",
                "  open sides facing each other; screw to the booth front with",
                "  M6 screws at 400 pitch, the lower rail 845 to 875 mm up, the",
                "  upper rail 1525 to 1555 mm up, from 0 to 2600 along the booth",
                "  front (running 150 mm past its right end). End stop each end.",
                "Sash: one panel 1250 x 650 of 1.5 mm galvanised sheet with all",
                "  edges folded 15 mm; two handles; edges run inside the channels.",
                "There is only one sash, so only one opening is open at a time:",
                "  over opening 2 to press, over opening 1 to cool and unload.",
                "Check: the sash slides end to end with one hand and covers each",
                "  opening with at least 25 mm to spare on both sides."])

    # 107 duct wall bracket
    one = C["duct_brackets"][2].solids()[0]
    make(107, part("Duct wall bracket", one, col("duct_brackets")),
         [ctx(6500, 7100, 4000, FY, 1500), part("Duct", win(C["duct"][2], 6500, 7100, 4000, FY, 1500, 2400), GH)],
         title="ReflowEconomy duct wall bracket (make 2): making sketch",
         material="Steel equal angle 50 x 50 x 5, plate 150 x 100 x 6", view_shape=one, inset_view=(20, -50),
         notes=["Make two. Arm: 571 mm of 50 x 50 x 5 angle, one leg flat on top",
                "  for the duct to sit on.",
                "Weld a 150 x 100 x 6 mm wall plate square to one end; two 11 mm",
                "  holes in it, 100 mm apart, for M10 rivet nuts in the wall.",
                "Drill two 9 mm holes 125 mm apart near the free end for the",
                "  M8 duct strap.",
                "Fit: arm horizontal, top 1925 mm above the floor, at 6775 and 7700 mm",
                "  from the outside of the intake end (either side of the booth wall).",
                "The duct sits on the arm and is strapped down; the arm reaches",
                "  from the wall to the duct's front face.",
                "Paint or galvanise after welding.",
                "Check: the duct runs level and the joints do not sag."])

    # 108 fan stand
    make(108, part("Fan stand", C["fan_stand"][2], col("fan_stand")),
         [ctx(7200, 9100, 4300, FY + 900), part("Fan and filter box", C["fan"][2], GH), part("Stack", C["stack"][2], GH)],
         title="ReflowEconomy fan stand (outside): making sketch", material="Steel SHS 50 x 50 x 3, angle 30 x 30 x 3",
         inset_view=(25, 120),
         notes=["Footprint 1000 x 700 mm, top frame 1750 mm above the ground.",
                "Four legs of 50 x 50 x 3 SHS, 1700 long, with 150 x 150 x 8",
                "  base plates (four 12 mm holes each).",
                "Top frame of the same tube, welded all round, 50 mm deep.",
                "One diagonal brace of 30 x 30 x 3 angle on each long side.",
                "Galvanise or paint after welding.",
                "Fit: bolted with M10 anchors to a concrete pad outside the back",
                "  wall, its near legs 80 mm from the wall, centred on the duct",
                "  hole (centre 8150 mm from the outside of the intake end).",
                "The fan and filter box bolts to the top frame (M10, four places);",
                "  the stack goes on the fan outlet and ends 1 m above the roof.",
                "Check: the frame is level and does not rock under a hand push."])

    # 109 acoustic enclosure
    enc = sh("shred_enc", "enc_door", "door_hinges", "chute", "chute_hood", "chute_lid")
    make(109, part("Acoustic enclosure", enc, col("shred_enc")),
         [part("Shredder", C["shredder"][2], GH), ctx(5300, 7900, -1, 2400)],
         title="ReflowEconomy shredder acoustic enclosure: making sketch",
         material="Lined panels 60 mm: steel skin, 50 mm mineral wool, perforated liner",
         inset_view=(25, -60),
         notes=["Box 1600 x 1400 x 1600 mm, no floor. Panels 60 mm: 1.5 mm steel",
                "  outer skin, 50 mm mineral wool, perforated inner liner, on a",
                "  frame of 40 x 40 x 4 angle, bolted together at the corners.",
                "Aisle face: door opening 800 x 1450, 400 from the washing end.",
                "Door: 790 x 1440 x 30 lined leaf on three self-closing spring",
                "  hinges at the washing-end edge, rubber seal, interlock switch.",
                "Roof: hole 500 x 410, 550 from the washing end and 500 from the",
                "  wall face; chute collar 500 x 410 x 160 of lined 2 mm sheet.",
                "Feed hood on the collar: 500 wide x 850 long x 180 tall, closed",
                "  top, lined sill 100 tall on the roof; feed slot 460 x 160 in",
                "  its aisle end, lip 1700 mm up; interlocked flap over the slot.",
                "Reach from the slot to the cutters 1060 mm (850 mm needed).",
                "Clear of the shredder: 140 and 135 at the ends, 370 in front,",
                "  360 behind, 28 above (rubber skirt from chute to hopper).",
                "Fit: angle cleats screwed to the floor at 600 pitch.",
                "Check: flap or door open stops the rotor; the door shuts itself."],
         date="2026-10-02", rev="P2",
         revisions=[("P1", "First issue (RFE-BLD-001 v0.1)", "2026-09-30", "AC"),
                    ("P2", "Feed hood for the reach check; self-closing door hinges", "2026-10-02", "AC")])

    # 110 drying rack and fan stand
    make(110, part("Drying rack and fan stand", sh("rack_dry", "dry_stand"), col("rack_dry")),
         [part("Drying fan", C["dry_fan"][2], GH), ctx(7300, 9300, -1, 1700)],
         title="ReflowEconomy drying rack and fan stand: making sketch",
         material="Steel SHS 40 x 40 x 3 and 60 x 60 x 3; angle 25 x 25 x 3; stainless mesh",
         inset_view=(25, -60),
         notes=["Rack 1200 x 600 x 1800 mm: four posts of 40 x 40 x 3 SHS,",
                "  1800 long, tied at top and bottom by the tray runners.",
                "Runners: 25 x 25 x 3 angle welded across the posts at 160 mm",
                "  pitch, ten levels from 200 mm up (top tray at 1640).",
                "Trays (make 10): 1120 x 600 frames of 25 x 25 x 3 angle with",
                "  stainless mesh, about 2 mm aperture, riveted in.",
                "Fan stand: base plate 500 x 300 x 10, post of 60 x 60 x 3 SHS",
                "  590 long welded on; fan bolted on top, axis 900 up.",
                "Fit: rack on the floor, 120 mm from the front wall; fan stand",
                "  in front, fan face 100 mm from the trays, blowing through them.",
                "Check: every tray slides out with one hand when full."])

    # 111 export cage
    make(111, part("Export cage and gates", sh("cage", "cage_gates", "gate_hinges"), col("cage")),
         [ctx(-1, 3000, 2600), part("Sand container and bale bags", C["cage_kit"][2], GH)],
         title="ReflowEconomy export and residue cage: making sketch",
         material="Welded mesh 50 x 50 x 4 on 40 x 40 x 4 angle frames",
         inset_view=(25, -60),
         notes=["Cage 2100 x 1400 x 1800 mm, no floor, open top: six panels of",
                "  50 x 50 x 4 welded mesh on 40 x 40 x 4 angle frames (60 mm),",
                "  bolted together at the corners with M8 bolts.",
                "Aisle face: gate opening 1200 wide, 350 from the export-door end.",
                "Gates (make 2): 590 x 1770 mesh leaves, 20 mm off the floor,",
                "  two self-closing hinges each, drop bolt on one, padlock hasp.",
                "Fit: 170 mm clear of the intake end wall, 96 mm from the back wall;",
                "  angle cleats screwed to the floor at each corner.",
                "Gates open into the aisle only while loading; keep them shut.",
                "Check: both gates swing fully open, shut themselves and lock."],
         date="2026-10-02", rev="P2",
         revisions=[("P1", "First issue (RFE-BLD-001 v0.1)", "2026-09-30", "AC"),
                    ("P2", "Self-closing gate hinges", "2026-10-02", "AC")])
    return out


GH = bv.GHOST


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []

    def j(n, parts, title, sub, **kw):
        if only is None or only == n:
            out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, size=(8, 6), **kw))

    # 1 seam beam end on the corner posts, floor seam plate (intake end, cut through the seam)
    W = (0, 700, 1900, 2980, -160, 2600)
    j(1, [part("Container end wall and corner posts", win(shell_open(), *W), "#D6D3CE"),
          part("Seam beam end on the corner posts", win(C["seam_beam"][2], *W), col("seam_beam")),
          part("Floor seam cover plate", win(C["seam_plate"][2], *W), col("seam_plate")),
          part("Painted aisle line", win(C["markings"][2], *W), col("markings"))],
      "seam beam and floor seam plate at the intake end",
      "Container option only. The beam sits on the corner posts; its section and fixings are the structural engineer's",
      elev=18, azim=-35)
    # 2 backboard with board, eyewash and tray riser
    W = (3250, 4750, 4300, FY, 500, 2250)
    j(2, [part("Back wall", win(C["shell"][2], *W), "#D6D3CE"),
          part("Backboard on rivet nuts", win(C["backboard"][2], *W), col("backboard")),
          part("Electrical board", win(C["board"][2], *W), col("board")),
          part("Eyewash", win(C["eyewash"][2], *W), col("eyewash")),
          part("Cable tray and riser from the board", win(C["tray"][2], *W), col("tray"))],
      "backboard, board, eyewash and tray riser",
      "Seen from the aisle. The board and eyewash screw to the plywood, never to the corrugated wall",
      elev=12, azim=-80)
    # 3 tray crossing under the seam beam
    W = (5300, 5900, 2000, 2900, 1700, 2400)
    j(3, [part("Seam beam", win(C["seam_beam"][2], *W), col("seam_beam")),
          part("Cable tray crossing, clamped under the beam", win(C["tray"][2], *W), col("tray")),
          part("Foam padding, yellow hazard tape", win(C["tray_pad"][2], *W), col("tray_pad")),
          part("Black hazard tape bands", win(C["tray_tape"][2], *W), col("tray_tape"))],
      "padded cable tray crossing under the seam beam",
      "Two beam clamps hold the tray at 2,038 mm; the taped padding leaves 2,023 mm of headroom", elev=-15, azim=-60)
    # 4 hood B on the extruder frame (cut along the barrel)
    W = (5650, 7050, 3950, 4520, 600, 1800)
    j(4, [part("Extruder frame, drive and hopper", win(C["extruder"][2], *W), col("extruder")),
          part("Hood B, bolted to the frame top", win(C["hood_b"][2], *W), col("hood_b")),
          part("Duct riser on the hood spigot", win(C["duct"][2], *W), col("duct"))],
      "hood B on the extruder frame (cut along the barrel)",
      "The barrel runs through a 120 mm hole in the hood end; the open face is toward the aisle",
      cut="+Y", elev=35, azim=-50)
    # 5 transfer bridge between the presses
    W = (8200, 9000, 3500, 4600, 600, 950)
    j(5, [part("Sheet press, cut at platen height", win(C["press_hot"][2], *W), col("press_hot")),
          part("Transfer bridge, bolted to the hot press", win(C["bridge"][2], *W), "#FACC15"),
          part("Cooling press, cut at platen height", win(C["press_cool"][2], *W), "#B45309")],
      "transfer bridge between the presses",
      "Presses cut off at platen height (950 mm). The roller top is level with both platens, so the mould slides across",
      elev=50, azim=-60)
    # 6 booth left end: duct through the end wall, booth against the back wall
    W = (6950, 7700, 3900, FY, 1500, 2420)
    j(6, [part("Back wall", win(C["shell"][2], *W), "#D6D3CE"),
          part("Booth end wall and roof", win(C["booth"][2], *W), col("booth")),
          part("Duct through a sealed collar", win(C["duct"][2], *W), col("duct")),
          part("Duct wall bracket", win(C["duct_brackets"][2], *W), col("duct_brackets")),
          part("Cable tray ends at the booth", win(C["tray"][2], *W), col("tray"))],
      "duct through the booth end wall",
      "Seen from the extruder side. The duct passes 65 mm under the booth roof",
      elev=20, azim=-130)
    # 7 sash in its rails, cut across
    W = (8400, 8800, 3100, 3300, 780, 1620)
    j(7, [part("Booth front panel", win(C["booth"][2], *W), col("booth")),
          part("Rails (aluminium channel)", win(C["rails"][2], *W), col("rails")),
          part("Sliding sash", win(C["sash"][2], *W), col("sash"))],
      "sliding sash in its rails (cut across)",
      "The sash edges run inside the channels in front of the booth face", cut="+X", elev=10, azim=-20)
    # 8 duct elbow, take-off and wall sleeve
    W = (7850, 8450, 4150, FY + 300, 1650, 2400)
    j(8, [part("Back wall", win(C["shell"][2], *W), "#D6D3CE"),
          part("Duct elbow to the wall", win(C["duct"][2], *W), col("duct")),
          part("Booth take-off with damper", win(C["takeoff"][2], *W), col("takeoff")),
          part("Flanged wall sleeve", win(C["sleeve"][2], *W), col("sleeve")),
          part("Fan and filter box (outside)", win(C["fan"][2], *W), col("fan"))],
      "duct elbow, booth take-off and wall sleeve (cut through the duct)",
      "Inside the booth: the take-off draws the booth air; the extruder branch joins at the elbow",
      cut="-X", elev=12, azim=-30)
    # 9 fan stand outside
    W = (7400, 8900, FY, FY + 900, -200, P["WALL_H"] + 1100)
    j(9, [part("Back wall (outside face)", win(C["shell"][2], 7400, 8900, FY - 80, FY, -200, P["WALL_H"]), "#D6D3CE"),
          part("Fan stand, braced, on anchors", win(C["fan_stand"][2], *W), col("fan_stand")),
          part("Fan and filter box", win(C["fan"][2], *W), col("fan")),
          part("Stack, 1 m above the roof", win(C["stack"][2], *W), col("stack")),
          part("Duct from the wall sleeve", win(C["duct"][2], *W), col("duct"))],
      "fan and filter box on its stand (outside the back wall)",
      "Seen from outside, behind the factory", elev=15, azim=120)
    # 10 chute collar over the shredder (cut)
    W = (6100, 7100, 400, 1650, 1050, 1950)
    j(10, [part("Shredder top and hopper", win(C["shredder"][2], *W), col("shredder")),
           part("Enclosure roof (lined)", win(C["shred_enc"][2], *W), col("shred_enc")),
           part("Chute collar through the roof", win(C["chute"][2], *W), col("chute")),
           part("Feed hood, closed top", win(C["chute_hood"][2], *W), col("chute_hood")),
           part("Interlocked flap over the slot", win(C["chute_lid"][2], *W), col("chute_lid"))],
       "feed hood and chute over the shredder hopper (cut across)",
       "Slot lip 1.70 m up; a hand must go 460 mm in and 600 mm down to the cutters", cut="+X", elev=12, azim=-155)
    # 11 enclosure door on the aisle face
    W = (5750, 7450, 1200, 1700, -10, 1700)
    j(11, [part("Enclosure (aisle face)", win(C["shred_enc"][2], *W), col("shred_enc")),
           part("Access door, interlocked", win(C["enc_door"][2], *W), col("enc_door")),
           part("Three self-closing hinges", win(C["door_hinges"][2], *W), col("door_hinges")),
           part("Shredder", win(C["shredder"][2], *W), col("shredder")),
           part("Painted aisle line", win(C["markings"][2], *W), col("markings"))],
       "enclosure access door on the aisle face",
       "Shuts itself; opens into the aisle only with the shredder locked off", elev=15, azim=-110)
    # 12 drying fan on its stand
    W = (7650, 8950, 150, 1250, -10, 1900)
    j(12, [part("Drying rack and trays", win(C["rack_dry"][2], *W), col("rack_dry")),
           part("Fan stand", win(C["dry_stand"][2], *W), col("dry_stand")),
           part("Drying fan", win(C["dry_fan"][2], *W), col("dry_fan"))],
       "drying fan on its stand, blowing through the trays",
       "Seen from the aisle side. Fan face 100 mm from the trays", elev=20, azim=60)
    # 13 cage gate
    W = (150, 2450, 3150, 4800, -10, 1900)
    j(13, [part("Mesh panels on angle frames", win(C["cage"][2], *W), col("cage")),
           part("Two gate leaves (aisle face)", win(C["cage_gates"][2], *W), "#A16207"),
           part("Self-closing gate hinges", win(C["gate_hinges"][2], *W), col("gate_hinges"))],
       "export cage gates on the aisle face",
       "Self-closing; they open into the aisle only while loading, never toward the export doors", elev=22, azim=-60)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []

    def st(n, done, new, title, sub, **kw):
        if only is None or only == n:
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def g(name, *keys):
        return part(name, sh(*keys), GH)

    def c(name, keys, e, color=None):
        return part(name, sh(*keys), color or col(keys[0]), e)

    whole = ctx(-1, P["FL_X"] + 1)
    st(1, [whole], [c("Seam beam (engineer's design)", ["seam_beam"], (0, 0, 1500))],
       "seam beam in, then the side walls out (container option)",
       "Props and beam to the engineer's design and sequence; only then are the joining side walls cut out",
       elev=28, azim=-62, label_done=False)
    st(2, [whole, g("Seam beam", "seam_beam")], [c("Floor seam cover plates (4)", ["seam_plate"], (0, -900, 600))],
       "floor seam cover plate", "Screwed along one edge only, into the intake-side container floor",
       elev=28, azim=-62, label_done=False)
    st(3, [whole, g("Seam plate", "seam_plate")], [c("Floor markings (paint)", ["markings"], (0, 0, 600))],
       "paint the aisle lines and the hot zone boundary", "50 mm lines; the hot zone line is 1.0 m from any stock",
       elev=35, azim=-62, label_done=False)
    loc = ctx(2200, 5600, 3000)
    st(4, [loc], [c("PPE and first aid cabinet", ["ppe"], (0, -800, 0)),
                  c("Fire extinguishers (hot zone pair)", ["extinguisher_1", "extinguisher_2"], (0, -800, 0))],
       "safety station first", "Cabinet against the back wall on two brackets; extinguishers in place before any power work",
       elev=22, azim=-60)
    st(5, [loc, g("Cabinet", "ppe")], [c("Backboard", ["backboard"], (0, -600, 0))],
       "backboard onto the back wall", "Six M8 screws into rivet nuts in the corrugation crests", elev=22, azim=-60)
    st(6, [loc, g("Cabinet and backboard", "ppe", "backboard")],
       [c("Eyewash", ["eyewash"], (0, -500, 0)), c("Electrical board", ["board"], (0, -500, 0))],
       "eyewash and electrical board onto the backboard",
       "The licensed electrician fits the board, RCDs, emergency stop circuit and heater interlock",
       elev=22, azim=-60)
    st(7, [whole, g("Board and backboard", "board", "backboard", "ppe")],
       [c("Cable tray and wall spacers", ["tray", "tray_spacers"], (0, 0, 700)),
        c("Crossing padding and hazard tape", ["tray_pad", "tray_tape"], (0, 0, 1300))],
       "cable tray", "Back run, crossing under the seam beam with taped padding over the aisle, front run",
       context=[part("Seam beam", C["seam_beam"][2], "#E5E7EB")], elev=30, azim=-62, label_done=False)
    hz = ctx(5200, 10100, 2900)
    st(8, [hz], [c("Extruder", ["extruder"], (0, -900, 0))],
       "extruder into the hot zone", "Built to its published design by the fabricator; levelled on its feet",
       elev=24, azim=-60)
    st(9, [hz, g("Extruder", "extruder")], [c("Hood B", ["hood_b"], (0, 0, 600))],
       "hood B onto the extruder frame", "Six M8 bolts through its bottom flange; the barrel passes through the end hole",
       elev=24, azim=-60)
    st(10, [hz, g("Extruder and hood B", "extruder", "hood_b")],
       [c("Sheet press", ["press_hot"], (0, -1100, 0)), c("Cooling press", ["press_cool"], (0, -1100, 0)),
        c("Transfer bridge", ["bridge"], (0, -1600, 400))],
       "presses and transfer bridge", "Both presses in before the booth; bridge bolted to the hot press, roller level with the platens",
       elev=24, azim=-60)
    st(11, [hz, g("Hot zone machines", "extruder", "hood_b", "press_hot", "press_cool", "bridge")],
       [c("Press booth panels", ["booth"], (0, 0, 1200))],
       "press booth round the presses", "Panels bolted together, cleated to the floor, back edges sealed to the wall",
       elev=24, azim=-60)
    st(12, [hz, g("Booth and machines", "booth", "extruder", "hood_b", "press_hot", "press_cool")],
       [c("Sash rails", ["rails"], (0, -500, 0)), c("Sliding sash", ["sash"], (0, -900, 0))],
       "sash rails and the sliding sash", "Rails screwed to the booth front; the sash is slid in from the right-hand end",
       elev=20, azim=-60)
    st(13, [hz, g("Booth and hood B", "booth", "hood_b", "extruder", "rails", "sash")],
       [c("Duct wall brackets", ["duct_brackets"], (0, -400, 0)), c("Duct, take-off and wall sleeve", ["duct", "takeoff", "sleeve"], (0, 0, 700))],
       "duct, brackets, booth take-off and wall sleeve",
       "Brackets first; the duct goes in through the booth end wall collar, then the elbow and sleeve",
       elev=24, azim=-60)
    out_ctx = ctx(7000, 9300, 3800, FY + 1000)
    st(14, [out_ctx, g("Duct", "duct", "sleeve")],
       [c("Fan stand", ["fan_stand"], (0, 900, 0)), c("Fan and filter box", ["fan"], (0, 900, 900)), c("Stack", ["stack"], (0, 900, 1500))],
       "fan stand, fan and filter box, stack (outside)", "Seen from behind. Stand anchored to a pad; fan box bolted on; stack 1 m above the roof",
       elev=18, azim=120)
    fr = ctx(5200, 8000, -1, 2400)
    st(15, [fr], [c("Shredder", ["shredder"], (0, -900, 0))],
       "shredder in place", "Built to its published design; levelled; emergency stop wired by the electrician",
       elev=24, azim=-60)
    st(16, [fr, g("Shredder", "shredder")],
       [c("Acoustic enclosure panels", ["shred_enc"], (0, 0, 1300)),
        c("Access door on self-closing hinges", ["enc_door", "door_hinges"], (0, 900, 0)),
        c("Chute collar, feed hood and flap", ["chute", "chute_hood", "chute_lid"], (0, 0, 2200))],
       "acoustic enclosure, door and feed chute", "Panels round the shredder, cleated down; feed hood on the collar; both interlocks in the stop circuit",
       elev=24, azim=-60, label_done=False)
    fr2 = ctx(3400, 9300, -1, 2400)
    st(17, [fr2, g("Shredder enclosure", "shred_enc", "enc_door", "door_hinges", "chute", "chute_hood", "chute_lid")],
       [c("Washing tanks and trap", ["wash"], (0, -900, 0)),
        c("Drying rack", ["rack_dry"], (0, -900, 0)), c("Drying fan on its stand", ["dry_stand", "dry_fan"], (0, 600, 0))],
       "washing tanks, drying rack and fan", "Tanks on level ground near the RCD-protected socket; fan stand in front of the rack",
       elev=24, azim=-60)
    ia = ctx(-1, 3800, -1, 2400)
    st(18, [ia], [c("Platform scale", ["scale"], (0, -900, 0)), c("Sorting table", ["table"], (0, -900, 0)),
                  c("Four bins", ["bin_pet", "bin_hdpe", "bin_pp", "bin_metals"], (0, 600, 0))],
       "intake: scale, sorting table and bins", "Bins stand behind the painted aisle line, not on it",
       elev=24, azim=-60)
    st(19, [whole, g("Equipment fitted", "shred_enc", "chute_hood", "wash", "rack_dry", "booth", "extruder", "board", "backboard", "ppe", "scale", "table")],
       [c("Racking bays", ["rack1", "rack2"], (0, 0, 900)), c("Passport desk", ["desk", "desk_kit"], (0, -900, 0)),
        c("Product-end extinguisher", ["extinguisher_3"], (0, -900, 0))],
       "racking, passport desk and the last extinguisher", "Racking anchored to the floor, 1.0 m clear of the hot zone line",
       elev=28, azim=-62, label_done=False)
    ce = ctx(-1, 3200, 2600)
    st(20, [ce], [c("Export cage panels", ["cage"], (0, 0, 900)), c("Gates on self-closing hinges", ["cage_gates", "gate_hinges"], (0, -900, 0)),
                  c("Sand container and bale bags", ["cage_kit"], (0, 0, 1900))],
       "export and residue cage", "Panels bolted together and cleated to the floor; gates on the aisle face",
       elev=24, azim=-60)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps}
    for w in what:
        name, _, n = w.partition(":")
        r = fns[name]() if not n else fns[name](int(n))
        print(w, "->", r)
