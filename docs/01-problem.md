---
doc_id: RFE-PRB-001
title: ReflowEconomy problem statement
project: ReflowEconomy
doc_type: Problem statement
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem with sources, users, context, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Sources checked online; UNEP 2023 figure corrected to 2.3 billion tonnes; single-phase supply and plastics-only reference line recorded as decided (RFE-DDR-001)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Supply figures updated for the 1.5 kW fume fan (maximum demand near 9 kW, about 14 kW connected); rented shed preferred; intake quality rule noted
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'First co-design partner decided by Amish on 2026-10-02: a waste-picker cooperative, first candidate SWaCH through WIEGO'
---

# ReflowEconomy problem statement

Smaller and lower-income countries export scrap and import finished goods, losing the value of their own materials. Most recycling know-how assumes industrial scale, and unsafe informal recovery (open burning, acid leaching of e-waste) harms workers and communities. ReflowEconomy is an open playbook for a small, safe, local micro-factory that recovers and remanufactures what can be handled at small scale, and exports only what needs industrial refining, with a material passport so buyers can trust the recycled feedstock. Design with, not for: requirements must come from co-design sessions with waste pickers, cooperatives and small recyclers through a local partner.

## The problem

Waste is growing fastest where formal recycling is weakest. The World Bank estimated 2.01 billion tonnes of municipal solid waste in 2016, rising to about 3.40 billion tonnes by 2050, with the fastest growth in lower-income regions ([World Bank, *What a Waste 2.0*, 2018](https://datatopics.worldbank.org/what-a-waste/)). UNEP's 2024 outlook puts the 2023 figure at 2.3 billion tonnes, heading for 3.8 billion tonnes by 2050 ([UNEP, *Global Waste Management Outlook 2024*](https://www.unep.org/resources/global-waste-management-outlook-2024)). After losses in recycling, only about 9 % of plastic waste was recycled worldwide in 2019 ([OECD, *Global Plastics Outlook*, 2022](https://www.oecd.org/en/publications/global-plastics-outlook_de747aef-en.html)).

Where value is recovered today, it is often recovered unsafely or sent abroad:

- **Informal recovery harms people.** The world generated a record 62 million tonnes of e-waste in 2022, and only 22.3 % was documented as formally collected and recycled ([ITU and UNITAR, *Global E-waste Monitor 2024*](https://ewastemonitor.info/the-global-e-waste-monitor-2024/)). Much of the rest is burned in the open or leached with acid to recover copper and gold. WHO reports that up to 12.9 million women work in the informal waste sector and that more than 18 million children and adolescents are active in the industrial sector, of which waste processing is a part, exposing them to lead, mercury and dioxins ([WHO, *Children and digital dumpsites*, 2021](https://www.who.int/publications/i/item/9789240023901)).
- **Value leaves the country.** Collected scrap is baled and sold to exporters at low prices, and products made from the same materials come back as imports. Export routes are also narrowing: the Basel Convention plastic waste amendments, in force since 1 January 2021, require prior informed consent for most mixed or contaminated plastic waste shipments ([Basel Convention, plastic waste amendments](https://www.basel.int/implementation/plasticwaste/amendments/overview/tabid/8426/default.aspx)).
- **Know-how assumes industrial scale.** Most recycling guidance describes plants processing tens of thousands of tonnes a year. The open designs that do exist for small scale, such as the Precious Plastic machines and workspace kits ([Precious Plastic](https://www.preciousplastic.com)), cover single machines well but give little guidance on which materials are safe to process locally, what must leave for industrial refining, how the economics work per kilogram and per shift, and how a buyer can trust the output.
- **Buyers cannot trust recycled feedstock.** Without a record of origin, sorting method, contamination and processing, a small recycler's flake or product sells at a discount or not at all. Large markets are moving toward mandatory product and battery passports ([EU Regulation 2024/1781, ESPR](https://eur-lex.europa.eu/eli/reg/2024/1781/oj); [EU Regulation 2023/1542, batteries](https://eur-lex.europa.eu/eli/reg/2023/1542/oj)), which small recyclers have no simple way to meet.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Waste picker or cooperative member | Better and more stable prices for sorted material; safer work than open burning; a path into processing, not only collection | Streets, dumpsites and transfer points; cash payment per kilogram; often no formal employment or protective equipment |
| Micro-factory operator (cooperative, social enterprise or small business) | A proven reference layout, equipment list, process recipes, safety rules and an economics model that works per kilogram and per shift | Rented shed, yard or shipping containers of about 30 to 100 m²; unreliable grid; limited capital (tens of thousands of USD, not millions) |
| Local buyer of recycled material or products | Feedstock or products of known material, grade and contamination, with a traceable origin | Local manufacturers, builders, furniture makers, schools, municipal procurement |
| Industrial refiner or exporter | Clean, correctly identified lots of what the micro-factory must not process: circuit boards, cells, mixed metals | Licensed facilities, often in another region or country |
| Municipality or NGO partner | A safe, permittable model for local recovery that creates jobs and reduces open burning | Waste management plans, donor programs, informal-sector integration |
| Open hardware community | A playbook that links the portfolio's machine repos (WasteWise Scan, WasteWise-ml and planned shredder, foundry and cell tester) into one system | Makerspaces, university labs, NGOs |

## Constraints

- ReflowEconomy is a playbook and a data standard, not a single machine. Machines live in their own repos. There is no hardware budget for this repo (`budget_usd` is null on purpose); the reference micro-factory equipment list gives indicative costs only.
- Small scale: the reference micro-factory fits a rented shed of about 60 m² (preferred, RFE-DDR-002 item 11) or the footprint of two 40 ft shipping containers side by side (about 12.2 x 4.9 m).
- Input quality matters: a site can only keep disposal at 20 % or less of input if deliveries carry about 10 % residue or less, so an intake quality rule is part of the playbook (RFE-DDR-002 item 8).
- Safe by default: no open burning, no acid or cyanide leaching, no heating of PVC, fume extraction on every melt process (see `docs/playbook/safety.md`).
- Recover and remanufacture locally; export only what needs industrial refining. The feasibility matrix (`docs/playbook/feasibility-matrix.md`) sets that boundary per material.
- Works on a weak grid: the reference micro-factory runs on a single-phase supply (taken as 230 V, 40 A) with staggered heating, so its maximum demand stays near 9 kW (8.75 kW with the 1.5 kW fume fan) although about 14 kW is connected. Decided by Amish, 2026-09-25 (RFE-DDR-001 item 5; fan size RFE-DDR-002 item 10).
- The reference line is plastics only; aluminium remelting is a separate add-on bay with its own safety case. Decided by Amish, 2026-09-25 (RFE-DDR-001 item 1).
- The material passport must be simple enough to fill in on a phone at the desk and structured enough (JSON Schema) for software to validate.
- Open: documents and schema are published under the repo licenses so any group can copy, adapt and improve them.

## Out of scope

- Chemical refining of metals, battery black mass and e-waste, and ore refining. These stay industrial.
- Medical, hazardous and chemical waste. The micro-factory does not accept it.
- Designing the machines themselves (shredder, extruder, sheet press, foundry, NIR scanner). The playbook references open designs and the portfolio's machine repos.
- Large material recovery facilities and municipal collection systems.

## Prior work

- Precious Plastic: open-source plastic recycling machines (shredder, extrusion, injection, sheet press), workspace starter kits and a community network ([preciousplastic.com](https://www.preciousplastic.com)). ReflowEconomy builds on this for the plastics line and adds the multi-material boundary, economics, safety rules and passport.
- World Bank *What a Waste 2.0* and UNEP *Global Waste Management Outlook 2024* for waste growth and the role of the informal sector (sources above).
- *Global E-waste Monitor 2024* and WHO *Children and digital dumpsites* for e-waste volumes and the harm of informal recovery (sources above).
- Aluminium remelting needs only a small fraction of the energy of primary production, about 5 %, or a saving of 95 % ([International Aluminium Institute](https://international-aluminium.org/landing/aluminium-recycling-saves-95-of-the-energy-needed-for-primary-aluminium-production/)); this is why aluminium rates high in the feasibility matrix.
- EU digital product passport and battery passport rules (sources above) as a direction of travel for the material passport, without claiming compliance.

Sources were checked online on 2026-09-25: the World Bank, UNEP, OECD, *Global E-waste Monitor 2024*, WHO, Basel Convention, International Aluminium Institute and EU regulation figures and titles match their publishers' pages, except the UNEP 2023 figure, which is corrected above. Precious Plastic is cited as a project, not for a figure.

## Open questions

- Which region and partner should the first co-design round use: a waste-picker cooperative, an existing Precious Plastic workspace or a municipal program? Decided by Amish on 2026-10-02 (RFE-DDR-001 item 7): a waste-picker cooperative; the first candidate to approach is a waste-picker cooperative, for example SWaCH in Pune, India, reached through the WIEGO network; nothing is agreed.
- What do local buyers actually require before they will pay a premium for recycled feedstock, and which passport fields matter to them?
- What share of collected material is target plastic in practice? The 60 % used in the concept is an estimate for source-separated collection; mixed dumpsite material will be lower.
- Which permits apply to a small plastics recycler in the first target region (environmental, fire, occupational safety, waste handling)?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
