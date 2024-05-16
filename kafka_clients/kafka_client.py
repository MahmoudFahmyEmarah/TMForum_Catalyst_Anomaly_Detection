from kafka import KafkaConsumer, KafkaProducer
import json
from config import config
import logging

logging.basicConfig(level=logging.INFO)


def kafka_consumer(topic_name):
    """
    Creates a Kafka consumer for a specific topic and yields messages from it.

    :param topic_name: The name of the Kafka topic to consume messages from.
    :type topic_name: str
    :return: A generator that yields messages from the Kafka topic.
    :rtype: generator
    :raises Exception: If there is an error consuming messages.
    """
    try:
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=[config.KAFKA_BROKER_URL]
            , **config.KAFKA_CONSUMER_CONFIG
        )
        for message in consumer:
            yield json.loads(message.value)
    except Exception as e:
        logging.error(f"Failed to consume messages: {e}")
        raise


def kafka_producer(topic_name, message):
    """
    Creates a Kafka producer and sends a message to a specific topic.

    :param topic_name: The name of the Kafka topic to send the message to.
    :type topic_name: str
    :param message: The message to send to the Kafka topic.
    :type message: str
    :raises Exception: If there is an error producing the message.
    """
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
