---
doc_id: RFE-DDR-002
title: ReflowEconomy recommendations accepted
project: ReflowEconomy
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 acceptance of all open recommendations, what changed in the repo and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 6 release, 8, 9, 10 and 11); item 7 remains proposed, awaiting Amish

> **Safety:** The reference micro-factory has a shredder, surfaces at 190 to 200 °C, melt fumes, water near electricity, lithium cells in the waste stream and a high fire load. None of these decisions relaxes a safety rule. Item 10 adds fan margin for the fume hoods, and item 11 makes the structurally simpler shell the preferred one.

## Context

After the TRL 3 session, RFE-DDR-001 and `docs/REVIEW.md` listed six items as "Proposed, awaiting Amish". On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is therefore decided as recommended; where the recommendation named several options, the recommended option is the decision. Items without a recommendation stay open. TRL 4 is on hold by Amish's instruction, so no item here starts build, test or purchasing work.

## Options considered

The options for each item are in RFE-DDR-001 ("Items raised at TRL 3") and are not repeated here.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 6 (release) | License for the first release of the playbook text | Option (b): documents under CC BY-SA 4.0, hardware under CERN-OHL-S-2.0, scripts under MIT, applied when the first release is tagged | Recorded in RFE-PRC-001 v0.4 and the README licenses section. No license file is changed now; the change is made with the first release |
| 8 | How R8 counts process losses | Options (c) with (a): keep the honest total (sorting residue plus process losses against 20 %) and add an intake quality rule | RFE-REQ-001 v0.4: R8 restated, new R16 (loads sampled at intake; above 10 % residue refused or charged). RFE-CAL-001 v0.2 section 2: the limit is 10.6 % residue; at the 10 % threshold disposal is 19.5 % and 58.0 % is kept local. R8 stays not met for the reference input (28.4 %). RFE-PRC-001 v0.4 intake step |
| 9 | Single-phase sheet press | Option (a): a derated 5 kW press for the playbook, with the published 15 kW press as an option where 400 V exists | No change to the design, which already used the 5 kW press. Recorded in RFE-CAL-001 v0.2 section 3, RFE-REQ-001 v0.4 assumptions and RFE-PRC-001 v0.4 |
| 10 | Fume fan size | Option (b): 1.5 kW fan | `bom/bom.csv` item 7: fan 1.1 kW to 1.5 kW, $2,800 to $2,950; equipment total $24,050 to $24,200 (R10 still met, margin $800). RFE-CAL-001 v0.2: maximum demand 8.35 kW (36.3 A) to 8.75 kW (38.0 A); connected load 13.35 kW to 13.75 kW; fan loading 91 % to 66 %; result per shift +$1.73 to +$1.61; energy unchanged at 42.9 kWh. `docs/playbook/economics_inputs.csv` capex 24,050 to 24,200. RFE-DWG-001 Rev P2 notes |
| 11 | Structure of the building shell | Option (c): a rented shed where available; option (a), container side-wall removal, only with a structural engineer's design | `bom/bom.csv` item 13 puts the shed first. RFE-PRC-001 v0.4 (zone table, layout, safety), RFE-PRB-001 v0.4 constraints, RFE-REQ-001 v0.4 assumptions, RFE-DWG-001 Rev P2 notes and the concept blueprint key figures. The footprint and geometry are unchanged |

`budget_usd` stays null: this is a playbook repo, and no recommendation set a budget. The pitch and problem line had no recommended rewording and are unchanged. The GA drawing geometry is unchanged; only its notes changed, so it moved from Rev P1 to Rev P2. `cad/src/model.py` needed no change and was re-run to regenerate the STEP and STL files.

### Items still open

These stay **Proposed, awaiting Amish**.

| # | Item | Why it stays open |
| --- | --- | --- |
| 7 | First co-design partner (waste-picker cooperative, Precious Plastic workspace or municipal program) | No single recommendation; partners are picked per area later under the cross-cutting rule in RFE-DDR-001 |

### Cross-repo actions

None. No recommendation here requires a change in another repo.

## Consequences

- Controlled documents moved one minor version: RFE-PRB-001 v0.4, RFE-PRC-001 v0.4, RFE-REQ-001 v0.4, RFE-CAL-001 v0.2 and RFE-DDR-001 v0.2.
- Requirement status at TRL 3: not met R1, R4, R8; at risk R6, R12; not verifiable at TRL 3 R11, R15; met on paper R2, R3, R5, R7, R9, R10, R13, R14 and the new R16.
- Meeting R8 now depends on collectors delivering loads at 10 % residue or less. That can only be confirmed with a co-design partner (item 7), which is TRL 4 work.
- TRL 4 remains on hold by Amish's instruction. Nothing in this record starts it.
