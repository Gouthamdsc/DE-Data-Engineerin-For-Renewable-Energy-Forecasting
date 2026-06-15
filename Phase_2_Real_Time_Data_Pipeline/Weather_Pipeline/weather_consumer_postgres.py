from kafka import KafkaConsumer
import psycopg2
import json
from datetime import datetime

# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres123"   # change if your password is different
)

cursor = conn.cursor()

# Kafka Consumer
consumer = KafkaConsumer(
    'weather_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='weather-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Weather Consumer Started...")

for message in consumer:
    try:
        data = message.value

        print("Received Data:", data)

        # Extract weather values
        current = data.get("current", {})

        temperature = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wind_speed = current.get("wind_speed_10m")

        # Time conversion
        weather_time = current.get("time")

        if weather_time:
            weather_time = datetime.fromisoformat(weather_time)

        # Insert into PostgreSQL
        insert_query = """
        INSERT INTO weather_data (
            city,
            temperature,
            humidity,
            wind_speed,
            weather_time
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            "Berlin",
            temperature,
            humidity,
            wind_speed,
            weather_time
        ))

        conn.commit()

        print("Inserted into PostgreSQL Successfully")

    except Exception as e:
        print("Error:", e)