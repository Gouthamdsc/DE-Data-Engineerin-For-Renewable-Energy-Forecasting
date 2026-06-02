from pyspark.sql import SparkSession
from pyspark.sql.functions import col, hour, dayofmonth, month
import pandas as pd

# Create Spark Session
spark = SparkSession.builder \
    .appName("RQ2_Preprocessing") \
    .getOrCreate()

print("Spark Started Successfully!")

# ==================================================
# SOLAR DATA
# ==================================================

solar_df = spark.read.csv(
    "cleaned_datasets/spark_cleaned_solar.csv",
    header=True,
    inferSchema=True
)

print("\nSolar Dataset Loaded")
print("Rows:", solar_df.count())

solar_df = solar_df.dropna()

solar_df = solar_df.withColumn(
    "hour", hour(col("timestamp"))
)

solar_df = solar_df.withColumn(
    "day", dayofmonth(col("timestamp"))
)

solar_df = solar_df.withColumn(
    "month", month(col("timestamp"))
)

print("Solar preprocessing completed!")

# Convert Spark → Pandas and save
solar_pd = solar_df.toPandas()
solar_pd.to_csv("cleaned_solar.csv", index=False)

print("Solar dataset saved successfully!")

# ==================================================
# WIND DATA
# ==================================================

wind_df = spark.read.csv(
    "cleaned_datasets/spark_cleaned_wind.csv",
    header=True,
    inferSchema=True
)

print("\nWind Dataset Loaded")
print("Rows:", wind_df.count())

wind_df = wind_df.dropna()

print("Wind preprocessing completed!")

wind_pd = wind_df.toPandas()
wind_pd.to_csv("cleaned_wind.csv", index=False)

print("Wind dataset saved successfully!")

# ==================================================
# GRID DATA
# ==================================================

grid_df = spark.read.csv(
    "cleaned_datasets/spark_cleaned_grid.csv",
    header=True,
    inferSchema=True
)

print("\nGrid Dataset Loaded")
print("Rows:", grid_df.count())

grid_df = grid_df.dropna()

print("Grid preprocessing completed!")

grid_pd = grid_df.toPandas()
grid_pd.to_csv("cleaned_grid.csv", index=False)

print("Grid dataset saved successfully!")

print("\nSpark Preprocessing Completed Successfully!")

spark.stop()