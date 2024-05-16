import requests
import logging
from config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_order_details(productOffering_id: str) -> dict:
    """
    Fetches the original order details from the API.

    :param (str) productOffering_id: The ID of the product offering
    :return: (dict) The order details as a dictionary
    :raises requests.exceptions.HTTPError: If an HTTP error occurs
    :raises requests.exceptions.RequestException: If the request fails
    """
    try:
        # Construct the API URL using the productOffering ID
        url = f"{config.API_BASE_URL}{productOffering_id}"
        headers = {'Cookie': 'STICKYQ=5990776d322bc0e13fc7ff91f7ceac42|ZkEkq|ZkEki'}

        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        api_order_details = response.json()

        return api_order_details

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise


def compare_order_details(api_order_details: dict, json_order_details: dict) -> int:
    """
    Compares the order details from the API with the order details from the JSON message.

    :param (dict) api_order_details: The order details fetched from the API
    :param (dict) json_order_details: The order details from the JSON message
    :return: (int) 1 if the order details match, 0 if they do not match
    """
    try:
        # Define the fields to compare
        fields_to_compare = ['offerName', 'mobileData', 'mobileVoice', 'text', 'price']

        # Compare the necessary fields
        for field in fields_to_compare:
            api_field_value = str(api_order_details.get(field.lower(), '')).strip()
            json_field_value = str(json_order_details.get(field, '')).strip()

            # Log discrepancies for troubleshooting
            if api_field_value != json_field_value:
                logging.info(f"Discrepancy found in {field}: API - {api_field_value}, JSON - {json_field_value}")
                return 0

        return 1

    except Exception as e:
        logging.error(f"An error occurred during comparison: {e}")
        raise
