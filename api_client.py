import requests
import logging
import config
logging.basicConfig(level=logging.INFO)

def fetch_order_details(product_id):
    try:
        url = f"{config.API_BASE_URL}{product_id}"
        headers = {'Cookie': 'STICKYQ=5990776d322bc0e13fc7ff91f7ceac42|ZkEkq|ZkEki'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise
