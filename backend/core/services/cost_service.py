import pandas as pd
import os
import random
from core.services.ml_service import predict_rates

random.seed(42)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "material_rates.csv")


# -----------------------------
# MATERIAL CALCULATION
# -----------------------------
def calculate_material(area, floors):
    total_area = area * floors

    return {
        "area": total_area,
        "cement": round(total_area * 0.4),
        "steel": round(total_area * 4),
        "sand": round(total_area * 1.8),
        "aggregate": round(total_area * 1.5),
        "brick": round(total_area * 8)
    }


# -----------------------------
# COST CALCULATION
# -----------------------------
def calculate_cost_ml(materials, year, month_num, temperature):

    rates = predict_rates(year, month_num, temperature)

    # CIVIL
    civil_material = (
        materials["cement"] * rates["cement_rate"] +
        materials["steel"] * rates["steel_rate"] +
        materials["sand"] * rates["sand_rate"] +
        materials["aggregate"] * rates["aggregate_rate"] +
        (materials["brick"] / 1000) * rates["brick_rate"]
    )
    civil_labour = civil_material * 0.3
    civil_total = civil_material + civil_labour

    # ELECTRICAL
    elec_material = materials["area"] * rates["electrical_material_rate"]
    elec_labour = elec_material * 0.4
    elec_total = elec_material + elec_labour

    # PLUMBING
    plumbing_material = materials["area"] * rates["plumbing_material_rate"]
    plumbing_labour = plumbing_material * 0.4
    plumbing_total = plumbing_material + plumbing_labour

    # TILES
    tile_material = materials["area"] * rates["tiles_material_rate"]
    tile_labour = materials["area"] * rates["tiles_labour_rate"]
    tile_total = tile_material + tile_labour

    # PAINT
    paint_material = materials["area"] * rates["paint_rate"]
    paint_labour = materials["area"] * rates["paint_labour_rate"]
    paint_total = paint_material + paint_labour

    total = civil_total + elec_total + plumbing_total + tile_total + paint_total

    return {
        "total": total,

        "civil_material": civil_material,
        "civil_labour": civil_labour,
        "civil_total": civil_total,

        "electrical_material": elec_material,
        "electrical_labour": elec_labour,
        "electrical_total": elec_total,

        "plumbing_material": plumbing_material,
        "plumbing_labour": plumbing_labour,
        "plumbing_total": plumbing_total,

        "tiles_material": tile_material,
        "tiles_labour": tile_labour,
        "tiles_total": tile_total,

        "paint_material": paint_material,
        "paint_labour": paint_labour,
        "paint_total": paint_total
    }


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def full_prediction(area, floors, year):

    df = pd.read_csv(DATA_PATH)

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    month_nums = list(range(1, 13))

    materials = calculate_material(area, floors)

    costs = []
    details = []

    for m, m_num in zip(months, month_nums):

        row = df[df["month_num"] == m_num].iloc[0]

        base_temp = row["temperature"]
        season = row["season"]

        temp = base_temp + (year - 2025) * ((m_num % 3) - 1)

        res = calculate_cost_ml(materials, year, m_num, temp)

        temp_factor = 1 + ((temp - 28) ** 2) * 0.002

        season_factor = {
            "Winter": 0.95,
            "Summer": 1.05,
            "Peak Summer": 1.08,
            "Monsoon": 1.10,
            "Pre-Monsoon": 1.06,
            "Post-Monsoon": 1.02
        }.get(season, 1)

        adjusted_total = res["total"] * temp_factor * season_factor

        noise = 1 + ((m_num % 5) - 2) * 0.01
        adjusted_total *= noise

        cost_lakh = round(adjusted_total / 100000, 2)

        costs.append(cost_lakh)
        details.append(res)

    # BEST MONTH (SMART)
    scores = []
    for i, m_num in enumerate(month_nums):
        row = df[df["month_num"] == m_num].iloc[0]
        temp = row["temperature"]
        season = row["season"]
        cost = costs[i]

        cost_score = (max(costs) - cost) * 1.5
        comfort_score = -abs(temp - 28) * 0.8

        season_penalty = {
            "Monsoon": -8,
            "Peak Summer": -5,
            "Summer": -2,
            "Pre-Monsoon": -1,
            "Post-Monsoon": 2,
            "Winter": 3
        }.get(season, 0)

        total_score = cost_score + comfort_score + season_penalty
        scores.append(total_score)

    best_index = scores.index(max(scores))
    best_month = months[best_index]

    duration = round(2 + (area * floors) / 1000 + floors * 0.5, 2)

    last = details[-1]

    return {
        "months": months,
        "costs": costs,
        "best_month": best_month,
        "duration": duration,

        "total_cost": float(costs[-1]),

        "materials": materials,

        "civil": {
            "material": int(last["civil_material"]),
            "labour": int(last["civil_labour"]),
            "total": int(last["civil_total"])
        },
        "electrical": {
            "material": int(last["electrical_material"]),
            "labour": int(last["electrical_labour"]),
            "total": int(last["electrical_total"])
        },
        "plumbing": {
            "material": int(last["plumbing_material"]),
            "labour": int(last["plumbing_labour"]),
            "total": int(last["plumbing_total"])
        },
        "tiles": {
            "material": int(last["tiles_material"]),
            "labour": int(last["tiles_labour"]),
            "total": int(last["tiles_total"])
        },
        "paint": {
            "material": int(last["paint_material"]),
            "labour": int(last["paint_labour"]),
            "total": int(last["paint_total"])
        }

    }