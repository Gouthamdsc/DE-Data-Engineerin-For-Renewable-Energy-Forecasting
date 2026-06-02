from kafka import KafkaProducer
import pandas as pd
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

grid = pd.read_csv(
    "cleaned_grid_dataset.csv"
)

print("Starting Grid Streaming...")

for index, row in grid.head(50).iterrows():

    producer.send(
        'grid_topic',
        value=row.to_dict()
    )

    print(f"Sent Row {index + 1}")

    time.sleep(2)

print("Grid Streaming Completed!")