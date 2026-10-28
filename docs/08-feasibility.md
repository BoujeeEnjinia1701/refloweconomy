---
doc_id: RFE-FEA-001
title: ReflowEconomy feasibility assessment
project: ReflowEconomy
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First feasibility assessment (kit 1.8 pipeline) of the reference micro-factory (option A)
---

# ReflowEconomy feasibility assessment

The reference micro-factory is technically feasible on paper with open machines and workshop fabrication, and its science checks out (RFE-STM-001), but two things decide whether a real site works: the electrical supply, which as designed is too small once motor currents are counted (RFE-DEC-001 D1), and the price its products fetch, which has to be about 2.49 USD/kg for the site to break even. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | Layout, zones, hoods, guarding and passport are complete at TRL 3 and constructable; every part is modelled at D3 with its fixings and passes the fidelity check with no interference | High | Hot zone clearance exactly at the 1.0 m limit; cooling press plates 0.9 m for a 1 m mould (to confirm when bought) | RFE-STM-001; RFE-CAL-001 sections 7 and 8; `cad/fidelity.json` |
| Materials | Standard stock (angle, SHS, RHS, flat bar, sheet, mesh, plywood), galvanised duct, mineral-wool panels, bought machines | High | Recycled feedstock quality varies with the input; PVC must be removed by hand at sorting | RFE-BLD-001; `bom/bom.csv` |
| Manufacturing and assembly | Eleven made components with making sketches; machines built to published open designs or bought; container seam only to a structural engineer's design | Medium | The derated 5 kW single-phase sheet press is not a published design; container wall removal needs an engineer and a certified welder | RFE-BLD-001; RFE-DDR-003 |
| Power and controls | On paper the morning loads draw about 55 A from the 40 A single-phase supply; a heater interlock exists but cannot fix motor currents | Low | Fixes change a decided input: three-phase (recommended), a longer day in three blocks, or less input (RFE-DEC-001 D1); interlock performance level to set (RFE-REG-001 G9) | RFE-CAL-001 section 5; RFE-STM-001 S14 |
| Throughput | 100 kg a shift with a 5 % shredder margin and 2.06 sheets of press capacity for 2 | Medium | Shredder and press rates are assumptions inside published ranges; to measure at TRL 4 | RFE-CAL-001 section 3; RFE-STM-001 S23, S24 |
| Safety and health | Guarding meets ISO 13857 on paper; hoods sized for 0.5 m/s and the booth extract carries the platen plume about 3.6 times over; noise 79 dB(A) on an assumed sound power | Medium | Air quality and noise can only be shown on a running site; fire load of plastic stock | RFE-STM-001 S10, S15 to S17, S21; RFE-RSK-001 |
| Economics | Breaks even at best: +0.17 USD per shift before rent at a product price of 2.50 USD/kg | Low | Indian listings for regenerated HDPE sheet are about 0.5 to 1 USD/kg; the site needs design-grade products or furniture buyers (RFE-MKT-001) | RFE-CAL-001 section 10 |
| Regulatory | Registration as a plastic waste processor (under 200 t a year band) and Air and Water Act consents in Maharashtra | Medium | Industry category and consent route to assess; local fire and building code review | RFE-REG-001 |
| Supply of parts | Every BOM line priced; machines from open-hardware workspaces or local fabricators | Medium | Single-phase variants of the published 400 V machines are uncommon | `bom/bom.csv`; RFE-MKT-001 |

Ratings: High, Medium, Low.
