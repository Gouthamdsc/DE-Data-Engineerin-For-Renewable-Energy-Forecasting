import pandas as pd

# -----------------------------
# LOAD GRID DATASET
# -----------------------------

grid = pd.read_csv(
    "../Datasets/household_power_consumption.txt",
    sep=";",
    low_memory=False
)

# -----------------------------
# CREATE TIMESTAMP
# -----------------------------

grid["timestamp"] = pd.to_datetime(
    grid["Date"] + " " + grid["Time"],
    format="%d/%m/%Y %H:%M:%S",
    dayfirst=True,
    errors="coerce"
)

# -----------------------------
# CLEAN DATA
# -----------------------------

# Convert power column to numeric
grid["Global_active_power"] = pd.to_numeric(
    grid["Global_active_power"],
    errors="coerce"
)

# Remove missing values
grid = grid.dropna(
    subset=["timestamp", "Global_active_power"]
)

# -----------------------------
# KEEP IMPORTANT COLUMNS
# -----------------------------

grid_cleaned = grid[
    [
        "timestamp",
        "Global_active_power",
        "Voltage",
        "Global_intensity"
    ]
]

# Rename for project clarity
grid_cleaned.rename(
    columns={
        "Global_active_power": "grid_demand"
    },
    inplace=True
)

# -----------------------------
# SAVE DATASET
# -----------------------------

grid_cleaned.to_csv(
    "cleaned_grid_dataset.csv",
    index=False
)

# -----------------------------
# OUTPUT
# -----------------------------

print("\nCleaned Grid Dataset Shape:")
print(grid_cleaned.shape)

print("\nFirst 5 Rows:")
print(grid_cleaned.head().to_string())