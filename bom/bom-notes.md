# BOM notes

`bom/bom.csv` is the equipment list for the reference micro-factory in RFE-PRC-001, numbered to match the exploded view (`media/exploded.png`).

- All prices are indicative USD for concept review, not quotes. They are outside any hardware budget: `budget_usd` in `project.yaml` is null on purpose, because this repo is a playbook, not a single machine.
- Equipment total for items 1 to 12: about $22,850. Item 13 (building shell, about $8,000) depends on the site and is listed separately.
- Excluded: land, rent, permits, grid connection, working capital, transport, and operating costs (wages, energy, PPE replacement, wear parts). The first-order shift economics are in RFE-PRC-001, Table 3.
- Machines marked "make" are open designs built by a local fabricator or an open-hardware workspace. Their prices vary widely by country and will be checked at TRL 3.
