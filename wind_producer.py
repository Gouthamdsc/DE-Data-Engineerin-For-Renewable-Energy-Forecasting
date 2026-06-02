from kafka import KafkaProducer
import pandas as pd
import json
import time

# -----------------------------
# CONNECT TO KAFKA
# -----------------------------

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# -----------------------------
# LOAD DATASET
# -----------------------------

wind = pd.read_csv(
    "merged_wind_dataset.csv"
)

# -----------------------------
# STREAM DATA
# -----------------------------

print("Starting Wind Data Streaming...")

for index, row in wind.head(50).iterrows():

    data = row.to_dict()

    producer.send(
        'wind_topic',
        value=data
    )

    print(f"Sent Row {index + 1}")

    time.sleep(2)

print("Wind Streaming Completed!")