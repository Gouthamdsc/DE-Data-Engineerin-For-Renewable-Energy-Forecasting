import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "Phase_3_Spark_Preprocessing",
    "output"
)

OUTPUT_PATH = os.path.join(BASE_DIR, "ML_Output")
os.makedirs(OUTPUT_PATH, exist_ok=True)

print("="*60)
print("Loading Processed Datasets...")
print("="*60)

solar_df = pd.read_csv(os.path.join(DATA_PATH, "solar_processed.csv"))
wind_df = pd.read_csv(os.path.join(DATA_PATH, "wind_processed.csv"))

print("Solar Shape :", solar_df.shape)
print("Wind Shape  :", wind_df.shape)

# =====================================================
# SOLAR MODEL
# =====================================================

print("\nTraining Solar Model...")

solar_features = [
    "IRRADIATION",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "hour",
    "day_of_week",
    "month",
    "year"

]

solar_target = "DC_POWER"

solar_df = solar_df.dropna(subset=solar_features+[solar_target])

X = solar_df[solar_features]
y = solar_df[solar_target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

solar_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

solar_model.fit(X_train, y_train)

solar_predictions = solar_model.predict(X_test)

solar_mae = mean_absolute_error(y_test, solar_predictions)
solar_rmse = mean_squared_error(
    y_test,
    solar_predictions
) ** 0.5
solar_r2 = r2_score(y_test, solar_predictions)

print("\n===== SOLAR MODEL =====")
print("MAE :", round(solar_mae,2))
print("RMSE:", round(solar_rmse,2))
print("R²  :", round(solar_r2,4))

plt.figure(figsize=(8,6))
plt.scatter(
    y_test[:500],
    solar_predictions[:500],
    alpha=0.6
)
plt.xlabel("Actual DC Power")
plt.ylabel("Predicted DC Power")
plt.title("Solar Power Prediction")
plt.tight_layout()
plt.savefig(os.path.join(
    OUTPUT_PATH,
    "solar_prediction_results.png"
))
plt.close()

joblib.dump(
    solar_model,
    os.path.join(OUTPUT_PATH,"solar_model.pkl")
)

# =====================================================
# WIND MODEL
# =====================================================

print("\nTraining Wind Model...")

wind_features = [
    "Wind Speed (m/s)",
    "Wind Direction (°)",
    "Theoretical_Power_Curve (KWh)"
]

wind_target = "LV ActivePower (kW)"

wind_df = wind_df.dropna(subset=wind_features+[wind_target])

X = wind_df[wind_features]
y = wind_df[wind_target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

wind_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

wind_model.fit(X_train, y_train)

wind_predictions = wind_model.predict(X_test)

wind_mae = mean_absolute_error(y_test, wind_predictions)
wind_rmse = mean_squared_error(
    y_test,
    wind_predictions
) ** 0.5
wind_r2 = r2_score(y_test, wind_predictions)

print("\n===== WIND MODEL =====")
print("MAE :", round(wind_mae,2))
print("RMSE:", round(wind_rmse,2))
print("R²  :", round(wind_r2,4))

plt.figure(figsize=(8,6))
plt.scatter(
    y_test[:500],
    wind_predictions[:500],
    alpha=0.6
)
plt.xlabel("Actual Wind Power")
plt.ylabel("Predicted Wind Power")
plt.title("Wind Power Prediction")
plt.tight_layout()
plt.savefig(os.path.join(
    OUTPUT_PATH,
    "wind_prediction_results.png"
))
plt.close()

joblib.dump(
    wind_model,
    os.path.join(OUTPUT_PATH,"wind_model.pkl")
)

# =====================================================
# SAVE METRICS
# =====================================================

with open(os.path.join(
    OUTPUT_PATH,
    "model_metrics.txt"
),"w") as f:

    f.write("SOLAR MODEL\n")
    f.write("--------------------------\n")
    f.write(f"MAE  : {solar_mae:.2f}\n")
    f.write(f"RMSE : {solar_rmse:.2f}\n")
    f.write(f"R2   : {solar_r2:.4f}\n\n")

    f.write("WIND MODEL\n")
    f.write("--------------------------\n")
    f.write(f"MAE  : {wind_mae:.2f}\n")
    f.write(f"RMSE : {wind_rmse:.2f}\n")
    f.write(f"R2   : {wind_r2:.4f}\n")

print("\n"+"="*60)
print("MACHINE LEARNING COMPLETED SUCCESSFULLY")
print("="*60)

print("\nOutput Folder:")
print(OUTPUT_PATH)