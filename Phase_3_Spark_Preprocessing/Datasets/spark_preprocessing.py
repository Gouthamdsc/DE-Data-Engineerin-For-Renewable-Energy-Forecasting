from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# =====================================================
# CREATE SPARK SESSION
# =====================================================

spark = SparkSession.builder \
    .appName("RenewableEnergyForecasting") \
    .master("local[*]") \
    .config("spark.sql.ansi.enabled", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("=" * 50)
print("SPARK STARTED SUCCESSFULLY")
print("=" * 50)

# =====================================================
# FILE PATHS
# =====================================================

PLANT1_GEN = r"C:\Users\Goutham\Downloads\Datasets\Solar Power Generation Data\Plant_1_Generation_Data.csv"

PLANT1_WEATHER = r"C:\Users\Goutham\Downloads\Datasets\Solar Power Generation Data\Plant_1_Weather_Sensor_Data.csv"

PLANT2_GEN = r"C:\Users\Goutham\Downloads\Datasets\Solar Power Generation Data\Plant_2_Generation_Data.csv"

PLANT2_WEATHER = r"C:\Users\Goutham\Downloads\Datasets\Solar Power Generation Data\Plant_2_Weather_Sensor_Data.csv"

WIND_DATA = r"C:\Users\Goutham\Downloads\Datasets\Wind Turbine Scada Dataset.csv"

HOUSEHOLD_DATA = r"C:\Users\Goutham\Downloads\Datasets\household_power_consumption.txt"

# =====================================================
# LOAD DATASETS
# =====================================================

print("\nLoading Solar Datasets...")

plant1_gen = spark.read.option("header", True).csv(PLANT1_GEN)

plant1_weather = spark.read.option("header", True).csv(PLANT1_WEATHER)

plant2_gen = spark.read.option("header", True).csv(PLANT2_GEN)

plant2_weather = spark.read.option("header", True).csv(PLANT2_WEATHER)

print("Loading Wind Dataset...")

wind_df = spark.read.option("header", True).csv(WIND_DATA)

print("Loading Household Dataset...")

house_df = spark.read \
    .option("header", True) \
    .option("sep", ";") \
    .csv(HOUSEHOLD_DATA)

# =====================================================
# DATASET COUNTS
# =====================================================

print("\nDataset Statistics")

print("Plant1 Generation :", plant1_gen.count())
print("Plant1 Weather    :", plant1_weather.count())

print("Plant2 Generation :", plant2_gen.count())
print("Plant2 Weather    :", plant2_weather.count())

print("Wind Records      :", wind_df.count())
print("Household Records :", house_df.count())

# =====================================================
# CLEAN DATA
# =====================================================

print("\nCleaning Data...")

plant1_gen = plant1_gen.dropDuplicates().na.drop()
plant1_weather = plant1_weather.dropDuplicates().na.drop()

plant2_gen = plant2_gen.dropDuplicates().na.drop()
plant2_weather = plant2_weather.dropDuplicates().na.drop()

wind_df = wind_df.dropDuplicates().na.drop()
house_df = house_df.dropDuplicates().na.drop()

# =====================================================
# FIX SOLAR JOIN
# =====================================================

print("\nJoining Solar Datasets...")

plant1_weather = plant1_weather.drop("SOURCE_KEY")
plant2_weather = plant2_weather.drop("SOURCE_KEY")

solar1 = plant1_gen.join(
    plant1_weather,
    on=["DATE_TIME", "PLANT_ID"],
    how="left"
)

solar2 = plant2_gen.join(
    plant2_weather,
    on=["DATE_TIME", "PLANT_ID"],
    how="left"
)

solar_df = solar1.unionByName(
    solar2,
    allowMissingColumns=True
)

print("Combined Solar Records:", solar_df.count())

# =====================================================
# VERIFY SCHEMA
# =====================================================

print("\nSolar Schema")

solar_df.printSchema()

# =====================================================
# TIMESTAMP CONVERSION
# =====================================================

print("\nProcessing Timestamp...")

solar_df = solar_df.withColumn(
    "DATE_TIME",
    expr("try_to_timestamp(DATE_TIME)")
)

solar_df = solar_df.filter(
    col("DATE_TIME").isNotNull()
)

# =====================================================
# FEATURE ENGINEERING
# =====================================================

print("\nCreating Features...")

solar_df = solar_df.withColumn(
    "hour",
    hour("DATE_TIME")
)

solar_df = solar_df.withColumn(
    "day_of_week",
    dayofweek("DATE_TIME")
)

solar_df = solar_df.withColumn(
    "month",
    month("DATE_TIME")
)

solar_df = solar_df.withColumn(
    "year",
    year("DATE_TIME")
)

print("Feature Engineering Completed")

# =====================================================
# NUMERIC COLUMN CASTING
# =====================================================

numeric_cols = [
    "DC_POWER",
    "AC_POWER",
    "DAILY_YIELD",
    "TOTAL_YIELD",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION"
]

for c in numeric_cols:

    if c in solar_df.columns:

        solar_df = solar_df.withColumn(
            c,
            col(c).cast("double")
        )

# =====================================================
# WIND DATA CLEANING
# =====================================================

print("\nCleaning Wind Dataset...")

for c in wind_df.columns:

    wind_df = wind_df.withColumn(
        c,
        regexp_replace(
            col(c),
            ",",
            "."
        )
    )

# =====================================================
# HOUSEHOLD DATA CLEANING
# =====================================================

print("\nCleaning Household Dataset...")

if "Global_active_power" in house_df.columns:

    house_df = house_df.withColumn(
        "Global_active_power",
        regexp_replace(
            col("Global_active_power"),
            "\\?",
            ""
        )
    )

    house_df = house_df.withColumn(
        "Global_active_power",
        col("Global_active_power").cast("double")
    )

# =====================================================
# QUALITY CHECKS
# =====================================================

print("\nRunning Quality Checks...")

null_report = solar_df.select([
    count(
        when(
            col(c).isNull(),
            c
        )
    ).alias(c)
    for c in solar_df.columns
])

null_report.show(truncate=False)

duplicates = (
    solar_df.count()
    -
    solar_df.dropDuplicates().count()
)

print("Duplicate Records:", duplicates)

# =====================================================
# DAILY SOLAR AGGREGATION
# =====================================================

print("\nCreating Daily Solar Aggregation...")

daily_solar = solar_df.groupBy(
    to_date("DATE_TIME").alias("date")
).agg(
    sum("DC_POWER").alias("daily_dc_power"),
    sum("AC_POWER").alias("daily_ac_power"),
    avg("IRRADIATION").alias("avg_irradiation"),
    avg("AMBIENT_TEMPERATURE").alias("avg_temperature")
)

daily_solar.show(10)

# =====================================================
# HOUSEHOLD STATS
# =====================================================

if "Global_active_power" in house_df.columns:

    print("\nHousehold Statistics")

    household_stats = house_df.groupBy().agg(
        avg("Global_active_power").alias(
            "avg_power"
        ),
        max("Global_active_power").alias(
            "max_power"
        ),
        min("Global_active_power").alias(
            "min_power"
        )
    )

    household_stats.show()

# =====================================================
# SAVE OUTPUTS AS CSV
# =====================================================

print("\nSaving Output Files...")

import os

os.makedirs("output", exist_ok=True)

solar_df.limit(100000).toPandas().to_csv(
    "output/solar_processed.csv",
    index=False
)

wind_df.limit(100000).toPandas().to_csv(
    "output/wind_processed.csv",
    index=False
)

house_df.limit(100000).toPandas().to_csv(
    "output/household_processed.csv",
    index=False
)

daily_solar.toPandas().to_csv(
    "output/daily_solar_generation.csv",
    index=False
)

print("\n" + "=" * 50)
print("PREPROCESSING COMPLETED SUCCESSFULLY")
print("=" * 50)

#spark.stop()


print("spark running")