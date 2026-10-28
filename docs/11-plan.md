---
doc_id: RFE-PLN-001
title: ReflowEconomy project plan
project: ReflowEconomy
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First project plan (kit 1.8 pipeline) at stage P3, with the reference list of every source cited in the repo
---

# ReflowEconomy project plan

ReflowEconomy is at stage P3 (design outputs) and TRL 3, the portfolio cap. The next gate, P4 (verification, TRL 4), is on hold by Amish's instruction; before it, three decisions are requested: how the site meets its supply limit (RFE-DEC-001 D1), which concept is the reference (D4), and the approach to the first co-design partner. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Playbook content | Design lead | Feasibility matrix with hazard, export point and sources (PR-001); export rules per stream (PR-004); food-contact rule from IS 14534 | Open: PR-001 and PR-004 not met |
| Reference micro-factory design | Design lead | Model at D3, drawings, priced BOM, build plan, calculation note | Done at P3; supply decision open (D1) |
| Concept selection | Amish | Choice between A, B and the staged start (RFE-OPT-001, RFE-DDR-004) | Proposed, awaiting Amish (D4) |
| Material passport | Design lead | Schema v0.2 with examples; a phone form for PR-015 | Schema done; form not started (P4) |
| Co-design | Amish with the partner | Sessions with a waste-picker cooperative (first candidate SWaCH through WIEGO) | Not started; nothing agreed |
| Regulatory | Operator with a consultant | Registration and consent route in Maharashtra (RFE-REG-001) | To assess |
| Verification (P4) | Design lead with the partner | Test plans and reports for the first checks in RFE-BLD-001 section 5 | On hold (TRL cap 3) |

## Resources needed

Table 2. Resources (indicative; for planning, not quotes).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Co-design facilitation with a waste-picker cooperative | Validated user requirements, input mix, prices, wages, working day | 3 sessions | To assess |
| Licensed electrician (partner region) | Supply design for the option chosen in D1; installation certificate at P4 | 1 to 2 days of design | To assess |
| Qualified safety professional | Review of layout, exits, headroom, guarding and interlocks | 2 days | To assess |
| Structural engineer (container option only) | Seam beam and propping design | 1 to 2 days | To assess |
| Equipment for a first site (P4, on hold) | The reference micro-factory, `bom/bom.csv` items 1 to 12 | Build to RFE-BLD-001 | 25,505 indicative (value-engineering target 25,000) |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Done 2026-10-25 (kit 1.9.1 upgrade) |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT | Done 2026-10-25 |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM check closed, feasibility closed | Done except the STEM check (open on S14, S15, S21) and the concept choice (awaiting Amish) |
| P3 Design outputs | Model at D3, STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability complete | Reached 2026-10-25 |
| P4 Verification | Test plans and lab reports for the first checks; air, noise and current measurements | On hold (TRL cap 3) |
| P5 Validation | Field trial with the partner; registration and consents | On hold |
| P6 Commercialization | Launch plan, operator training, standard cost; only with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish to decide D1 (supply: three-phase recommended, single-phase in three blocks as the fallback) and D4 (concept: the staged start recommended).
2. Approach SWaCH through WIEGO for co-design, as decided on 2026-10-02.
3. Write the missing playbook columns and export rules (PR-001, PR-004).
4. TRL 4 stays on hold until Amish lifts the cap.

## References

Every source cited in this repo's documents, Chicago style (all checked online on the dates given in the citing documents).

- ABB. *Technical Note: IEC 60034-30-1 Standard on Efficiency Classes for Low Voltage AC Motors*. 2018. https://library.e.abb.com/public/db64d153e3c346938e18916e66fb1d0d/9AKK107319%20EN%2005-2018_20848_ABB_Technical_note_IEC_60034_30_1.pdf.
- Axelent. "Standards." https://www.axelent.dk/media/3343/normsen.pdf.
- Basel Convention. "Plastic Waste Amendments." https://www.basel.int/implementation/plasticwaste/amendments/overview/tabid/8426/default.aspx.
- Borealis. *Statement on Impurities: Polyolefins*. Edition 6, 2022. https://www.borealisgroup.com/storage/Emission-EN-ed.06.pdf.
- Brooks, Amy L., Shunli Wang, and Jenna R. Jambeck. "The Chinese Import Ban and Its Impact on Global Plastic Waste Trade." *Science Advances* 4, no. 6 (2018). https://doi.org/10.1126/sciadv.aat0131.
- Bureau of Indian Standards. *IS 14534:1998, Guidelines for Recycling of Plastics*. https://law.resource.org/pub/in/bis/S11/is.14534.1998.pdf.
- Elliott Electric Supply. "Full Load Current in Amps for Single Phase AC Motors" (NEC Table 430.248). https://elliottelectric.com/StaticPages/ElectricalReferences/ElectricalTables/Amperes_Single_Phase_Alternate.aspx.
- European Union. Regulation (EU) 2023/1542 on batteries. https://eur-lex.europa.eu/eli/reg/2023/1542/oj.
- European Union. Regulation (EU) 2024/1781, Ecodesign for Sustainable Products. https://eur-lex.europa.eu/eli/reg/2024/1781/oj.
- factoHR. "Occupational Safety, Health and Working Conditions (OSH) Code, 2020." https://factohr.com/occupational-safety-health-and-working-conditions-code/.
- Government of India. *The Factories Act, 1948*. https://rskr.irimee.in/sites/default/files/FACTORIESACT-CPN.pdf.
- Government of India, MoEFCC. *Solid Waste Management Rules, 2016*. https://cdnbbsr.s3waas.gov.in/s30f46c64b74a6c964c674853a89796c8e/uploads/2024/07/20240710555191345.pdf.
- HDFC Sky. "Rupee Rises 24 Paise to Close at 95.46 Against US Dollar." August 25, 2026. https://hdfcsky.com/news/rupee-rises-24-paise-to-close-at-95-46-against-us-dollar.
- IndiaMART. "PET Bottle Flake and Crush"; "PET Flakes Scrap"; "Recycled Plastic Sheets, Panels and Boards"; S M Engineering, Chennai, "10 Ton Compact Baling Press." https://m.indiamart.com/impcat/pet-bottle-flake.html; https://m.indiamart.com/impcat/pet-flakes-scrap.html; https://m.indiamart.com/impcat/recycled-plastic-sheets.html; https://m.indiamart.com/smengineeringchennai.
- International Aluminium Institute. "Aluminium Recycling Saves 95 % of the Energy Needed for Primary Aluminium Production." https://international-aluminium.org/landing/aluminium-recycling-saves-95-of-the-energy-needed-for-primary-aluminium-production/.
- ITU and UNITAR. *Global E-waste Monitor 2024*. https://ewastemonitor.info/the-global-e-waste-monitor-2024/.
- Maharashtra Pollution Control Board. "Registration of Plastic Waste Processor." https://mpcb.gov.in/sites/default/files/plastic_processor.pdf.
- Maharashtra State Electricity Distribution Co. *Conditions of Supply*. 2010. https://www.mahadiscom.in/wp-content/uploads/2018/08/CoS_MSEDCL_2010.pdf.
- OECD. *Global Plastics Outlook*. 2022. https://www.oecd.org/en/publications/global-plastics-outlook_de747aef-en.html.
- OSHA. "Table Z-1, Limits for Air Contaminants." https://www.osha.gov/annotated-pels/table-z-1.
- Plastics Technology. "How to Dry PET for Container Applications." https://www.ptonline.com/articles/how-to-dry-pet-for-container-applications.
- Precious Plastic. Academy pages for the Shredder Pro, Extrusion Pro and sheetpress; Bazar listings for the V4 extrusion, the 1 x 1 m hot sheet press, the sheet press workshop and the Shredder Pro 3.0. https://www.preciousplastic.com; https://bazar.preciousplastic.com.
- RJC Mold. "Plastic Melting Point Chart." https://rjcmold.com/guides/plastic-melting-point-chart.
- Schneider Electric. ATV12HU22M2 and ATV12HU15M2 product data sheets. https://media.cetnaj.com.au/Datasheets/Schneider/Schneider_ATV12HU22M2.pdf; https://www.mouser.com/datasheet/2/357/Altivar_12_ATV12HU15M2-1782510.pdf.
- Szarka, Györgyi, and Béla Iván. "Thermal Properties, Degradation and Stability of Poly(vinyl chloride) Predegraded Thermooxidatively in the Presence of Dioctyl Phthalate Plasticizer." *Journal of Macromolecular Science, Part A* 50, no. 2 (2013): 208 to 214. https://real.mtak.hu/4463/.
- TIS (GDV). "Permissible Loading Capacity of Containers." https://www.tis-gdv.de/tis_e/containe/belast/belast-htm/.
- Troax. *Safety Guide*. https://www.troax.com/app/uploads/Brochure-Safety-Guide_EN.pdf.
- UNEP. *Global Waste Management Outlook 2024*. https://www.unep.org/resources/global-waste-management-outlook-2024.
- US EPA. *An Analysis of Lithium-ion Battery Fires in Waste Management and Recycling*. 2021. https://www.epa.gov/system/files/documents/2021-08/lithium-ion-battery-report-update-7.01_508.pdf.
- WHO. *Children and Digital Dumpsites*. 2021. https://www.who.int/publications/i/item/9789240023901.
- WIEGO. "Fact Sheet: Cooperative SWaCH." https://wiego.org/wp-content/uploads/2019/09/fact_sheet_cooperative_swach.pdf.
- World Bank. *What a Waste 2.0*. 2018. https://datatopics.worldbank.org/what-a-waste/.
- Standards cited without a public text: ISO 13857:2019, ISO 13849-1, ISO 14119, ISO 14021, ISO 11228-1, IEC 60204-1, IEC 60034-30-1, NFPA 92, ACGIH *Industrial Ventilation*, IS 875 (Part 2), National Building Code of India 2016, EU Directive 2003/10/EC; B. Wunderlich, *Thermal Analysis of Polymeric Materials* (Springer, 2005).
