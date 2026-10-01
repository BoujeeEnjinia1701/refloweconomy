---
doc_id: RFE-DEC-001
title: ReflowEconomy design decisions register
project: ReflowEconomy
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open decisions from RFE-DDR-001 to RFE-DDR-003; equipment cost treated as a value-engineering target
---

# ReflowEconomy design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction: accept the changes that make the layout buildable (seam beam and floor plate, hood B on the extruder frame, duct route and booth take-off, sliding sash with two openings and the transfer bridge, shredder enclosure without a floor and with a lower roof, backboard, cable tray, fan stand and stack, drying fan stand, cage gate, bins behind the aisle line) | (a) accept all; (b) accept with named exceptions | (a) | The whole build plan follows these changes | RFE-DDR-003, Table 1 |
| 2 | Shredder feed height and reach distance (safety case) | (a) chute mouth at 1.70 m as modelled, reach distance to the cutters checked against ISO 13857 at the safety review and the chute lengthened if short; (b) the concept's 2.1 m mouth with a fixed step platform and handrail | (a): no work at height; the interlocked lid still stops the rotor | Enclosure roof height, chute collar (RFE-DWG-109) | RFE-DDR-003, A1 |
| 3 | Second opening in the press booth (safety case) | (a) one sliding sash over two openings, as modelled; (b) two sashes with an electrical interlock; (c) one opening only, cooled sheets taken out through it | (a): "one opening at a time" is mechanical, not a rule | Booth front panel, sash and rails (RFE-DWG-105, 106) | RFE-DDR-003, A2 |
| 4 | Shredder enclosure door and cage gates opening into the aisle (safety case) | (a) hinged, opening into the aisle only during locked-off maintenance or loading; (b) sliding door and gates (about +$300) | (a), with the rule written into the playbook safety section | Enclosure door, cage gates (RFE-DWG-109, 111) | RFE-DDR-003, A3 |
| 5 | Aisle headroom of 2.04 m under the tray crossing and about 2.09 m under the seam beam (container option; safety case) | (a) accept, if the local code allows 2.0 m on an escape route; (b) cables through a sleeve in the beam web, if the engineer allows | (a), confirmed against the local code by the safety professional | Cable tray crossing, seam beam | RFE-DDR-003, A4 |
| 6 | First co-design partner and region | (a) a waste-picker cooperative; (b) an existing Precious Plastic workspace; (c) a municipal program | (a) or (b); left open under the rule that partners are picked per area later | Site, shell choice, local prices and the input quality that R8 depends on | RFE-DDR-001, item 7; RFE-DDR-002 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The structural engineer's seam beam section, fixings and propping sequence fit the 165 x 305 mm space reserved under the roof | The tray crossing and the aisle headroom are set from it | RFE-DDR-003, P1 |
| 2 | The shredder's size, hopper position and top height (about 1,205 x 550 x 1,512) | The enclosure clears it by only 28 mm above, and the chute sits over the hopper | RFE-DDR-003, P5 |
| 3 | The gearmotor stays within its rated temperature with the enclosure closed through a shift | The lined enclosure has no ventilation; add a lined vent baffle if it runs hot | RFE-DDR-003, P5 |
| 4 | The extruder frame top is flat at about 900 mm with room for six bolts, and the barrel axis is where hood B's hole is | Hood B is made to fit the frame and barrel | RFE-DDR-003, P2 |
| 5 | Both press platens are at the same working height (taken as 950 mm) and a 1 m mould fits the cooling press and the 1.04 m second opening | The transfer bridge and the booth openings are set from them | RFE-DDR-003, P4 |
| 6 | The fan and filter box size, mass, inlet height (2.05 m) and outlet position | The fan stand and the stack are made to fit it | RFE-DDR-003, P8 |
| 7 | The board's size fits its 700 x 800 mm place on the backboard | The backboard is cut before the board is chosen | RFE-DDR-003, P6 |

## Value engineering

Value-engineering target: USD 25,000 for equipment items 1 to 12 (requirement R10; a hypothetical control target, not a limit; `budget_usd` is null because this is a playbook repo). Estimated cost of the constructable design: USD 25,300 (USD 300 over the target), plus about USD 9,200 for the container shell, which is site-dependent and outside the target. Main cost drivers and savings worth trying:

- The largest lines are the sheet press, cooling press and transfer bridge (USD 6,250), the shredder with its enclosure (USD 4,100), the extruder (USD 4,000) and the fume extraction (USD 3,350). Together they are 70 % of the equipment.
- Making the design constructable added USD 1,100 to the equipment (sash, take-off, brackets, wall sleeve and fan stand USD 400; backboard and cable tray USD 400; transfer bridge USD 250; drying fan stand USD 50) and USD 1,200 to the container shell (seam beam, floor plate, flashing).
- Savings worth trying: a cooling press built from scrap steel plate and the drying rack and fan stand from offcuts of the same stock (about USD 300 together); second-hand pallet racking (about USD 150); a rented shed instead of containers, which removes the USD 1,200 of seam work and most of the shell cost; quotes from two local fabricators for the press, which is the largest single line.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Plastics-only reference line with aluminium as a separate add-on bay; two 40 ft container footprints or a shed of about 60 m²; PET sold as clean flake; passport schema v0.2 with example records; single-phase supply with staggered heating; keep CERN-OHL-S-2.0 on the playbook text for now | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | RFE-DDR-001, items 1 to 6 |
| 2026-09-25 | First release licensing (documents CC BY-SA 4.0, hardware CERN-OHL-S-2.0, scripts MIT); R8 keeps the honest total with an intake quality rule (R16, 10 % residue threshold); derated 5 kW single-phase sheet press as the reference; 1.5 kW fume fan; rented shed preferred, container side walls removed only to a structural engineer's design | Amish: "i accept all your recommendations, go with them across all repos." | RFE-DDR-002, items 6 (release) and 8 to 11 |
| 2026-09-25 | TRL 4 on hold for every repo | Amish: "Make sure we don't proceed to TRL 4 on any of them." | RFE-DDR-001 |
| 2026-10-01 | Budgets are value-engineering targets, not limits; R10 reported as over or under its target | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | This register; RFE-CAL-001 v0.3 |
