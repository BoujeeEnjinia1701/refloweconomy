---
doc_id: RFE-REG-001
title: ReflowEconomy regulatory and standards register
project: ReflowEconomy
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First register (kit 1.8 pipeline) for the reference micro-factory, with the first partner region (Maharashtra, India) and the international standards the design uses
---

# ReflowEconomy regulatory and standards register

Which standards and regulations apply to a small plastics micro-factory, where, and what is needed. The first partner region is Maharashtra, India (first candidate partner SWaCH, Pune; nothing agreed), so state and national rules are listed for it; other regions are to assess when a partner is found. Not legal advice; anything marked "to assess" needs a qualified reviewer before any site operates or any claim is made. Method: STANDARDS section 23. Every source was checked on 2026-10-25.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Plastic Waste Management Rules, 2016, as amended (registration of plastic waste processors) | India; administered in Maharashtra by MPCB | Processors register on the CPCB portal (eprplastic.cpcb.gov.in); fresh registration valid one year, renewal three years; application fee by capacity, INR 5,000 under 200 t a year; physical audit by the board ([MPCB service page](https://mpcb.gov.in/sites/default/files/plastic_processor.pdf)) | Applies: the reference site processes about 25 t a year (PR-020) | Site operator | Applies; to do at P5 with a real site |
| G2 | Air (Prevention and Control of Pollution) Act, 1981 and Water (Prevention and Control of Pollution) Act, 1974: consents; Hazardous and Other Wastes Rules, 2016: authorisation | India | MPCB requires the Air and Water Act consents and the hazardous waste authorisation as part of processor registration (same page) | Applies: melt fumes discharged through a stack; wash water and sludge; the industry category and consent route for a 25 t a year site are to assess | Site operator with a consultant | To assess |
| G3 | IS 14534:1998, *Guidelines for recycling of plastics* | India (BIS) | Selection, segregation and processing; wastewater treated before discharge (7.3.1); no burning of plastic waste (8.4); indoor air quality and exhausts (8.2); fire protection (8.3); no recycled material in food, pharmaceutical or drinking-water contact (8.5) ([BIS text](https://law.resource.org/pub/in/bis/S11/is.14534.1998.pdf)) | Applies as guidance; the design meets 7.3.1, 8.2, 8.3 and 8.4 by design; 8.5 goes into the passport and product rules | Design lead | Met by design (8.5 to add to the playbook) |
| G4 | Solid Waste Management Rules, 2016, Rule 15 | India | Local bodies recognise organisations of waste pickers and integrate them into collection | Applies to the partner model, not the hardware | Partner and municipality | Applies |
| G5 | Occupational Safety, Health and Working Conditions Code, 2020 (in force 21 November 2025; replaces the Factories Act, 1948) | India | A factory is a workplace of 20 or more workers with power ([factoHR summary](https://factohr.com/occupational-safety-health-and-working-conditions-code/)); under the Factories Act the threshold was 10 ([Factories Act, s. 2(m)](https://rskr.irimee.in/sites/default/files/FACTORIESACT-CPN.pdf)) | A four-worker site is below the factory threshold; which of the code's general duties still apply, and the state rules, are to assess | Site operator | To assess |
| G6 | MSEDCL Conditions of Supply, clause 6.4.1 | Maharashtra | Single-phase supply up to 40 A; above that, three-phase LT up to 80 kW ([MSEDCL](https://www.mahadiscom.in/wp-content/uploads/2018/08/CoS_MSEDCL_2010.pdf)) | Applies: the morning loads exceed 40 A on paper (RFE-DEC-001 D1) | Site operator and electrician | Applies; decision with Amish |
| G7 | E-Waste (Management) Rules, 2022 and Battery Waste Management Rules, 2022 | India | Boards and cells go only to registered recyclers or refurbishers | Applies to the export cage and the cell container; receiver types to name per stream (PR-004) | Site operator | Applies; per-stream rules to write |
| G8 | ISO 13857:2019, safety distances to prevent hazard zones being reached | International | Table 4: reaching through slots of 40 to 120 mm, 850 mm; over 120 mm, the reaching-over distances ([Troax](https://www.troax.com/app/uploads/Brochure-Safety-Guide_EN.pdf); [Axelent](https://www.axelent.dk/media/3343/normsen.pdf)) | Applies to the shredder feed slot (460 x 120 mm, 1,060 mm path) | Design lead | Met by design (RFE-CAL-001 section 7; RFE-DEC-001 D3) |
| G8a | EN 12012 series, safety requirements for size reduction machines for plastics and rubber (type C) | European; used internationally | Machine-specific requirements that take precedence over the generic ISO 13857 distances | Applies to the shredder; which part applies and its feed-opening rules are to assess (text not checked) | Design lead and safety professional | To assess |
| G9 | ISO 14119 (interlocking devices) and ISO 13849-1 (safety-related parts of control systems) | International | Interlock selection and the performance level of the feed flap, door and heater interlocks | Applies to the shredder interlocks and the heater interlock | Electrician and safety professional | To assess (performance level not yet set) |
| G10 | IEC 60204-1, electrical equipment of machines; the local wiring code | International; local | Emergency stop, isolation, protective bonding of the machines and the board | Applies to the board and the machines | Licensed electrician | Certification needed later (installation certificate, build plan stop S2) |
| G11 | IEC 60034-30-1, efficiency classes of motors | International | Minimum motor efficiencies used in the energy budget ([ABB note](https://library.e.abb.com/public/db64d153e3c346938e18916e66fb1d0d/9AKK107319%20EN%2005-2018_20848_ABB_Technical_note_IEC_60034_30_1.pdf)) | Applies to the motors bought (IE3 assumed) | Design lead | Met by design (on paper) |
| G12 | Occupational exposure limits (local; the playbook uses the US OSHA PELs as a floor: formaldehyde 0.75 ppm over 8 h, acrolein 0.1 ppm) | Local; United States as a floor | Air at the workstations | Applies; can only be shown by air monitoring (PR-011) | Safety professional | To assess at TRL 4 (on hold) |
| G13 | Noise at work (local limit; the playbook uses 85 dB(A) over 8 h, as in EU Directive 2003/10/EC) | Local | Operator exposure and hearing protection zones | Applies (PR-012) | Safety professional | To assess (measurement at TRL 4) |
| G14 | National building and fire code (in India, the National Building Code 2016, Part 4) | Local | Exits, escape widths, headroom, extinguishers, storage of combustible stock | Applies to the layout; the safety professional confirms escape widths and the 2.02 m headroom (stop S7) | Safety professional | To assess |
| G15 | Container modification: structural design | Local | Removing the adjoining side walls of two containers | Applies to the container option only; the rented shed (preferred) needs none | Structural engineer | Certification needed later |
| G16 | ISO 14021, self-declared environmental claims (recycled content) | International | Recycled content statements in passport schema v0.2 | Applies to every passport | Design lead | Met by design (schema v0.2) |
| G17 | Basel Convention plastic waste amendments (in force 1 January 2021) | International | Prior informed consent for most mixed or contaminated plastic waste shipments | Applies to export lots that cross borders; most export streams here are metals and boards to national refiners | Site operator | To assess per stream |
| G18 | EU Regulations 2024/1781 (ESPR, digital product passport) and 2023/1542 (batteries) | European Union | Product and battery passports | Direction of travel for the passport only; no compliance is claimed | Design lead | Does not apply (reference only) |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

All checked on 2026-10-25: MPCB, *Plastic processor registration* service page; BIS, IS 14534:1998; factoHR, *OSH Code 2020* summary; Factories Act, 1948 (IRIMEE copy); MSEDCL, *Conditions of Supply*, 2010; Troax, *Safety guide*; Axelent, *Standards*; ABB, *Technical note IEC 60034-30-1*, 2018. The OSHA limits, ISO 14021, Basel Convention and EU regulations are cited with links in RFE-PRB-001 and RFE-CAL-001.
