---
doc_id: RFE-RSK-001
title: ReflowEconomy risk register and hazard analysis
project: ReflowEconomy
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis and first-pass design FMEA (kit 1.8 pipeline, stage P3) for the reference micro-factory (option A)
---

# ReflowEconomy risk register and hazard analysis

The top project risks are the electrical supply (the morning loads exceed a 40 A single-phase supply once motor currents are counted), product prices too low to pay for the equipment, and the input mix carrying more residue than the 10 % the disposal target needs. The top hazards are the shredder, melt fumes, hot platens, lithium cells in the input and the fire load of plastic stock. Method: STANDARDS section 23. Likelihood, impact, severity, occurrence and detection are scored 1 (low) to 5 (high); for detection, 5 means the failure is hardest to detect.

> **Safety:** This is a paper analysis at TRL 3. A qualified safety professional, a licensed electrician and, for the container option, a structural engineer must review the design before any site operates (RFE-BLD-001 stops S1 to S7).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | The site cannot run on the supply it can get | Motor drives and single-phase motors draw about 55 A in the morning block against a 40 A single-phase supply (RFE-STM-001 S14) | Breakers trip; or the line runs fewer hours or less input | 5 | 4 | Design lead, with Amish | Decision D1: three-phase recommended; single-phase fallback in three blocks |
| P2 | Products do not sell at the assumed price | The site needs 2.49 USD/kg; regenerated HDPE sheet is listed in India at about 0.5 to 1 USD/kg (RFE-MKT-001) | Losses every shift | 4 | 5 | Partner and operator | Design-grade sheets and furniture for named buyers; staged start as a sort-and-bale hub (RFE-DEC-001 D4) |
| P3 | Input carries too much residue | Mixed collection; the 10 % intake threshold refuses loads pickers bring | Disposal over 20 % (PR-008) or loss of supply goodwill | 4 | 3 | Partner | Agree the intake rule with collectors in co-design (UR-019) |
| P4 | Machine rates below the assumptions | Shredder at the low end of 8.8 to 41.8 kg/h; derated press | Less than 100 kg a shift (PR-006) | 3 | 3 | Design lead | Measure at TRL 4; three-phase supply allows the published 15 kW press |
| P5 | No co-design partner agrees | Partner priorities and capacity | Requirements stay first-pass; no site | 3 | 4 | Amish | Approach SWaCH through WIEGO as decided; second candidates in the plan |
| P6 | Permits take long or cost more | Consent route and category not yet known (RFE-REG-001 G2) | Delay before operation | 3 | 3 | Operator with a consultant | Assess the category early with MPCB |
| P7 | Exposure limits exceeded in practice | Hood gaps, sash left open, filters not changed | Harm to workers; site closure | 2 | 5 | Safety professional | Face velocity checks, filter log, air monitoring at TRL 4 |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Shredder cutters | Hand or arm reaching through the feed or the door | Amputation | 5 | 2 | Cranked feed hood, 120 mm slot and 1,060 mm reach path (ISO 13857 Table 4), interlocked flap and door, emergency stops, lockout | Low |
| H2 | Melt fumes | Formaldehyde, acrolein and aerosol from HDPE and PP at 190 to 210 C; PVC releasing HCl if missed at sorting | Respiratory harm | 4 | 3 | Two enclosing hoods at 0.5 m/s, sash covering one opening, filters and stack, PVC excluded at sorting | Medium until air monitoring |
| H3 | Hot platens and barrel | Contact at 190 to 200 C | Burns | 4 | 3 | Insulated platen packs, booth with sash, gloves and face shields, cool-down rule | Medium |
| H4 | Press closing force | Hands between platens | Crushing | 4 | 2 | Mould loaded on the transfer bridge, hands clear before the jacks are pumped; sash closed while pressing | Low |
| H5 | Noise | Shredder in a reverberant steel room | Hearing loss | 3 | 3 | Lined enclosure (79 dB(A) on paper), hearing protection zone until measured | Medium |
| H6 | Electric shock | Water near electricity at the tanks | Death or injury | 5 | 2 | 30 mA RCDs, splash-rated sockets, licensed installation | Low |
| H7 | Lithium cell fire | A cell in the input reaches the shredder or is crushed | Fire, smoke | 5 | 3 | Cells pulled out at intake, dry-sand container in the cage, three extinguishers | Medium |
| H8 | Fire in plastic stock | Ignition near flake and products; dust | Fire | 5 | 2 | Stock 1.0 m from the hot zone, daily cleanup, exits at both ends | Medium |
| H9 | Sharps and contaminated input | Needles, glass, chemical containers | Cuts, infection, poisoning | 3 | 4 | Puncture-resistant gloves, sharps container, refusal of medical and chemical waste | Medium |
| H10 | Manual handling | Bags and sheets | Back injury | 3 | 3 | Bags of 25 kg or less; transfer bridge between presses | Low |
| H11 | Container structure | Side walls removed at the seam | Collapse | 5 | 1 | Seam beam and propping to a structural engineer's design; shed preferred | Low |
| H12 | Low headroom | Cable tray crossing at 2.04 m | Head strike | 2 | 2 | Padding and hazard tape (2.02 m under the padding) | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Electrical supply | Carry the morning loads | Breaker trips under load | Line stops; heaters cool mid-cycle | Input currents about 55 A on a 40 A supply | 4 | 5 | 2 | 40 | Decision D1; clamp-meter check at TRL 4 (BLD first checks) |
| F2 | Heater interlock | Keep the press heaters off while a motor runs | Contactor welded or bypassed | Overload, nuisance trips, overheating cables | Contact wear; manual bypass | 4 | 2 | 4 | 32 | Set a performance level (ISO 13849-1); test at every start-up |
| F3 | Feed flap interlock | Stop the rotor when the flap opens | Switch defeated or fails to danger | Exposure to the cutters | Tampering; single-channel switch | 5 | 2 | 3 | 30 | Coded or guard-locking switch (ISO 14119); daily check |
| F4 | Feed hood and slot | Keep a hand 850 mm from the cutters | Slot widened or hood removed for big parts | Reach to the cutters | Operators feeding oversize pieces | 5 | 2 | 3 | 30 | Pre-cut and crush at sorting; bolted hood; training |
| F5 | Fume fan and filters | Hold 0.5 m/s at the hood faces | Face velocity drops | Fume exposure | Filters loaded; damper moved; fan belt or motor fault | 4 | 3 | 4 | 48 | Filter log; pressure gauge across the filters; anemometer check monthly |
| F5a | Fume duct | Carry fume to the filters | Wax condensate builds up and catches fire | Duct fire | Aerosol condensing in the cool galvanised duct | 5 | 2 | 4 | 40 | Cleaning schedule and inspection hatch; no heat source downstream of the hoods |
| F6 | Booth sash | Leave only one opening uncovered | Both openings open | Lower face velocity | Sash removed for cleaning and not refitted | 3 | 2 | 2 | 12 | Stops on the rails; check before heaters on (stop S4) |
| F7 | Shredder enclosure | Cut noise by about 15 dB | Insertion loss well below 15 dB | Exposure above 85 dB(A) | Gaps, door seal worn, slot flap left open | 3 | 3 | 3 | 27 | Measure at TRL 4; seal and flap checks |
| F8 | Enclosure ventilation | Keep the gearmotor cool | Motor overheats | Trip or motor damage | No vent in the lined enclosure | 3 | 3 | 3 | 27 | Confirm temperature when bought (DEC confirm item 3); lined vent baffle if hot |
| F9 | Float-sink tank | Separate PP and HDPE from PET and PVC | PVC or filled plastics pass to the melt | HCl fumes; product defects | Filled or foamed plastics; PVC not removed at sorting | 4 | 3 | 3 | 36 | Sorting rule; NIR or WasteWise check for unclear parts |
| F10 | Hot press | Hold 190 to 200 C through the cycle | Platen overheats past 230 C | Degraded melt, more fume | Thermocouple fault or controller failure | 4 | 2 | 3 | 24 | Independent over-temperature cut-out |
| F11 | Cell container | Hold a burning cell | Fire spreads | Fire in the cage | Sand missing or container left open | 5 | 2 | 3 | 30 | Lid and sand checked at each shift; extinguisher at the entrance |
| F12 | Seam beam (container option) | Carry the roof edges over the 12 m seam | Lateral-torsional buckling | Roof sags or fails | Top flange not tied to the roof | 5 | 1 | 4 | 20 | Structural engineer's design ties the flange (RFE-STM-001 S18) |
| F13 | Cable tray crossing | Cross the aisle above head height | Head strike | Minor injury | Padding missing | 2 | 2 | 2 | 8 | Padding and tape in place (stop S7) |
| F14 | Passport desk | Issue a valid passport for every lot | Lot leaves without a passport | Buyer distrust; export refused | Rush at the end of a shift | 3 | 3 | 3 | 27 | Labels printed only from a valid record; end-of-shift check |
