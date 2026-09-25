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
