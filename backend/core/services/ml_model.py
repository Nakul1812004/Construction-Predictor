import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import joblib
import os

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "..", "data", "material_rates.csv")
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
RF_PATH = os.path.join(MODEL_DIR, "rf_model.pkl")
LR_PATH = os.path.join(MODEL_DIR, "lr_model.pkl")

def train_models():
    df = pd.read_csv(DATA_PATH)

    X = df[["year", "month_num", "temperature"]]

    y = df[[
        "cement_rate","steel_rate","sand_rate",
        "aggregate_rate","brick_rate",
        "paint_rate","paint_labour_rate",
        "electrical_material_rate",
        "plumbing_material_rate",
        "tiles_material_rate","tiles_labour_rate"
    ]]

    # 🔹 Random Forest (pattern)
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    rf.fit(X, y)

    # 🔹 Linear Regression (trend)
    lr = LinearRegression()
    lr.fit(X, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(rf, RF_PATH)
    joblib.dump(lr, LR_PATH)

    print("✅ RF + LR models trained and saved")

if __name__ == "__main__":
    train_models()