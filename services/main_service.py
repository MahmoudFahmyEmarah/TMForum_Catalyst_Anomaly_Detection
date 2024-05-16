import logging

from pandas import DataFrame

from api.api_client import fetch_order_details, compare_order_details
from config import config
from kafka_clients.kafka_client import kafka_consumer, kafka_producer
from llm_models.model_inference import format_and_send_prompt
from utils.data_helpers import get_offername_stat
from utils.data_validtion import DataValidationError
from utils.kafka_utils import KafkaHelper


def main_service(df: DataFrame):
    """
    Main service that Contains the main processing steps.
    Steps:
    - Consume messages from the Kafka topic
    - Parse the response
    - Get offer statistics
    - Format and send prompt to the OpenAI model
    - Compare order details
    - Push response to the producer topic

    :param (DataFrame) df: The DataFrame containing the data
    """
    for order_details in kafka_consumer(config.KAFKA_CONSUMER_TOPIC):
        valid_order = DataValidationError.validate_order_details(order_details)
        if not valid_order:
            logging.error("Invalid order details , the shape of the order details is not as expected")
            print("ss")

        order_details = KafkaHelper.parse_response(order_details)

        offer_statistics = get_offername_stat(df, order_details['OfferName'])

        #openai model
        response = format_and_send_prompt(offer_statistics, order_details)

        if response['potentialComplaint'] == 1:
            logging.info(f"Processing order: {order_details['OrderId']}")

            productOffering_id = order_details.get("productOffering", "")
            api_order_details = fetch_order_details(productOffering_id)

            orders_status = compare_order_details(api_order_details, order_details)
            if orders_status == 0:
                kafka_producer(config.KAFKA_PRODUCER_TOPIC, response)
                logging.info("Response pushed to the producer topic")
