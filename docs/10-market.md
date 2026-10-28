---
doc_id: RFE-MKT-001
title: ReflowEconomy market and viability
project: ReflowEconomy
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First market and viability note (kit 1.8 pipeline), with cited machine, flake, scrap and sheet prices for the first partner region
---

# ReflowEconomy market and viability

The users are waste-picker cooperatives and small recyclers who now sell baled scrap; the alternatives are selling bales as they are, buying a commercial turnkey line, or assembling Precious Plastic machines one by one without a system view. The open playbook matters because the value is in the system (what to process, safety, economics and a passport buyers trust), not in any one machine, and because the cited prices show the site only pays its way if its products sell well above commodity regenerated sheet. Prices are asking prices from public listings, checked on 2026-10-25, converted at INR 95.46 per USD (closing rate of 25 August 2026, [HDFC Sky](https://hdfcsky.com/news/rupee-rises-24-paise-to-close-at-95-46-against-us-dollar)); none is a quote. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Waste-picker cooperatives moving into processing | Organised waste pickers, for example SWaCH in Pune (more than 2,100 members serving over 360,000 homes, [WIEGO](https://wiego.org/wp-content/uploads/2019/09/fact_sheet_cooperative_swach.pdf)) | Selling unwashed PET bottle scrap at about INR 55/kg, 0.58 USD/kg ([IndiaMART listings](https://m.indiamart.com/impcat/pet-flakes-scrap.html)); hot-washed clear PET flake lists at INR 78 to 90/kg, 0.82 to 0.94 USD/kg ([IndiaMART](https://m.indiamart.com/impcat/pet-bottle-flake.html)) | 25,505 for the equipment of the reference micro-factory (option A, `bom/bom.csv` items 1 to 12); about 8,000 for a sort-and-bale hub (option B, RFE-OPT-001) | Keeps 51.6 % of input local as products and clean flake on paper, with a passport that lets buyers trust the material |
| Small recyclers and social enterprises | Workshops of 30 to 100 m2 on a weak grid | Precious Plastic 1 x 1 m sheet press workshop (hot press, cold press, table and trolleys), EUR 7,000, 15 kW three-phase ([Bazar](https://bazar.preciousplastic.com/machines/sheetpress/sheet-press-fully-built/1x1-meter-sheet-press-workshop-hot-and-cold-press-preparation-table-trolleys/)); a hot press alone listed at 5,044 (currency not stated, [Bazar](https://bazar.preciousplastic.com/machines/sheetpress/sheet-press-fully-built/1x1-meter-hot-sheet-press)); Shredder Pro 3.0 listed at 12,450 (currency not stated, 4 kW, 400 V, [Bazar](https://bazar.preciousplastic.com/machines/shredder-pro/shredder-pro-fully-built/new-shreeder-pro-3.0-by-maleon)) | As above; the press line of the BOM (USD 6,250 for the 5 kW press, cooling press and bridge) sits below the cited workshop | One layout, recipes, safety rules and an economics model for the whole floor, not just one machine |
| Buyers of recycled sheet and beams | Furniture makers, builders, schools in the partner region | Regenerated HDPE sheet 12 mm at INR 55 per sq ft, about 0.54 USD/kg ([IndiaMART, Kriyanshi Chemical, Morbi](https://m.indiamart.com/impcat/recycled-plastic-sheets.html)); speckled design-grade PP sheet 10 mm at INR 180 per sq ft, about 2.2 USD/kg (same page) | Break-even product price 2.49 USD/kg (RFE-CAL-001 section 10) | Traceable, single-polymer sheets with a recycled content statement (ISO 14021) |
| Municipal and NGO programmes | Local bodies integrating waste pickers under the SWM Rules, 2016 | To assess (no public benchmark found for a municipal micro-factory programme) | As above | A permittable, documented model with a passport for public procurement |

The comparison that matters most is the product price. At the reference 2.50 USD/kg the site makes +0.17 USD per shift before rent; commodity regenerated HDPE sheet listed at about 0.5 to 1 USD/kg would lose money on every shift, while design-grade sheet listed at about 2.2 USD/kg is close to break-even. A site therefore has to sell design-grade sheets or finished products to named buyers, or start as a sort-and-bale hub (option B), which needs a third of the capital and sells bales at the prices above while it builds that market (RFE-DEC-001 D4). Bale prices for HDPE and PP, the price for e-waste lots and local wages are to assess with the partner.

## Open route

The playbook, models and passport schema are published under CERN-OHL-S-2.0 (hardware) and MIT (scripts), with the documents moving to CC BY-SA 4.0 at the first release (RFE-DDR-002). A micro-factory would be built by a cooperative or social enterprise with a local fabricator or open-hardware workspace building the shredder, extruder and presses to their published designs and the fit-out to the making sketches in RFE-BLD-001; machines can also be bought from Precious Plastic workspaces. It spreads through waste-picker networks (WIEGO, the Alliance of Indian Wastepickers), Precious Plastic workspaces, universities and NGOs, each publishing what it learns back to the repository. Keeping the passport schema open is what lets a buyer trust lots from many small sites at once.

## Sources

All checked on 2026-10-25: IndiaMART category pages for PET flake, PET scrap and recycled plastic sheets; Precious Plastic Bazar listings for the sheet press workshop, the 1 x 1 m hot press and the Shredder Pro 3.0; WIEGO, *SWaCH fact sheet*; HDFC Sky, rupee closing rate of 25 August 2026. A 10 t compact baling press listed at INR 150,000 ([IndiaMART, S M Engineering, Chennai](https://m.indiamart.com/smengineeringchennai); the listing's description is unreliable) is used for option B in RFE-OPT-001.
