from kafka_client import consume_orders, produce_complaint
from data_processing import get_unique_records
from model_inference import format_and_send_prompt
from api_client import fetch_order_details
import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        for order_details in consume_orders("order.completed.topic"):
            #processing logic here
            logging.info(f"Processing order: {order_details['OrderId']}")
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
