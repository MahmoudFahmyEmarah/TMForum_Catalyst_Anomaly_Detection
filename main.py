import pandas as pd
from classfiction_service import classification_model
from kafka_client import consume_orders, produce_complaint, consumer_service
from data_processing import get_unique_records
from model_inference import format_and_send_prompt
from api_client import fetch_order_details
import logging

logging.basicConfig(level=logging.INFO)


def main():
    df = pd.read_csv("data/Mismatched_Data.csv")
    try:
        consumer_service(df)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
