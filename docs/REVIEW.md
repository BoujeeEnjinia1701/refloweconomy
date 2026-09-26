# Review note: ReflowEconomy

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (RFE-PRB-001 v0.2): problem with cited sources, users and context, constraints, out of scope, prior work, open questions; co-design checklist kept.
- `docs/03-requirements.md` (RFE-REQ-001 v0.2): 15 measurable requirements in three groups (playbook, reference micro-factory, material passport), each with a target, planned verification and status at TRL 2.
- `docs/02-concept.md` (RFE-PRC-001 v0.2): material flow diagram near the top, reference micro-factory layout, how it works, zone table numbered to the BOM, mass balance, energy per shift, illustrative shift economics, passport attachment points and an example record, proposed design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of a reference micro-factory floor on two 40 ft container footprints (12.2 x 4.9 m) with 13 numbered zones and items, a 1.75 m person, and a custom material flow diagram.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` (numbered zones matching `bom/bom.csv`, walls omitted) and `flow.png` (mass fractions marked as estimates; passport points marked MP). No cutaway: the layout is open and the inside of each machine does not carry the idea.
- `bom/bom.csv`: reference micro-factory equipment list, 13 lines with indicative USD costs; `bom/bom-notes.md` rewritten. **These costs are indicative and outside any hardware budget.** `budget_usd` stays null in `project.yaml` because this is a playbook repo.
- `README.md`: hero image and links line before "## Problem"; Concept, Key components, Safety and layout table updated.
- `docs/playbook/safety.md`: five rules added (cells at intake, refused waste, shredder guarding and noise, RCDs and sludge, no workers under 18); the original rules are unchanged. `docs/playbook/feasibility-matrix.md` and `standards/material-passport.schema.json` are unchanged.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` is unchanged; the pitch and problem still match the numbers.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Footprint | about 60 m² (12.2 x 4.9 m) | R5 met |
| Input per shift | 100 kg mixed collected material | R6 met on paper |
| Remanufactured or sold locally as clean feedstock | 50 kg per 100 kg (30 kg products, 20 kg PET flake) | R7 met at the limit |
| Exported for industrial refining | 10 kg (8 kg metals, 2 kg boards and cells) | R4 partly met |
| Residue to licensed disposal | 20 kg, plus 10 kg process losses | R8 met at the limit |
| Energy | about 45 kWh per shift, about 0.9 kWh/kg of output; about 13 kW connected | R9 met on paper |
| Equipment cost, items 1 to 12 | about $22,850 indicative; building shell about $8,000 more | R10 met on paper |
| Shift economics | operating margin about $18; about $0 after equipment recovery | R3 not met; marginal |

Requirements **not met**: R2 (no process recipes), R3 (no economics model; the estimate shows break-even at best), R11 (fume hood not sized, filters and exposure limits not chosen), R12 (shredder noise likely above 85 dB(A); guarding not designed), R14 (the passport schema cannot link lots to intake batches). R15 is not verified. R1, R4 and R13 are partly met; R6 to R10 are met only on paper, and R7 and R8 only at the limit.

### Sources

Web search and page fetches were not available in this session, so the sources in RFE-PRB-001 (World Bank *What a Waste 2.0*, UNEP *GWMO 2024*, OECD *Global Plastics Outlook*, *Global E-waste Monitor 2024*, WHO *Children and digital dumpsites*, the Basel Convention, Precious Plastic, the International Aluminium Institute and EU Regulations 2023/1542 and 2024/1781) are cited from prior knowledge of well-known publications. Each link and figure should be checked before the documents are released.

### Proposed, awaiting Amish

1. **Reference line.** (a) Plastics only (recommended); (b) plastics plus an aluminium remelting bay on the same site; (c) a multi-material site. Recommendation: (a), with aluminium as a separate add-on bay that has its own safety case.
2. **Footprint.** (a) Two 40 ft container footprints or a shed of about 60 m² (recommended); (b) one 40 ft container (too narrow for safe aisles around a press); (c) a larger workshop of about 100 m². Recommendation: (a).
3. **PET route.** (a) Sell PET as clean flake (recommended); (b) process PET in house, which needs a dryer and a better extruder. Recommendation: (a).
4. **Passport schema v0.2.** Add `parent_batch_ids`, `schema_version`, `product_form` and a recycled content statement aligned with ISO 14021, and publish example records. Recommendation: do this at TRL 3; the v0.1 file is unchanged here.
5. **Electrical supply.** (a) Three-phase supply; (b) single-phase with staggered heating (press and extruder never heating at once). Recommendation: design for (b) so the playbook works on weak grids.
6. **Licensing of the text.** The playbook text is under CERN-OHL-S-2.0 with the repo. CC BY-SA 4.0 is the usual license for documents; changing it is a licensing decision. Recommendation: keep as is for now and decide before the first release. No license was changed.
7. **First co-design partner.** (a) A waste-picker cooperative; (b) an existing Precious Plastic workspace; (c) a municipal program. Recommendation: (a) or (b), because they already handle the material and can validate the mass balance and prices.

### Safety concerns

- The shredder is the main injury risk: guarding, hopper interlock, emergency stop, lockout and hearing protection are required.
- Melt fumes: only identified HDPE and PP are melted; PVC is never heated. The hood is not yet sized, so R11 is open.
- Lithium cells hidden in collected waste can ignite in the shredder or in storage; the intake rule pulls them out first.
- Water near 13 kW of heaters and motors: RCDs and a licensed installation are required.
- High fire load from plastic stock and dust; the hot zone is kept away from stock.
- Contaminated input (sharps, chemical containers) and child labor risk in the informal sector: refusal rules and a no-under-18 rule are stated.
- A qualified safety professional must review the layout before any site operates.

### Recommended next step

Review this note, the flow diagram and the layout. If approved, run `/advance-trl3` to: verify the cited sources; write the process recipes (R2) and an operator-editable economics model (R3); size the fume hood (R11); define the shredder guarding and noise controls (R12); draft passport schema v0.2 with example records (R14); and produce the layout drawing sheet.

## Session 2026-09-25: TRL 3

Authority: on 2026-09-25 Amish wrote "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session applied the recommendations, produced the TRL 3 evidence and stopped. **TRL 4 is on hold by Amish's instruction.**

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (RFE-DDR-001 v0.1): items 1 to 5 decided by Amish, 2026-09-25 (plastics-only line with an aluminium add-on bay, two 40 ft container footprints, PET sold as flake, passport schema v0.2, single-phase supply with staggered heating); item 6 decided for the interim (keep CERN-OHL-S-2.0); open items listed.
- `docs/04-calcs/01-sizing.md` (RFE-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `docs/04-calcs/results.csv`: mass balance, throughput and time budget, energy, single-phase supply, fume hood sizing, shredder noise, layout checks, equipment cost, economics and passport validation, with every requirement's status. The script stops if the economics inputs disagree with it.
- `docs/playbook/economics_model.py` and `docs/playbook/economics_inputs.csv`: operator-editable economics model (copy the CSV, change values, run the script).
- `docs/playbook/recipes/` (README, `pet-flake.md`, `hdpe.md`, `pp.md`, `aluminium.md`): process recipes for R2 as playbook documents, each with input grade, steps, temperature window, yield, rejects, PPE, a safety note and sources. The aluminium recipe is for the add-on bay only.
- `standards/material-passport-v0.2.schema.json`: schema v0.2 with `schema_version`, `product_form`, `parent_batch_ids` and an ISO 14021 aligned `recycled_content` statement; `standards/examples/` holds three example records. `standards/material-passport.schema.json` (v0.1) is unchanged.
- `cad/src/model.py`: parametric floor layout (build123d) with the zone envelopes the calculation checks; exports `cad/step/refloweconomy-{layout,shell,equipment}.step` and matching STL files.
- `cad/src/sheets.py` builds `cad/drawings/RFE-DWG-001.svg`, `.pdf` and `.png`: floor plan general arrangement at Rev P1 (plan section at 1.45 m and front elevation at 1:50, zone balloons matching the BOM, aisle and hot zone marked, "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION"). The concept sheet keeps RFE-DWG-010, so the GA took RFE-DWG-001.
- `bom/bom.csv` and `bom/bom-notes.md`: every line priced with a supplier type; items 1 to 12 total $24,050 against the R10 target of $25,000. `budget_usd` stays null (playbook repo).
- `cad/src/concept_media.py` now renders from the parametric model; `media/hero.png`, `exploded.png`, `flow.png`, `concept-blueprint.*`, `model.glb` and `viewer.html` refreshed and checked by eye. The front wall is left out of the media so the floor shows.
- RFE-PRB-001, RFE-PRC-001 and RFE-REQ-001 moved to v0.3; `README.md` and `project.yaml` (trl: 3, trl_target: 3, evidence list) updated; PDFs in `docs/pdf/`.
- `docs/playbook/feasibility-matrix.md`, `docs/playbook/safety.md` and the rest of the existing playbook content are unchanged. No TRL 4 material existed in the repo, and none was created.

### Requirements at TRL 3 (RFE-CAL-001)

8 met on paper, **3 not met**, 2 at risk, 2 not verifiable at TRL 3.

| Status | Requirements |
| --- | --- |
| **Not met** | **R1** feasibility matrix lacks hazard, export point and source columns; **R4** per-stream export rules not written; **R8** 28.4 % of input goes to licensed disposal (20 % sorting residue plus 8.4 % process losses) against 20 % |
| At risk | R6 shredder needs 3.79 h of 4 h at an assumed 15 kg/h (published range 8.8 to 41.8 kg/h), and the 5 kW press has 2.06 sheets of capacity for 2; R12 operator noise 94 dB(A) bare and 79 dB(A) enclosed, from an assumed sound power |
| Not verifiable at TRL 3 | R11 hoods sized for 0.5 m/s, but exposure needs air monitoring; R15 passport form time needs a trial |
| Met on paper | R2 recipes; R3 economics model (result +$1.73 per shift before rent, break-even product price $2.45/kg); R5 59.4 m², clear aisle 1.52 m, hot zone 1.00 m from stock (at the limit); R7 51.6 % kept local; R9 0.83 kWh/kg; R10 $24,050; R13 3 of 3 example passports valid; R14 parent IDs and version required |

Key numbers: 42.9 kWh per shift; maximum demand 8.35 kW (36.3 A at 230 V) with the heater interlock, 13.35 kW connected; hoods 0.572 m³/s at about 815 Pa with a 1.00 kW fan input (91 % of the 1.1 kW rating). The TRL 2 figures (30 kg products, 20 kg flake, about 45 kWh, about 13 kW peak, $22,850, margin about $18) are corrected in RFE-PRC-001 v0.3 and RFE-CAL-001 section 13. The main new finding: the published Precious Plastic sheetpress is 15 kW on a 400 V, 32 A supply, so the decided single-phase line needs a derated press that is not a published design.

### Decisions recorded (RFE-DDR-001)

Decided by Amish, 2026-09-25, go with recommendation: 1 plastics-only reference line with aluminium as a separate add-on bay; 2 two 40 ft container footprints; 3 PET sold as clean flake; 4 passport schema v0.2 with example records, as a new file beside v0.1; 5 single-phase supply with staggered heating; 6 keep CERN-OHL-S-2.0 on the playbook text for now. Cross-cutting SwapCell items and the shared-pack pricing rule do not apply to this repo. The pitch, problem line and `budget_usd` (null) are unchanged; the TRL 2 review recommended no change to them.

### Still proposed, awaiting Amish (status updated 2026-09-25, see the next session)

1. License for the first release of the playbook text (item 6, release): recommendation CC BY-SA 4.0 for documents, CERN-OHL-S-2.0 for hardware, MIT for scripts. **Decided by Amish, 2026-09-25: go with recommendation** (RFE-DDR-002).
2. First co-design partner (item 7): left open under the rule that partners are picked per area later. Still proposed, awaiting Amish (no single recommendation).
3. How R8 counts process losses (item 8): recommendation keep the honest total and add an intake quality rule. **Decided by Amish, 2026-09-25: go with recommendation** (RFE-DDR-002).
4. Single-phase sheet press (item 9): recommendation a derated 5 kW press for the playbook, with the published 15 kW press where 400 V exists. **Decided by Amish, 2026-09-25: go with recommendation** (RFE-DDR-002).
5. Fume fan size (item 10): recommendation 1.5 kW for margin (maximum demand rises to 38 A). **Decided by Amish, 2026-09-25: go with recommendation** (RFE-DDR-002).
6. Container structure (item 11): recommendation a rented shed where available; side-wall removal only with a structural engineer's design. **Decided by Amish, 2026-09-25: go with recommendation** (RFE-DDR-002).

### Sources

Web search and fetch were available in this session. The TRL 2 sources in RFE-PRB-001 were checked against their publishers' pages: World Bank (2.01 and 3.40 billion tonnes), OECD (9 % in 2019), *Global E-waste Monitor 2024* (62 Mt, 22.3 %), WHO (12.9 million women, more than 18 million children), Basel Convention amendments (1 January 2021), International Aluminium Institute (95 % energy saving) and EU Regulations 2023/1542 and 2024/1781 match. **The UNEP 2023 figure was wrong** (2.1 billion tonnes); UNEP gives 2.3 billion tonnes, corrected in RFE-PRB-001 v0.3. New sources in the recipes and RFE-CAL-001 (Precious Plastic Academy machine pages, RJC Mold processing ranges, Kitech densities, Plastics Technology on PET drying, Borealis on polyolefin emissions, OSHA Table Z-1, the NIH formaldehyde summary, MIT sand casting notes, the Aluminum Association guidelines and an ISO 14021 declaration) were fetched and quoted. ISO 14021 itself and ISO 13857 were not read; they are cited by name only.

### Safety concerns

- A bare shredder in the steel room puts the whole floor near 95 dB(A); the enclosure result depends on an assumed sound power and insertion loss. Keep the hearing protection zone until measured.
- The fume design relies on enclosing hoods with sashes; if operators leave sashes open or the filters load up, the face velocity drops. Plain carbon holds formaldehyde poorly, so discharge must be above the roof.
- The heater interlock is a safety and supply measure; bypassing it would draw 58 A on a 40 A supply.
- Removing container side walls needs a structural engineer.
- Molten aluminium stays off the reference floor until the add-on bay has its own safety case.
- Lithium cells at intake, fire load of plastic stock (hot zone exactly 1.0 m from racking), water near electricity and the refusal of hazardous waste remain as before. A qualified safety professional must review the layout before any site operates.

### Recommended next step

TRL 4 is on hold by Amish's instruction; do not start it. Within TRL 3, the next session could close R1 and R4 in the playbook (hazard, export point and source columns in the feasibility matrix; per-stream export rules) and settle the open items above. For reference only, TRL 4 would need: a co-design partner and site; measured shredder rate and sound power, sheet press cycle on a single-phase press, and wash and melt losses; air monitoring at the hoods; a timed passport form trial; a TST report with `environment: lab`; and build log entries.

## Session 2026-09-25: recommendations accepted

Authority: on 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (RFE-DDR-002 v0.1). RFE-DDR-001 moved to v0.2 with the new status column. **TRL 4 remains on hold by Amish's instruction**; `trl: 3` and `trl_target: 3` are unchanged.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| 6 (release) License for the first release | CC BY-SA 4.0 for documents, CERN-OHL-S-2.0 for hardware, MIT for scripts | Open | Applied when the first release is tagged; noted in README and RFE-PRC-001; no license file changed now |
| 8 R8 and process losses | Keep the honest total; add an intake quality rule | R8 not met, method open | R8 restated (losses counted), still not met at 28.4 % for the reference input; new R16: loads above 10 % sampled residue refused or charged (limit 10.6 %; 19.5 % to disposal at the threshold, 58.0 % kept local) |
| 9 Single-phase sheet press | Derated 5 kW press as reference; published 15 kW press where 400 V exists | Proposed | Recorded as decided; design unchanged |
| 10 Fume fan | 1.5 kW | 1.1 kW, 91 % loaded, $2,800 | 1.5 kW, 66 % loaded, $2,950 |
| 10 (effect) | | Maximum demand 8.35 kW, 36.3 A; connected 13.35 kW | 8.75 kW, 38.0 A (5 % margin on 40 A); connected 13.75 kW |
| 10 (effect) | | Equipment $24,050; result +$1.73 per shift | Equipment $24,200 (R10 still met, $800 margin); result +$1.61 per shift; break-even product price unchanged at $2.45/kg |
| 11 Building shell | Rented shed preferred; container side walls only to a structural engineer's design | Containers first | Shed first in BOM item 13, RFE-PRC-001, RFE-PRB-001, RFE-REQ-001, RFE-DWG-001 notes and the blueprint key figures; footprint unchanged |

`budget_usd` stays null (playbook repo; no budget recommendation). The pitch and problem line are unchanged.

Files changed: RFE-PRB-001 v0.4, RFE-PRC-001 v0.4, RFE-REQ-001 v0.4, RFE-CAL-001 v0.2 (`docs/04-calcs/sizing.py` and `results.csv` re-run), RFE-DDR-001 v0.2, new RFE-DDR-002 v0.1, `bom/bom.csv`, `bom/bom-notes.md`, `docs/playbook/economics_inputs.csv` (capex), `cad/src/sheets.py` (RFE-DWG-001 Rev P1 to P2: notes and revision row only), `cad/src/concept_media.py` (key figures), `project.yaml` (evidence list) and `README.md`. `cad/src/model.py` was re-run unchanged to regenerate STEP and STL. All drawings, media and PDFs were regenerated, which also replaces the old site address with designmolecule.com. The README gained the sections Concept rationale, Burning platform, Where it could be used and What sparked the idea (China's 2018 plastic waste import ban and the Brooks, Wang and Jambeck study).

### Requirement status now (RFE-CAL-001 v0.2)

| Status | Requirements |
| --- | --- |
| **Not met** | **R1** feasibility matrix lacks hazard, export point and source columns; **R4** per-stream export rules not written; **R8** 28.4 % to licensed disposal at the reference input (20 % residue), against 20 % |
| At risk | R6 shredder 3.79 h of 4 h and press 2.06 sheets for 2; R12 noise 79 dB(A) enclosed from an assumed sound power |
| Not verifiable at TRL 3 | R11 air monitoring; R15 timed passport trial |
| Met on paper | R2, R3 (+$1.61 per shift), R5, R7 (51.6 %), R9 (0.83 kWh/kg), R10 ($24,200), R13, R14, R16 (intake rule, 10 % threshold) |

The new finding: the reference input assumed 20 % residue, which the new intake rule would refuse. Meeting R8 depends on collectors delivering loads at about 10 % residue or less; only a co-design partner can confirm that.

### Still awaiting Amish

- First co-design partner and region (RFE-DDR-001 item 7): no single recommendation; partners are picked per area later.

### Cross-repo actions

None.

### Safety

No safety rule was relaxed. The larger fan keeps face velocity as filters load; the heater interlock is still required (without it the connected 13.75 kW would draw 60 A on a 40 A supply). The container option still needs a structural engineer. A qualified safety professional must review the layout before any site operates.

### Recommended next step

TRL 4 is on hold by Amish's instruction. Within TRL 3, close R1 and R4 in the playbook and choose the first co-design partner when Amish is ready.
