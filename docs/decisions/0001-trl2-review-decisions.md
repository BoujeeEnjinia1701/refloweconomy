---
doc_id: RFE-DDR-001
title: ReflowEconomy TRL 2 review decisions
project: ReflowEconomy
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Items 6 (release license), 8, 9, 10 and 11 marked decided; item 7 stays open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 6, 8, 9, 10 and 11; items 6 (release) and 8 to 11 decided by Amish on 2026-09-25 through RFE-DDR-002); item 7 remains proposed, awaiting Amish

> **Safety:** The reference micro-factory has a shredder, surfaces at 190 to 200 °C, melt fumes, water near electricity, lithium cells in the waste stream and a high fire load. None of the decisions below relaxes a safety rule. Item 1 keeps molten aluminium out of the reference floor until an add-on bay has its own safety case.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed seven items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." The same instruction approved cross-cutting SwapCell interface items, a pricing rule for shared SwapCell packs, and a rule that community designs pick co-design partners per area later.

This record lists what that instruction decides and what it leaves open because there was no single recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 section) and RFE-PRC-001 v0.2. They are not repeated here, except for the open items.

## Decision

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Reference line | Decided by Amish, 2026-09-25: go with recommendation. Option (a): plastics only. Aluminium is a separate add-on bay with its own safety case, not part of the reference floor | RFE-PRC-001 v0.3, RFE-REQ-001 v0.3 R2 (redefined), `docs/playbook/recipes/aluminium.md` |
| 2 | Footprint | Decided by Amish, 2026-09-25: go with recommendation. Option (a): two 40 ft container footprints or a shed of about 60 m² | `cad/src/model.py`, RFE-DWG-001, RFE-CAL-001 section 8 |
| 3 | PET route | Decided by Amish, 2026-09-25: go with recommendation. Option (a): PET is sold as clean flake, not processed in house | `docs/playbook/recipes/pet-flake.md`, RFE-REQ-001 assumptions |
| 4 | Passport schema v0.2 | Decided by Amish, 2026-09-25: go with recommendation. Add `parent_batch_ids`, `schema_version`, `product_form` and a recycled content statement aligned with ISO 14021, and publish example records, at TRL 3. Issued as a new file; v0.1 is kept unchanged | `standards/material-passport-v0.2.schema.json`, `standards/examples/`, RFE-REQ-001 R13 and R14 |
| 5 | Electrical supply | Decided by Amish, 2026-09-25: go with recommendation. Option (b): design for single-phase with staggered heating, so the playbook works on weak grids. Implemented as a heater interlock (press heaters locked out while the shredder or extruder runs) on a 230 V, 40 A supply | RFE-CAL-001 section 5, `bom/bom.csv` item 11, RFE-REQ-001 assumptions |
| 6 | Licensing of the text | Decided by Amish, 2026-09-25: go with recommendation. Keep the playbook text under CERN-OHL-S-2.0 with the repo for now. No license was changed. The choice of license for the first release remains open (see below) | This record |

The pitch and problem line had no recommended rewording in the TRL 2 review and are unchanged. `budget_usd` stays null: this is a playbook repo, and the TRL 2 review made no budget recommendation. The reference equipment list is checked against R10 instead.

Cross-cutting approvals from the same instruction, recorded here:

- **SwapCell interface v0.3.** Decided by Amish, 2026-09-25 (cross-cutting): a wake method for hosts without CAN, a charge-while-discharging mode and a latch vibration rating for vehicles. ReflowEconomy does not use SwapCell, so no v0.3 items apply.
- **Shared packs are priced once.** Decided by Amish, 2026-09-25 (cross-cutting). Not applicable: ReflowEconomy has no SwapCell pack.
- **Co-design partners per area later.** Decided by Amish, 2026-09-25 (cross-cutting): community designs pick co-design partners per area later. Item 7 stays open under this rule.

### Items raised at TRL 3

On 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Every item below that carries a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**; see RFE-DDR-002 (`0002-recommendations-accepted.md`) for what changed. Item 7 has no single recommendation and stays **Proposed, awaiting Amish**.

| # | Item | Options | Recommendation | Status |
| --- | --- | --- | --- | --- |
| 6 (release) | License for the first release of the playbook text | (a) keep CERN-OHL-S-2.0 for everything; (b) CC BY-SA 4.0 for documents, CERN-OHL-S-2.0 for hardware and MIT for scripts | (b), decided before the first release; this is a licensing decision for Amish | Decided by Amish, 2026-09-25: go with recommendation (b), applied when the first release is tagged |
| 7 | First co-design partner | (a) a waste-picker cooperative; (b) an existing Precious Plastic workspace; (c) a municipal program | (a) or (b); left open under the cross-cutting rule that partners are picked per area later | Proposed, awaiting Amish |
| 8 | R8 definition (new at TRL 3) | (a) keep "residue to licensed disposal 20 % or less" and count process losses (not met at 28.4 %); (b) apply the 20 % limit to sorting residue only and report process losses separately; (c) keep the target and set a minimum input quality at intake | (c) with (a): keep the honest total and add an intake quality rule, because the site can refuse poor loads but cannot make losses disappear | Decided by Amish, 2026-09-25: go with recommendation |
| 9 | Single-phase sheet press (new at TRL 3) | (a) a derated 5 kW press with lighter platens (the TRL 3 design, not a published open design); (b) the published 15 kW press on a site with a 400 V supply; (c) buy sheets pressed elsewhere and make only beams | (a) for the playbook, with (b) as an option where three-phase exists; RFE-CAL-001 shows (a) has almost no time margin | Decided by Amish, 2026-09-25: go with recommendation |
| 10 | Fume fan size (new at TRL 3) | (a) 1.1 kW, 91 % loaded with dirty filters; (b) 1.5 kW, which raises the maximum demand to 38 A | (b), because filter loading is hard to police on a small site | Decided by Amish, 2026-09-25: go with recommendation |
| 11 | Structure of the container option (new at TRL 3) | (a) remove the adjoining side walls with engineered reinforcement; (b) keep the walls and cut two wide openings; (c) prefer a rented shed | (c) where available, (a) only with a structural engineer's design | Decided by Amish, 2026-09-25: go with recommendation |

## Consequences

- RFE-PRB-001, RFE-PRC-001 and RFE-REQ-001 move to v0.3 with these decisions. The design choices in items 1 to 5 are no longer "proposed".
- RFE-REQ-001 R2 is redefined: the aluminium recipe serves the add-on bay, not the reference floor. R13 and R14 now name schema v0.2. The assumptions state the single-phase supply.
- The TRL 3 evidence (RFE-CAL-001, `cad/src/model.py`, RFE-DWG-001 and `bom/bom.csv`) follows these decisions.
- TRL 4 is on hold by Amish's instruction. Nothing in this record starts TRL 4 work.
