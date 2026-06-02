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
# LOAD SOLAR DATASET
# -----------------------------

solar = pd.read_csv(
    "merged_solar_dataset.csv"
)

# -----------------------------
# STREAM DATA
# -----------------------------

print("Starting Solar Data Streaming...")

for index, row in solar.head(50).iterrows():

    data = row.to_dict()

    producer.send(
        'solar_topic',
        value=data
    )

    print(f"Sent Row {index + 1}")

    # Simulate sensor delay
    time.sleep(2)

print("Streaming Completed!")