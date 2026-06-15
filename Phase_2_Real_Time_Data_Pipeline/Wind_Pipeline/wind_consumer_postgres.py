from kafka import KafkaConsumer
import psycopg2

# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres123"
)

cursor = conn.cursor()

# Kafka Consumer
consumer = KafkaConsumer(
    'wind_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='wind-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("Wind Consumer started...")

for message in consumer:
    try:
        data = message.value.strip().split(",")

        # Skip invalid rows
        if len(data) < 4:
            print("Skipped:", data)
            continue

        values = [
            data[0].strip(),  # timestamp
            float(data[1].strip()),  # wind_speed
            float(data[2].strip()),  # power_output
            float(data[3].strip())   # wind_direction
        ]

        cursor.execute("""
        INSERT INTO wind_data (
            timestamp,
            wind_speed,
            power_output,
            wind_direction
        )
        VALUES (%s, %s, %s, %s)
        """, values)

        conn.commit()
        print("Inserted:", values)

    except Exception as e:
        print("Error:", e)
        conn.rollback()