import pandas as pd
from classfiction_service import classification_model
from kafka_client import consume_orders, produce_complaint
from data_processing import get_unique_records
from model_inference import format_and_send_prompt
from api_client import fetch_order_details
import logging

logging.basicConfig(level=logging.INFO)

def main():
    df = pd.read_csv("data/Mismatched_Data.csv")
    try:
        for order_details in consume_orders("complains"):
            #processing logic here
            print("classification model response")
            classification_model(order_details)

            print("offer statistics")
            offer_statistics = get_unique_records(df, order_details['OfferName'])
            print(offer_statistics)

            response = format_and_send_prompt(offer_statistics, order_details)
            print(response)
            #fetch_order_details(order_details['OrderId'])

            logging.info(f"Processing order: {order_details['OrderId']}")
    except Exception as e:
        logging.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
