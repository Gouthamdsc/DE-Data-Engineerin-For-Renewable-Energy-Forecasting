import pandas as pd

# -----------------------------
# LOAD DATASETS
# -----------------------------

solar_gen = pd.read_csv(
    "../Datasets/Solar Power Generation Data/Plant_1_Generation_Data.csv"
)

solar_weather = pd.read_csv(
    "../Datasets/Solar Power Generation Data/Plant_1_Weather_Sensor_Data.csv"
)

# -----------------------------
# STANDARDIZE TIMESTAMP
# -----------------------------

solar_gen["timestamp"] = pd.to_datetime(
    solar_gen["DATE_TIME"],
    format="%d-%m-%Y %H:%M",
    dayfirst=True
)

solar_weather["timestamp"] = pd.to_datetime(
    solar_weather["DATE_TIME"]
)

# -----------------------------
# MERGE DATASETS
# -----------------------------

merged_solar = pd.merge(
    solar_gen,
    solar_weather,
    on=["timestamp", "PLANT_ID"],
    how="inner"
)

# -----------------------------
# SELECT IMPORTANT COLUMNS
# -----------------------------

merged_solar = merged_solar[
    [
        "timestamp",
        "PLANT_ID",
        "DC_POWER",
        "AC_POWER",
        "DAILY_YIELD",
        "AMBIENT_TEMPERATURE",
        "MODULE_TEMPERATURE",
        "IRRADIATION"
    ]
]

# -----------------------------
# SAVE DATASET
# -----------------------------

merged_solar.to_csv(
    "merged_solar_dataset.csv",
    index=False
)

print("\nMerged Dataset Shape:")
print(merged_solar.shape)

print("\nFirst 5 Rows:")
print("\nTimestamp Sample:")
print(merged_solar["timestamp"].iloc[0:50].tolist())