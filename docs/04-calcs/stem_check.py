"""RFE-STM-001: STEM check of the ReflowEconomy reference micro-factory (option A) and the sort-and-bale hub
(option B), STANDARDS section 20.

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv, which the table in docs/01b-stem-check.md reproduces. Option A's figures
are taken from the calculation note's script (docs/04-calcs/sizing.py, RFE-CAL-001), imported here so the
check reruns whenever the design changes; the rest are first-order checks against cited limits.

Fix rule (Amish's standing instruction of 2026-10-23): S13 (motor energy counted at the shaft) and S17 (feed
slot above the ISO 13857 Table 4 range) failed in detail and were fixed in the design and calculation in this
session (RFE-DEC-001 D2 and D3); they are closed here by the fix. S14 (supply current) fails and its fixes
change a decided input (the single-phase supply, the working day or the throughput), so it goes to Amish
(RFE-DEC-001 D1) and stays "Fails, fix proposed".
"""
import contextlib
import io
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "docs" / "04-calcs"), str(ROOT / "cad" / "src")]
from stem_check import Check, FIX, PLAUSIBLE, WITHIN, G  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    import sizing as S  # noqa: E402  (prints RFE-CAL-001; silenced here)
from model import PARAMS as MP  # noqa: E402

c = Check(out=ROOT / "docs/04-calcs/stem_results.csv")

# ---------------------------------------------------------------- option A: mass, separation, thermal
inputs = {"input": S.A["input"]}
outputs = {"products": S.products, "flake": S.pet_flake, "metals": S.c["metals"], "ewaste": S.c["ewaste"],
           "paper": S.c["paper"], "residue": S.c["residue"], "losses": S.losses}
c.balance("S1", "Every kilogram of the 100 kg input leaves as products (32.3), flake (19.3), metals, e-waste, paper or disposal (28.4)",
          "Mathematics", "Numerical method", inputs, outputs, "kg", tolerance=0.001, law="Conservation of mass (RFE-CAL-001 section 2)",
          closed_by="RFE-CAL-001 section 2")
c.claim("S2", "In water, PP and HDPE flake floats and PET and PVC sink, so float-sink separates them (it cannot split HDPE from PP, which are sorted into their own bins at the table)", "Physics", "Fluid mechanics",
        law="Archimedes: a flake floats if its density is below water's (1.00 g/cm3); HDPE 0.94 to 0.97, PP 0.90 to 0.91, PET 1.33 to 1.45, PVC 1.38 to 1.41 g/cm3 (KiTech; recipes)",
        value=0.97, limit=1.00, unit="g/cm3", rule="below", closed_by="docs/playbook/recipes/pet-flake.md")
# press standing loss: 50 mm mineral wool round the platen packs, 50 % extra for edges, frame and openings
k_ins, t_ins, dT = 0.045, 0.050, S.C["t_press"] - S.C["t_amb"]
area = 2 * 1.1 * 1.1 + 4 * 1.1 * 0.07 * 2
loss_est = k_ins * dT / t_ins * area * 1.5 / 1000
c.order_of_magnitude("S3", "The hot sheet press loses about 0.8 kW standing when hot", "Physics", "Heat transfer",
                     claimed=S.C["press_loss_kw"], estimate=loss_est, unit="kW",
                     law="Conduction through 50 mm mineral wool (k 0.045 W/m K) over the platen packs at 175 K, plus 50 % for edges and frame; closed press only (losses while loading and through the frame and jacks not counted)",
                     closed_by="Open: measure the standing loss on the built press (TRL 4, on hold)")
c.rows[-1]["verdict"] = PLAUSIBLE   # an assumption checked against an estimate (independent review, 2026-10-25)
t_heat = S.sheet_kwh / (S.C["press_kw"] - S.C["press_loss_kw"]) * 60
c.claim("S4", "At full heater power the 5 kW press puts a 12 mm HDPE sheet's heat in within the published 55 min cycle (cooling is in the separate cooling press)",
        "Physics", "Thermodynamics", law="Energy balance: sheet and mould heat 2.56 kWh (HDPE cp 2.25 kJ/kg K over 175 K plus 180 kJ/kg fusion, about 62 % of the 293 J/g of fully crystalline PE) at 5.0 kW less the 0.8 kW standing loss; average draw over the cycle 3.6 kW",
        value=round(t_heat, 1), limit=55, unit="min", rule="below", closed_by="RFE-CAL-001 section 4")
alpha = 0.45 / (950 * 2250)                         # m2/s, solid HDPE
t_cond = (0.006 ** 2 / alpha) * 1.5 * 4 / 60        # min: half-thickness 6 mm; x1.5 for melting; x4 for a loose flake bed
c.claim("S5", "Heat reaches the middle of a 12 mm sheet well inside the 55 min cycle", "Physics", "Heat transfer",
        law="Transient conduction t = L^2 / alpha (alpha 0.21 mm2/s for HDPE), x1.5 for the latent heat, x4 for a loose flake bed",
        value=round(t_cond, 1), limit=55, unit="min", rule="below", closed_by="RFE-CAL-001 section 4")
c.claim("S6", "HDPE and PP are processed at 190 to 210 C, below the 230 C (HDPE) and 240 C (PP) ceilings of their processing ranges",
        "Chemistry", "Materials and polymer chemistry", law="Processing ranges HDPE 190 to 230 C, PP 200 to 240 C (RJC Mold chart; Precious Plastic Extrusion Pro)",
        value=210, limit=230, unit="C", rule="below", closed_by="docs/playbook/recipes/hdpe.md, pp.md")
c.cited("S7", "PVC is never heated: it releases hydrogen chloride at press temperatures, and float-sink cannot remove it from PET",
        "Chemistry", "Materials and polymer chemistry",
        "PVC dehydrochlorination: 0.4 mol % HCl lost in 30 min at 200 C (Szarka and Ivan, 2013); PVC 1.38 to 1.41 g/cm3 sinks with PET",
        "Exclusion rule at sorting (safety rules, recipes, BLD stop S6); within known chemistry", WITHIN, "docs/playbook/safety.md")
c.cited("S8", "PET is sold as flake, not melted: it must be dried to about 0.005 % moisture at 150 to 175 C for 4 to 5 h or it hydrolyses in the melt",
        "Chemistry", "Materials and polymer chemistry", "Hydrolytic degradation of PET in the melt (Plastics Technology, How to Dry PET)",
        "Design choice decided by Amish, 2026-09-25 (RFE-DDR-001 item 3); consistent with the chemistry", WITHIN, "RFE-DDR-001")
c.cited("S9", "Polyolefin melt fumes contain formaldehyde, acetaldehyde, acrolein, CO and a wax aerosol, so every melt process needs local exhaust",
        "Chemistry", "Environmental and atmospheric chemistry", "Borealis, Statement on impurities: polyolefins, ed. 6, 2022",
        "Two enclosing hoods, G4 and F7 filters, impregnated carbon, stack above the roof (RFE-CAL-001 section 6)", WITHIN, "RFE-CAL-001 section 6")
# booth plume: axisymmetric plume from the open hot platen (natural convection 8 W/m2 K over 1.21 m2 at 175 K)
qc = 8.0 * 1.21 * dT / 1000                         # kW convective
z_pl = 2.24 - 0.95                                  # m, platen to booth roof
m_plume = 0.071 * qc ** (1 / 3) * z_pl ** (5 / 3) + 0.0018 * qc
q_booth = S.Q * (MP["HOOD_A_OPEN"][0] * MP["HOOD_A_OPEN"][1]) / S.a_open * 1.2   # kg/s through the booth
c.claim("S10", "The press booth's extract (0.5 m/s at the sash) carries away the hot-platen plume, so fume does not spill out of the sash",
        "Physics", "Fluid mechanics", law="Axisymmetric plume mass flow m = 0.071 Qc^(1/3) z^(5/3) + 0.0018 Qc (NFPA 92, a fire-plume equation used here as a heuristic well below its range), Qc from natural convection off the open 1.1 m platen, z to the booth roof; a hot mould being unloaded is a larger, short source",
        value=round(m_plume, 3), limit=round(q_booth, 3), unit="kg/s", rule="below", closed_by="RFE-CAL-001 section 6")
c.claim("S11", "The 250 mm duct runs at a transport velocity that keeps the wax aerosol from settling", "Engineering and technology", "Standards practice",
        law="Duct design velocity: ACGIH gives about 5 to 10 m/s for vapours and fumes; 10 m/s is used here so the condensed wax aerosol does not settle (design choice, both hoods drawing)",
        value=round(S.v_duct, 1), limit=10.0, unit="m/s", rule="above", closed_by="RFE-CAL-001 section 6")
c.claim("S12", "The 1.5 kW fan moves 0.57 m3/s against 815 Pa with dirty filters", "Engineering and technology", "Power and link budgets",
        law="Fan input = Q dp / (fan 0.55 x motor 0.85)", value=round(S.fan_kw, 2), limit=S.F["fan_rated_kw"], unit="kW", rule="below",
        closed_by="RFE-CAL-001 section 6")
c.claim("S13", "The line uses 1.0 kWh or less per kilogram of output with motor and drive losses counted (was 0.83 on shaft power)",
        "Engineering and technology", "Power and link budgets",
        law="Electrical energy = shaft energy / (motor x drive); IE3 minimum efficiencies, IEC 60034-30-1 (ABB note): 2.2 kW 86.7 %, 1.5 kW 85.3 %; drive 96 %; single-phase pump 75 %",
        value=round(S.e_total / S.output, 2), limit=1.0, unit="kWh/kg", rule="below",
        closed_by="RFE-DEC-001 D2 (fix made 2026-10-25: CAL counts motor and drive losses)")
c.cited("S14", "The block A loads run on a 230 V, 40 A single-phase supply (the old figure was 8.75 kW = 38.0 A at unity power factor)",
        "Physics", "Electromagnetism and circuits",
        "I = P / (V x PF x eta); drive input currents from datasheets (Schneider ATV12: 20.2 A at 2.2 kW, 14.9 A at 1.5 kW, 240 V); single-phase motor currents NEC Table 430.248",
        f"Block A {S.ia_run:.1f} A running ({S.ia_fl:.1f} A at full load; arithmetic sum of table currents, a conservative upper estimate) against {S.D['amps']:.0f} A; block B {S.ib_run:.1f} A, 91 % of the supply as a continuous load. Fixes: three-phase 400 V supply ({S.ia_3ph:.1f} A per phase if balanced) or three time blocks on single phase (largest {max(S.i_three.values()):.1f} A, about {S.day_three:.1f} h day, about 13 USD a shift more in wages)",
        FIX, "Open: RFE-DEC-001 D1, proposed, awaiting Amish")
c.claim("S15", "With the lined enclosure the shredder operator's 8 h exposure is 85 dB(A) or less (sound power assumed 102 dB(A))",
        "Physics", "Acoustics and vibration", law="Lp = Lw + 10 log(Q / 4 pi r^2 + 4 / R) in the reverberant steel room; 15 dB insertion loss; LEX over 3.79 h",
        value=round(S.lex_enc, 1), limit=85.0, unit="dB(A)", rule="below", margin=0.0,
        closed_by="Open: measure the machine's sound power and the enclosure on site (TRL 4, on hold)")
c.rows[-1]["verdict"] = PLAUSIBLE   # rests on an assumed sound power, so only a measurement closes it
slot_w, slot_h = MP["CHUTE_SLOT"]
s_enc = 2 * (1.6 * 1.4 + 1.6 * 1.6 + 1.4 * 1.6)
il_max = 10 * math.log10(s_enc / (slot_w * slot_h / 1e6))
c.claim("S16", "A 15 dB insertion loss is possible with the feed slot open", "Physics", "Acoustics and vibration",
        law="Open-area limit on insertion loss IL <= 10 log(S_enclosure / S_open)", value=15.0, limit=round(il_max, 1), unit="dB", rule="below",
        closed_by="RFE-CAL-001 section 7")
c.claim("S17", "A hand through the feed slot cannot reach the cutters: the slot is 120 mm high (ISO 13857 Table 4 range) and the path is 1,060 mm against 850 mm",
        "Engineering and technology", "Standards practice",
        law="ISO 13857 Table 4: slot 40 < e <= 120 mm, safety distance 850 mm; above 120 mm the reaching-over distances apply (Troax and Axelent guides to ISO 13857)",
        value=S.reach if slot_h <= 120 else 0.0, limit=MP["REACH_SR"], unit="mm", rule="above",
        closed_by="Open: fix D3 made 2026-10-25 (slot 160 to 120 mm); the EN 12012 type C standard for size reduction machines, which takes precedence over ISO 13857, still to check; cutter height assumed")
c.rows[-1]["verdict"] = PLAUSIBLE   # independent review, 2026-10-25
# seam beam: UB 305 x 165 x 40 S355 in the reserved space, simply supported over the 12.03 m seam, roof edges of both boxes
L_b = (MP["FL_X"] - 2 * MP["WALL_T"]) / 1000
trib = 2.438                       # m: half of each 2.35 m roof span plus the rails
gk, qk = 0.20 * trib + 0.40, 0.75 * trib     # kN/m: roof sheet and rails plus beam; imposed load on a roof without access (IS 875 Part 2)
w_uls = 1.35 * gk + 1.5 * qk
M_ed = w_uls * L_b ** 2 / 8
M_rd = 623e3 * 355 / 1e6           # kN m, Wpl,y 623 cm3, S355, top flange held by the roof
c.claim("S18", "A UB 305 x 165 x 40 that fits the reserved 165 x 305 mm space carries the roof edges over the 12 m seam (top flange held by the roof)",
        "Physics", "Strength of materials",
        law="Bending only: M = w L^2 / 8 at ULS (1.35 g + 1.5 q; roof 0.20 kN/m2 plus 0.40 kN/m beam, imposed 0.75 kN/m2 over 2.44 m) against Wpl fy (623 cm3, S355). Unrestrained it would buckle laterally, so the top flange must be tied to the roof; service deflection about 41 mm (L/290) misses L/360, and racking stiffness lost with the side walls is not checked: both for the structural engineer",
        value=round(M_ed, 1), limit=round(M_rd, 1), unit="kN m", rule="below", closed_by="Structural engineer's design (RFE-DEC-001 confirm item 1)")
c.claim("S19", "The container floor carries the 430 kg hot press", "Physics", "Mechanics and statics",
        law="Line load on a 40 ft container floor, 3.0 t/m allowed (TIS, ISO 1496 limits); press over 1.2 m",
        value=round(0.43 / 1.2, 2), limit=3.0, unit="t/m", rule="below", closed_by="RFE-CAL-001 section 8")
c.claim("S20", "No one lifts more than 25 kg: flake and product lots are packed in 25 kg bags or moved on the transfer bridge",
        "Biology", "Ergonomics", law="ISO 11228-1 reference mass 25 kg is for ideal conditions; frequency, height (the feed lip is at 1.70 m) and reach multipliers reduce it", value=25.0, limit=25.0, unit="kg", rule="below",
        closed_by="Open: apply the ISO 11228-1 multipliers to the real lifts with the partner; smaller bags if needed")
c.rows[-1]["verdict"] = PLAUSIBLE   # independent review, 2026-10-25
c.cited("S21", "Air at the workstations stays below the occupational exposure limits for formaldehyde and acrolein with the hoods running",
        "Biology", "Toxicology", "OSHA PELs: formaldehyde 0.75 ppm (8 h), acrolein 0.1 ppm; emission rates of small open machines are not published",
        "Hoods sized for 0.5 m/s; exposure can only be shown by air monitoring on a running site", PLAUSIBLE,
        "Open: air monitoring on a running site (TRL 4, on hold)")
water = 0.30 * (S.po_flake + S.pet_flake)          # kg of water on washed flake: 30 % (no dewatering centrifuge), a pessimistic figure
air_cap = 0.3 * 1.2 * 0.004 * 3600                 # kg/h: 0.3 m3/s past the trays picking up 4 g/kg
c.claim("S22", "Washed flake on 7.2 m2 of trays dries by the next shift with the 0.4 kW fan running through the 8 h shift", "Physics", "Thermodynamics",
        law="Psychrometric moisture pick-up: about 0.3 m3/s past the trays at 4 g of water per kg of air, against 30 % water on the day's flake over the 8 h the fan runs (still air overnight not counted)",
        value=round(water / 8, 2), limit=round(air_cap, 1), unit="kg/h", rule="below", closed_by="RFE-CAL-001 section 3")
c.claim("S23", "The shredder's assumed 15 kg/h lies inside the published 8.8 to 41.8 kg/h range for its class", "Engineering and technology", "Standards practice",
        law="Precious Plastic Shredder Pro published range", value=S.B["shred_rate"], limit=S.B["shred_range"][1], unit="kg/h", rule="below",
        closed_by="RFE-CAL-001 section 3 (rate measured at TRL 4)")
c.claim("S24", "The extruder's assumed 5 kg/h lies at the low end of the published 5 to 15 kg/h for the Extrusion Pro class",
        "Engineering and technology", "Standards practice", law="Precious Plastic Bazar listing, V4 extrusion: 5 to 15 kg/h at 4 kW, 400 V",
        value=S.B["extr_rate"], limit=5.0, unit="kg/h", rule="above", closed_by="RFE-CAL-001 section 3")
c.cited("S25", "Every passport record validates against schema v0.2, and a product lot without parents is rejected", "Engineering and technology",
        "Standards practice", "JSON Schema draft 2020-12 validation of the example records (RFE-CAL-001 section 11)",
        "3 of 3 examples valid; the negative case is rejected", WITHIN, "RFE-CAL-001 section 11")
r, i = S.r, S.inp
costs = (i["input_kg"] * i["feedstock_price"] + i["workers"] * i["wage"] + i["energy_kwh"] * i["tariff"] + i["disposal_kg"] * i["disposal_price"]
         + i["consumables"] + i["filters"] + i["rent"] + i["capex"] / (i["years"] * i["shifts_per_year"]))
other = i["pet_flake_kg"] * i["pet_flake_price"] + i["metals_kg"] * i["metals_price"] + i["paper_kg"] * i["paper_price"] + i["ewaste_kg"] * i["ewaste_price"]
c.order_of_magnitude("S26", f"The site breaks even at a product price of about {r['be_product_price']:.2f} USD/kg (arithmetic only: the inputs, including the 2.50 USD/kg price, are assumptions)", "Mathematics", "Orders of magnitude",
                     claimed=round(r["be_product_price"], 2), estimate=(costs - other) / i["products_kg"], unit="USD/kg", factor=1.05,
                     law="Hand recomputation: (all costs per shift including equipment recovery - other sales) / product mass", closed_by="RFE-CAL-001 section 10")
c.cited("S27", "A lithium cell crushed in the shredder can start a fire, so cells are pulled out at intake and kept in dry sand",
        "Chemistry", "Electrochemistry and batteries", "US EPA, An Analysis of Lithium-ion Battery Fires in Waste Management and Recycling, 2021",
        "Intake rule, fire-safe sand container in the cage, BLD stop S5", WITHIN, "docs/playbook/safety.md")

# ---------------------------------------------------------------- option B: sort-and-bale hub
c.order_of_magnitude("B1", "Option B: a 10 t vertical baler makes bales of about 120 kg of sorted PET bottles", "Physics", "Mechanics and statics",
                     claimed=120, estimate=1.0 * 0.7 * 0.75 * 230, unit="kg",
                     law="Bale mass = chamber volume (1.0 x 0.7 x 0.75 m) x bale density, taken as about 230 kg/m3 to match the supplier listing's 120 kg (so not an independent estimate); platen pressure only about 0.14 MPa",
                     closed_by="Open: bale density on a trial bale (TRL 4, on hold)")
c.rows[-1]["verdict"] = PLAUSIBLE
F_b = 10 * 1000 * G
v_b = 2200 * 0.7 / F_b * 1000
c.claim("B2", "Option B: a 2.2 kW single-phase power pack drives the 10 t ram at a usable speed", "Physics", "Fluid mechanics",
        law="Ram speed v = P eta / F (eta 0.7) against a usable minimum of about 10 mm/s (a 1 m stroke in under 2 min)",
        value=round(v_b, 1), limit=10.0, unit="mm/s", rule="above", closed_by="RFE-OPT-001")
i_b = 17.0 + 1.7 + 4.9
c.claim("B3", "Option B: the baler, fans and lights run on the 40 A single-phase supply", "Physics", "Electromagnetism and circuits",
        law="NEC Table 430.248: 3 hp (2.2 kW) single-phase motor 17 A at 230 V; lights 1.7 A; a 0.4 kW fan 4.9 A",
        value=i_b, limit=40.0, unit="A", rule="below", closed_by="RFE-OPT-001")
c.claim("B4", "Option B: four people sort and bale 300 kg of input in a shift", "Mathematics", "Orders of magnitude",
        law="Three sorters at 25 kg/h for 4 h (the rate in RFE-CAL-001) with the fourth weighing, baling and issuing passports",
        value=3 * 25 * 4, limit=300, unit="kg", rule="above", closed_by="RFE-OPT-001")
c.claim("B5", "Option B: a 120 kg bale is never lifted by hand; it moves on a pallet truck", "Biology", "Ergonomics",
        law="ISO 11228-1 reference mass 25 kg; bales and pallets on a hand pallet truck", value=0, limit=25, unit="kg lifted", rule="below",
        closed_by="RFE-OPT-001")

state = c.write()
print(f"stem_check: {state}")

# ---------------------------------------------------------------- refresh the claims table in RFE-STM-001
doc = ROOT / "docs/01b-stem-check.md"
if doc.exists():
    text = doc.read_text(encoding="utf-8")
    a, b = "<!-- STM_TABLE -->", "<!-- /STM_TABLE -->"
    if a in text and b in text:
        head = ("| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        rows = "".join(f"| {r['id']} | {r['claim']} | {r['field']} | {r['branch']} | {r['law']} | {r['check']} | {r['verdict']} | {r['closed_by'] or 'Open'} |\n"
                       for r in c.rows)
        i, j = text.index(a) + len(a), text.index(b)
        doc.write_text(text[:i] + "\n" + head + rows + text[j:], encoding="utf-8")
        print("refreshed the claims table in docs/01b-stem-check.md")
