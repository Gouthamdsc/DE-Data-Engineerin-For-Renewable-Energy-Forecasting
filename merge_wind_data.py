import pandas as pd

# -----------------------------
# LOAD DATASETS
# -----------------------------

wind = pd.read_csv(
    "../Datasets/Wind Turbine Scada Dataset.csv"
)

weather = pd.read_csv(
    "../Datasets/weather_germany_final-checkpoint.csv",
    skiprows=13
)

# -----------------------------
# STANDARDIZE TIMESTAMP
# -----------------------------

wind["timestamp"] = pd.to_datetime(
    wind["Date/Time"],
    format="%d %m %Y %H:%M"
)

# -----------------------------
# KEEP IMPORTANT WEATHER COLUMNS
# -----------------------------

weather = weather[
    [
        "T2M",
        "RH2M",
        "WS2M",
        "ALLSKY_SFC_SW_DWN"
    ]
]

# -----------------------------
# MATCH LENGTHS
# -----------------------------

weather = weather.sample(
    n=len(wind),
    replace=True,
    random_state=42
).reset_index(drop=True)

wind = wind.reset_index(drop=True)

# -----------------------------
# COMBINE DATASETS
# -----------------------------

merged_wind = pd.concat(
    [wind, weather],
    axis=1
)

# -----------------------------
# SELECT IMPORTANT COLUMNS
# -----------------------------

merged_wind = merged_wind[
    [
        "timestamp",
        "LV ActivePower (kW)",
        "Wind Speed (m/s)",
        "Wind Direction (°)",
        "T2M",
        "RH2M",
        "WS2M",
        "ALLSKY_SFC_SW_DWN"
    ]
]

# -----------------------------
# SAVE DATASET
# -----------------------------

merged_wind.to_csv(
    "merged_wind_dataset.csv",
    index=False
)

# -----------------------------
# OUTPUT
# -----------------------------

print("\nMerged Wind Dataset Shape:")
print(merged_wind.shape)

print("\nFirst 5 Rows:")
print(merged_wind.head().to_string())