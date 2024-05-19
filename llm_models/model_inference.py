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
    df.columns = ['OfferName', 'MobileData', 'Order_status', 'TicketTitle', "Number of Records"]

    def prefix_entry(entry, col_name):
        """
        Prefix the entry with the column name for formatting.
        """
        if entry == 0:
            return 'Order_status:Not Complained'
        elif entry == 1:
            return 'Order_status:Complained'
        return f"{col_name}:{entry}"

    formatted_df = df.apply(lambda col: col.apply(prefix_entry, col_name=col.name))
    #remove column names
    #formatted_df.columns = ['' for col in formatted_df.columns]
    dataset = formatted_df.to_string(index=False)
    order_query = (f"- OfferName: {order_details_json['OfferName']} \n"
                   f"\t- MobileData: {order_details_json['MobileData']}GB")
    return dataset, order_query


def send_prompt(client: OPENAI, dataset: str, order_query: str) -> dict:
    """
    Send the prompt to the OpenAI model and get the response.

    :param (OPENAI) client: The OpenAI client
    :param (str) dataset: The formatted dataset
    :param (str) order_query: The formatted order query
    :return: (dict) The response from the OpenAI model
    """
    template_text = f""" System: You are a data analysis tool specialized in identifying potential complaints from 
    order data. Use the provided dataset to analyze and predict the likelihood of complaints for specific orders 
    based on historical data.

      Dataset:
      {dataset}

      Order Details:
        {order_query}
        
      Task:
      1. Predict whether the order with the details provided will result in a complaint (0 for no complaint, 1 for complaint).
      2. Estimate the probability of a complaint occurrence for this order, expressed as a decimal from 0 to 1 rounded to two decimal points.
      3. Predict the likely ticket title if a complaint occurs.
      4. Suggest a solution if a complaint is detected, considering past data where a similar issue was addressed by a self-healing engine modifying the order.

      Format the response as a JSON object with the fields:
      - Potential_Complaint
      - Probability_of_Complaint
      - TicketTitle
      - Recommended_solution
      """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
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
