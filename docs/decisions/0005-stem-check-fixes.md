---
doc_id: RFE-DDR-005
title: ReflowEconomy STEM check fixes
project: ReflowEconomy
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Two STEM check failures fixed under Amish's standing instruction of 2026-10-23 (motor energy at the electrical input; 120 mm feed slot); the supply-current failure put to Amish
---

# 0005: STEM check fixes

- **Date:** 2026-10-25
- **Status:** D2 and D3 decided under Amish's standing instruction of 2026-10-23 (he can reverse them); D1 proposed, awaiting Amish

> **Safety:** D3 tightens the guarding of the shredder feed. D1 concerns the electrical supply; whatever is chosen, the licensed electrician confirms the supply, earthing and protection on site (build plan stop S2).

## Context

The first STEM check of the existing design (RFE-STM-001, 2026-10-25) found three detail failures. Amish's standing instruction of 2026-10-23: "when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it in DEC as decided under that instruction; a fix that changes the working principle, pitch or scope goes to Amish instead."

## Options considered and decisions

**D2, motor energy (S13).** RFE-CAL-001 used rated motor power, which is shaft output, as if it were electricity drawn. Options: (a) count motor and drive losses with cited efficiencies; (b) keep the figure and note the error. Decided under the standing instruction: (a). Electrical input = shaft energy / (motor x drive), with IE3 minimum efficiencies (IEC 60034-30-1: 86.7 % at 2.2 kW, 85.3 % at 1.5 kW), a 96 % drive and a 75 % single-phase pump motor. Energy per shift 42.9 to 45.6 kWh; 0.83 to 0.88 kWh/kg of output (PR-009 still met); energy cost 6.43 to 6.84 USD per shift; result +0.57 to +0.17 USD per shift; break-even product price 2.48 to 2.49 USD/kg. No hardware change; cost USD 0.

**D3, feed slot height (S17).** The feed slot was 460 x 160 mm. ISO 13857 Table 4, which gives 850 mm from an opening to the hazard for the arm up to the shoulder, covers openings up to 120 mm; above that the reaching-over distances apply, so the 850 mm check did not hold for a 160 mm slot. Options: (a) lower the slot to 120 mm and keep the 1,060 mm path; (b) keep 160 mm and lengthen the hood until the reaching-over tables are met; (c) a second baffle inside the hood. Decided under the standing instruction: (a), because it keeps the hood, collar and chute mouth height as decided on 2026-10-02 and needs no new part. The hood is 140 mm tall instead of 180 (less sheet); feed pieces are crushed flat or cut under 120 mm at the sorting table. Changed: `cad/src/model.py` (CHUTE_SLOT), RFE-DWG-109 Rev P3, RFE-BLD-001 v0.4, RFE-CAL-001 section 7, `bom/bom.csv` line 3 text, `docs/playbook/safety.md`. Cost: none (slightly less sheet).

**D1, supply current (S14).** Counted as currents, the morning block draws about 55 A running (72 A at full load) against the 40 A single-phase supply decided by Amish on 2026-09-25 (RFE-DDR-001 item 5). Options: (a) a 400 V three-phase supply, about 18.5 A a phase; in Maharashtra any supply above 40 A is given as three-phase (MSEDCL Conditions of Supply, clause 6.4.1), and it would also allow the published 15 kW press; (b) keep single phase and split the morning so the shredder and the extruder never run together (largest block 36 A; working day about 10.6 h, about 13 USD a shift more in wages, so the result per shift turns to about -12.7 USD); (c) keep 8 h and single phase and cut the input per shift. Each changes a decided input or the throughput, so it goes to Amish. Recommendation: (a), with (b) written into the playbook as the single-phase fallback.

## Consequences

PR-009 stays met at 0.88 kWh/kg; PR-012 is checked against Table 4 directly; PR-017 is not met until D1 is decided. The STEM check stays open until D1 is decided and the plausible rows (S3, S15, S17, S20, S21) are closed; the independent review of 2026-10-25 moved S3, S17 and S20 from within known science to plausible, and S17 now waits on the EN 12012 type C standard for size reduction machines as well as the measured cutter height.
