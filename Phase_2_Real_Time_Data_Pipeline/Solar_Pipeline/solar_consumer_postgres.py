from kafka import KafkaConsumer
import psycopg2

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres123"
)

cursor = conn.cursor()

# Kafka Consumer
consumer = KafkaConsumer(
    'solar_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("Consumer started...")

for message in consumer:
    try:
        data = message.value.strip()

        # Split incoming chunk into lines
        rows = data.splitlines()

        for line in rows:

            # Skip empty/header lines
            if not line or "DATE_TIME" in line:
                continue

            row = line.split(",")

            # Solar table has 6 columns
            if len(row) == 6:

                cursor.execute("""
                    INSERT INTO solar_data
                    (timestamp, plant_id, source_key,
                     ambient_temperature, module_temperature, irradiation)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                ))

                conn.commit()
                print("Inserted:", row)

            else:
                print("Skipped:", line)

    except Exception as e:
        print("Error:", e)
        conn.rollback()