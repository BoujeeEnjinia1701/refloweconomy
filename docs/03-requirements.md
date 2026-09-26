---
doc_id: RFE-REQ-001
title: ReflowEconomy requirements
project: ReflowEconomy
doc_type: Requirements
version: "0.4"
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
  change: Populate to TRL 2 (15 measurable requirements for the playbook, reference micro-factory and material passport, with status)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply RFE-DDR-001 decisions (R2 redefined for the aluminium add-on bay, R13 and R14 name schema v0.2, single-phase supply assumption) and replace the TRL 2 status with the TRL 3 status from RFE-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R8 restated (process losses counted); new R16 intake quality rule; R10 value $24,200 with the 1.5 kW fume fan; R11 fan 1.5 kW; shell and press assumptions updated
---

# ReflowEconomy requirements

These are first-pass requirements for the playbook, its reference micro-factory and the material passport. Targets are proposals for review, not user-validated needs, and will be revised after co-design sessions. Status is judged at TRL 3 against the calculation note RFE-CAL-001 v0.2 (`docs/04-calcs/01-sizing.md`, results in `docs/04-calcs/results.csv`): **3 are not met (R1, R4, R8)**, 2 are at risk (R6, R12), 2 cannot be verified at TRL 3 (R11, R15) and 9 are met on paper. Decisions from RFE-DDR-001 (Amish, 2026-09-25) are applied: R2 is redefined for the aluminium add-on bay, and R13 and R14 name passport schema v0.2. Decisions from RFE-DDR-002 (recommendations accepted by Amish, 2026-09-25) are applied: R8 is restated to count process losses, and R16 adds an intake quality rule.

## Playbook content

| ID | Requirement | Target | Verification | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Say which materials a small operation can recover safely | Feasibility matrix covers at least 7 material groups (plastics, aluminium, steel, glass, lithium cells, e-waste, ore), each with route, feasibility rating, main hazard and export point, and at least one cited source per row | Document review | **Not met**: the matrix has routes, ratings and reasons for 7 groups; hazard, export point and source columns are still to add |
| R2 | Give a process recipe for each locally processed material | One recipe each for PET, HDPE, PP and aluminium: input grade, steps, temperature window, drying, yield, rejects and PPE, each sourced. Redefined by RFE-DDR-001 item 1: the aluminium recipe serves the add-on bay, which has its own safety case, not the reference floor | Document review against published processing data | Met: four sourced recipes in `docs/playbook/recipes/` |
| R3 | Show whether a micro-factory can pay its way | Economics model per kilogram and per shift with local inputs (feedstock price, wage, energy tariff, product prices) and a break-even output; editable by an operator | Model review; later with at least one operating recycler | Met on paper: `docs/playbook/economics_model.py` with `economics_inputs.csv`; result +$1.61 per shift before rent, break-even product price $2.45/kg, break-even input 98 kg per shift |
| R4 | Export only what needs industrial refining | Every export stream names the refining step it needs, the licensed receiver type and the packing rule (for example, cells taped and in a fire-safe container) | Document review | **Not met**: principle and the cell packing rule only; per-stream rules still to write |

## Reference micro-factory

| ID | Requirement | Target | Verification | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R5 | Fit a small site | Floor area 60 m² or less (two 40 ft container footprints or a small workshop), with aisles of 1.0 m or more and a separate hot zone | Layout drawing (RFE-DWG-001) and RFE-CAL-001 section 8 | Met: 59.4 m², clear aisle 1.52 m, hot zone 1.00 m from stock (at the limit) |
| R6 | Process a useful amount per shift | 100 kg or more of mixed collected input per 8 h shift | Time budget from machine ratings (RFE-CAL-001 section 3) | At risk: shredder needs 3.79 h of 4 h at an assumed 15 kg/h (published range 8.8 to 41.8 kg/h); sheet press has 2.06 sheets of capacity for the 2 needed |
| R7 | Keep value local | 50 % or more of input mass remanufactured or sold locally as clean feedstock | Mass balance, then site data | Met on paper: 51.6 % |
| R8 | Limit what goes to disposal | Residue to licensed disposal 20 % or less of input mass, counting sorting residue and process losses together; nothing burned in the open. Restated by RFE-DDR-002 (item 8): the honest total is kept and R16 controls input quality | Mass balance, then site data | **Not met** for the reference input: 28.4 % (20 % sorting residue plus 8.4 % process losses). A load at the R16 threshold gives 19.5 % |
| R9 | Use little energy | 1.0 kWh or less per kilogram of output (products plus clean flake) | Energy budget per shift | Met on paper: 0.83 kWh/kg (42.9 kWh per shift) |
| R10 | Stay affordable | Equipment for items 1 to 12 of `bom/bom.csv` $25,000 or less, excluding the building shell | Priced equipment list | Met on paper: $24,200 indicative (was $24,050; +$150 for the 1.5 kW fume fan, RFE-DDR-002) |
| R11 | Protect workers from fumes | Local exhaust on every melt process with a face velocity of 0.5 m/s or more at the hood; no processing of PVC, PS or unknown plastics; workstation air below the local occupational exposure limits | Hood sizing calculation; later air monitoring | Not verifiable at TRL 3: two enclosing hoods sized for 0.5 m/s (0.57 m³/s, 1.00 kW input on a 1.5 kW fan, RFE-DDR-002), filters chosen and limits named; exposure needs air monitoring on a running site |
| R12 | Protect workers from machinery, heat, noise and electricity | Guarded shredder with interlocked hopper and emergency stop; insulated hot surfaces; 30 mA RCD on every circuit near water; noise 85 dB(A) or less over 8 h or hearing protection zones | Safety checklist and design review | At risk: guarding defined; operator exposure 94 dB(A) with a bare shredder and 79 dB(A) in a lined enclosure, based on an assumed sound power |
| R16 | Control input quality | Every delivery sampled at intake; a load whose sampled residue exceeds a set threshold is refused or charged a disposal fee; the threshold keeps R8 within 20 % (new, RFE-DDR-002 item 8) | Mass balance (RFE-CAL-001 section 2); later intake records | Met on paper: threshold 10 % residue by sampled mass (the limit is 10.6 %); the reference input at 20 % residue would fail it |

## Material passport

| ID | Requirement | Target | Verification | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R13 | Travel with every lot that leaves | A passport valid against `standards/material-passport-v0.2.schema.json` for every product lot, flake bag and export lot (schema named by RFE-DDR-001 item 4; v0.1 is kept) | Schema validation of example records | Met on paper: 3 of 3 example records in `standards/examples/` are valid |
| R14 | Trace a lot back to its intake batches | Each passport lists its parent batch IDs and the schema version, so a buyer can follow a product back to its collection points | Schema review | Met: v0.2 requires `schema_version`, and `parent_batch_ids` for every lot that is not an intake batch |
| R15 | Be quick to fill in | A passport completed in 2 min or less per lot on a phone or a shared laptop at the desk | Timed trial with operators | Not verifiable at TRL 3: needs a form and a timed trial |

## Assumptions

- Reference input: source-separated or picker-sorted post-consumer material, of which about 60 % by mass is target plastic (PET, HDPE, PP). Mixed dumpsite material will yield less.
- One 8 h shift a day, 250 shifts a year, four workers.
- PET is sold as clean flake rather than remanufactured in house, because it must be dried thoroughly and degrades easily in small extruders; HDPE and PP become products. Decided by Amish, 2026-09-25 (RFE-DDR-001 item 3).
- The reference line is plastics only; aluminium is a separate add-on bay with its own safety case. Decided by Amish, 2026-09-25 (RFE-DDR-001 item 1).
- Electrical supply: single-phase, taken as 230 V and 40 A, with staggered heating enforced by an interlock. Decided by Amish, 2026-09-25 (RFE-DDR-001 item 5). Maximum demand 8.75 kW (38.0 A) with the 1.5 kW fume fan (RFE-DDR-002 item 10).
- Sheet press: a derated 5 kW single-phase press is the playbook reference; the published 15 kW press is an option where a 400 V supply exists. Decided by Amish, 2026-09-25 (RFE-DDR-002 item 9).
- Building shell: a rented shed of about 60 m² is preferred; the two-container option is used only where no shed is available, and its side walls are removed only to a structural engineer's design. Decided by Amish, 2026-09-25 (RFE-DDR-002 item 11).
- Costs are indicative USD for new or locally built equipment and exclude land, building, permits and working capital.
