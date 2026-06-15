from kafka import KafkaConsumer
import psycopg2

consumer = KafkaConsumer(
    'grid_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='grid-group-final',
    value_deserializer=lambda x: x.decode('utf-8')
)

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres123"
)

cursor = conn.cursor()

print("Grid Consumer Started...")

for message in consumer:
    try:
        row = message.value.strip()

        # skip empty rows
        if not row:
            continue

        # skip header
        if row.startswith("datetime"):
            print("Header skipped")
            continue

        values = row.split(",")

        print("Columns:", len(values))

        if len(values) != 8:
            print("Skipped invalid row")
            continue

        query = """
        INSERT INTO grid_data (
            datetime,
            global_active_power,
            global_reactive_power,
            voltage,
            global_intensity,
            sub_metering_1,
            sub_metering_2,
            sub_metering_3
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query, (
            values[0],
            float(values[1]),
            float(values[2]),
            float(values[3]),
            float(values[4]),
            float(values[5]),
            float(values[6]),
            float(values[7])
        ))

        conn.commit()

        print("Inserted:", values[0])

    except Exception as e:
        print("Error:", e)