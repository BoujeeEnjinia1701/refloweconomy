---
doc_id: RFE-PRC-001
title: ReflowEconomy design precis
project: ReflowEconomy
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (reference micro-factory, material flow, first-order numbers, passport attachment points, safety, media)
---

# ReflowEconomy design precis

ReflowEconomy is an open playbook for local micro-factories, built around one reference design: a plastics micro-factory on about 60 m² (two 40 ft container footprints) that takes in 100 kg of collected material per shift, sorts out metals, e-waste and residue, and turns HDPE and PP into beams and sheets while selling PET as clean flake. First-order estimates suggest about 50 % of input mass is remanufactured or sold locally as clean feedstock, about 10 % is exported for industrial refining, about 10 % is sold to local recyclers and about 20 % goes to licensed disposal, using about 0.9 kWh per kilogram of output. The equipment costs about $23,000 (indicative, excluding the building). The economics are marginal at the assumed prices, so the product price, not the machinery, decides whether a site pays its way. A material passport opens at intake and travels with every lot that leaves.

![Material flow](../media/flow.png)

*Figure 1. Material flow through the reference micro-factory per 100 kg of mixed collected input. MP marks where a material passport record is opened (intake) and issued (every lot that leaves). All mass fractions are estimates.*

![Reference micro-factory](../media/hero.png)

*Figure 2. Massing model of the reference micro-factory floor with a 1.75 m person for scale. Material moves left to right from the intake door to the product store; the hot zone sits under one fume hood.*

## What the playbook contains

| Part | File | State at TRL 2 |
| --- | --- | --- |
| Material feasibility matrix | `docs/playbook/feasibility-matrix.md` | Draft, 7 material groups, sources to add |
| Safety and environmental rules | `docs/playbook/safety.md` | Draft, five core rules; expanded in the safety section below |
| Reference micro-factory | This precis, `bom/bom.csv`, `media/` | Concept layout and equipment list |
| Material passport | `standards/material-passport.schema.json` | Schema v0.1 |
| Process recipes | To be written at TRL 3 | Not started (R2) |
| Economics model | To be written at TRL 3 | First-order shift estimate below (R3) |

Machines live in their own repos: [wastewise-scan](https://github.com/BoujeeEnjinia1701/wastewise-scan) identifies plastic resin at intake, [WasteWise-ml](https://github.com/BoujeeEnjinia1701/WasteWise-ml) classifies material class and grade from a phone photo, and a shredder, an aluminium micro-foundry and a cell tester are planned.

## How it works

1. **Intake.** Pickers and collectors deliver bags at the intake door. Each delivery is weighed on the platform scale and gets a batch record: batch ID, origin (collection point), mass and date. This opens the material passport. The picker is paid by weight and grade.
2. **Sorting.** At the sorting table, material is split by hand, helped by WasteWise-ml on a phone or a WasteWise Scan NIR reader for unclear plastics. Target plastics go to color-coded bins (PET, HDPE, PP). Aluminium and steel go to a metals bin, paper and card to bags, and circuit boards and cells to the export cage. PVC, multilayer packaging, film, polystyrene and organics go to residue. Lithium cells are pulled out first and stored in a fire-safe container.
3. **Washing.** Bottles and rigid parts are soaked, scrubbed and rinsed in two tanks. A float-sink step separates PP and HDPE (float) from PET (sinks) and removes paper labels and dirt. Wash water settles in a sediment trap and is reused; sludge goes to licensed disposal.
4. **Shredding.** A guarded 2.2 kW shredder cuts clean parts into flake of about 5 to 10 mm, one polymer at a time.
5. **Drying.** Flake dries on mesh trays with a fan. PET flake is bagged and sold as clean feedstock.
6. **Extrusion or pressing.** HDPE and PP flake becomes beams and profiles in the extruder and 1 x 1 m sheets in the sheet press, both under one fume hood. Edge trim and off-cuts go back to the shredder.
7. **Product store and passport.** Every product lot, flake bag and export lot gets a passport at the desk (material, grade, mass, contamination, process, identification method) and a printed label with its batch ID, then goes to the racking or the export cage.

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Zone or item | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Intake scale and sorting table | 300 kg platform scale, 2.0 x 0.9 m steel table, four color-coded bins (PET, HDPE, PP, metals) | Opens the batch record |
| 2 | Washing tanks and sediment trap | Two 400 to 500 L polyethylene tanks, 0.75 kW pump, settling trap | Float-sink separation and rinse |
| 3 | Shredder | Open-design single-shaft or twin-shaft shredder, 2.2 kW gearmotor, interlocked hopper | Precious Plastic class or the portfolio's planned shredder |
| 4 | Drying rack and fan | Mesh tray rack, 0.4 kW fan | Passive plus forced air |
| 5 | Extruder | Open-design extruder for beams and profiles, about 3.5 kW | HDPE and PP only |
| 6 | Sheet press | 1 x 1 m heated press, about 5 kW | HDPE and PP sheets |
| 7 | Fume extraction hood and filter | Hood over the hot zone, duct through the wall, 1.1 kW fan, particulate and activated carbon filter | Face velocity target in R11 |
| 8 | Product store racking | Two bays of steel pallet racking | Labeled lots |
| 9 | Passport and quality desk | Desk, label printer, 30 kg bench scale, moisture meter, phone or laptop | Issues passports |
| 10 | Safety and PPE station | PPE cabinet, eyewash, first aid, two fire extinguishers | By the entrance and at the hot zone |
| 11 | Electrical board | 30 mA RCDs, circuit breakers, emergency stop circuit, energy meter | Installed by a licensed electrician |
| 12 | Export and residue cage | Lockable mesh cage, fire-safe cell container, bales and bags | Holds lots awaiting collection |
| 13 | Building shell | Two 40 ft containers side by side, or a rented shed of about 60 m² | Site-dependent; excluded from the equipment total |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view of the reference layout with numbered zones matching `bom/bom.csv`. The walls are omitted so nothing is hidden.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3.

### Mass balance

Assumptions: source-separated or picker-sorted post-consumer input; 60 % target plastic by mass; washing removes 10 % of plastic mass as labels, glue and dirt; about 2 % of the extruder and press feed is lost as purge and degraded material; trim is re-shredded. Masses are on a dry basis.

Table 1. Mass balance per 100 kg of input (estimates).

| Stream | Mass | Where it goes |
| --- | --- | --- |
| HDPE and PP products (beams, sheets) | 30 kg | Local sale, with passport |
| PET clean flake | 20 kg | Local or regional sale as feedstock, with passport |
| Metals (aluminium, steel) | 8 kg | Sold to smelters, or aluminium to a local micro-foundry when one exists; with passport |
| E-waste boards and cells | 2 kg | Cells tested and graded first; boards exported to a licensed refiner; with passport |
| Paper and card | 10 kg | Sold to a local mill |
| Residue (PVC, multilayer, film, organics) | 20 kg | Licensed disposal; never burned |
| Process losses (sludge, fines, purge) | 10 kg | Sediment and dust to licensed disposal |

### Throughput and energy per shift

Assumptions: one 8 h shift, four workers, machines running part of the shift at partial load.

Table 2. Energy per shift (estimates).

| Load | Rating | Use | Energy |
| --- | --- | --- | --- |
| Shredder | 2.2 kW | 5 h at 70 % | 7.7 kWh |
| Washing pump | 0.75 kW | 4 h | 3.0 kWh |
| Drying fan | 0.4 kW | 8 h | 3.2 kWh |
| Extruder | 3.5 kW | 5 h at 55 % | 9.6 kWh |
| Sheet press | 5 kW | 4 h at 50 % | 10.0 kWh |
| Fume extraction | 1.1 kW | 8 h | 8.8 kWh |
| Lighting, desk and small loads | 0.4 kW | 8 h | 3.2 kWh |
| **Total** | about 13 kW connected | | **about 45 kWh, about 0.9 kWh/kg of output** |

The shredder must handle about 53 kg in about 5 h, or about 11 kg/h. The sheet press makes about two 12 mm sheets of 1 x 1 m per shift (about 11 kg each at a density of 950 kg/m³), and the extruder about 8 kg of beams. Both rates need checking against the chosen machines at TRL 3. The peak load of about 13 kW needs a three-phase supply or staggered heating on a single-phase supply; this is an open question.

### Economics per shift

Table 3 is illustrative. Prices and wages vary widely by country and must come from the co-design partner.

Table 3. Illustrative operating result per shift (estimates, USD).

| Item | Basis | Amount |
| --- | --- | --- |
| Products | 30 kg at $2.50/kg | +75.00 |
| PET flake | 20 kg at $0.60/kg | +12.00 |
| Metals | 8 kg at $0.50/kg | +4.00 |
| Paper and card | 10 kg at $0.05/kg | +0.50 |
| Feedstock paid to pickers | 100 kg at $0.15/kg | -15.00 |
| Wages | 4 workers at $10 per shift | -40.00 |
| Energy | 45 kWh at $0.15/kWh | -6.75 |
| Disposal | 30 kg at $0.05/kg | -1.50 |
| Wear parts, PPE and consumables | Allowance | -10.00 |
| **Operating margin** | | **about +18** |
| Equipment recovery | $22,850 over 5 years of 250 shifts | -18.30 |
| **Result before rent and finance** | | **about 0** |

The site breaks even at best on these assumptions. Each $0.50/kg on the product price moves the result by $15 per shift, so product design and local buyers matter more than machine cost. R3 stays unmet until an operator-editable model is built and checked against a working site.

## Material passport

The passport is a JSON record, one per lot, validated against `standards/material-passport.schema.json` (v0.1). It opens at intake as a batch record and is issued with every lot that leaves (Figure 1).

```json
{"batch_id": "RFE-DEMO-0001", "material": "HDPE", "grade": "natural, rigid",
 "mass_kg": 11.2, "origin": {"country": "XX", "collection_point": "Market cooperative A"},
 "identification": {"method": "wastewise-ml", "confidence": 0.93},
 "contamination_pct": 1.5, "processed_by": "Demo micro-factory", "process": "shred-wash, sheet-press",
 "date": "2026-09-25"}
```

This example uses invented values. Schema v0.1 cannot yet link a product lot back to its intake batches or state its own version (R14 not met). A v0.2 with `parent_batch_ids`, `schema_version`, `product_form` and a recycled content statement aligned with ISO 14021 is proposed, awaiting Amish.

## Key design choices (proposed, awaiting Amish)

- **Plastics line as the reference micro-factory.** Plastics have the most open machine designs and the lowest entry cost. Aluminium remelting, rated high in the feasibility matrix, is a separate add-on bay with its own safety case, not part of the reference floor.
- **Two 40 ft container footprints.** A single 40 ft container is about 2.35 m wide inside, too narrow for safe aisles around a sheet press. Two side by side (or a shed of the same area) give about 60 m².
- **PET sold as flake; HDPE and PP made into products.** This keeps the hot zone to the two polymers that small extruders and presses handle well.
- **One hot zone under one hood.** Concentrates fume extraction and fire protection in one place away from the intake and product store.
- **Passport at the desk, not at each machine.** One person issues passports for all outgoing lots, which keeps the process simple.

## Safety

> **Safety:** A micro-factory combines moving machinery, hot surfaces, fumes, water near electricity, sharp and contaminated input and a high fire load of plastic. These rules extend `docs/playbook/safety.md` and must be reviewed by a qualified safety professional before any site operates.

- **Shredder (moving machinery).** Fixed guards, a hopper interlock that stops the rotor when opened, an emergency stop within reach, lockout before clearing jams, and no hands or tools in the hopper. Noise is likely above 85 dB(A), so the shredder area is a hearing protection zone.
- **Heat.** Extruder barrels and press platens run at about 180 to 250 °C. Insulated covers, heat-resistant gloves, face shields and a cool-down rule before maintenance. Never leave heaters on unattended.
- **Fumes.** Only identified HDPE and PP are melted. PVC is never heated (it releases hydrogen chloride), and polystyrene, PET and unknown plastics are not melted in the reference line. Extraction runs whenever a heater is on.
- **Electricity and water.** 30 mA RCDs on every circuit, splash-rated sockets near the wash tanks, and an installation by a licensed electrician.
- **Input hazards.** Needles, broken glass, cans and chemical containers arrive mixed in. Puncture-resistant gloves, a sharps container, and a rule that medical, chemical and hazardous waste is refused at the door.
- **Lithium cells.** Pulled out first at intake, never punctured or crushed, terminals taped and stored in a fire-safe container with dry sand. A cell in the shredder can start a fire.
- **Fire.** Plastic stock and flake are a high fire load. Two extinguishers, stock kept away from the hot zone, clear exits, no smoking and a daily cleanup of dust and flake. Fine plastic dust can be combustible.
- **Wastewater and sludge.** Settled and disposed of through a licensed route, never discharged to drains or open ground.
- **People.** No workers under 18. PPE is supplied free. Manual handling limited to bags of 25 kg or less.

## Open questions

- [ ] Real target-plastic share and contamination of collected input in the first partner region
- [ ] Shredder, extruder and sheet press rates and costs for specific open designs
- [ ] Three-phase supply or staggered heating on a single-phase supply for about 13 kW peak
- [ ] Fume hood size, face velocity and filter type for HDPE and PP melt fumes
- [ ] Local prices for products, flake, metals and paper, and local wages (economics model)
- [ ] Passport schema v0.2 fields that buyers actually need
- [ ] Permits for a small plastics recycler in the first target region
