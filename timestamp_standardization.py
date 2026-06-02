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

wind = pd.read_csv(
    "../Datasets/Wind Turbine Scada Dataset.csv"
)

grid = pd.read_csv(
    "../Datasets/household_power_consumption.txt",
    sep=";",
    low_memory=False
)

weather = pd.read_csv(
    "../Datasets/weather_germany_final-checkpoint.csv",
    skiprows=13
)

# -----------------------------
# STANDARDIZE TIMESTAMPS
# -----------------------------

# Solar Generation
solar_gen["timestamp"] = pd.to_datetime(
    solar_gen["DATE_TIME"],
    format="%d-%m-%Y %H:%M",
    dayfirst=True
)

# Solar Weather
solar_weather["timestamp"] = pd.to_datetime(
    solar_weather["DATE_TIME"],
    format="%Y-%m-%d %H:%M:%S"
)

# Wind
wind["timestamp"] = pd.to_datetime(
    wind["Date/Time"],
    format="%d %m %Y %H:%M"
)

# Grid
grid["timestamp"] = pd.to_datetime(
    grid["Date"] + " " + grid["Time"],
    format="%d/%m/%Y %H:%M:%S",
    dayfirst=True,
    errors="coerce"
)

# Weather Germany
weather["timestamp"] = pd.to_datetime(
    weather[["YEAR", "MO", "DY"]]
    .rename(
        columns={
            "YEAR": "year",
            "MO": "month",
            "DY": "day"
        }
    )
)

# -----------------------------
# CHECK RESULTS
# -----------------------------

# -----------------------------
# CHECK RESULTS
# -----------------------------

print("\nSolar Timestamp:")
print(solar_gen["timestamp"].head(20).to_string())

print("\nSolar Weather Timestamp:")
print(solar_weather["timestamp"].head(20).to_string())

print("\nWind Timestamp:")
print(wind["timestamp"].head())

print("\nGrid Timestamp:")
print(grid["timestamp"].head())

print("\nWeather Timestamp:")
print(weather["timestamp"].head())