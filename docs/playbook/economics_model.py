"""ReflowEconomy micro-factory economics model (operator-editable), part of RFE-CAL-001.

How to use it:
  1. Copy docs/playbook/economics_inputs.csv and change the "value" column to your local
     prices, wages, tariff and yields. Leave the "key" column as it is.
  2. Run:  python docs/playbook/economics_model.py [your_inputs.csv]
  3. Read the result per shift, per kilogram, the break-even product price and the
     break-even input per shift.

The model is linear: product, flake, metal, paper, e-waste and disposal masses scale with
input_kg; energy is split into a fixed part per shift and a part that scales with input;
wages, consumables, filters, rent and equipment recovery are fixed per shift. All values
are in USD. The reference values are estimates for concept review, not market data.
"""
import csv
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent / "economics_inputs.csv"


def load(path=DEFAULT):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["key"]: float(r["value"]) for r in csv.DictReader(f)}


def run(i):
    """Return a dict of results for the inputs dict i."""
    sales = {
        "Products": i["products_kg"] * i["product_price"],
        "PET flake": i["pet_flake_kg"] * i["pet_flake_price"],
        "Metals": i["metals_kg"] * i["metals_price"],
        "Paper and card": i["paper_kg"] * i["paper_price"],
        "E-waste": i["ewaste_kg"] * i["ewaste_price"],
    }
    costs = {
        "Feedstock": i["input_kg"] * i["feedstock_price"],
        "Wages": i["workers"] * i["wage"],
        "Energy": i["energy_kwh"] * i["tariff"],
        "Disposal": i["disposal_kg"] * i["disposal_price"],
        "Consumables": i["consumables"],
        "Filters": i["filters"],
        "Rent": i["rent"],
    }
    revenue, opex = sum(sales.values()), sum(costs.values())
    recovery = i["capex"] / (i["years"] * i["shifts_per_year"])
    margin = revenue - opex
    result = margin - recovery
    output_kg = i["products_kg"] + i["pet_flake_kg"]
    # break-even product price at the reference input
    other = revenue - sales["Products"]
    be_price = (opex + recovery - other) / i["products_kg"]
    # break-even input: contribution per kg of input against the fixed costs per shift
    var_energy = (i["energy_kwh"] - i["energy_fixed_kwh"]) / i["input_kg"]
    contrib = revenue / i["input_kg"] - i["feedstock_price"] \
        - var_energy * i["tariff"] - i["disposal_kg"] / i["input_kg"] * i["disposal_price"]
    fixed = costs["Wages"] + costs["Consumables"] + costs["Filters"] + costs["Rent"] \
        + i["energy_fixed_kwh"] * i["tariff"] + recovery
    be_input = fixed / contrib if contrib > 0 else float("inf")
    return {
        "sales": sales, "costs": costs, "revenue": revenue, "opex": opex, "margin": margin,
        "recovery": recovery, "result": result, "result_per_kg_in": result / i["input_kg"],
        "cost_per_kg_out": (opex + recovery) / output_kg, "output_kg": output_kg,
        "be_product_price": be_price, "contrib_per_kg_in": contrib, "fixed_per_shift": fixed,
        "be_input_kg": be_input, "capacity_kg": i["capacity_kg"],
        "per_year": result * i["shifts_per_year"],
        "sens_price_050": 0.50 * i["products_kg"],
    }


def report(i, r):
    lines = ["ReflowEconomy economics per shift (USD, estimates)", ""]
    for k, v in r["sales"].items():
        lines.append(f"  + {k:<16} {v:8.2f}")
    for k, v in r["costs"].items():
        lines.append(f"  - {k:<16} {v:8.2f}")
    lines += [
        f"  = Operating margin   {r['margin']:8.2f}",
        f"  - Equipment recovery {r['recovery']:8.2f}  (${i['capex']:,.0f} over {i['years']:g} years of {i['shifts_per_year']:g} shifts)",
        f"  = Result             {r['result']:8.2f}  per shift; {r['per_year']:,.0f} per year",
        "",
        f"Output sold as products and flake: {r['output_kg']:.1f} kg; full cost {r['cost_per_kg_out']:.2f} USD/kg of output",
        f"Break-even product price at this input: {r['be_product_price']:.2f} USD/kg (now {i['product_price']:.2f})",
        f"Break-even input: {r['be_input_kg']:.0f} kg per shift (line capacity {r['capacity_kg']:.0f} kg)",
        f"Each 0.50 USD/kg on the product price moves the result by {r['sens_price_050']:.2f} USD per shift",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    inputs = load(sys.argv[1] if len(sys.argv) > 1 else DEFAULT)
    print(report(inputs, run(inputs)))
