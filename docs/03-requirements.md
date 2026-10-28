---
doc_id: RFE-PRS-001
title: ReflowEconomy product requirements and specifications
project: ReflowEconomy
doc_type: Product requirements and specifications
version: "0.7"
status: Draft
date: '2026-10-25'
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
- version: "0.5"
  date: '2026-09-30'
  author: Amish Chadha
  change: "Design for construction (RFE-DDR-003): R3, R5 and R10 figures updated; R10 reported against its value-engineering target"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Approved follow-ups (decided by Amish, 2026-10-02): R3, R5, R10 and R12 figures updated (result +$0.57 per shift; headroom 2.02 m under the padded tray crossing; $25,505; feed reach check passes); no status changes"
- version: "0.7"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.8 pipeline: REQ migrated to PRS (RFE-REQ-001 becomes RFE-PRS-001); every R becomes a PR traced to a user requirement in RFE-URS-001, with tolerance and units; new PR-017 supply current, PR-018 local fabrication, PR-019 fire and cells, PR-020 registration; STEM check fixes applied (PR-009 0.88 kWh/kg, PR-012 120 mm feed slot, PR-003 result +0.17 USD per shift)"
---

# ReflowEconomy product requirements and specifications

What the playbook, its reference micro-factory (concept option A, the existing design) and the material passport must do, each requirement traced to a user need in RFE-URS-001 (links in RFE-RTM-001). Targets are proposals for review with a co-design partner, not user-validated needs. Status is judged at TRL 3 against the calculation note RFE-CAL-001 v0.6 (`docs/04-calcs/01-sizing.md`, results in `docs/04-calcs/results.csv`) and the STEM check RFE-STM-001: **4 are not met (PR-001, PR-004, PR-008, PR-017)**, 2 are at risk (PR-006, PR-012), 3 can only be verified on a running site (PR-011, PR-015, PR-020), 1 is over its value-engineering target (PR-010, by USD 505) and 10 are met on paper or by design. PR-001 to PR-016 are the old R1 to R16 of RFE-REQ-001 with the same targets ("Was" column). Decisions from RFE-DDR-001 and RFE-DDR-002 (Amish, 2026-09-25) and RFE-DDR-003 (accepted 2026-10-02) are applied as before; the STEM check fixes of 2026-10-25 (RFE-DEC-001 D2, D3) are applied; the supply decision (D1) is open.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Feasibility matrix | The playbook shall say, for every material group, whether a small operation can recover it safely, with route, feasibility rating, main hazard, export point and at least one cited source per row | 7 | min | material groups | Inspection (document review), TRL 3 | **Not met**: routes, ratings and reasons for 7 groups; hazard, export point and source columns still to add | R1 |
| PR-002 | UR-002 | Usability | Process recipes | The playbook shall give a sourced recipe (input grade, steps, temperature window, drying, yield, rejects, PPE) for each locally processed material | 4 (PET, HDPE, PP, aluminium add-on bay) | min | recipes | Inspection against published processing data, TRL 3 | Met on paper: four sourced recipes in `docs/playbook/recipes/` | R2 |
| PR-003 | UR-003 | Performance | Economics model | The playbook shall include an operator-editable economics model per kilogram and per shift with local inputs and a break-even output and price | 1 | min | model | Analysis (RFE-CAL-001 section 10), TRL 3; review with an operating recycler at P5 | Met on paper: result +0.17 USD per shift before rent; break-even product price 2.49 USD/kg; break-even input 100 kg per shift | R3 |
| PR-004 | UR-004 | Logistics | Export rules | Every export stream shall name the refining step it needs, the licensed receiver type and the packing rule | 100 | min | % of export streams | Inspection (document review), TRL 3 | **Not met**: principle and the cell packing rule only | R4 |
| PR-005 | UR-005 | Physical architecture | Small site | The reference micro-factory shall fit 60 m2 with clear aisles and headroom over the aisle and a separate hot zone 1.0 m from stock | 60; 1.0; 2.0; 1.0 | max; min; min; min | m2; m aisle; m headroom; m to stock | Analysis of the model and RFE-DWG-001 (RFE-CAL-001 section 8), TRL 3; tape measure at TRL 4 | Met on paper: 59.4 m2; aisle 1.57 m; headroom 2.02 m under the padded tray crossing; hot zone 1.00 m from stock (at the limit) | R5 |
| PR-006 | UR-006 | Performance | Throughput | The line shall process mixed collected input in one 8 h shift | 100 | min | kg per shift | Analysis (RFE-CAL-001 section 3), TRL 3; measured rates at TRL 4 | **At risk**: shredder 3.79 h of 4 h at an assumed 15 kg/h (published 8.8 to 41.8 kg/h); press 2.06 sheets of capacity for 2; at the PR-016 intake threshold the shredder needs 4.26 h | R6 |
| PR-007 | UR-007 | Performance | Value kept local | The share of input mass remanufactured or sold locally as clean feedstock shall be at least the target | 50 | min | % of input mass | Analysis (mass balance, RFE-CAL-001 section 2), TRL 3; site data at P5 | Met on paper: 51.6 % | R7 |
| PR-008 | UR-008 | Performance | Disposal | Residue to licensed disposal, counting sorting residue and process losses together, shall be at most the target; nothing is burned | 20 | max | % of input mass | Analysis (mass balance, RFE-CAL-001 section 2), TRL 3; site data at P5 | **Not met** for the reference input: 28.4 %; 19.5 % for a load at the PR-016 threshold | R8 |
| PR-009 | UR-009 | Electrical | Energy | Electricity per kilogram of output (products plus clean flake), with motor and drive losses counted, shall be at most the target | 1.0 | max | kWh/kg | Analysis (RFE-CAL-001 section 4), TRL 3; energy meter at TRL 4 | Met on paper: 0.88 kWh/kg (45.6 kWh per shift; 0.83 before the STEM check fix, RFE-DEC-001 D2) | R9 |
| PR-010 | UR-016, UR-003 | Performance | Equipment cost | Equipment for items 1 to 12 of `bom/bom.csv`, excluding the building shell, shall be reported against the value-engineering target (a hypothetical control target, not a limit) | 25,000 | target | USD | Analysis (priced BOM, RFE-CAL-001 section 9), TRL 3 | Over the value-engineering target by USD 505: USD 25,505 indicative | R10 |
| PR-011 | UR-011 | Safety | Fume capture | Every melt process shall have local exhaust with a face velocity of at least the target; no PVC, PS or unknown plastics are processed; workstation air stays below the local occupational exposure limits | 0.5 | min | m/s at the hood face | Analysis (RFE-CAL-001 section 6; RFE-STM-001 S10), TRL 3; anemometer and air monitoring at TRL 4 | To verify at TRL 4: two enclosing hoods sized for 0.5 m/s (0.57 m3/s, fan 1.00 kW of 1.5 kW); exposure needs air monitoring | R11 |
| PR-012 | UR-012 | Safety | Machine, heat, noise and electrical safety | The shredder shall be guarded with an interlocked feed and door and an emergency stop, with the reach from the feed slot to the cutters at least the ISO 13857 Table 4 distance through a slot of 120 mm or less; hot surfaces insulated; 30 mA RCDs near water; operator exposure at most the target or a hearing protection zone | 850; 120; 85 | min reach; max slot; max | mm; mm; dB(A) LEX,8h | Analysis (RFE-CAL-001 section 7; RFE-STM-001 S15 to S17), TRL 3; measurement at TRL 4 | **At risk**: reach 1,060 mm through a 460 x 120 mm slot (passes; slot lowered from 160 mm, RFE-DEC-001 D3); LEX 79 dB(A) enclosed on an assumed sound power; the EN 12012 type C standard for size reduction machines still to check | R12 |
| PR-013 | UR-013 | Software | Passport on every lot | Every product lot, flake bag and export lot shall leave with a passport valid against schema v0.2 | 100 | min | % of lots | Test (schema validation of the example records, RFE-CAL-001 section 11), TRL 3 | Met on paper: 3 of 3 examples valid | R13 |
| PR-014 | UR-013 | Software | Trace to intake | Each passport shall list its parent batch IDs and the schema version | 100 | min | % of non-intake lots | Inspection of the schema, TRL 3 | Met by design: v0.2 requires both | R14 |
| PR-015 | UR-014 | Usability | Quick to fill in | A passport shall be completed on a phone or shared laptop at the desk within the target | 2 | max | min per lot | Test (timed trial with operators), TRL 4 | To verify at TRL 4: needs a form and a timed trial | R15 |
| PR-016 | UR-008, UR-019 | Performance | Intake quality rule | Every delivery shall be sampled at intake, and a load whose sampled residue exceeds the threshold is refused or charged a disposal fee; the threshold keeps PR-008 within 20 % | 10 | max | % residue by sampled mass | Analysis (RFE-CAL-001 section 2), TRL 3; intake records at P5 | Met on paper: threshold 10 % (limit 10.6 %); a cleaner load carries more plastic and pushes PR-006 past its 4 h block | R16 |
| PR-017 | UR-010 | Electrical | Supply current | The loads that run together shall stay within the rating of a 230 V, 40 A single-phase supply, counted as input currents (drive input current, motor efficiency and power factor) | 40 | max | A | Analysis (RFE-CAL-001 section 5; RFE-STM-001 S14), TRL 3; clamp meter at TRL 4 | **Not met**: block A about 55 A running (72 A at full load); block B 36 A. Supply decision proposed, awaiting Amish (RFE-DEC-001 D1) | |
| PR-018 | UR-015 | Physical architecture | Local fabrication | Every made part of the fit-out shall be cut, drilled, welded, folded or riveted from standard stock (angle, SHS, flat bar, sheet, mesh, plywood) with workshop tools, and every machine shall be an open design a local fabricator can build or a standard bought item | 100 | min | % of made parts | Inspection of the model, drawings and build plan (RFE-BLD-001), TRL 3 | Met by design: 11 made components with making sketches; detailed model at D3 in standard stock (RFE-CAL-001 section 8) | |
| PR-019 | UR-018 | Safety | Fire and lithium cells | Lithium cells shall be pulled out at intake and stored in a fire-safe container with dry sand; three extinguishers (entrance, hot zone, product end); stock at least 1.0 m from the hot zone | 3; 1.0 | min; min | extinguishers; m | Inspection of the model, BOM lines 10 and 12 and the build plan stop S5, TRL 3 | Met by design (RFE-STM-001 S27; RFE-CAL-001 section 8) | |
| PR-020 | UR-017 | Regulatory | Registration | The playbook shall list the registrations and consents a small plastics processor needs in the first partner region, with the capacity band the reference site falls in | 1 | min | register (RFE-REG-001) | Inspection (RFE-REG-001; RFE-CAL-001 section 11), TRL 3; registration itself at P5 | To verify at TRL 4: listed for Maharashtra (MPCB registration on the CPCB portal, under 200 t a year band; Air and Water Act consents) | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software, logistics, regulatory. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- Reference input: source-separated or picker-sorted post-consumer material, of which about 60 % by mass is target plastic (PET, HDPE, PP). Mixed dumpsite material will yield less.
- One 8 h shift a day, 250 shifts a year, four workers.
- PET is sold as clean flake rather than remanufactured in house, because it must be dried thoroughly and degrades easily in small extruders; HDPE and PP become products. Decided by Amish, 2026-09-25 (RFE-DDR-001 item 3).
- The reference line is plastics only; aluminium is a separate add-on bay with its own safety case. Decided by Amish, 2026-09-25 (RFE-DDR-001 item 1).
- Electrical supply: single-phase, taken as 230 V and 40 A, with staggered heating enforced by an interlock. Decided by Amish, 2026-09-25 (RFE-DDR-001 item 5). Counted as currents, the morning loads exceed it on paper (PR-017); the options are proposed, awaiting Amish (RFE-DEC-001 D1).
- Sheet press: a derated 5 kW single-phase press is the playbook reference; the published 15 kW press is an option where a 400 V supply exists. Decided by Amish, 2026-09-25 (RFE-DDR-002 item 9).
- Building shell: a rented shed of about 60 m2 is preferred; the two-container option is used only where no shed is available, and its side walls are removed only to a structural engineer's design. Decided by Amish, 2026-09-25 (RFE-DDR-002 item 11).
- Costs are indicative USD for new or locally built equipment and exclude land, building, permits and working capital.
