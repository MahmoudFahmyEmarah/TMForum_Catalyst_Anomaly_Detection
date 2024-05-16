import json
import logging
from typing import Tuple

from openai import OpenAI as OPENAI
from dotenv import load_dotenv
from pandas import DataFrame

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def format_data(df: DataFrame, order_details_json: dict) -> Tuple[str, str]:
    """
    Format the data and order details for the prompt
    to be sent to the OpenAI model.

    :param (DataFrame) df: The DataFrame containing the data
    :param (dict) order_details_json: The order details as a dictionary
    :return: (Tuple[str, str]) The formatted dataset and order query
    """

    def prefix_entry(entry, col_name):
        """
        Prefix the entry with the column name for formatting.
        """
        if entry == 0:
            return 'Not Complained'
        elif entry == 1:
            return 'Order Complained'
        return f"{col_name}:{entry}"

    formatted_df = df.apply(lambda col: col.apply(prefix_entry, col_name=col.name))
    dataset = formatted_df.to_string(index=False)
    order_query = f"OfferName: {order_details_json['OfferName']} ,MobileData: {order_details_json['MobileData']}GB"
    return dataset, order_query


def send_prompt(client: OPENAI, dataset: str, order_query: str) -> dict:
    """
    Send the prompt to the OpenAI model and get the response.

    :param (OPENAI) client: The OpenAI client
    :param (str) dataset: The formatted dataset
    :param (str) order_query: The formatted order query
    :return: (dict) The response from the OpenAI model
    """
    template_text = f"""
    Analyze the provided order data for complaints and ticket types.
    Given the dataset taking in consideration that Number of Records represents the number of occurence of unique orders with the compination of OfferName and MobileData fields in our dataset:

    {dataset}

    For the orders details data frame: '{order_query}', predict based on the compination of OfferName and MobileData fields represented in the previous data frame:
    1. The likelihood of a complaint predict the value of the Complained filed for the given oredr (0 or 1)
    2. The probability of complaint occurrence based on the records count as a float number from 0 to 1 rounded to two decimal points
    3. The likely ticket type.
    4- Generate a text to recommend that the solution caused by Catalogue mismatch detected, a new modify order has been created by Self Healing engine

    Format the response as a json object with the fields:
    - Potential_Complaint
    - Probability_of_Complaint
    - TicketTitle
    - Recommended_solution
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": template_text}
        ]
    )
    return response


def process_response(response: dict, order_details_json: dict) -> dict:
    """
    Process the response from the OpenAI model and extract the relevant information.

    :param (dict) response: The response from the OpenAI model
    :param (dict) order_details_json: The order details as a dictionary
    :return: (dict) The extracted information from the response
    """
    response = response.choices[0].message.content
    response_data = json.loads(response)
    print("response_data", response_data)
    print("order_details_json", order_details_json)
    result = {
        "orderID": order_details_json['OrderId'],
        "orderItemID": order_details_json['orderItemId'],
        "productOffering": order_details_json['productOffering'],
        "potentialComplaint": response_data["Potential_Complaint"],
        "probabilityOfComplaint": response_data["Probability_of_Complaint"],
        "ticketTitle": response_data["TicketTitle"],
        "recommendedSolution": response_data["Recommended_solution"]
    }
    return result


def format_and_send_prompt(df: DataFrame, order_details_json: dict) -> dict:
    try:
        load_dotenv()
        client = OPENAI()
        dataset, order_query = format_data(df, order_details_json)
        response = send_prompt(client, dataset, order_query)
        result = process_response(response, order_details_json)
        return result
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON response: {e}")
        raise ValueError("Failed to parse JSON from model response.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise RuntimeError("An unexpected error occurred while formatting and sending the prompt.")
