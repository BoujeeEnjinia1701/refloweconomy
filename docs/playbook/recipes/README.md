# Process recipes

One recipe per locally processed material (requirement R2 of RFE-REQ-001). Each recipe gives the input grade, the steps, the temperature window, drying, the expected yield, what is rejected, the PPE and the sources. Yields and times come from RFE-CAL-001 (`docs/04-calcs/01-sizing.md`); they are estimates for a paper design and must be replaced by site data.

| Recipe | Material | Route in the reference micro-factory |
| --- | --- | --- |
| [pet-flake.md](pet-flake.md) | PET bottles | Wash, shred, float-sink, dry, sell as clean flake. PET is not melted in house (RFE-DDR-001, item 3) |
| [hdpe.md](hdpe.md) | HDPE rigid packaging | Wash, shred, float-sink, dry, press into 1 x 1 m sheets or extrude into beams |
| [pp.md](pp.md) | PP rigid packaging and caps | As HDPE, at a higher temperature; never mixed with HDPE in one sheet |
| [aluminium.md](aluminium.md) | Aluminium cans and clean castings | Add-on bay only, with its own safety case; not part of the reference floor (RFE-DDR-001, item 1) |

> **Safety:** Every recipe involves moving machinery, hot surfaces or molten material. The rules in `docs/playbook/safety.md` and the safety section of RFE-PRC-001 apply to all of them. These recipes are a paper design at TRL 3 and have not been trialled; a qualified safety professional must review them before any site uses them.

Common rules for all plastics recipes:

- Only identified PET, HDPE and PP enter the line. PVC is never heated (it releases hydrogen chloride), and polystyrene, multilayer, film and unknown plastics go to residue.
- One polymer at a time through the shredder, washer and dryer; clean out between polymers.
- Every lot gets a material passport (schema v0.2, `standards/material-passport-v0.2.schema.json`) with its parent intake batch IDs.
- Fume extraction runs whenever a heater is on and for 30 min after.
