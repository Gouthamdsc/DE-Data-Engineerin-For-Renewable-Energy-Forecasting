from kafka import KafkaProducer
import pandas as pd
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

weather = pd.read_csv(
    "live_weather_data.csv"
)

print("Starting Weather Streaming...")

for index, row in weather.iterrows():

    producer.send(
        'weather_topic',
        value=row.to_dict()
    )

    print(f"Sent Weather Row {index + 1}")

    time.sleep(3)

print("Weather Streaming Completed!")