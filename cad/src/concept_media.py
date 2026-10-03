"""ReflowEconomy reference micro-factory: concept media from the TRL 3 parametric model.

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py (the floor layout); the material flow values come from
RFE-CAL-001 (python docs/04-calcs/sizing.py) and are estimates. Not for fabrication.

The reference micro-factory is a plastics line (PET, HDPE, PP) with sorting-out of metals,
paper, e-waste and residue, on two 40 ft container footprints side by side (12.19 x 4.88 m).
Axes: X along the line (intake at X = 0), Y from the front wall (Y = 0) to the back wall,
Z up. Units mm. Each Part carries the BOM line number used in bom/bom.csv.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from concept import Part, render_all, ACCENT, INK
from model import PARAMS as P, box, build_parts

import csv

SLAB = box(0, P["FL_X"], 0, P["FL_Y"], -150, 0)
FRONT_WALL = box(-1, P["FL_X"] + 1, -1, P["WALL_T"] + 0.5, 0, P["WALL_H"] + 1)   # left out of the media so the floor shows
BOM_NAMES = {int(r["item"].split()[0]): r["item"].split(" ", 1)[1]
             for r in csv.DictReader((ROOT / "bom" / "bom.csv").open())}

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

EXPLODE = {1: (0, -1300, 0), 2: (0, 0, 1500), 3: (0, -1700, 0), 4: (0, 0, 1300), 5: (0, 1500, 0),
           6: (0, 0, 500), 7: (0, 0, 2600), 8: (1600, 0, 0), 9: (1600, -1600, 0), 10: (0, 1600, 0),
           11: (0, 1600, 1400), 12: (0, 1500, 0), 13: (0, 0, 0), 0: (0, 0, 0)}


def zone_parts(exploded=False):
    """Parts list from cad/src/model.py. The first shape of each zone carries the BOM callout.
    The exploded variant drops the walls (so nothing hides behind them) and keeps the slab as item 13."""
    out = []
    for bom, items in sorted(build_parts().items(), key=lambda kv: (kv[0] in (0, 13), kv[0])):
        for j, (name, shape, colour) in enumerate(items):
            if bom == 13 and j > 0 and exploded:
                continue                     # seam beam and seam plate: shown in the build plan, not the zone key
            if bom == 13 and j == 0:
                shape = SLAB if exploded else shape - FRONT_WALL
                name = "Building shell (floor slab shown; walls omitted)" if exploded else "Building shell (front wall omitted)"
            elif j == 0 and bom:
                name = BOM_NAMES[bom]
            off = EXPLODE[bom] if exploded else (0, 0, 0)
            out.append(Part(name, shape, colour, bom if (j == 0 and bom != 0) else None, off))
    return out


parts = zone_parts()


# Material flow, per 100 kg of mixed collected input. All values are ESTIMATES for concept review.
FLOW = {
    "main": [("Intake\n(weighed)", 100), ("Sorting\n(target plastics)", 60), ("Washing and\nfloat-sink", 54.0),
             ("Shredding", 53.2), ("Drying", 52.7), ("Extrusion or\npressing (PE, PP)", 33.4)],
    "from_sort": [("Metals (Al, steel)", 8, "export"), ("E-waste boards, cells", 2, "export"),
                  ("Paper and card", 10, "sale"), ("Residue (PVC, multilayer,\nfilm, organics)", 20, "residue")],
    "losses": [(2, "Labels, dirt, rejects", 6.0), (3, "Fines", 0.8), (4, "Fines, spills", 0.5), (5, "Purge, degraded", 1.1)],
    "outputs": [("Products (beams, sheets)", 32.3, 5), ("PET clean flake", 19.3, 4)],
}


def flow_png(out):
    """Material flow through the reference micro-factory with passport attachment points."""
    EXPORT, SALE, RESID, LOSS = "#1D4ED8", "#6D28D9", "#78716C", "#C2410C"
    fig = plt.figure(figsize=(15, 6.6), dpi=160)
    ax = fig.add_axes([0.005, 0.0, 0.99, 0.88])
    ax.set_xlim(0, 21.4); ax.set_ylim(-6.1, 2.5); ax.set_axis_off()
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
    # outputs: products from the hot zone to the right; PET flake leaves after drying, drawn above the row
    xo = xs[-1] + bw + 0.7
    for name, kg, src in FLOW["outputs"]:
        if src == len(main) - 1:
            yy, start, cs = 0.0, (xs[-1] + bw + 0.02, y0), "arc3,rad=0"
        else:
            yy, start, cs = 1.75, (xs[src] + bw / 2, y0 + bh / 2 + 0.02), "angle,angleA=90,angleB=180,rad=0"
        ax.add_patch(FancyArrowPatch(start, (xo, yy), arrowstyle="-|>", mutation_scale=12,
                                     lw=width(kg), color=ACCENT, alpha=0.55, connectionstyle=cs))
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
    items = [(ACCENT, "Products and clean flake: 51.6 kg"), (EXPORT, "Exported for industrial refining: 10 kg"),
             (SALE, "Sold locally for recycling: 10 kg"), (RESID, "Sorting residue to disposal: 20 kg"),
             (LOSS, "Process losses to disposal: 8.4 kg")]
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
        key_figures=["Footprint 12.19 x 4.88 m, 59.4 m2 (shed or two 40 ft boxes)",
                     "Plastics line: PET flake; HDPE, PP sheets and beams",
                     "100 kg input per shift: 51.6 kg kept local (est.)",
                     "10 kg exported for refining; 28.4 kg to disposal (est.)",
                     "0.83 kWh/kg of output; 8.75 kW max demand, 230 V",
                     "Equipment $25,505 indicative (VE target $25,000)",
                     "Passport v0.2 on every lot that leaves (RFE-CAL-001)"],
        cut=False, date="2026-10-02")
    # Re-render the exploded view on a wider canvas so the legend clears the long floor plan
    from concept import _render
    _render(zone_parts(exploded=True), ROOT / "media" / "exploded.png", offsets=True, labels=True, size=(12, 6),
            title="ReflowEconomy: exploded view (numbers match bom/bom.csv)")
    flow_png(ROOT / "media" / "flow.png")
    for d in (ROOT / "media").glob("_views*"):
        shutil.rmtree(d)
