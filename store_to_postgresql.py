from sqlalchemy import create_engine
import pandas as pd

# -----------------------------
# DATABASE CONNECTION
# -----------------------------

username = "postgres"
password = "postgres123"   # change if different
host = "localhost"
port = "5432"
database = "renewable_energy_db"

engine = create_engine(
    f"postgresql://{username}:{password}@{host}:{port}/{database}"
)

print("Database Connected Successfully!")

# -----------------------------
# LOAD DATASETS
# -----------------------------

solar = pd.read_csv(
    "../Data_Integration/merged_solar_dataset.csv"
)

wind = pd.read_csv(
    "../Data_Integration/merged_wind_dataset.csv"
)

grid = pd.read_csv(
    "../Data_Integration/cleaned_grid_dataset.csv"
)

weather = pd.read_csv(
    "../Weather_API/live_weather_data.csv"
)

# -----------------------------
# STORE INTO POSTGRESQL
# -----------------------------

solar.to_sql(
    "solar_data",
    engine,
    if_exists="replace",
    index=False
)

print("Solar Data Stored!")

wind.to_sql(
    "wind_data",
    engine,
    if_exists="replace",
    index=False
)

print("Wind Data Stored!")

grid.to_sql(
    "grid_data",
    engine,
    if_exists="replace",
    index=False
)

print("Grid Data Stored!")

weather.to_sql(
    "weather_data",
    engine,
    if_exists="replace",
    index=False
)

print("Weather Data Stored!")

print("\nAll Data Stored Successfully!")