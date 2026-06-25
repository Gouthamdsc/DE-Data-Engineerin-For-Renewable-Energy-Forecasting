import os
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("Loading Processed Datasets...")
print("=" * 60)

# =====================================================
# Paths
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "Phase_3_Spark_Preprocessing",
    "output"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "dashboard_figures"
)

os.makedirs(OUTPUT_PATH, exist_ok=True)

# =====================================================
# Load datasets
# =====================================================

solar_df = pd.read_csv(
    os.path.join(DATA_PATH, "solar_processed.csv")
)

wind_df = pd.read_csv(
    os.path.join(DATA_PATH, "wind_processed.csv")
)

grid_df = pd.read_csv(
    os.path.join(DATA_PATH, "household_processed.csv")
)

print("Solar Shape :", solar_df.shape)
print("Wind Shape  :", wind_df.shape)
print("Grid Shape  :", grid_df.shape)

# =====================================================
# SOLAR POWER TREND
# =====================================================

print("\nGenerating Solar Trend...")

plt.figure(figsize=(12,5))

plt.plot(
    solar_df["DC_POWER"].head(1000),
    color="orange"
)

plt.title("Solar Power Generation Trend")
plt.xlabel("Samples")
plt.ylabel("DC Power")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_PATH,
        "solar_power_trend.png"
    )
)

plt.close()

# =====================================================
# WIND POWER TREND
# =====================================================

print("Generating Wind Trend...")

plt.figure(figsize=(12,5))

plt.plot(
    wind_df["LV ActivePower (kW)"].head(1000),
    color="green"
)

plt.title("Wind Power Generation Trend")
plt.xlabel("Samples")
plt.ylabel("Power Output (kW)")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_PATH,
        "wind_power_trend.png"
    )
)

plt.close()

# =====================================================
# GRID POWER CONSUMPTION TREND
# =====================================================

print("Generating Grid Trend...")

# Combine Date and Time into one datetime column
grid_df["DateTime"] = pd.to_datetime(
    grid_df["Date"] + " " + grid_df["Time"]
)

plt.figure(figsize=(12,5))

plt.plot(
    grid_df["DateTime"].head(1000),
    grid_df["Global_active_power"].head(1000),
    color="blue"
)

plt.title("Household Grid Power Consumption")
plt.xlabel("Date & Time")
plt.ylabel("Global Active Power")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_PATH,
        "grid_consumption_trend.png"
    )
)

plt.close()

# =====================================================
# SOLAR vs WIND COMPARISON
# =====================================================

print("Generating Solar vs Wind Comparison...")

plt.figure(figsize=(12,5))

plt.plot(
    solar_df["DC_POWER"].head(300).reset_index(drop=True),
    label="Solar",
    color="orange"
)

plt.plot(
    wind_df["LV ActivePower (kW)"].head(300).reset_index(drop=True),
    label="Wind",
    color="green"
)

plt.title("Solar vs Wind Power Comparison")
plt.xlabel("Samples")
plt.ylabel("Power Output")

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_PATH,
        "solar_vs_wind_comparison.png"
    )
)

plt.close()

# =====================================================
# DAILY SOLAR GENERATION
# =====================================================

daily_file = os.path.join(
    DATA_PATH,
    "daily_solar_generation.csv"
)

if os.path.exists(daily_file):

    print("Generating Daily Solar Generation...")

    daily_df = pd.read_csv(daily_file)

    plt.figure(figsize=(12,5))

    if len(daily_df.columns) >= 2:

        plt.plot(
            daily_df.iloc[:, 1],
            marker="o",
            color="red"
        )

        plt.title("Daily Solar Generation")
        plt.xlabel("Days")
        plt.ylabel("Energy Generated")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                OUTPUT_PATH,
                "daily_solar_generation.png"
            )
        )

        plt.close()

# =====================================================
# SOLAR POWER DISTRIBUTION
# =====================================================

print("Generating Solar Distribution...")

plt.figure(figsize=(10,5))

plt.hist(
    solar_df["DC_POWER"],
    bins=30,
    color="gold",
    edgecolor="black"
)

plt.title("Distribution of Solar DC Power")
plt.xlabel("DC Power")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_PATH,
        "solar_distribution.png"
    )
)

plt.close()

# =====================================================
# WIND POWER DISTRIBUTION
# =====================================================

print("Generating Wind Distribution...")

plt.figure(figsize=(10,5))

plt.hist(
    wind_df["LV ActivePower (kW)"],
    bins=30,
    color="skyblue",
    edgecolor="black"
)

plt.title("Distribution of Wind Power")
plt.xlabel("Wind Power (kW)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_PATH,
        "wind_distribution.png"
    )
)

plt.close()

# =====================================================
# GRID POWER DISTRIBUTION
# =====================================================

print("Generating Grid Distribution...")

plt.figure(figsize=(10,5))

plt.hist(
    grid_df["Global_active_power"],
    bins=30,
    color="purple",
    edgecolor="black"
)

plt.title("Distribution of Household Power Consumption")
plt.xlabel("Global Active Power")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_PATH,
        "grid_distribution.png"
    )
)

plt.close()

print("\n" + "=" * 60)
print("Dashboard Visualizations Generated Successfully!")
print("Figures saved in:")
print(OUTPUT_PATH)
print("=" * 60)