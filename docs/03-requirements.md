---
doc_id: RFE-REQ-001
title: ReflowEconomy requirements
project: ReflowEconomy
doc_type: Requirements
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
  change: Populate to TRL 2 (15 measurable requirements for the playbook, reference micro-factory and material passport, with status)
---

# ReflowEconomy requirements

These are first-pass requirements for the playbook, its reference micro-factory and the material passport. Targets are proposals for review, not user-validated needs. They will be checked by calculation and source review at TRL 3 and revised after co-design sessions. Status is judged against the concept estimates in RFE-PRC-001; six requirements are **not met** today and four are only partly met.

## Playbook content

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Say which materials a small operation can recover safely | Feasibility matrix covers at least 7 material groups (plastics, aluminium, steel, glass, lithium cells, e-waste, ore), each with route, feasibility rating, main hazard and export point, and at least one cited source per row | Document review | Partly met: matrix exists with routes and reasons; hazards, export points and sources still to add |
| R2 | Give a process recipe for each locally processed material | One recipe each for PET, HDPE, PP and aluminium: input grade, steps, temperature window, drying, yield, rejects and PPE, each sourced | Document review against published processing data | **Not met**: no recipes yet |
| R3 | Show whether a micro-factory can pay its way | Economics model per kilogram and per shift with local inputs (feedstock price, wage, energy tariff, product prices) and a break-even output; editable by an operator | Model review with at least one operating recycler | **Not met**: first-order shift estimate only (RFE-PRC-001), no model |
| R4 | Export only what needs industrial refining | Every export stream names the refining step it needs, the licensed receiver type and the packing rule (for example, cells taped and in a fire-safe container) | Document review | Partly met: principle stated; per-stream rules to write |

## Reference micro-factory

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R5 | Fit a small site | Floor area 60 m² or less (two 40 ft container footprints or a small workshop), with aisles of 1.0 m or more and a separate hot zone | Layout drawing | Met in the massing model (about 60 m²); aisle widths to check on the drawing |
| R6 | Process a useful amount per shift | 100 kg or more of mixed collected input per 8 h shift | Throughput calculation from machine ratings | Met on paper (estimate); shredder and sheet press rates unverified |
| R7 | Keep value local | 50 % or more of input mass remanufactured or sold locally as clean feedstock | Mass balance (Figure 2 of RFE-PRC-001), then site data | Met at the limit: about 50 % (estimate) |
| R8 | Limit what goes to disposal | Residue to licensed disposal 20 % or less of input mass; nothing burned in the open | Mass balance, then site data | Met at the limit: about 20 % (estimate); depends on collection quality |
| R9 | Use little energy | 1.0 kWh or less per kilogram of output (products plus clean flake) | Energy budget per shift | Met on paper: about 0.9 kWh/kg (estimate) |
| R10 | Stay affordable | Equipment for items 1 to 12 of `bom/bom.csv` $25,000 or less, excluding the building shell | Priced equipment list | Met on paper: about $22,850 indicative |
| R11 | Protect workers from fumes | Local exhaust on every melt process with a face velocity of 0.5 m/s or more at the hood; no processing of PVC, PS or unknown plastics; workstation air below the local occupational exposure limits | Hood sizing calculation; later air monitoring | **Not met**: hood not sized; filter type and exposure limits not chosen |
| R12 | Protect workers from machinery, heat, noise and electricity | Guarded shredder with interlocked hopper and emergency stop; insulated hot surfaces; 30 mA RCD on every circuit near water; noise 85 dB(A) or less over 8 h or hearing protection zones | Safety checklist and design review | **Not met**: shredder noise likely above 85 dB(A), so hearing protection is required; guarding not designed |

## Material passport

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R13 | Travel with every lot that leaves | A passport valid against `standards/material-passport.schema.json` for every product lot, flake bag and export lot | Schema validation of example records | Partly met: schema v0.1 exists; no example records |
| R14 | Trace a lot back to its intake batches | Each passport lists its parent batch IDs and the schema version, so a buyer can follow a product back to its collection points | Schema review | **Not met**: the schema has no parent batch or version fields (proposed change, awaiting Amish) |
| R15 | Be quick to fill in | A passport completed in 2 min or less per lot on a phone or a shared laptop at the desk | Timed trial with operators | Not verified: needs a form and a trial (TRL 4) |

## Assumptions

- Reference input: source-separated or picker-sorted post-consumer material, of which about 60 % by mass is target plastic (PET, HDPE, PP). Mixed dumpsite material will yield less.
- One 8 h shift a day, 250 shifts a year, four workers.
- PET is sold as clean flake rather than remanufactured in house, because it must be dried thoroughly and degrades easily in small extruders; HDPE and PP become products. This choice is proposed, awaiting Amish.
- Costs are indicative USD for new or locally built equipment and exclude land, building, permits and working capital.
