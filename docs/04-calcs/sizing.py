"""RFE-CAL-001: first-principles sizing of the ReflowEconomy reference micro-factory.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv (one row per requirement).

Sections: A mass balance, B throughput and time budget, C energy, D electrical supply,
E fume extraction, F noise, G layout checks (from cad/src/model.py), H equipment cost
(from bom/bom.csv), I economics (docs/playbook/economics_model.py), J material passport.
All inputs are estimates for a paper proof of concept (TRL 3). Units SI unless noted.
"""
import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
sys.path.insert(0, str(ROOT / "docs" / "playbook"))
import economics_model as econ  # noqa: E402
from model import PARAMS as MP, ZONES  # noqa: E402

OUT = []


def say(s=""):
    print(s)


# ---------------------------------------------------------------- A mass balance
A = {
    "input": 100.0,                      # kg mixed collected input per shift
    "comp": {"PET": 22.0, "HDPE": 20.0, "PP": 18.0, "metals": 8.0, "ewaste": 2.0,
             "paper": 10.0, "residue": 20.0},   # kg per 100 kg (estimate, source-separated)
    "wash_loss": 0.10,                   # labels, glue, dirt, float-sink rejects (fraction of plastic)
    "shred_loss": 0.015,                 # fines
    "dry_loss": 0.01,                    # fines and spills
    "melt_loss": 0.03,                   # purge and degraded melt, fraction of melt feed
    "trim": 0.08,                        # trim and off-cuts, fraction of gross melt output, re-shredded
}
c = A["comp"]
assert abs(sum(c.values()) - A["input"]) < 1e-9
k_mech = (1 - A["wash_loss"]) * (1 - A["shred_loss"]) * (1 - A["dry_loss"])
pet_flake = c["PET"] * k_mech
po_flake = (c["HDPE"] + c["PP"]) * k_mech          # dried HDPE and PP flake to the hot zone
# trim loop at steady state: flake + trim = feed; gross = feed (1 - melt_loss); trim = trim * gross
gross = po_flake / (1 / (1 - A["melt_loss"]) - A["trim"])
trim = A["trim"] * gross
products = gross - trim
losses = (c["PET"] + c["HDPE"] + c["PP"]) - pet_flake - products
local = pet_flake + products
disposal = c["residue"] + losses
washed = (c["PET"] + c["HDPE"] + c["PP"]) * (1 - A["wash_loss"])

say("A. Mass balance per shift (kg, estimates)")
say(f"  PET clean flake {pet_flake:.1f}; HDPE and PP products {products:.1f} (gross melt output {gross:.1f}, trim re-shredded {trim:.1f})")
say(f"  Metals {c['metals']:.1f}; e-waste {c['ewaste']:.1f}; paper and card {c['paper']:.1f}; sorting residue {c['residue']:.1f}; process losses {losses:.1f}")
say(f"  Kept local as products or clean flake: {local:.1f} kg = {local / A['input'] * 100:.1f} % of input (R7 target 50 %)")
say(f"  Exported for refining: {c['metals'] + c['ewaste']:.1f} kg; to licensed disposal {disposal:.1f} kg = {disposal:.1f} % (R8 target 20 %)")
say(f"  Mass closes: {local + c['metals'] + c['ewaste'] + c['paper'] + disposal:.2f} kg")

# intake quality rule (RFE-DDR-001 item 8, decided by Amish 2026-09-25 in RFE-DDR-002): R8 keeps counting process losses;
# the site refuses or charges for loads whose sampled residue is above a threshold.
# For a load with residue r (%), the other streams scale in proportion, so process losses
# scale with (100 - r) / (100 - r_ref).
R8_LIMIT = 20.0
loss_per_nonres = losses / (A["input"] - c["residue"])


def disposal_at(r):
    return r + loss_per_nonres * (A["input"] - r)


r_max = (R8_LIMIT - loss_per_nonres * A["input"]) / (1 - loss_per_nonres)
r_rule = math.floor(r_max)
local_at_rule = local * (A["input"] - r_rule) / (A["input"] - c["residue"])
say(f"  Intake quality rule: disposal is 20 % or less when sampled residue is {r_max:.1f} % or less; rule threshold {r_rule:.0f} %")
say(f"  At the {r_rule:.0f} % threshold: disposal {disposal_at(r_rule):.1f} %, kept local {local_at_rule:.1f} %; the reference mix ({c['residue']:.0f} % residue) would be refused or charged")

# ---------------------------------------------------------------- B throughput and time budget
B = {
    "block_a": 4.0, "block_b": 4.0,        # h: A = sort, wash, shred, extrude; B = press
    "sort_rate": 25.0, "sorters": 2,       # kg/h per person (assumption)
    "shred_rate": 15.0,                    # kg/h effective (assumption within sourced 8.8 to 41.8 kg/h)
    "shred_range": (8.8, 41.8),            # Precious Plastic Shredder Pro published range
    "sheet_kg": 1.0 * 1.0 * 0.012 * 950,   # 1 x 1 m x 12 mm HDPE at 950 kg/m3
    "sheets": 2,
    "press_cycle_h": 55 / 60,              # per 12 mm sheet (published Precious Plastic sheetpress figure)
    "extr_rate": 5.0,                      # kg/h beams (assumption)
    "extr_heatup_h": 1 / 3,
    "heaters_off_before_end_h": 0.5,
    "tray_area": 1.2 * 0.6 * 10, "tray_load": 10.0,   # m2, kg/m2
}
sort_h = A["input"] / (B["sort_rate"] * B["sorters"])
shred_load = washed + trim
shred_h = shred_load / B["shred_rate"]
shred_h_lo = shred_load / B["shred_range"][0]
sheets_gross = B["sheets"] * B["sheet_kg"]
beams_gross = gross - sheets_gross
extr_h = beams_gross / B["extr_rate"]
extr_total_h = extr_h + B["extr_heatup_h"]

# press heat-up and cycle energy from first principles
C = {
    "platen_kg": 2 * 1.1 * 1.1 * 0.015 * 7850,    # two 15 mm steel platens 1.1 x 1.1 m
    "mould_kg": 2 * 1.0 * 1.0 * 0.002 * 7850,     # two 2 mm steel mould sheets per cycle
    "cp_steel": 0.49, "cp_hdpe": 2.25, "latent_hdpe": 180.0,   # kJ/kg K, kJ/kg K, kJ/kg
    "t_press": 200.0, "t_amb": 25.0,
    "press_kw": 5.0, "press_loss_kw": 0.8,         # heater rating, standing loss when hot (assumption)
    "extr_heater_kw": 2.0, "extr_motor_kw": 1.5, "extr_heater_duty": 0.6, "extr_motor_load": 0.6,
    "shred_kw": 2.2, "shred_load": 0.7,
    "pump_kw": 0.75, "pump_h": 4.0,
    "fan_kw": 0.4, "fan_h": 8.0,
    "light_kw": 0.4, "light_h": 8.0,
    "fume_run_after_h": 0.5,
}
dT = C["t_press"] - C["t_amb"]
heatup_kwh = C["platen_kg"] * C["cp_steel"] * dT / 3600
heatup_h = heatup_kwh / (C["press_kw"] - C["press_loss_kw"])
sheet_kwh = (B["sheet_kg"] * (C["cp_hdpe"] * dT + C["latent_hdpe"]) + C["mould_kg"] * C["cp_steel"] * dT) / 3600
cycle_kw = sheet_kwh / B["press_cycle_h"] + C["press_loss_kw"]
press_window = B["block_b"] - B["heaters_off_before_end_h"]
press_capacity = (press_window - heatup_h) / B["press_cycle_h"]
press_hot_h = heatup_h + B["sheets"] * B["press_cycle_h"]

say("\nB. Throughput and time budget per 8 h shift")
say(f"  Sorting {A['input']:.0f} kg by {B['sorters']} people at {B['sort_rate']:.0f} kg/h each: {sort_h:.1f} h of block A ({B['block_a']:.0f} h)")
say(f"  Shredder load {shred_load:.1f} kg (washed plastic {washed:.1f} + trim {trim:.1f}); at {B['shred_rate']:.0f} kg/h: {shred_h:.2f} h of {B['block_a']:.0f} h; at the low end {B['shred_range'][0]} kg/h: {shred_h_lo:.1f} h")
say(f"  Required shredder rate: {shred_load / B['block_a']:.1f} kg/h")
say(f"  Extruder: beams {beams_gross:.1f} kg gross at {B['extr_rate']:.0f} kg/h = {extr_h:.2f} h + {B['extr_heatup_h']:.2f} h heat-up = {extr_total_h:.2f} h in block A")
say(f"  Sheet press: {B['sheets']} sheets of {B['sheet_kg']:.1f} kg = {sheets_gross:.1f} kg; heat-up {heatup_h:.2f} h, cycle {B['press_cycle_h'] * 60:.0f} min")
say(f"  Press capacity in the {press_window:.1f} h heating window: {press_capacity:.2f} sheets (need {B['sheets']}); hot for {press_hot_h:.2f} h")
say(f"  Press power during cycles {cycle_kw:.2f} kW of {C['press_kw']:.1f} kW installed")
say(f"  Drying: {po_flake + pet_flake:.1f} kg flake on {B['tray_area']:.1f} m2 of trays = {(po_flake + pet_flake) / B['tray_area']:.1f} kg/m2 (limit {B['tray_load']:.0f})")

# ---------------------------------------------------------------- C energy
E = {
    "Shredder": C["shred_kw"] * C["shred_load"] * shred_h,
    "Washing pump": C["pump_kw"] * C["pump_h"],
    "Drying fan": C["fan_kw"] * C["fan_h"],
    "Extruder": C["extr_heater_kw"] * B["extr_heatup_h"] + (C["extr_heater_kw"] * C["extr_heater_duty"]
                + C["extr_motor_kw"] * C["extr_motor_load"]) * extr_h,
    "Sheet press": C["press_kw"] * heatup_h + B["sheets"] * sheet_kwh + C["press_loss_kw"] * B["sheets"] * B["press_cycle_h"],
}

# ---------------------------------------------------------------- E fume extraction (needed for fan energy)
F = {
    "v_face": 0.5,                         # m/s, R11
    "leak": 0.10,                          # allowance for enclosure gaps
    "duct_d": MP["DUCT_D"] / 1000, "rho": 1.2, "nu": 1.5e-5, "f": 0.018,
    "duct_len": 8.0,                       # m equivalent straight length
    "fittings_vp": 1.4,                    # three elbows and a junction, in velocity pressures
    "hood_entry_vp": 1.5,                  # acceleration plus enclosing-hood entry loss
    "prefilter_pa": 250.0, "carbon_pa": 200.0,   # final (dirty) pressure drops
    "stack_vp": 1.0,
    "eta": 0.55 * 0.85,                    # fan times motor efficiency
    "fan_rated_kw": 1.5,                  # RFE-DDR-001 item 10, decided by Amish 2026-09-25 (RFE-DDR-002); was 1.1 kW
}
a_open = MP["HOOD_A_OPEN"][0] * MP["HOOD_A_OPEN"][1] + MP["HOOD_B_OPEN"][0] * MP["HOOD_B_OPEN"][1]
Q = F["v_face"] * a_open * (1 + F["leak"])
A_duct = math.pi * F["duct_d"] ** 2 / 4
v_duct = Q / A_duct
vp = 0.5 * F["rho"] * v_duct ** 2
dp_friction = F["f"] * F["duct_len"] / F["duct_d"] * vp
dp = F["hood_entry_vp"] * vp + dp_friction + F["fittings_vp"] * vp + F["prefilter_pa"] + F["carbon_pa"] + F["stack_vp"] * vp
fan_kw = Q * dp / F["eta"] / 1000
canopy_q = F["v_face"] * 2.0 * 3.5
canopy_kw = canopy_q * dp / F["eta"] / 1000
fume_h = (extr_total_h + C["fume_run_after_h"]) + (press_hot_h + C["fume_run_after_h"])
room_vol = (MP["FL_X"] - 2 * MP["WALL_T"]) * (MP["FL_Y"] - 2 * MP["WALL_T"]) * 2390 / 1e9
ach = Q * 3600 / room_vol
makeup_area = Q / 1.5

E["Fume extraction"] = fan_kw * fume_h
E["Lighting, desk and small loads"] = C["light_kw"] * C["light_h"]
e_total = sum(E.values())
e_fixed = (C["press_kw"] * heatup_h + C["extr_heater_kw"] * B["extr_heatup_h"] + E["Fume extraction"]
           + E["Lighting, desk and small loads"] + E["Drying fan"])
output = local

say("\nC. Energy per shift (kWh, estimates)")
for k, v in E.items():
    say(f"  {k:<32} {v:6.1f}")
say(f"  {'Total':<32} {e_total:6.1f}  = {e_total / output:.2f} kWh/kg of output ({output:.1f} kg); R9 target 1.0")
say(f"  Fixed part (heat-up, fume fan, lights, drying fan) {e_fixed:.1f} kWh")
say(f"  Press heat-up energy {heatup_kwh:.2f} kWh; per sheet {sheet_kwh:.2f} kWh; platens {C['platen_kg']:.0f} kg")

# ---------------------------------------------------------------- D electrical supply
D = {"volts": 230.0, "amps": 40.0}
load_a = {"Shredder": C["shred_kw"], "Washing pump": C["pump_kw"], "Drying fan": C["fan_kw"], "Lighting": C["light_kw"],
          "Extruder": C["extr_heater_kw"] + C["extr_motor_kw"], "Fume fan": F["fan_rated_kw"]}
load_b = {"Sheet press heaters": C["press_kw"], "Drying fan": C["fan_kw"], "Lighting": C["light_kw"], "Fume fan": F["fan_rated_kw"]}
connected = C["shred_kw"] + C["pump_kw"] + C["fan_kw"] + C["extr_heater_kw"] + C["extr_motor_kw"] + C["press_kw"] + F["fan_rated_kw"] + C["light_kw"]
peak_a, peak_b = sum(load_a.values()), sum(load_b.values())
peak = max(peak_a, peak_b)
supply_kw = D["volts"] * D["amps"] / 1000
say("\nD. Electrical supply (decided: single-phase with staggered heating)")
say(f"  Connected load {connected:.2f} kW; block A peak {peak_a:.2f} kW; block B peak {peak_b:.2f} kW")
say(f"  Maximum demand {peak:.2f} kW = {peak * 1000 / D['volts']:.1f} A at {D['volts']:.0f} V; supply {D['amps']:.0f} A ({supply_kw:.1f} kW); margin {(1 - peak / supply_kw) * 100:.0f} %")
say(f"  Without the interlock: {connected:.2f} kW = {connected * 1000 / D['volts']:.0f} A")

say("\nE. Fume extraction")
say(f"  Hood openings {a_open:.2f} m2 at {F['v_face']} m/s + {F['leak'] * 100:.0f} % = {Q:.3f} m3/s ({Q * 3600:.0f} m3/h)")
say(f"  Duct {F['duct_d'] * 1000:.0f} mm: {v_duct:.1f} m/s, velocity pressure {vp:.0f} Pa, friction {dp_friction:.0f} Pa")
say(f"  System pressure {dp:.0f} Pa with dirty filters; fan input {fan_kw:.2f} kW of {F['fan_rated_kw']} kW rated ({fan_kw / F['fan_rated_kw'] * 100:.0f} %)")
say(f"  Canopy alternative over 2.0 x 3.5 m: {canopy_q:.1f} m3/s, about {canopy_kw:.1f} kW (rejected)")
say(f"  Room {room_vol:.0f} m3: {ach:.0f} air changes per hour; make-up opening {makeup_area:.2f} m2 at 1.5 m/s")
say(f"  Fan runs {fume_h:.1f} h per shift")

# ---------------------------------------------------------------- F noise
N = {"Lw": 102.0, "IL": 15.0, "alpha": 0.10, "Qdir": 2.0, "r_op": 1.0, "r_other": 4.0, "limit": 85.0}
ix, iy, iz = (MP["FL_X"] - 2 * MP["WALL_T"]) / 1000, (MP["FL_Y"] - 2 * MP["WALL_T"]) / 1000, 2.39
S = 2 * (ix * iy + ix * iz + iy * iz)
Rc = S * N["alpha"] / (1 - N["alpha"])


def lp(lw, r):
    return lw + 10 * math.log10(N["Qdir"] / (4 * math.pi * r ** 2) + 4 / Rc)


def lex(l_, h):
    return l_ + 10 * math.log10(h / 8)


lp_bare, lp_bare_far = lp(N["Lw"], N["r_op"]), lp(N["Lw"], N["r_other"])
lp_enc, lp_enc_far = lp(N["Lw"] - N["IL"], N["r_op"]), lp(N["Lw"] - N["IL"], N["r_other"])
lex_bare, lex_enc = lex(lp_bare, shred_h), lex(lp_enc, shred_h)
say("\nF. Shredder noise (sound power assumed, to be measured)")
say(f"  Room surface {S:.0f} m2, mean absorption {N['alpha']}, room constant {Rc:.1f} m2")
say(f"  Bare shredder LwA {N['Lw']:.0f} dB: {lp_bare:.1f} dB(A) at 1 m, {lp_bare_far:.1f} dB(A) at 4 m; LEX,8h {lex_bare:.1f} dB(A) for {shred_h:.2f} h")
say(f"  With {N['IL']:.0f} dB enclosure: {lp_enc:.1f} dB(A) at 1 m, {lp_enc_far:.1f} dB(A) at 4 m; LEX,8h {lex_enc:.1f} dB(A)")
lw_max = N["Lw"] + (N["limit"] - lex_enc)
say(f"  Largest bare-machine LwA that still meets 85 dB(A) LEX with the enclosure: {lw_max:.1f} dB")

# ---------------------------------------------------------------- G layout checks
fx, fy, t = MP["FL_X"], MP["FL_Y"], MP["WALL_T"]
area_ext = fx * fy / 1e6
area_int = (fx - 2 * t) * (fy - 2 * t) / 1e6
front_max = max(z[5] for z in ZONES.values() if z[7] == "front")
back_min = min(z[4] for z in ZONES.values() if z[7] == "back")
aisle = back_min - front_max
hx0, hx1 = MP["HOT_X"]
stock = [ZONES[k] for k in ("store1", "store2", "cage")]


def gap(z, x0, x1, y0, y1):
    dx = max(z[2] - x1, x0 - z[3], 0)
    dy = max(z[4] - y1, y0 - z[5], 0)
    return math.hypot(dx, dy)


hot_y0 = MP["AISLE_Y0"] + MP["AISLE_W"]
hot_clear = min(gap(z, hx0, hx1, hot_y0, fy - t) for z in stock)
# worst travel distance to the nearest exit along the aisle (from the far corner of each zone)
exits_x = [t, fx - t]
travel = max(min(abs(x - ex) for ex in exits_x) + abs(y - (MP["AISLE_Y0"] + MP["AISLE_W"] / 2))
             for z in ZONES.values() for x in (z[2], z[3]) for y in (z[4], z[5]))
overlap = [(a, b) for a in ZONES for b in ZONES if a < b and ZONES[a][2] < ZONES[b][3] and ZONES[b][2] < ZONES[a][3]
           and ZONES[a][4] < ZONES[b][5] and ZONES[b][4] < ZONES[a][5]]
say("\nG. Layout checks (cad/src/model.py)")
say(f"  Footprint {fx / 1000:.2f} x {fy / 1000:.2f} m = {area_ext:.1f} m2 external, {area_int:.1f} m2 inside (R5 target 60 m2)")
say(f"  Central aisle {aisle:.0f} mm clear (R5 target 1000 mm); front row depth {front_max - t:.0f} mm, back row depth {fy - t - back_min:.0f} mm")
say(f"  Hot zone {hx0:.0f} to {hx1:.0f} mm; nearest stock {hot_clear:.0f} mm away (target {MP['HOT_CLEAR']:.0f} mm)")
say(f"  Worst travel distance to an exit along the aisle {travel / 1000:.1f} m; zone overlaps: {overlap or 'none'}")

# ---------------------------------------------------------------- H equipment cost
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
cost = {int(r["item"].split()[0]): float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows}
equip = sum(v for k, v in cost.items() if k <= 12)
say("\nH. Equipment cost (bom/bom.csv, indicative)")
say(f"  Items 1 to 12: ${equip:,.0f} (R10 target $25,000; margin ${25000 - equip:,.0f}); building shell ${cost[13]:,.0f} extra")
say(f"  budget_usd in project.yaml is null (playbook repo); the equipment list is checked against R10 instead")

# ---------------------------------------------------------------- I economics
inp = econ.load()
checks = {"products_kg": products, "pet_flake_kg": pet_flake, "disposal_kg": disposal, "energy_kwh": e_total,
          "energy_fixed_kwh": e_fixed, "capex": equip}
say("\nI. Economics (docs/playbook/economics_model.py with economics_inputs.csv)")
for k, v in checks.items():
    ok = abs(inp[k] - v) <= max(0.06, 0.005 * abs(v))
    say(f"  inputs.csv {k} = {inp[k]:g} vs calculation {v:.2f}: {'consistent' if ok else 'MISMATCH'}")
    assert ok, f"economics_inputs.csv {k} disagrees with RFE-CAL-001"
r = econ.run(inp)
for line in econ.report(inp, r).splitlines():
    say("  " + line)

# ---------------------------------------------------------------- J material passport
try:
    import jsonschema
    s1 = json.loads((ROOT / "standards/material-passport.schema.json").read_text())
    s2 = json.loads((ROOT / "standards/material-passport-v0.2.schema.json").read_text())
    ex = sorted((ROOT / "standards/examples").glob("*.json"))
    v2 = [not list(jsonschema.Draft202012Validator(s2).iter_errors(json.loads(p.read_text()))) for p in ex]
    v1 = [not list(jsonschema.Draft202012Validator(s1).iter_errors(json.loads(p.read_text()))) for p in ex]
    bad = json.loads((ROOT / "standards/examples/intake-batch.json").read_text())
    bad["product_form"] = "sheet"   # a product lot without parents must fail
    neg = bool(list(jsonschema.Draft202012Validator(s2).iter_errors(bad)))
    trace = all(("parent_batch_ids" in json.loads(p.read_text())) or json.loads(p.read_text())["product_form"] == "intake-batch" for p in ex)
    say("\nJ. Material passport")
    say(f"  {sum(v2)} of {len(ex)} example records valid against v0.2; {sum(v1)} of {len(ex)} also valid against v0.1")
    say(f"  A sheet lot without parent_batch_ids is rejected: {neg}; every non-intake example lists its parents: {trace}")
    pp_ok = all(v2) and neg and trace
except ImportError:
    say("\nJ. Material passport: jsonschema not installed; validation skipped")
    pp_ok, v2, ex = False, [], []

# ---------------------------------------------------------------- results table
R = [
    ("R1", "Feasibility matrix: 7 groups with route, rating, hazard, export point and a source per row",
     "7 groups with route and reason; no hazard, export point or source columns", "Not met"),
    ("R2", "Sourced recipe for PET, HDPE, PP and aluminium", "4 recipes in docs/playbook/recipes/ (aluminium as the add-on bay)", "Met"),
    ("R3", "Operator-editable economics model with break-even", f"Model and CSV delivered; result {r['result']:+.2f} USD/shift; break-even product price {r['be_product_price']:.2f} USD/kg", "Met"),
    ("R4", "Every export stream names refining step, receiver type and packing rule", "Principle and cell packing rule only", "Not met"),
    ("R5", "60 m2 or less, aisles 1.0 m or more, separate hot zone", f"{area_ext:.1f} m2; aisle {aisle / 1000:.2f} m; hot zone {hot_clear / 1000:.2f} m from stock", "Met"),
    ("R6", "100 kg or more mixed input per 8 h shift", f"Shredder {shred_h:.2f} h of {B['block_a']:.0f} h at an assumed {B['shred_rate']:.0f} kg/h; press {press_capacity:.2f} sheets of capacity for {B['sheets']}", "At risk"),
    ("R7", "50 % or more of input kept local as products or clean flake", f"{local:.1f} %", "Met"),
    ("R8", "Residue to licensed disposal 20 % or less, process losses counted", f"{disposal:.1f} % at the reference mix ({c['residue']:.0f} % sorting residue + {losses:.1f} % process losses); {disposal_at(r_rule):.1f} % for a load at the R16 threshold", "Not met"),
    ("R9", "1.0 kWh/kg of output or less", f"{e_total / output:.2f} kWh/kg", "Met"),
    ("R10", "Equipment items 1 to 12 $25,000 or less", f"${equip:,.0f}", "Met"),
    ("R11", "0.5 m/s face velocity on every melt process; no PVC, PS or unknown; air below OELs",
     f"Hoods sized for 0.5 m/s ({Q:.2f} m3/s, fan {fan_kw:.2f} kW); exposure needs air monitoring", "Not verifiable at TRL 3"),
    ("R12", "Guarded shredder, insulated hot surfaces, RCDs, 85 dB(A) LEX or hearing zones",
     f"Guarding defined; LEX {lex_bare:.0f} dB(A) bare, {lex_enc:.0f} dB(A) with enclosure (sound power assumed)", "At risk"),
    ("R13", "Valid passport for every outgoing lot", f"{sum(v2)} of {len(ex)} examples valid against schema v0.2", "Met" if pp_ok else "Not met"),
    ("R14", "Passport lists parent batch IDs and schema version", "v0.2 requires schema_version and parent_batch_ids for every non-intake lot", "Met" if pp_ok else "Not met"),
    ("R15", "Passport filled in 2 min or less", "Needs a form and a timed trial", "Not verifiable at TRL 3"),
    ("R16", "Intake quality rule with a residue threshold that keeps R8 within 20 %",
     f"Threshold {r_rule:.0f} % residue by sampled mass (limit {r_max:.1f} %); loads above it refused or charged", "Met"),
]
with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "target", "value", "status"])
    w.writerows(R)
say("\nResults (also written to docs/04-calcs/results.csv)")
for row in R:
    say(f"  {row[0]:<4} {row[3]:<24} {row[2]}")
counts = {}
for row in R:
    counts[row[3]] = counts.get(row[3], 0) + 1
say("  " + "; ".join(f"{k}: {v}" for k, v in counts.items()))
