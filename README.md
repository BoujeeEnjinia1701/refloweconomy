# ReflowEconomy

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Circular Materials · **TRL:** 2 of 9 (concept formulated)

Open playbook for local micro-factories that recover and remanufacture materials safely at small scale: a feasibility matrix by material, process recipes, a micro-factory economics model, safety rules, and a material passport data standard so buyers can trust recycled feedstock. Machines live in their own repos. The guiding principle is to recover and remanufacture locally and export only what needs industrial refining.

## Problem

Smaller and lower-income countries export scrap and import finished goods, losing the value of their own materials. Most recycling know-how assumes industrial scale, and unsafe informal recovery (open burning, acid leaching of e-waste) harms workers and communities.

## Concept

Open playbook for local micro-factories that recover and remanufacture materials safely at small scale: a feasibility matrix by material, process recipes, a micro-factory economics model, safety rules, and a material passport data standard so buyers can trust recycled feedstock. Machines live in their own repos. The guiding principle is to recover and remanufacture locally and export only what needs industrial refining.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Material feasibility matrix (plastics, aluminum, steel, glass, lithium cells, e-waste)
- Process recipe templates per material
- Micro-factory economics model (per kg, per shift)
- Safety and environmental rules
- Material passport data schema (JSON)
- Links to machine repos (WasteWise Scan, CellCheck, shredder, foundry)

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Chemical refining of metals, battery black mass and e-waste is out of scope for small-scale operations; the playbook limits itself to safe dismantling, sorting, remelting and re-forming.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements and design decisions |
| `docs/playbook/` | Feasibility matrix, process recipes, economics, safety |
| `standards/` | Material passport schema and examples |
| `bom/` | Starter equipment list for a micro-factory |
| `media/` | Diagrams and photos |
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
