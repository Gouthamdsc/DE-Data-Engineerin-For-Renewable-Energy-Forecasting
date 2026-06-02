import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading datasets...")

# Load cleaned datasets
solar_df = pd.read_csv("../Phase_2_Data_Preparation/cleaned_solar.csv")
wind_df = pd.read_csv("../Phase_2_Data_Preparation/cleaned_wind.csv")
grid_df = pd.read_csv("../Phase_2_Data_Preparation/cleaned_grid.csv")

print("Datasets loaded successfully!")

# ==================================================
# SOLAR ANALYSIS
# ==================================================

print("Generating Solar Plots...")

plt.figure(figsize=(8,5))
plt.hist(solar_df['DC_POWER'], bins=30)
plt.title("Solar DC Power Distribution")
plt.xlabel("DC Power")
plt.ylabel("Frequency")
plt.savefig("solar_power_distribution.png")
plt.close()

plt.figure(figsize=(8,5))
plt.scatter(
    solar_df['IRRADIATION'],
    solar_df['DC_POWER']
)
plt.title("Solar Irradiation vs DC Power")
plt.xlabel("Irradiation")
plt.ylabel("DC Power")
plt.savefig("solar_irradiation_vs_power.png")
plt.close()

# ==================================================
# WIND ANALYSIS
# ==================================================

print("Generating Wind Plots...")

plt.figure(figsize=(8,5))
plt.scatter(
    wind_df['Wind Speed (m/s)'],
    wind_df['LV ActivePower (kW)']
)
plt.title("Wind Speed vs Power Output")
plt.xlabel("Wind Speed")
plt.ylabel("Power Output")
plt.savefig("wind_speed_vs_power.png")
plt.close()

# ==================================================
# GRID ANALYSIS
# ==================================================

print("Generating Grid Plots...")

plt.figure(figsize=(8,5))
plt.plot(grid_df['grid_demand'].head(1000))
plt.title("Grid Demand Trend")
plt.xlabel("Time")
plt.ylabel("Grid Demand")
plt.savefig("grid_demand_trend.png")
plt.close()

# ==================================================
# HEATMAP
# ==================================================

print("Generating Correlation Heatmap...")

plt.figure(figsize=(10,6))
sns.heatmap(
    solar_df.select_dtypes(include=['number']).corr(),
    annot=False
)
plt.title("Solar Dataset Correlation Heatmap")
plt.savefig("solar_heatmap.png")
plt.close()

print("\nEDA Completed Successfully!")