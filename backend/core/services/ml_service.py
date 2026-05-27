import os
import joblib
import numpy as np
import math
BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

RF_PATH = os.path.join(MODEL_DIR, "rf_model.pkl")
LR_PATH = os.path.join(MODEL_DIR, "lr_model.pkl")

DATA_PATH = os.path.join(BASE_DIR, "..", "..", "data", "material_rates.csv")


_rf = None
_lr = None
_inflation = None


def load_models():
    global _rf, _lr
    if _rf is None:
        if not os.path.exists(RF_PATH) or not os.path.exists(LR_PATH):
            raise FileNotFoundError("Models not found. Run ml_model.py first.")
        _rf = joblib.load(RF_PATH)
        _lr = joblib.load(LR_PATH)
    return _rf, _lr


def get_inflation_rate():
    global _inflation

    if _inflation is not None:
        return _inflation

    import pandas as pd

    df = pd.read_csv(DATA_PATH)

    yearly = df.groupby("year")["cement_rate"].mean()

    growth_rates = []
    years = sorted(yearly.index)

    for i in range(1, len(years)):
        prev = yearly[years[i-1]]
        curr = yearly[years[i]]

        growth = (curr - prev) / prev
        growth_rates.append(growth)

    _inflation = sum(growth_rates) / len(growth_rates)
    return _inflation

def get_min_rates():
    import pandas as pd

    df = pd.read_csv(DATA_PATH)

    return {
        "cement_rate": df["cement_rate"].min(),
        "steel_rate": df["steel_rate"].min(),
        "sand_rate": df["sand_rate"].min(),
        "aggregate_rate": df["aggregate_rate"].min(),
        "brick_rate": df["brick_rate"].min(),
        "paint_rate": df["paint_rate"].min(),
        "paint_labour_rate": df["paint_labour_rate"].min(),
        "electrical_material_rate": df["electrical_material_rate"].min(),
        "plumbing_material_rate": df["plumbing_material_rate"].min(),
        "tiles_material_rate": df["tiles_material_rate"].min(),
        "tiles_labour_rate": df["tiles_labour_rate"].min()
    }

def predict_rates(year, month_num, temperature):
    rf, lr = load_models()

    X = [[year, month_num, temperature]]

    rf_pred = rf.predict(X)[0]
    lr_pred = lr.predict(X)[0]

    # HYBRID MODEL
    final = np.maximum(rf_pred, lr_pred)

    keys = [
        "cement_rate","steel_rate","sand_rate",
        "aggregate_rate","brick_rate",
        "paint_rate","paint_labour_rate",
        "electrical_material_rate",
        "plumbing_material_rate",
        "tiles_material_rate","tiles_labour_rate"
    ]

    rates = {k: float(v) for k, v in zip(keys, final)}
    min_rates = get_min_rates()

    for k in rates:
        rates[k] = max(rates[k], min_rates[k])
    # 🔥 AUTO INFLATION
    base_year = 2025
    if year > base_year:
        inflation = get_inflation_rate()
        factor = (1 + inflation + 0.02) ** (year - base_year)

        for k in rates:
            rates[k] *= factor

    #  MONTH VARIATION
    seasonal_variation = 1 + 0.12 * math.sin((month_num / 12) * 2 * math.pi)


    year_factor = 1 + 0.02 * (year - 2025)

    for k in rates:
        rates[k] *= seasonal_variation * year_factor

    return rates