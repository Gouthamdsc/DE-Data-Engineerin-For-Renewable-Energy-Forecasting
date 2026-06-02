from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'wind_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=None,
    value_deserializer=lambda x: x.decode('utf-8')
)

print("Listening to Wind Topic...")

for message in consumer:
    try:
        data = json.loads(message.value)
        print(data)
    except Exception:
        print("Skipped invalid message")