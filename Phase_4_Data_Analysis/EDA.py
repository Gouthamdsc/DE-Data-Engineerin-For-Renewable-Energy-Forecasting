import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# Create Output Folder
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "Phase_3_Spark_Preprocessing",
    "output"
)

OUTPUT_PATH = os.path.join(BASE_DIR, "EDA_Output")

os.makedirs(OUTPUT_PATH, exist_ok=True)

print("=" * 60)
print("Loading Processed Datasets...")
print("=" * 60)

print("Dataset Path:", DATA_PATH)

# =====================================================
# Load Datasets
# =====================================================

solar_df = pd.read_csv(os.path.join(DATA_PATH, "solar_processed.csv"))
wind_df = pd.read_csv(os.path.join(DATA_PATH, "wind_processed.csv"))
grid_df = pd.read_csv(os.path.join(DATA_PATH, "household_processed.csv"))
daily_df = pd.read_csv(os.path.join(DATA_PATH, "daily_solar_generation.csv"))

print("Solar Shape :", solar_df.shape)
print("Wind Shape  :", wind_df.shape)
print("Grid Shape  :", grid_df.shape)
print("Daily Shape :", daily_df.shape)

# =====================================================
# Solar Dataset
# =====================================================

print("\nGenerating Solar Dataset Visualizations...")

numeric = solar_df.select_dtypes(include="number").columns

if "DC_POWER" in solar_df.columns:

    plt.figure(figsize=(8,5))
    plt.hist(solar_df["DC_POWER"], bins=30)
    plt.title("Solar DC Power Distribution")
    plt.xlabel("DC Power")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH,"solar_dc_power_distribution.png"))
    plt.close()

if "IRRADIATION" in solar_df.columns and "DC_POWER" in solar_df.columns:

    plt.figure(figsize=(8,5))
    plt.scatter(
        solar_df["IRRADIATION"],
        solar_df["DC_POWER"],
        s=8
    )
    plt.title("Solar Irradiation vs DC Power")
    plt.xlabel("Irradiation")
    plt.ylabel("DC Power")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH,"solar_irradiation_vs_power.png"))
    plt.close()

plt.figure(figsize=(10,8))
sns.heatmap(
    solar_df[numeric].corr(),
    cmap="coolwarm"
)
plt.title("Solar Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH,"solar_heatmap.png"))
plt.close()

# =====================================================
# Daily Solar Generation
# =====================================================

print("Generating Daily Solar Generation Plot...")

if daily_df.shape[1] >= 2:

    plt.figure(figsize=(12,5))
    plt.plot(
        daily_df.iloc[:,0],
        daily_df.iloc[:,1]
    )

    plt.xticks(rotation=45)

    plt.title("Daily Solar Generation")
    plt.xlabel("Date")
    plt.ylabel("Generation")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH,"daily_solar_generation.png"))
    plt.close()

# =====================================================
# Wind Dataset
# =====================================================

print("Generating Wind Dataset Visualizations...")

if "Wind Speed (m/s)" in wind_df.columns and "LV ActivePower (kW)" in wind_df.columns:

    plt.figure(figsize=(8,5))
    plt.scatter(
        wind_df["Wind Speed (m/s)"],
        wind_df["LV ActivePower (kW)"],
        s=8
    )

    plt.title("Wind Speed vs Power Output")
    plt.xlabel("Wind Speed")
    plt.ylabel("Power Output")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH,"wind_speed_vs_power.png"))
    plt.close()

wind_numeric = wind_df.select_dtypes(include="number")

plt.figure(figsize=(10,8))
sns.heatmap(
    wind_numeric.corr(),
    cmap="viridis"
)
plt.title("Wind Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH,"wind_heatmap.png"))
plt.close()

# =====================================================
# Household Dataset
# =====================================================

print("Generating Household Dataset Visualizations...")

if "global_active_power" in grid_df.columns:

    plt.figure(figsize=(12,5))
    plt.plot(grid_df["global_active_power"].head(1000))
    plt.title("Global Active Power Trend")
    plt.xlabel("Samples")
    plt.ylabel("Global Active Power")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH,"global_active_power_trend.png"))
    plt.close()

if "voltage" in grid_df.columns:

    plt.figure(figsize=(8,5))
    plt.hist(grid_df["voltage"], bins=40)
    plt.title("Voltage Distribution")
    plt.xlabel("Voltage")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH,"voltage_distribution.png"))
    plt.close()

grid_numeric = grid_df.select_dtypes(include="number")

plt.figure(figsize=(10,8))
sns.heatmap(
    grid_numeric.corr(),
    cmap="rocket"
)
plt.title("Household Power Correlation Heatmap")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH,"household_heatmap.png"))
plt.close()

# =====================================================
# Dataset Information
# =====================================================

print("\nSaving Dataset Summary...")

with open(os.path.join(OUTPUT_PATH,"dataset_summary.txt"),"w") as f:

    f.write("SOLAR DATASET\n")
    f.write(str(solar_df.describe()))
    f.write("\n\n")

    f.write("WIND DATASET\n")
    f.write(str(wind_df.describe()))
    f.write("\n\n")

    f.write("HOUSEHOLD DATASET\n")
    f.write(str(grid_df.describe()))

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Output Folder:")
print(OUTPUT_PATH)