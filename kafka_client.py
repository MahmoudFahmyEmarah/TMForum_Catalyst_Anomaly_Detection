from kafka import KafkaConsumer, KafkaProducer
import json
import config
import logging

from classfiction_service import classification_model
from data_processing import get_unique_records
from model_inference import format_and_send_prompt

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


def consumer_service(df):
    for order_details in consume_orders("complains"):
        print(order_details)
        # processing logic here
        print("classification model response")
        classification_model(order_details)

        print("offer statistics")
        offer_statistics = get_unique_records(df, order_details['OfferName'])
        print(offer_statistics)

        #openai model
        response = format_and_send_prompt(offer_statistics, order_details)
        print(response)

        # fetch_order_details(order_details['OrderId'])

        logging.info(f"Processing order: {order_details['OrderId']}")


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

#Parse the response we get from kafka consumer
def parse_kafka_response(order_details):
    try:
        # Check if the order status is 'Completed'
        if order_details["state"] != "Completed":
            return {'Error':"Order is not completed."}

        # Initialize the flattened result dictionary with the OrderId and CustomerId
        flattened = {
            "OrderId": order_details["OrderId"],
            "CustomerId": order_details["CustomerId"]
        }

        # Find the productOrderItem with action 'ADD'
        found_add_action = False
        for item in order_details.get("productOrderItem", []):
            if item.get("action") == "ADD":
                found_add_action = True
                # Add relevant fields from this item to the flattened dictionary
                flattened.update({
                    "OfferName": item.get("OfferName", ""),
                    "productOffering": item.get("productOffering", ""),
                    "MobileData": item.get("MobileData", ""),
                    "MobileVoice": item.get("MobileVoice", ""),
                    "Text": item.get("Text", ""),
                    "Price": f"€{item.get('Price', '')}"
                })
                break  # Stop after the first match

        if not found_add_action:
            # If no item with action 'ADD' is found, raise an exception
            raise ValueError("No productOrderItem with action 'ADD' found.")

    except KeyError as e:
        # Handle missing key errors
        return f"Key error: {str(e)} - required key not found in the input."
    except Exception as e:
        # Handle any other exceptions that might occur
        return f"An error occurred: {str(e)}"

    # Return the successfully flattened dictionary
    return flattened
