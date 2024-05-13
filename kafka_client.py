from kafka import KafkaConsumer, KafkaProducer
import json
import config
import logging

logging.basicConfig(level=logging.INFO)

def consume_orders(topic_name):
    try:
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=[config.KAFKA_BROKER_URL]
            #,**config.KAFKA_CONSUMER_CONFIG
        )
        for message in consumer:
            yield json.loads(message.value)
    except Exception as e:
        logging.error(f"Failed to consume messages: {e}")
        raise

def produce_complaint(topic_name, message):
    try:
        producer = KafkaProducer(
            bootstrap_servers=[config.KAFKA_BROKER_URL],
            **config.KAFKA_CONSUMER_CONFIG
        )
        producer.send(topic_name, json.dumps(message).encode('utf-8'))
        producer.flush()
    except Exception as e:
        logging.error(f"Failed to produce message: {e}")
        raise



#
# message = {
#     "OrderId": "e062d2b4-2e82-4fc8-856e-c06a7e7dd134",
#     "CustomerId": 46,
#     "OfferName": "Global Unlimited",
#     "MobileData": "50GB",
#     "MobileVoice": "Unlimited",
#     "Text": "Unlimited",
#     "Price": "€40"
# }
#
# # Usage
# produce_complaint("complains", message)
