import pandas as pd
from classfiction_service import classification_model
from kafka_client import consume_orders, produce_complaint, consumer_service, parse_kafka_response
from data_processing import get_unique_records
from model_inference import format_and_send_prompt
import logging

logging.basicConfig(level=logging.INFO)


def main():
    df = pd.read_csv("data/Mismatched_Data.csv")
    try:
        message = {
            "OrderId": "e062d2b4-2e82-4fc8-856e-c06a7e7dd134",
            "state": "Completed",
            "CustomerId": 46,
            "productOrderItem": [
                {
                    "OfferName": "Global Mobile Plus",
                    "productOffering": "154",
                    "action": "ADD",
                    "MobileData": "20GB",
                    "MobileVoice": "Unlimited",
                    "Text": "Unlimited",
                    "Price": "40",
                    "Duration": "1 Month"
                },
                {
                    "OfferName": "Global Pre Unlimited",
                    "action": "REMOVE"
                }
            ],
            "attrs": [
                {
                    "name": "OrderTypeReset",
                    "value": "false"
                }
            ]
        }
        order_details=parse_kafka_response(message)
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
        consumer_service(df)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
