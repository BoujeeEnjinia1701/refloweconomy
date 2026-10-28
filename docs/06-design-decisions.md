---
doc_id: RFE-DEC-001
title: ReflowEconomy design decisions register
project: ReflowEconomy
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the build plan; open decisions from RFE-DDR-001 to RFE-DDR-003; equipment cost treated as a value-engineering target
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Amish approved the recommendations for all six open decisions (2026-10-02); RFE-DDR-003 accepted; moved to decisions made'
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Approved follow-ups carried into the design: feed hood, self-closing hinges, tray padding; Value engineering restated at USD 25,505'
- version: "0.4"
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Kit 1.9.1 upgrade: STEM check fixes D2 and D3 recorded as decided under Amish''s standing instruction of 2026-10-23; D1 (supply current) and D4 (concept selection) proposed, awaiting Amish'
---

# ReflowEconomy design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | What is to be decided | Options | Recommendation | What it affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| D1 | How the micro-factory meets its supply limit. Counted as currents, the morning block (shredder, extruder, pump, fans, lights) draws about 55 A running and 72 A at full load from the 230 V, 40 A single-phase supply decided on 2026-09-25 (RFE-STM-001 S14; PR-017 not met) | (a) a 400 V three-phase supply (about 18.5 A a phase; in Maharashtra any supply over 40 A is three-phase); (b) keep single phase and split the morning so the shredder and extruder never run together (largest block 36 A, working day about 10.6 h, about 13 USD a shift more in wages, result about -12.7 USD a shift); (c) keep 8 h and single phase and take less input per shift | (a), with (b) written into the playbook as the single-phase fallback | The electrical board, the drives (three-phase drives under (a)), the heater interlock logic, the shift pattern in the recipes and economics model, and the pitch line "works on a weak grid" | RFE-DDR-005; RFE-CAL-001 section 5 |
| D4 | Concept selection. The sort-and-bale hub (B) outscores the reference micro-factory (A) in RFE-OPT-001 by more than 10 % | (1) A; (2) B; (3) A with a staged start taken from B (open as a sort-and-bale hub, add the remanufacturing line later) | (3): it keeps the pitch, which B alone gives up, and takes B's low-capital, low-power start | Nothing in A's model, drawing, BOM or build plan under (1) or (3); a new playbook section under (3); a full redesign under (2) | RFE-DDR-004; RFE-OPT-001 |

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
| 8 | The cutter height of the shredder actually built (taken as 1,100 mm) and that its feed opening takes pieces under 120 mm | The 1,060 mm reach path through the 120 mm slot rests on it (RFE-DEC-001 D3) | RFE-DDR-005 |
| 9 | The input current of the drives chosen (single-phase input drives draw about 2.4 times their power divided by the voltage) | The supply check (D1) uses datasheet currents of one drive family | RFE-DDR-005 |

## Value engineering

Value-engineering target: USD 25,000. Estimated cost of the constructable design: USD 25,505 (USD 505 over the target).

The target covers equipment items 1 to 12 (requirement R10; a hypothetical control target, not a limit; `budget_usd` is null because this is a playbook repo). The container shell adds about USD 9,200; it is site-dependent and outside the target. Main cost drivers and savings worth trying:

- The largest lines are the sheet press, cooling press and transfer bridge (USD 6,250), the shredder with its enclosure and feed hood (USD 4,205), the extruder (USD 4,000) and the fume extraction (USD 3,350). Together they are 70 % of the equipment.
- Making the design constructable added USD 1,100 to the equipment (sash, take-off, brackets, wall sleeve and fan stand USD 400; backboard and cable tray USD 400; transfer bridge USD 250; drying fan stand USD 50) and USD 1,200 to the container shell (seam beam, floor plate, flashing).
- Carrying the decisions of 2026-10-02 into the design added USD 205: the cranked feed hood and three self-closing door hinges (USD 105), two pairs of self-closing cage gate hinges (USD 60), and padding and hazard tape on the tray crossing (USD 40).
- Savings worth trying: a cooling press built from scrap steel plate and the drying rack and fan stand from offcuts of the same stock (about USD 300 together); second-hand pallet racking (about USD 150); a rented shed instead of containers, which removes the USD 1,200 of seam work and most of the shell cost (a shell saving, outside the equipment target, so it does not reduce the USD 505 gap); quotes from two local fabricators for the press, which is the largest single line.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Plastics-only reference line with aluminium as a separate add-on bay; two 40 ft container footprints or a shed of about 60 m²; PET sold as clean flake; passport schema v0.2 with example records; single-phase supply with staggered heating; keep CERN-OHL-S-2.0 on the playbook text for now | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | RFE-DDR-001, items 1 to 6 |
| 2026-09-25 | First release licensing (documents CC BY-SA 4.0, hardware CERN-OHL-S-2.0, scripts MIT); R8 keeps the honest total with an intake quality rule (R16, 10 % residue threshold); derated 5 kW single-phase sheet press as the reference; 1.5 kW fume fan; rented shed preferred, container side walls removed only to a structural engineer's design | Amish: "i accept all your recommendations, go with them across all repos." | RFE-DDR-002, items 6 (release) and 8 to 11 |
| 2026-09-25 | TRL 4 on hold for every repo | Amish: "Make sure we don't proceed to TRL 4 on any of them." | RFE-DDR-001 |
| 2026-10-01 | Budgets are value-engineering targets, not limits; R10 reported as over or under its target | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | This register; RFE-CAL-001 v0.3 |
| 2026-10-02 | Design for construction accepted: all the changes of Table 1 and their knock-on changes, as made, with the four safety-case items decided separately (A1 to A4, below) | Amish: "i approve your recommendations for all 555 open decisions." | RFE-DDR-003, Table 1 |
| 2026-10-02 | Shredder feed: keep the 1.70 m chute mouth, but do the ISO 13857 reach check from the model now rather than at the safety review, and lengthen or baffle the chute until it passes | Amish: "i approve your recommendations for all 555 open decisions." | RFE-DDR-003, A1 |
| 2026-10-02 | Press booth: one sliding sash over the two openings, as modelled | Amish: "i approve your recommendations for all 555 open decisions." | RFE-DDR-003, A2 |
| 2026-10-02 | Shredder enclosure door and cage gates: hinged, opening into the aisle only during locked-off maintenance or loading, with self-closing hinges and the rule in the playbook's safety section; sliding door and gates instead if the open door leaves less than the local code's minimum escape width | Amish: "i approve your recommendations for all 555 open decisions." | RFE-DDR-003, A3 |
| 2026-10-02 | Aisle headroom: accept 2.04 m, confirmed against the local code by the safety professional, with the tray crossing padded and marked with hazard tape | Amish: "i approve your recommendations for all 555 open decisions." | RFE-DDR-003, A4 |
| 2026-10-02 | First co-design partner and region: (a), a waste-picker cooperative; first candidate to approach, SWaCH in Pune, India, reached through the WIEGO network (not agreed) | Amish: "i approve your recommendations for all 555 open decisions." | RFE-DDR-001, item 7; RFE-DDR-002 |
| 2026-10-25 | D2: the energy budget counts motor and drive losses (electrical input = shaft energy / (motor x drive), IE3 efficiencies, 96 % drive); 45.6 kWh per shift, 0.88 kWh/kg | Decided under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it in DEC as decided under that instruction"); Amish can reverse it | RFE-DDR-005; RFE-STM-001 S13 |
| 2026-10-25 | D3: the feed slot in the cranked feed hood is 460 x 120 mm (was 160 mm tall) so ISO 13857 Table 4 applies to the 1,060 mm reach path; hood 140 mm tall | Decided under Amish's standing instruction of 2026-10-23; Amish can reverse it | RFE-DDR-005; RFE-STM-001 S17 |
