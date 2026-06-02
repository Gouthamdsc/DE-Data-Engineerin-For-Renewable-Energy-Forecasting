import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# ==================================================
# SOLAR MODEL
# ==================================================

print("Loading Solar Dataset...")

solar_df = pd.read_csv("../Phase_2_Data_Preparation/cleaned_solar.csv")

solar_features = [
    'IRRADIATION',
    'AMBIENT_TEMPERATURE',
    'MODULE_TEMPERATURE',
    'hour',
    'day',
    'month'
]

solar_target = 'DC_POWER'

X = solar_df[solar_features]
y = solar_df[solar_target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
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

solar_r2 = r2_score(
    y_test,
    solar_predictions
)

print("\n===== SOLAR MODEL =====")
print("MAE:", round(solar_mae, 2))
print("RMSE:", round(solar_rmse, 2))
print("R2 Score:", round(solar_r2, 4))

plt.figure(figsize=(8,5))
plt.scatter(y_test[:500], solar_predictions[:500])
plt.xlabel("Actual Solar Power")
plt.ylabel("Predicted Solar Power")
plt.title("Solar Power Prediction")
plt.savefig("solar_prediction_results.png")
plt.close()

# ==================================================
# WIND MODEL
# ==================================================

print("\nLoading Wind Dataset...")

wind_df = pd.read_csv("../Phase_2_Data_Preparation/cleaned_wind.csv")

wind_features = [
    'Wind Speed (m/s)',
    'Wind Direction (°)',
    'T2M',
    'RH2M',
    'WS2M'
]

wind_target = 'LV ActivePower (kW)'

X = wind_df[wind_features]
y = wind_df[wind_target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

wind_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

wind_model.fit(X_train, y_train)

wind_predictions = wind_model.predict(X_test)

wind_mae = mean_absolute_error(
    y_test,
    wind_predictions
)

wind_rmse = mean_squared_error(
    y_test,
    wind_predictions
) ** 0.5

wind_r2 = r2_score(
    y_test,
    wind_predictions
)

print("\n===== WIND MODEL =====")
print("MAE:", round(wind_mae, 2))
print("RMSE:", round(wind_rmse, 2))
print("R2 Score:", round(wind_r2, 4))

plt.figure(figsize=(8,5))
plt.scatter(y_test[:500], wind_predictions[:500])
plt.xlabel("Actual Wind Power")
plt.ylabel("Predicted Wind Power")
plt.title("Wind Power Prediction")
plt.savefig("wind_prediction_results.png")
plt.close()

print("\nModeling Completed Successfully!")