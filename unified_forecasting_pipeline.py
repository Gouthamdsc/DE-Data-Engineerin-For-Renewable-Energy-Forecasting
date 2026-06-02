import pandas as pd

# -----------------------------
# LOAD DATASETS
# -----------------------------

solar = pd.read_csv(
    "merged_solar_dataset.csv"
)

wind = pd.read_csv(
    "merged_wind_dataset.csv"
)

grid = pd.read_csv(
    "cleaned_grid_dataset.csv"
)

weather = pd.read_csv(
    "../Weather_API/live_weather_data.csv"
)

# -----------------------------
# ADD DATA SOURCE LABELS
# -----------------------------

solar["energy_type"] = "solar"
wind["energy_type"] = "wind"

# -----------------------------
# STANDARDIZE COLUMN NAMES
# -----------------------------

solar = solar.rename(
    columns={
        "DC_POWER": "energy_output"
    }
)

wind = wind.rename(
    columns={
        "LV ActivePower (kW)": "energy_output"
    }
)

# -----------------------------
# KEEP COMMON COLUMNS
# -----------------------------

solar_final = solar[
    [
        "timestamp",
        "energy_output",
        "AMBIENT_TEMPERATURE",
        "IRRADIATION",
        "energy_type"
    ]
]

wind_final = wind[
    [
        "timestamp",
        "energy_output",
        "T2M",
        "ALLSKY_SFC_SW_DWN",
        "energy_type"
    ]
]

# Rename for consistency
solar_final.columns = [
    "timestamp",
    "energy_output",
    "temperature",
    "irradiation",
    "energy_type"
]

wind_final.columns = [
    "timestamp",
    "energy_output",
    "temperature",
    "irradiation",
    "energy_type"
]

# -----------------------------
# COMBINE SOLAR + WIND
# -----------------------------

renewable_data = pd.concat(
    [solar_final, wind_final],
    ignore_index=True
)

# -----------------------------
# SAVE FINAL DATASET
# -----------------------------

renewable_data.to_csv(
    "unified_renewable_dataset.csv",
    index=False
)

# -----------------------------
# OUTPUT
# -----------------------------

print("\nUnified Dataset Shape:")
print(renewable_data.shape)

print("\nFirst 5 Rows:")
print(renewable_data.head().to_string())