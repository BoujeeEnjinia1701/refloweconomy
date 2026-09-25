# ReflowEconomy

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Circular Materials · **TRL:** 3 of 9 (proof of concept on paper; TRL 4 on hold by Amish's instruction)

Open playbook for local micro-factories that recover and remanufacture materials safely at small scale: a feasibility matrix by material, process recipes, a micro-factory economics model, safety rules, and a material passport data standard so buyers can trust recycled feedstock. Machines live in their own repos. The guiding principle is to recover and remanufacture locally and export only what needs industrial refining.

![ReflowEconomy reference micro-factory](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Floor plan GA (PDF)](cad/drawings/RFE-DWG-001.pdf) · [Calculation note](docs/04-calcs/01-sizing.md) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Material flow](media/flow.png) · [Review note](docs/REVIEW.md)

## Problem

Smaller and lower-income countries export scrap and import finished goods, losing the value of their own materials. Most recycling know-how assumes industrial scale, and unsafe informal recovery (open burning, acid leaching of e-waste) harms workers and communities.

## Concept

The playbook is built around one reference design: a plastics micro-factory on 59.4 m² (two 40 ft container footprints or a small workshop) with a central aisle, intake and sorting, washing and float-sink, an enclosed shredder, drying, a hot zone with an extruder and a sheet press under enclosing hoods, a product store, a passport desk and a safety station. Per 100 kg of collected input, the calculation note (RFE-CAL-001) gives on paper 32.3 kg of HDPE and PP products and 19.3 kg of clean PET flake kept local (51.6 %), 10 kg exported for industrial refining (metals, circuit boards, cells), 10 kg of paper sold locally and 28.4 kg to licensed disposal, using 0.83 kWh per kilogram of output with a maximum demand of 8.35 kW on a single-phase supply. The equipment costs $24,050 (indicative, outside any hardware budget), and the site only breaks even at the assumed prices. A material passport (schema v0.2) opens at intake and travels with every lot that leaves.

![Material flow](media/flow.png)

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Material feasibility matrix: [docs/playbook/feasibility-matrix.md](docs/playbook/feasibility-matrix.md)
- Process recipes for PET flake, HDPE, PP and aluminium (add-on bay): [docs/playbook/recipes/](docs/playbook/recipes/README.md)
- Operator-editable economics model per kg and per shift: [docs/playbook/economics_model.py](docs/playbook/economics_model.py) with [economics_inputs.csv](docs/playbook/economics_inputs.csv)
- Safety and environmental rules: [docs/playbook/safety.md](docs/playbook/safety.md)
- Reference micro-factory: parametric layout [cad/src/model.py](cad/src/model.py), floor plan [RFE-DWG-001](cad/drawings/RFE-DWG-001.pdf), sizing [RFE-CAL-001](docs/04-calcs/01-sizing.md) and equipment list [bom/bom.csv](bom/bom.csv)
- Material passport schema v0.2 (JSON): [standards/material-passport-v0.2.schema.json](standards/material-passport-v0.2.schema.json), with [example records](standards/examples/); v0.1 kept at [standards/material-passport.schema.json](standards/material-passport.schema.json)
- Links to machine repos (WasteWise Scan, WasteWise-ml, planned shredder, foundry and cell tester)

## Safety

> Chemical refining of metals, battery black mass and e-waste is out of scope for small-scale operations; the playbook limits itself to safe dismantling, sorting, remelting and re-forming.

A micro-factory has moving machinery (shredder), hot surfaces (extruder and press at about 190 to 200 °C), melt fumes, water near electricity, sharp and contaminated input, lithium cells in the waste stream and a high fire load. No open burning, no heating of PVC, fume extraction on every melt process, and a review by a qualified safety professional before any site operates. See the safety section of [docs/02-concept.md](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculation note (`04-calcs/`) and design decisions |
| `docs/playbook/` | Feasibility matrix, process recipes, economics model, safety |
| `standards/` | Material passport schema and examples |
| `bom/` | Reference micro-factory equipment list with indicative costs |
| `cad/src/` | Parametric layout (`model.py`), drawing sheet (`sheets.py`) and media script (`concept_media.py`) |
| `cad/step/`, `cad/stl/` | STEP and STL exports of the layout |
| `cad/drawings/` | Floor plan general arrangement RFE-DWG-001 |
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
