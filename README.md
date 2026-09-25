# ReflowEconomy

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Circular Materials · **TRL:** 2 of 9 (concept formulated)

Open playbook for local micro-factories that recover and remanufacture materials safely at small scale: a feasibility matrix by material, process recipes, a micro-factory economics model, safety rules, and a material passport data standard so buyers can trust recycled feedstock. Machines live in their own repos. The guiding principle is to recover and remanufacture locally and export only what needs industrial refining.

![ReflowEconomy reference micro-factory](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Material flow](media/flow.png) · [Review note](docs/REVIEW.md)

## Problem

Smaller and lower-income countries export scrap and import finished goods, losing the value of their own materials. Most recycling know-how assumes industrial scale, and unsafe informal recovery (open burning, acid leaching of e-waste) harms workers and communities.

## Concept

The playbook is built around one reference design: a plastics micro-factory on about 60 m² (two 40 ft container footprints or a small workshop) with seven zones: intake and sorting, washing, shredding, drying, extrusion or pressing, product store, and a safety and PPE station. Per 100 kg of collected input, first-order estimates give about 50 kg remanufactured or sold locally as clean feedstock, about 10 kg exported for industrial refining (metals, circuit boards, cells), about 10 kg of paper sold locally and about 20 kg of residue to licensed disposal, using about 0.9 kWh per kilogram of output. The equipment costs about $23,000 (indicative, outside any hardware budget). A material passport opens at intake and travels with every lot that leaves.

![Material flow](media/flow.png)

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Material feasibility matrix: [docs/playbook/feasibility-matrix.md](docs/playbook/feasibility-matrix.md)
- Safety and environmental rules: [docs/playbook/safety.md](docs/playbook/safety.md)
- Reference micro-factory layout and equipment list: [bom/bom.csv](bom/bom.csv)
- Material passport data schema (JSON): [standards/material-passport.schema.json](standards/material-passport.schema.json)
- Process recipe templates per material (planned, TRL 3)
- Micro-factory economics model per kg and per shift (first-order estimate in the precis; full model planned)
- Links to machine repos (WasteWise Scan, WasteWise-ml, planned shredder, foundry and cell tester)

## Safety

> Chemical refining of metals, battery black mass and e-waste is out of scope for small-scale operations; the playbook limits itself to safe dismantling, sorting, remelting and re-forming.

A micro-factory has moving machinery (shredder), hot surfaces (extruder and press at about 180 to 250 °C), melt fumes, water near electricity, sharp and contaminated input, lithium cells in the waste stream and a high fire load. No open burning, no heating of PVC, fume extraction on every melt process, and a review by a qualified safety professional before any site operates. See the safety section of [docs/02-concept.md](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements and design decisions |
| `docs/playbook/` | Feasibility matrix, process recipes, economics, safety |
| `standards/` | Material passport schema and examples |
| `bom/` | Reference micro-factory equipment list with indicative costs |
| `cad/src/` | Massing model and media script (`concept_media.py`) |
| `media/` | Concept renders, blueprint, 3D viewer, exploded view and material flow |
| `build-log/` | Dated notes |

## Machine repos

- [wastewise-scan](https://github.com/BoujeeEnjinia1701/wastewise-scan): identify plastic resin type at intake
- [WasteWise-ml](https://github.com/BoujeeEnjinia1701/WasteWise-ml): image classifier for material class and grade
- Planned: cell tester and grader for battery reuse, plastic shredder, aluminum micro-foundry

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (RFE-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `RFE-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
