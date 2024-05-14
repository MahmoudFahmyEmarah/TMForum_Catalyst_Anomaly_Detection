import requests
import logging
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_order_details(json_order_details):
    try:
        #Get productOffering from the oder details
        productOffering = json_order_details.get("productOffering", "")
        print(productOffering)
        # Construct the API URL using the productOffering ID
        url = f"{config.API_BASE_URL}{productOffering}"
        headers = {'Cookie': 'STICKYQ=5990776d322bc0e13fc7ff91f7ceac42|ZkEkq|ZkEki'}

        # Fetch the original order details from the API
        response = requests.get(url, headers=headers,verify=False)
        response.raise_for_status()
        api_order_details = response.json()

        # Define the fields to compare
        fields_to_compare = ['offerName', 'mobileData', 'mobileVoice', 'text', 'price']

        # Compare the necessary fields
        for field in fields_to_compare:
            api_field_value = str(api_order_details.get(field.lower(), '')).strip()
            json_field_value = str(json_order_details.get(field, '')).strip()

            # Log discrepancies for troubleshooting
            if api_field_value != json_field_value:
                logging.info(f"Discrepancy found in {field}: API - {api_field_value}, JSON - {json_field_value}")
                return 0  # Return 0 if any field does not match

        # Return 1 if all fields match
        return 1

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise
