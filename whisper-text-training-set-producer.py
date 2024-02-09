import os
import json
from dotenv import load_dotenv
from kafka import KafkaConsumer, KafkaProducer

load_dotenv()

source_topic = os.getenv('SOURCE_TOPIC_NAME')
destination_topic = os.getenv('DESTINATION_TOPIC_NAME')
bootstrap_servers = [os.getenv('BROKER')]  
group_id = os.getenv('GROUP_ID')  

consumer = KafkaConsumer(
    source_topic,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest', 
    group_id=group_id,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  
)

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda m: json.dumps(m).encode('utf-8')  
)

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    return text

for message in consumer:
    msg_data = message.value

    if msg_data.get('chat_id') == -1001888622530:

        processed_message = preprocess_text(msg_data.get('message', ''))

        new_message = {
            "title": msg_data.get('title'),
            "message": processed_message
        }

        producer.send(destination_topic, new_message)
        print(f"Produced to {destination_topic}: {new_message}")

consumer.close()
producer.close()

