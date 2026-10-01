---
doc_id: RFE-DDR-003
title: ReflowEconomy design for construction
project: ReflowEconomy
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the reference micro-factory physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; they are open for his review. The questions in Table 3 touch the safety case and are **Proposed, awaiting Amish**; they are also listed in the design decisions register (RFE-DEC-001).

> **Safety:** The reference micro-factory has a shredder, surfaces at 190 to 200 °C, melt fumes, water near electricity, lithium cells in the waste stream and a high fire load. No change here relaxes a safety rule. Four changes touch the safety case (the shredder feed height, the booth's second opening, doors and gates that open into the aisle, and the aisle headroom); each is recorded below and put to Amish, not decided.

## Context

On 2026-09-30 Amish asked for a prototype build plan for every repo that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." For ReflowEconomy the prototype is the reference micro-factory itself, fitted out in its shell.

The TRL 3 layout model (`cad/src/model.py` as of RFE-DDR-002) showed where everything goes and passed the zone-level checks in RFE-CAL-001, but it was a set of envelopes. Checking it with build123d (pairwise solid intersections, lowest point of every part, height against the container roof) and walking through how each part would be fixed found the problems in Table 1: four solid overlaps, eight parts hanging in the air with no support or fixing, a duct that ran through the press booth without connecting to it, a cooling press that could not be reached, a feed chute mouth 2.1 m above the floor, a door that could not open, and no structure for the container option.

The changes keep what the micro-factory does: the same footprint, zones, rows, aisle, hot zone, machines, hood openings and flows, mass balance, energy and electrical figures. The model now runs 1,457 constructability checks (`python cad/src/model.py --check`): no two parts overlap, 37 listed pairs touch where they must be fixed, nothing inside is above the roof underside, nothing stands in the painted aisle, and the aisle keeps at least 2.0 m headroom. All pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem found | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | Container option: with the adjoining side walls removed, nothing carried the roof along the 12 m seam, and the floor had an open joint down the middle of the aisle. | A seam beam under the roof along the seam, carried on the container corner posts at both ends, with a 165 x 305 mm space reserved for it; its section, fixings and the propping sequence are the structural engineer's (the walls are cut only after it is in). A 300 x 4.5 mm aluminium tread plate covers the floor seam in four lengths, screwed along one edge only. | RFE-DDR-002 item 11 already requires an engineer's design for the wall removal; reserving the space lets the rest of the layout be checked against it. Screwing one edge lets the two containers move without tearing the plate. Not needed in a rented shed. |
| P2 | Hood B (the extruder barrel enclosure) cut 100 mm into the extruder and hung in the air (2,000 cm³ overlap, lowest point 1.0 m up). | The extruder is drawn as a frame, drive, hopper and barrel. Hood B is a 1,000 x 500 x 450 mm open-bottomed sheet box that stands on the frame top and is bolted to it; the barrel passes through a 120 mm hole in its end; the open face (0.8 x 0.4 m, unchanged) faces the aisle; the duct riser stands on a spigot in its top. | The frame is the only thing there to carry the hood, and bolting to it keeps the hood aligned with the barrel. The open face area and so the airflow are unchanged. |
| P3 | The main duct ran straight through the press booth wall and roof (13,200 cm³ overlap) and had no inlet inside the booth, so booth A was not actually extracted. | The duct is lowered to a 2.05 m centre so it passes under the booth roof; it enters through a sealed collar in the booth's end wall, turns to the back wall inside the booth and leaves through a flanged wall sleeve. A booth take-off with a balancing damper sits below the elbow inside the booth. Two wall brackets carry the run. | A two-branch system (booth take-off and hood B branch meeting at the elbow) is the normal way to serve two hoods from one fan; the damper sets the split. The route is shorter than the 8 m equivalent length in RFE-CAL-001, so the fan sizing stays conservative. |
| P4 | The booth had one sash in front of the hot press. The cooling press stood behind a blank wall, so a hot mould could neither be moved to it nor the cooled sheet taken out. | Two front openings (1.2 x 0.6 m at the hot press, 1.04 x 0.6 m at the cooling press) and one 1.25 x 0.65 m sash that slides in rails along the booth front and covers one opening at a time. A 50 mm roller transfer bridge between the presses at platen height lets the mould slide across inside the booth. The cooling press moves 50 mm toward the hot press so a 1 m mould fits the second opening. | One sash means only one opening can ever be open, so the open area used to size the fan (1.2 x 0.6 m) is never exceeded. The hot mould does not leave the booth. |
| P5 | The shredder enclosure had a 60 mm floor slab that the shredder stood inside (39,800 cm³ overlap); its feed chute was a solid block with its mouth 2.1 m up, too high to tip a tote into; its access door opened into the washing tanks 300 mm away. | No floor: the panels stand on the building floor round the shredder and are cleated down. The roof is lowered to 1.60 m (28 mm over the shredder) and the chute is a hollow collar through it with its mouth at 1.70 m and an interlocked lid. The interlocked access door moves to the aisle face. | The shredder's own hopper still takes the material; the collar and lid keep the interlocked feed of the concept. The door now opens where there is room and where the flake bin comes out. See A1 and A3. |
| P6 | Electrical board and eyewash were drawn on the corrugated container wall with nothing to fix to (lowest points 1.2 and 0.8 m). | An 18 mm fire-retardant plywood backboard, 1.3 x 1.55 m, on rivet nuts in the corrugation crests; the board and eyewash screw to it. | A flat, fixable face that does not depend on hitting a corrugation with every screw. |
| P7 | No cable route: every motor and heater is fed from the board on the back wall, but the shredder, pump and drying fan are across the aisle. | A 100 x 50 mm perforated cable tray: a back run on the backboard and wall spacers to the booth, one crossing of the aisle clamped under the seam beam (underside 2.04 m above the floor), and a front run on the front wall. | One crossing, carried by the beam, with the least loss of headroom. See A4. |
| P8 | The fan and filter box floated outside the back wall, 1.6 m up, and above the wall top. | A braced stand of 50 x 50 mm tube on anchored base plates carries the box; the discharge stack in the BOM is drawn, ending 1 m above the roof. | The stack was already specified (RFE-CAL-001); the stand is the simplest support that does not load the container wall. |
| P9 | The drying fan hung in the air in front of the rack. | A floor stand (base plate and 60 mm post) carries the fan with its axis 0.9 m up, 100 mm from the trays. | |
| P10 | The export cage stood 170 mm from the export doors, with its only possible gate facing them, so it could not be opened. | A 1.2 m double gate on the cage's aisle face. | The gates open into the aisle only while loading. See A3. |
| P11 | The four bins stood 30 mm over the painted aisle line; the flake bags were drawn through a racking shelf. | The sorting table moves 40 mm toward the front wall and the bins stand behind the line; the bags sit on the racking levels. | Keeps the aisle clear; the clear aisle widens from 1.52 to 1.57 m. |
| P12 | The hot zone boundary line ran under the booth wall. | The line's far leg is 50 mm wide and runs along the outside of the booth wall. | Paint cannot go under a wall that is already there; the boundary and the 1.0 m clearance to stock are unchanged. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Cost | BOM items 4 (+$50), 6 (+$250), 7 (+$400) and 11 (+$400): items 1 to 12 go from $24,200 to $25,300, $300 over the R10 value-engineering target of $25,000. Item 13 (container option) +$1,200 to $9,200. Items 3 and 12 change in specification only. | Parts added for construction. |
| Economics | Capex in `economics_inputs.csv` $25,300; result +$0.73 per shift before rent (was +$1.61); break-even product price $2.48/kg (was $2.45/kg); break-even input 99 kg (was 98 kg). | Follows the cost. |
| Layout | Clear aisle 1.57 m (was 1.52 m); aisle headroom 2.04 m; hot zone clearance to stock unchanged at 1.00 m. | P11, P7. |
| Hoods, energy, electrical | Unchanged: openings, airflow, pressure, fan power, energy per shift and maximum demand are the same. | P3, P4 keep the sized open area. |
| Drawing | RFE-DWG-001 Rev P3; making sketches RFE-DWG-101 to 111 added. | Follows the model. |
| Documents | RFE-CAL-001 v0.3, RFE-REQ-001 v0.5, RFE-PRC-001 v0.5; build plan RFE-BLD-001 v0.1; design decisions register RFE-DEC-001 v0.1. | Follows the model. |

*Table 3. Proposed, awaiting Amish (these touch the safety case).*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Shredder feed. The chute mouth is now 1.70 m up (was 2.1 m), so the distance from the mouth to the cutters is shorter than in the concept. | (a) 1.70 m mouth as modelled, with the reach distance from the mouth to the cutters checked against ISO 13857 at the safety review and the chute lengthened if it falls short; (b) the concept's 2.1 m mouth with a fixed step platform and handrail. | (a): no work at height, and the interlocked lid still stops the rotor whenever it is open. |
| A2 | Booth A now has a second opening at the cooling press, covered by the one sliding sash. | (a) one sliding sash over two openings, as modelled; (b) two sashes with an electrical interlock so only one opens; (c) one opening only, with the cooled sheet taken out through it. | (a): the single panel makes "one opening at a time" mechanical, not a rule. |
| A3 | The shredder enclosure door and the cage gates open into the aisle. | (a) hinged, opening into the aisle only during locked-off maintenance or loading; (b) sliding door and gates (about +$300). | (a), with the rule written into the safety section of the playbook. |
| A4 | Aisle headroom is 2.04 m under the cable tray crossing and about 2.09 m under the seam beam (container option). | (a) accept, if the local code allows 2.0 m on an escape route; (b) take the cables through a sleeve in the beam web, if the engineer allows. | (a), confirmed against the local building code by the safety professional. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan RFE-BLD-001 (`docs/05-build-plan.md`) shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: 3 not met (R1, R4, R8), 2 at risk (R6, R12), 2 not verifiable at TRL 3 (R11, R15), 8 met on paper, and R10 $300 over its value-engineering target (RFE-CAL-001 v0.3). No requirement became not met.
- The photoreal render (`media/render-hero.png`), `media/card.png` and `media/social-preview.png` still show the concept layout (no seam beam, cable tray, fan stand, sash or new hood B); they need regenerating on Amish's Mac.
- The machines (shredder, extruder, presses) are built to their published open designs or bought; their dimensions must be confirmed when they are chosen (RFE-DEC-001, items to confirm).
