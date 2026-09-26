---
doc_id: RFE-CAL-001
title: ReflowEconomy reference micro-factory sizing and economics
project: ReflowEconomy
doc_type: Calculation note
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue at TRL 3 (mass balance, throughput, energy, supply, fume hoods, noise, layout, cost, economics model, passport v0.2 check)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Fume fan 1.5 kW (maximum demand 8.75 kW, 38.0 A; equipment $24,200; result +$1.61 per shift); intake quality rule (R16, 10 % residue threshold) added to the mass balance; rented shed preferred over containers
---

# ReflowEconomy reference micro-factory sizing and economics

On paper, the reference micro-factory handles 100 kg of mixed input per 8 h shift on 59.4 m², keeps 51.6 % of the input local as products and clean flake, uses 0.83 kWh per kilogram of output, needs at most 8.75 kW (38.0 A at 230 V) on a single-phase supply with staggered heating, and costs $24,200 in equipment. It breaks even at best: the result is about +$1.61 per shift before rent at the reference prices, and the break-even product price is $2.45/kg against an assumed $2.50/kg. Three requirements are **not met** (R1, R4 and R8: 28.4 % of the reference input goes to licensed disposal against a 20 % target; the new intake quality rule R16 shows a load needs 10.6 % residue or less to meet it), two are **at risk** (R6 throughput, R12 noise) and two cannot be verified at TRL 3 (R11 exposure, R15 form time).

Every number in this note is printed by `python docs/04-calcs/sizing.py`, which also writes `docs/04-calcs/results.csv`. The script reads the layout from `cad/src/model.py`, the equipment cost from `bom/bom.csv` and the economics from `docs/playbook/economics_model.py` with `docs/playbook/economics_inputs.csv`, and it stops with an error if the economics inputs disagree with this calculation. All values are estimates for a paper proof of concept; none has been measured.

> **Safety:** This note sizes guarding, fume extraction and electrical supply on paper only. The micro-factory combines a shredder, surfaces at 190 to 200 °C, melt fumes, water near electricity and a high fire load. A qualified safety professional and a licensed electrician must review the design before any site operates.

## 1. Basis

Decisions applied (RFE-DDR-001, decided by Amish on 2026-09-25): plastics-only reference line, with aluminium as a separate add-on bay (item 1); two 40 ft container footprints (item 2); PET sold as clean flake (item 3); passport schema v0.2 (item 4); single-phase supply with staggered heating (item 5). Further decisions accepted by Amish on 2026-09-25 (RFE-DDR-002): R8 keeps counting process losses and an intake quality rule is added (item 8); the derated 5 kW single-phase press stays the reference, with the published 15 kW press where 400 V exists (item 9); a 1.5 kW fume fan (item 10); a rented shed is preferred to the container option (item 11).

Shift pattern (assumption): one 8 h shift, four workers. Block A (hours 0 to 4) is sorting, washing, shredding and extrusion; block B (hours 4 to 8) is the sheet press. The hot zone runs on flake dried during the previous shift, so extrusion can start at once.

## 2. Mass balance

Assumptions: source-separated or picker-sorted post-consumer input of 22 % PET, 20 % HDPE, 18 % PP (60 % target plastic), 8 % metals, 2 % e-waste, 10 % paper and card and 20 % residue by mass; washing and float-sink remove 10 % of plastic mass; shredding loses 1.5 % and drying 1 % as fines and spills; 3 % of the melt feed is lost as purge and degraded material; trim of 8 % of the gross melt output is re-shredded and returned. Dry basis.

*Table 1. Mass balance per 100 kg of input (estimates).*

| Stream | Mass | Destination |
| --- | --- | --- |
| HDPE and PP products (sheets, beams) | 32.3 kg | Local sale with passport |
| PET clean flake | 19.3 kg | Local or regional sale with passport |
| Metals (aluminium, steel) | 8.0 kg | Sold for smelting, with passport |
| E-waste boards and cells | 2.0 kg | Licensed refiner or cell tester, with passport |
| Paper and card | 10.0 kg | Local mill |
| Sorting residue (PVC, multilayer, film, organics) | 20.0 kg | Licensed disposal, never burned |
| Process losses (labels, dirt, fines, purge) | 8.4 kg | Licensed disposal |

The mass closes at 100.00 kg. Products and flake kept local are **51.6 %** (R7, target 50 %: met with a margin of 1.6 points). Everything sent to licensed disposal is **28.4 %** (R8, target 20 %: **not met**). The sorting residue alone is exactly 20 %; the process losses push the total over. R8 depends mostly on collection quality, which the site does not control directly.

**Intake quality rule (R16).** Amish decided on 2026-09-25 (RFE-DDR-002, item 8) to keep the honest total in R8, process losses included, and to add an intake quality rule. For a load with sampled residue r, the other streams scale with (100 - r), so the process losses are 8.4 x (100 - r) / 80 kg per 100 kg. Disposal stays at 20 % or less when r is **10.6 %** or less. The rule threshold is set at **10 %** residue by sampled mass: at that threshold disposal is 19.5 % and 58.0 % of input is kept local. Loads above it are refused or charged a disposal fee. The reference mix (20 % residue) would fail the rule, so R8 stays **not met** for the reference input; meeting it depends on a cleaner supply agreed with collectors, which only a co-design partner can confirm. The TRL 2 precis gave 30 kg of products, 20 kg of flake and 10 kg of losses; those figures are replaced by Table 1.

## 3. Throughput and time budget

Assumptions: two sorters at 25 kg/h each; shredder effective rate 15 kg/h, within the 8.8 to 41.8 kg/h range published for the Precious Plastic Shredder Pro ([Precious Plastic Academy](https://onearmy.github.io/academy/build/shredderpro)); extruder 5 kg/h of beams; sheet press cycle 55 min per 12 mm sheet, as published for the Precious Plastic sheetpress ([Precious Plastic Academy](https://onearmy.github.io/academy/build/sheetpress)); heaters off 30 min before the end of the shift.

*Table 2. Time budget per shift.*

| Step | Load | Time needed | Time available | Margin |
| --- | --- | --- | --- | --- |
| Sorting | 100 kg | 2.0 h | 4 h (block A) | Ample |
| Shredding | 56.8 kg (54.0 kg washed plastic plus 2.8 kg trim) | 3.79 h at 15 kg/h | 4 h | 5 %; needs 14.2 kg/h |
| Extrusion | 12.3 kg of beams | 2.79 h including 0.33 h heat-up | 4 h | 30 % |
| Sheet press | 2 sheets of 11.4 kg | 1.62 h heat-up plus 2 x 55 min | 3.5 h | 2.06 sheets of capacity for 2 |
| Drying | 52.7 kg of flake | 7.3 kg/m² on 7.2 m² of trays | 10 kg/m² | 27 % |

R6 (100 kg or more per shift) is **at risk**. The shredder has 5 % margin at an assumed rate; at the low end of the published range (8.8 kg/h) it would need 6.5 h. The sheet press has almost no margin because heating 285 kg of steel platens from cold on 5 kW takes 1.62 h. A 5 kW single-phase press is a derated variant: the published Precious Plastic sheetpress is 15 kW on a 400 V, 32 A supply, and the Shredder Pro and Extrusion Pro are also specified for 400 V. Their motors can run on single-phase-input variable-frequency drives; the press heaters cannot deliver 15 kW on a 40 A single-phase supply. Amish decided on 2026-09-25 (RFE-DDR-002, item 9) that the derated 5 kW press stays the playbook reference, with the published 15 kW press as an option where a 400 V supply exists; the 15 kW press would heat up in well under an hour and remove the press constraint, but it needs three-phase. The rates must be measured on the chosen machines.

## 4. Energy per shift

The sheet press is sized from first principles. Heat-up: two 1.1 x 1.1 m steel platens 15 mm thick (285 kg, specific heat 0.49 kJ/kg K) from 25 to 200 °C take 6.79 kWh. Per sheet: 11.4 kg of HDPE (specific heat 2.25 kJ/kg K over 175 K plus 180 kJ/kg latent heat) and 31 kg of steel mould take 2.56 kWh. The standing loss of the hot press is taken as 0.8 kW (assumption). During cycles the press draws about 3.6 kW of its 5.0 kW, so the heaters can hold the published 55 min cycle.

*Table 3. Energy per shift (estimates).*

| Load | Basis | Energy |
| --- | --- | --- |
| Shredder | 2.2 kW at 70 % for 3.79 h | 5.8 kWh |
| Washing pump | 0.75 kW for 4 h | 3.0 kWh |
| Drying fan | 0.4 kW for 8 h | 3.2 kWh |
| Extruder | 2.0 kW heat-up for 0.33 h; 2.0 kW heaters at 60 % duty and 1.5 kW motor at 60 % for 2.45 h | 5.8 kWh |
| Sheet press | Heat-up at 5 kW for 1.62 h; 2 sheets at 2.56 kWh; 0.8 kW loss over 2 cycles | 14.7 kWh |
| Fume extraction | 1.00 kW input for 7.2 h (1.5 kW fan) | 7.2 kWh |
| Lighting, desk and small loads | 0.4 kW for 8 h | 3.2 kWh |
| **Total** | | **42.9 kWh** |

The line uses **0.83 kWh per kilogram** of products and flake (51.6 kg), against the R9 target of 1.0 kWh/kg: met on paper. Of the total, 22.4 kWh per shift is fixed (heat-up, fume fan, lights and drying fan) and does not fall if less material comes in. The TRL 2 estimate of about 45 kWh and 0.9 kWh/kg is replaced by these figures.

## 5. Electrical supply

Amish decided on single-phase supply with staggered heating (RFE-DDR-001, item 5). The supply is taken as 230 V, 40 A (9.2 kW). The staggering rule is enforced by an interlock contactor on the electrical board: the press heaters are locked out while the shredder or the extruder runs.

*Table 4. Peak demand.*

| Block | Loads running together | Peak |
| --- | --- | --- |
| A (sort, wash, shred, extrude) | Shredder 2.2, pump 0.75, drying fan 0.4, lights 0.4, extruder 3.5, fume fan 1.5 kW | 8.75 kW |
| B (press) | Press heaters 5.0, drying fan 0.4, lights 0.4, fume fan 1.5 kW | 7.30 kW |

The maximum demand is **8.75 kW, 38.0 A** at 230 V, 5 % below the 40 A supply (it was 8.35 kW and 36.3 A with the 1.1 kW fan in v0.1). Without the interlock the connected load of 13.75 kW would draw 60 A. Motor starting currents are not included; the shredder and extruder motors start through their drives. The licensed electrician must confirm the supply rating, earthing and RCD selection on site.

## 6. Fume extraction

R11 asks for a face velocity of 0.5 m/s or more at the hood of every melt process. A canopy over the whole hot zone (2.0 x 3.5 m) would need 3.5 m³/s and about 6.1 kW of fan power, more than the single-phase supply can spare, so the design uses two enclosing hoods:

- **Hood A**, a booth over the sheet press and its cooling press, with a 1.2 x 0.6 m sliding sash for loading.
- **Hood B**, an enclosure over the extruder barrel with a 0.8 x 0.4 m open face at the nozzle and mould.

*Table 5. Hood and fan sizing.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Open face area | 1.04 m² | 0.72 m² (A) plus 0.32 m² (B) |
| Air flow | 0.572 m³/s (2,059 m³/h) | 0.5 m/s plus 10 % for enclosure gaps |
| Main duct | 250 mm, 11.7 m/s, velocity pressure 81 Pa | Galvanized steel |
| Duct friction | 47 Pa | Friction factor 0.018 over 8 m equivalent |
| System pressure | 815 Pa | Hood entry 1.5 VP, fittings 1.4 VP, stack 1 VP, filters dirty: 250 Pa (G4 plus F7) and 200 Pa (carbon) |
| Fan input power | 1.00 kW (66 % of the 1.5 kW rating) | Fan 55 % times motor 85 % |
| Room air changes | 15 per hour in 136 m³ | Make-up opening of 0.38 m² at 1.5 m/s |

Contaminants and limits. Processing polyolefins releases hydrocarbons, formaldehyde, acetaldehyde, formic acid and acetone, carbon monoxide and a wax-like aerosol ([Borealis, *Statement on impurities: polyolefins*, ed. 6, 2022](https://www.borealisgroup.com/storage/Emission-EN-ed.06.pdf)). The playbook uses the lower of the local limit and the following US OSHA permissible exposure limits as a floor: formaldehyde 0.75 ppm over 8 h and 2 ppm over 15 min ([NIH summary of 29 CFR 1910.1048](https://ors.od.nih.gov/sr/dohs/Documents/formaldehyde-program.pdf)); acrolein 0.1 ppm; acetaldehyde 200 ppm ([OSHA Table Z-1](https://www.osha.gov/annotated-pels/table-z-1)). More protective limits exist (for example the ACGIH ceiling for formaldehyde), and a site should adopt them where it can.

Filters. A G4 prefilter and an F7 bag filter catch the wax aerosol; an impregnated activated carbon stage takes organic vapors. Plain activated carbon holds formaldehyde poorly, which is one reason the fan and filter sit outside and discharge through a stack above the roof, away from doors and air intakes.

R11 status: the hoods meet 0.5 m/s by design, and PVC, polystyrene and unknown plastics are excluded by the recipes. Whether air at the workstations stays below the exposure limits can only be shown by air monitoring on a running site, so R11 is **not verifiable at TRL 3**. Amish decided on 2026-09-25 (RFE-DDR-002, item 10) to fit a 1.5 kW fan, because filter loading is hard to police on a small site: with dirty filters it runs at 66 % of its rating instead of 91 % with the 1.1 kW fan. The block A peak rises from 8.35 kW to 8.75 kW (38.0 A).

## 7. Shredder noise and guarding

Assumptions: the bare shredder chopping rigid plastic has an A-weighted sound power level of 102 dB (a typical value for small granulators, not a measurement); the room is the steel shell (surface 194 m², mean absorption coefficient 0.1, room constant 21.5 m²); the source sits on the floor (directivity 2); the operator is 1 m away and other workers 4 m away; the shredder runs 3.79 h per shift.

*Table 6. Noise at the workstations.*

| Case | 1 m | 4 m | Operator LEX,8h |
| --- | --- | --- | --- |
| Bare shredder | 97.4 dB(A) | 94.9 dB(A) | 94.1 dB(A) |
| In a lined enclosure (15 dB insertion loss) | 82.4 dB(A) | 79.9 dB(A) | 79.1 dB(A) |

The steel room is reverberant, so a bare shredder puts the whole floor above 85 dB(A), not only the shredder zone. With the lined acoustic enclosure the operator exposure is 79.1 dB(A) over 8 h, below the 85 dB(A) limit in R12. With a 15 dB enclosure, the design still meets 85 dB(A) for any bare-machine sound power up to 107.9 dB; both the sound power and the insertion loss are assumptions. The shredder area stays a hearing protection zone until the level is measured.

Guarding (defined, not detailed): fixed guards on all drive parts; feed through an interlocked chute in the enclosure roof, so the rotor cannot be reached with the lid open; interlocked enclosure door; emergency stop at the chute and at the board; lockout before clearing jams. Opening sizes and reach distances must be checked against ISO 13857 at the detailed design stage.

R12 status: **at risk**. The noise result rests on an assumed sound power and insertion loss, and the guarding is defined but not detailed. The insulated hot surfaces and 30 mA RCDs are specified in the BOM.

## 8. Layout checks

The layout is built by `cad/src/model.py` and drawn on RFE-DWG-001 Rev P2.

*Table 7. Layout checks against R5.*

| Check | Value | Target |
| --- | --- | --- |
| Footprint | 12.19 x 4.88 m = 59.4 m² (56.7 m² inside) | 60 m² or less |
| Central aisle | 1.52 m clear between equipment; 1.20 m painted | 1.0 m or more |
| Hot zone clearance to stock | 1.00 m (to racking bay 1) | 1.0 m or more |
| Exits | Intake and export doors at X = 0, personnel exit at the far end; worst travel along the aisle 7.9 m | Two exits |
| Zone overlaps | None | None |

R5 is **met**, with the hot zone clearance exactly at its limit. Amish decided on 2026-09-25 (RFE-DDR-002, item 11) that a rented shed of the same size is the preferred shell where one is available. The container option is kept for sites without a shed; removing the adjoining side walls of two containers weakens them, so it is done only to a structural engineer's design.

## 9. Equipment cost

`bom/bom.csv` prices every line. Items 1 to 12 total **$24,200**, $800 under the R10 target of $25,000 (met on paper). The building shell adds about $8,000. Against the TRL 2 list, the shredder line gained a $600 acoustic enclosure, the fume line $300 for a second hood and the carbon stage, and the board $300 for the heater interlock. In v0.2 the fume line gains a further $150 for the 1.5 kW fan (RFE-DDR-002), which moves the total from $24,050 to $24,200. `budget_usd` in `project.yaml` stays null because this is a playbook repo; the equipment list is checked against R10 instead.

## 10. Economics model

The operator-editable model is `docs/playbook/economics_model.py` with its inputs in `docs/playbook/economics_inputs.csv`. An operator copies the CSV, changes the values to local prices, wages, tariff and yields, and runs `python docs/playbook/economics_model.py my_inputs.csv`. The model scales product, flake, metal, paper and disposal masses with input, splits energy into a fixed part (22.4 kWh per shift) and a part that scales with input, and treats wages, consumables, filters, rent and equipment recovery as fixed per shift. The reference inputs are illustrative and must come from the co-design partner.

*Table 8. Result per shift at the reference inputs (USD, estimates).*

| Item | Basis | Amount |
| --- | --- | --- |
| Products | 32.3 kg at $2.50/kg | +80.75 |
| PET flake | 19.3 kg at $0.60/kg | +11.58 |
| Metals | 8.0 kg at $0.50/kg | +4.00 |
| Paper and card | 10.0 kg at $0.05/kg | +0.50 |
| E-waste | 2.0 kg at $0 until a receiver quotes | 0.00 |
| Feedstock | 100 kg at $0.15/kg | -15.00 |
| Wages | 4 workers at $10 | -40.00 |
| Energy | 42.9 kWh at $0.15/kWh | -6.43 |
| Disposal | 28.4 kg at $0.05/kg | -1.42 |
| Consumables | Allowance | -10.00 |
| Filters | Allowance | -3.00 |
| **Operating margin** | | **+20.97** |
| Equipment recovery | $24,200 over 5 years of 250 shifts | -19.36 |
| **Result before rent and finance** | | **+1.61** |

Break-even product price: **$2.45/kg** at 100 kg input (the reference is $2.50/kg). Break-even input: **98 kg per shift** against a line capacity of 100 kg. Each $0.50/kg on the product price moves the result by $16.15 per shift, far more than any machine choice. The full cost of products and flake is $1.85/kg of output. R3 is **met**: the model exists, works per kilogram and per shift, gives the break-even points and is editable. Its review with an operating recycler is later work.

## 11. Material passport

Schema v0.2 (`standards/material-passport-v0.2.schema.json`) adds the fields Amish approved: `schema_version`, `product_form`, `parent_batch_ids` and an ISO 14021 aligned `recycled_content` statement. Schema v0.1 (`standards/material-passport.schema.json`) is kept unchanged. The v0.2 schema requires `parent_batch_ids` for every lot that is not an intake batch and a recycled content statement for flake, sheet, beam and profile lots. Following ISO 14021, rework or regrind reclaimed within the same process (the sheet trim here) is not counted as pre-consumer material ([ISO 14021 definitions as quoted in a published declaration](https://info.sculpteo.com/hubfs/Material%20documentation/Ultrafuse%20rPET/ISO%2014021%20Recycled%20Content%20Declaration_Ultrafuse%C2%AE%20rPET_EN_V1.0.pdf)).

The script validates the three example records in `standards/examples/` (an intake batch, an HDPE sheet lot and a circuit-board export lot): 3 of 3 are valid against v0.2, and 3 of 3 are also valid against v0.1. A sheet lot without `parent_batch_ids` is rejected. R13 and R14 are **met** on paper. The example values are invented.

## 12. Results against requirements

*Table 9. Requirement status at TRL 3 (from `docs/04-calcs/results.csv`).*

| ID | Target | Value | Status |
| --- | --- | --- | --- |
| R1 | Feasibility matrix: 7 groups with route, rating, hazard, export point and a source per row | 7 groups with route and reason; no hazard, export point or source columns | **Not met** |
| R2 | Sourced recipe for PET, HDPE, PP and aluminium | 4 recipes in `docs/playbook/recipes/` (aluminium as the add-on bay) | Met |
| R3 | Operator-editable economics model with break-even | Model and CSV; result +$1.61 per shift; break-even product price $2.45/kg | Met |
| R4 | Every export stream names refining step, receiver type and packing rule | Principle and cell packing rule only | **Not met** |
| R5 | 60 m² or less, aisles 1.0 m or more, separate hot zone | 59.4 m²; aisle 1.52 m; hot zone 1.00 m from stock | Met |
| R6 | 100 kg or more of mixed input per 8 h shift | Shredder 3.79 h of 4 h at an assumed 15 kg/h; press capacity 2.06 sheets for 2 | At risk |
| R7 | 50 % or more kept local as products or clean flake | 51.6 % | Met |
| R8 | Residue to licensed disposal 20 % or less, process losses counted | 28.4 % at the reference mix (20 % sorting residue plus 8.4 % process losses); 19.5 % for a load at the R16 threshold | **Not met** |
| R9 | 1.0 kWh/kg of output or less | 0.83 kWh/kg | Met |
| R10 | Equipment items 1 to 12 $25,000 or less | $24,200 | Met |
| R11 | 0.5 m/s on every melt process; no PVC, PS or unknown plastics; air below exposure limits | Hoods sized for 0.5 m/s (0.57 m³/s, fan 1.00 kW); exposure needs air monitoring | Not verifiable at TRL 3 |
| R12 | Guarded shredder, insulated hot surfaces, RCDs, 85 dB(A) LEX or hearing zones | Guarding defined; LEX 94 dB(A) bare, 79 dB(A) enclosed (sound power assumed) | At risk |
| R13 | Valid passport for every outgoing lot | 3 of 3 examples valid against schema v0.2 | Met |
| R14 | Passport lists parent batch IDs and schema version | v0.2 requires both for every non-intake lot | Met |
| R15 | Passport filled in 2 min or less | Needs a form and a timed trial | Not verifiable at TRL 3 |
| R16 | Intake quality rule with a residue threshold that keeps R8 within 20 % | Threshold 10 % residue by sampled mass (limit 10.6 %); loads above it refused or charged | Met |

Summary: 3 not met (R1, R4, R8), 2 at risk (R6, R12), 2 not verifiable at TRL 3 (R11, R15), 9 met (including the new R16).

## 13. Corrections to earlier figures

The TRL 2 documents quoted first-order values that this calculation replaces: products 30 kg (now 32.3 kg), flake 20 kg (19.3 kg), process losses 10 kg (8.4 kg), energy about 45 kWh and 0.9 kWh/kg (42.9 kWh and 0.83 kWh/kg), peak load about 13 kW (8.35 kW maximum demand with the interlock; 13.35 kW connected), equipment $22,850 (now $24,050), operating margin about $18 and result about $0 (now $20.97 and +$1.73 in v0.1, updated below). The TRL 2 note that about 2 % of the melt feed is lost as purge did not match its own 2 kg figure; the calculation uses 3 %. R8 was reported as met at the limit because only the sorting residue was counted; counting the process losses that also go to licensed disposal, it is not met.

In v0.2 (RFE-DDR-002, 2026-09-25) the 1.5 kW fume fan changes the maximum demand from 8.35 kW (36.3 A) to 8.75 kW (38.0 A), the connected load from 13.35 kW to 13.75 kW, the equipment total from $24,050 to $24,200 and the result per shift from +$1.73 to +$1.61. Energy per shift is unchanged, because the fan input depends on the air flow and pressure, not on the motor rating.
