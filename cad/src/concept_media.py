"""ReflowEconomy reference micro-factory: concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main zones only; not for fabrication.

The reference micro-factory is a plastics line (PET, HDPE, PP) with sorting-out of metals,
paper, e-waste and residue. It sits on the footprint of two 40 ft shipping containers side by
side (about 12.2 x 4.9 m, about 60 m2), which also fits a small rented workshop.

Axes: X along the line (intake at X = 0, product store at the +X end), Y from the open
front (Y = 0) to the back wall (+Y), Z up. Units mm. Material flows left to right in X.
Each Part carries the BOM line number used in bom/bom.csv and the exploded view.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all, ACCENT, INK

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

FL_X, FL_Y = 12200.0, 4880.0      # floor: two 40 ft container footprints side by side
WALL_T, WALL_H = 100.0, 2600.0


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# 13 Building shell: floor slab, back wall and intake end wall only (front and +X end left open
# so the layout reads). Doors and roof are not modeled.
slab = box(0, FL_X, 0, FL_Y, -150, 0)
back = box(0, FL_X, FL_Y - WALL_T, FL_Y, 0, WALL_H)
end_wall = box(-WALL_T, 0, 0, FL_Y, 0, WALL_H) - box(-WALL_T - 1, 1, 400, 2400, 0, 2200)   # intake door opening
shell = slab + back + end_wall

# Zone floor markings (painted areas), shown as thin pads under each zone
pads = (box(150, 2650, 250, 3300, 0, 12)      # intake and sorting
        + box(2850, 4850, 1200, 3300, 0, 12)  # washing
        + box(5000, 6450, 1200, 3300, 0, 12)  # shredding
        + box(6600, 7900, 1200, 3300, 0, 12)  # drying
        + box(8050, 10250, 900, 4700, 0, 12)  # extrusion and pressing
        + box(10400, 12100, 250, 4700, 0, 12))  # product store and passport desk

# 1 Intake and sorting: platform scale, sorting table and four material bins at the front
intake = box(300, 1300, 400, 1400, 0, 100)                              # platform scale, 1 x 1 m
intake = intake + box(400, 2500, 1900, 2800, 850, 900)                  # sorting table top
for x in (450, 2400):
    for y in (1950, 2700):
        intake = intake + box(x, x + 50, y, y + 50, 0, 850)             # table legs
BIN_COLORS = ["#2563EB", "#16A34A", "#EAB308", "#9CA3AF"]               # PET, HDPE, PP, metals
bins = [box(1450 + i * 300, 1720 + i * 300, 350, 1000, 0, 800) for i in range(4)]

# 2 Washing: two-tank float-sink and rinse station with a sediment trap between them
washing = box(2950, 3900, 1600, 2300, 0, 900) + box(3950, 4750, 1600, 2300, 0, 900)
washing = washing + box(3500, 4200, 2500, 3000, 0, 450)                 # sediment trap and pump skid

# 3 Shredder: frame, motor box and hopper
shredder = box(5300, 6100, 1800, 2600, 0, 1100) + box(5400, 6000, 1900, 2500, 1100, 1350)
shredder = shredder + box(5250, 6150, 1750, 2650, 1350, 1700) - box(5350, 6050, 1850, 2550, 1400, 1701)
shredder = shredder + box(6100, 6400, 1950, 2450, 200, 600)             # 2.2 kW gearmotor

# 4 Drying: mesh rack and fan
drying = box(6700, 7800, 1500, 2100, 0, 1800)
drying = drying + Pos(7250, 2350, 1000) * Rot(90, 0, 0) * Cylinder(300, 180)

# 5 Extruder (beams and profiles) along the front of the hot zone
extruder = box(8200, 10100, 1100, 1600, 0, 950) + box(8300, 9900, 1250, 1450, 950, 1150)
extruder = extruder + box(8250, 8550, 1200, 1500, 1150, 1450)           # hopper

# 6 Sheet press at the back of the hot zone
press = box(8400, 9600, 3100, 4300, 0, 1500) + box(8500, 9500, 3200, 4200, 1500, 1650)

# 7 Fume extraction: hood over the hot zone and a duct to the back wall
fume = box(8150, 10150, 1000, 4500, 2050, 2250)
fume = fume + box(9000, 9400, 4500, FL_Y - WALL_T, 2100, 2400)
fume = fume + box(9000, 9400, FL_Y - WALL_T, FL_Y + 250, 2100, 2400)   # through the wall to the filter

# 8 Product store: two racking bays at the back of the +X end
store = box(10500, 12000, 3700, 4650, 0, 2000) - box(10560, 11940, 3690, 4600, 150, 1950)
for z in (650, 1300):
    store = store + box(10560, 11940, 3700, 4600, z, z + 40)
store = store + box(10600, 11100, 3750, 4250, 690, 1150) + box(11200, 11900, 3750, 4250, 40 + 150, 600)  # product lots

# 9 Passport and quality desk: desk, label printer, bench scale and moisture meter
desk = box(10600, 11800, 1300, 2000, 700, 750)
for x in (10620, 11730):
    for y in (1320, 1930):
        desk = desk + box(x, x + 50, y, y + 50, 0, 700)
qa = box(10700, 10950, 1500, 1750, 750, 900) + box(11100, 11500, 1450, 1850, 750, 820)

# 10 Safety and PPE station on the back wall near the entrance
ppe = box(2900, 3700, FL_Y - WALL_T - 450, FL_Y - WALL_T, 0, 1900)     # PPE and first aid cabinet
eyewash = box(3800, 4150, FL_Y - WALL_T - 300, FL_Y - WALL_T, 800, 1300)
ext1 = Pos(4350, FL_Y - WALL_T - 150, 300) * Cylinder(90, 600)
ext2 = Pos(10300, 900, 300) * Cylinder(90, 600)                          # second extinguisher at the hot zone

# 11 Electrical distribution board with RCDs and emergency stop
board = box(4500, 5200, FL_Y - WALL_T - 200, FL_Y - WALL_T, 1200, 2000)

# 12 Export and residue cage: baled metals, e-waste and residue awaiting collection
cage = box(200, 2400, 3300, FL_Y - WALL_T - 50, 0, 1800) - box(260, 2340, 3360, FL_Y - WALL_T - 110, 60, 1801)
cage_lots = box(350, 1100, 3450, 4300, 60, 900) + box(1300, 2200, 3450, 4300, 60, 700)

def zone_parts(exploded=False):
    """Parts list. The exploded variant drops the walls (so nothing hides behind them) and keeps the slab
    as item 13; the offsets pull each zone's equipment clear of the floor."""
    e = (lambda *v: v) if exploded else (lambda *v: (0, 0, 0))
    out = [
        Part("Intake scale and sorting table", intake, "#8B5E34", 1, e(0, -1300, 0)),
        Part("PET bin", bins[0], BIN_COLORS[0], None, e(0, -2300, 0)),
        Part("HDPE bin", bins[1], BIN_COLORS[1], None, e(0, -2300, 0)),
        Part("PP bin", bins[2], BIN_COLORS[2], None, e(0, -2300, 0)),
        Part("Metals bin", bins[3], BIN_COLORS[3], None, e(0, -2300, 0)),
        Part("Washing tanks and sediment trap", washing, "#38BDF8", 2, e(0, 0, 1500)),
        Part("Shredder, 2.2 kW", shredder, "#374151", 3, e(0, -1600, 0)),
        Part("Drying rack and fan", drying, "#A3A3A3", 4, e(0, 0, 1300)),
        Part("Extruder", extruder, "#C2410C", 5, e(0, -1700, 0)),
        Part("Sheet press", press, "#9A3412", 6, e(0, 0, 500)),
        Part("Fume extraction hood and filter", fume, "#6B7280", 7, e(0, 0, 2300)),
        Part("Product store racking", store, "#0F766E", 8, e(1600, 0, 0)),
        Part("Passport and quality desk", desk, "#E5E7EB", 9, e(1600, -1600, 0)),
        Part("Passport label printer and meters", qa, "#111827", None, e(1600, -1600, 0)),
        Part("Safety and PPE station", ppe + eyewash, "#15803D", 10, e(0, 1600, 0)),
        Part("Fire extinguishers", ext1 + ext2, "#DC2626", None),
        Part("Electrical board with RCDs and E-stop", board, "#D4A017", 11, e(0, 1600, 1400)),
        Part("Export and residue cage", cage + cage_lots, "#78716C", 12, e(0, 1500, 0)),
        Part("Zone floor markings", pads, "#CCE7E3", None),
    ]
    if exploded:
        out.append(Part("Building shell (floor slab shown; walls omitted)", slab, "#D6D3CE", 13))
    else:
        out.append(Part("Building shell (2 x 40 ft footprint)", shell, "#D6D3CE", 13))
    return out


parts = zone_parts()


# Material flow, per 100 kg of mixed collected input. All values are ESTIMATES for concept review.
FLOW = {
    "main": [("Intake\n(weighed)", 100), ("Sorting\n(target plastics)", 60), ("Washing", 54),
             ("Shredding", 53), ("Drying", 52), ("Extrusion or\npressing", 50)],
    "from_sort": [("Metals (Al, steel)", 8, "export"), ("E-waste boards, cells", 2, "export"),
                  ("Paper and card", 10, "sale"), ("Residue (PVC, multilayer,\nfilm, organics)", 20, "residue")],
    "losses": [(2, "Labels, dirt, glue", 6), (3, "Fines", 1), (4, "Fines, spills", 1), (5, "Purge, degraded", 2)],
    "outputs": [("Products (beams, sheets)", 30), ("Clean flake for sale", 20)],
}


def flow_png(out):
    """Material flow through the reference micro-factory with passport attachment points."""
    EXPORT, SALE, RESID, LOSS = "#1D4ED8", "#6D28D9", "#78716C", "#C2410C"
    fig = plt.figure(figsize=(15, 6.6), dpi=160)
    ax = fig.add_axes([0.005, 0.0, 0.99, 0.88])
    ax.set_xlim(0, 21.4); ax.set_ylim(-6.1, 1.9); ax.set_axis_off()
    main = FLOW["main"]
    bw, bh, pitch, y0 = 2.35, 1.35, 3.0, 0.0
    xs = [0.3 + i * pitch for i in range(len(main))]
    width = lambda kg: 0.6 + 7.0 * kg / 100
    for i, ((name, kg), x) in enumerate(zip(main, xs)):
        ax.add_patch(FancyBboxPatch((x, y0 - bh / 2), bw, bh, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="#F0FDFA", ec=ACCENT, lw=1.4))
        ax.text(x + bw / 2, y0 + 0.2, name, ha="center", va="center", fontsize=8.5, fontweight="bold", color=INK)
        ax.text(x + bw / 2, y0 - 0.42, f"{kg} kg", ha="center", va="center", fontsize=9, color=ACCENT)
        if i < len(main) - 1:
            ax.add_patch(FancyArrowPatch((x + bw + 0.02, y0), (xs[i + 1] - 0.02, y0), arrowstyle="-|>",
                                         mutation_scale=14, lw=width(main[i + 1][1]), color=ACCENT, alpha=0.55))
    # outputs to the right
    xo = xs[-1] + bw + 0.7
    for j, (name, kg) in enumerate(FLOW["outputs"]):
        yy = 0.85 - j * 1.7
        ax.add_patch(FancyArrowPatch((xs[-1] + bw + 0.02, y0), (xo, yy), arrowstyle="-|>", mutation_scale=12,
                                     lw=width(kg), color=ACCENT, alpha=0.55, connectionstyle="arc3,rad=0"))
        ax.add_patch(FancyBboxPatch((xo, yy - 0.5), 2.9, 1.0, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="#CCFBF1", ec=ACCENT, lw=1.4))
        ax.text(xo + 1.45, yy + 0.18, name, ha="center", va="center", fontsize=8, fontweight="bold", color=INK)
        ax.text(xo + 1.45, yy - 0.2, f"{kg} kg, local sale", ha="center", va="center", fontsize=8.5, color=ACCENT)
        tag(ax, xo + 2.75, yy + 0.5)
    # branches from sorting
    xsrt = xs[1] + bw / 2
    colors = {"export": EXPORT, "sale": SALE, "residue": RESID}
    bx = [0.2, 3.35, 6.5, 9.65]
    for k, ((name, kg, kind), x) in enumerate(zip(FLOW["from_sort"], bx)):
        c = colors[kind]
        ax.add_patch(FancyArrowPatch((xsrt - 0.6 + 0.4 * k, y0 - bh / 2 - 0.02), (x + 1.4, -3.35),
                                     arrowstyle="-|>", mutation_scale=12, lw=width(kg) * 0.8, color=c, alpha=0.55))
        ax.add_patch(FancyBboxPatch((x, -4.35), 2.8, 1.0, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="white", ec=c, lw=1.3))
        ax.text(x + 1.4, -3.72, name, ha="center", va="center", fontsize=7.8, fontweight="bold", color=INK)
        dest = {"export": "export for refining", "sale": "sold to a local mill",
                "residue": "disposal, never burned"}[kind]
        ax.text(x + 1.4, -4.12, f"{kg} kg, {dest}", ha="center", va="center", fontsize=7, color=c)
        if kind == "export":
            tag(ax, x + 2.65, -3.35)
    # process losses
    for i, name, kg in FLOW["losses"]:
        x = xs[i] + bw / 2 + (0.25 if i == 2 else 0)
        ax.add_patch(FancyArrowPatch((x, y0 - bh / 2 - 0.02), (x, -1.55), arrowstyle="-|>", mutation_scale=10,
                                     lw=width(kg) * 0.8, color=LOSS, alpha=0.6))
        right = i == len(main) - 1
        ax.text(x if right else x + 0.12, -1.8 if right else -1.25, f"{name}: {kg} kg", ha="center" if right else "left", va="center", fontsize=7.6, color=LOSS)
    tag(ax, xs[0] + bw - 0.15, y0 + bh / 2)
    # legend and notes
    ly = -5.05
    items = [(ACCENT, "Remanufactured locally: 50 kg"), (EXPORT, "Exported for industrial refining: 10 kg"),
             (SALE, "Sold locally for recycling: 10 kg"), (RESID, "Residue to licensed disposal: 20 kg"),
             (LOSS, "Process losses to sludge and dust: 10 kg")]
    for x, (c, t) in zip((0.3, 3.9, 8.3, 12.2, 16.3), items):
        ax.add_patch(plt.Rectangle((x, ly - 0.12), 0.35, 0.24, fc=c, alpha=0.7, ec="none"))
        ax.text(x + 0.5, ly, t, va="center", fontsize=8, color=INK)
    tag(ax, 0.45, -5.75, small=True)
    ax.text(0.75, -5.75, "Material passport: batch record opened at intake (origin, mass); passport issued with every "
            "product lot, flake bag and export lot (material, grade, mass, contamination, process).",
            va="center", fontsize=8, color=INK)
    fig.text(0.01, 0.975, "ReflowEconomy: material flow through the reference micro-factory, per 100 kg of mixed "
             "collected input (all mass fractions are estimates)", fontsize=10.5, fontweight="bold", color=INK, va="top")
    fig.text(0.01, 0.935, "CONCEPT, NOT FOR FABRICATION", fontsize=6.5, color="#B45309", va="top")
    out = Path(out); fig.savefig(out, facecolor="white", bbox_inches="tight"); plt.close(fig)
    return out


def tag(ax, x, y, small=False):
    """Material passport marker: a small tag labeled MP."""
    s = 0.22 if small else 0.28
    ax.add_patch(FancyBboxPatch((x - s, y - s * 0.6), 2 * s, 1.2 * s, boxstyle="round,pad=0.02,rounding_size=0.05",
                                fc="#FDE68A", ec="#B45309", lw=1.0, zorder=5))
    ax.text(x, y, "MP", ha="center", va="center", fontsize=6.5 if small else 7, fontweight="bold",
            color="#92400E", zorder=6)


if __name__ == "__main__":
    import os, shutil
    os.chdir(ROOT)
    render_all(
        parts, project="ReflowEconomy", title="Reference micro-factory layout", dwg_no="RFE-DWG-010",
        key_figures=["Footprint 12.2 x 4.9 m (two 40 ft containers), about 60 m2",
                     "Plastics line: PET, HDPE, PP; metals, e-waste sorted out",
                     "100 kg mixed input per 8 h shift (estimate)",
                     "About 50 kg remanufactured locally per shift (est.)",
                     "About 10 kg exported for industrial refining (est.)",
                     "Equipment about $23,000 indicative, excl. site",
                     "Passport on every product lot, flake bag and export lot"],
        cut=False, date="2026-09-25")
    # Re-render the exploded view on a wider canvas so the legend clears the long floor plan
    from concept import _render
    _render(zone_parts(exploded=True), ROOT / "media" / "exploded.png", offsets=True, labels=True, size=(12, 6),
            title="ReflowEconomy: exploded view (numbers match bom/bom.csv)")
    flow_png(ROOT / "media" / "flow.png")
    for d in (ROOT / "media").glob("_views*"):
        shutil.rmtree(d)
