import json
import logging
from openai import OpenAI as OPENAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def format_and_send_prompt(df, order_details_json):
    try:
        # Initialize your OpenAI client
        load_dotenv()
        client = OPENAI()
        offer_name = order_details_json['OfferName']
        offer_data = order_details_json['MobileData']

        # Function to prefix each entry with its column name
        def prefix_entry(entry, col_name):
            return f"{col_name}:{entry}"

        # Apply the function to each element in the DataFrame
        formatted_df = df.apply(lambda col: col.apply(prefix_entry, col_name=col.name))

        # Convert the DataFrame to a string that looks like a table
        dataset = formatted_df.to_string(index=False)
        order_query = f"OfferName: {offer_name} ,MobileData: {offer_data}"
        # Prepare the template text with the dataset formatted as a table
        # Prepare the template text with the dataset formatted as a table
        template_text = f"""
        Analyze the provided order data for complaints and ticket types.
        Given the dataset taking in consideration that Number of Records represents the number of occurence of unique orders with the compination of OfferName and MobileData fields in our dataset:

        {dataset}

        For the orders details data frame: '{order_query}', predict based on the compination of OfferName and MobileData fields represented in the previous data frame:
        1. The likelihood of a complaint predict the value of the Complained filed for the given oredr (0 or 1) 
        for example if the order is : OfferName:Global Mobile Plus MobileData:100GB Complained:0 then the Potential_Complaint is 0
        and if OfferName:Global Mobile Plus  MobileData:10GB Complained:1 Then then the Potential_Complaint is 1 and so on.
        2. The probability of complaint occurrence based on the records count as a float number from 0 to 1 rounded to two decimal points
        3. The likely ticket type.
        4- Generate a text to recommend that the solution caused by Catalogue mismatch detected, a new modify order has been created by Self Healing engine

        Format the response as a json object with the fields:
        - Potential_Complaint
        - Probability_of_Complaint
        - TicketTitle
        - Recommended_solution
        """
        print("Raw Template Body:", template_text)
        # Send the prompt to the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": template_text}
            ]
        )
        print("Raw Response Body:", response)
        # Return the response content
        response = response.choices[0].message.content
        # Parse the JSON string to a Python dictionary
        response_data = json.loads(response)

        # Construct result based on the response
        result = {
            "OrderID": order_details_json['OrderId'],
            "Potential_Complaint": response_data["Potential_Complaint"],
            "Probability_of_Complaint": response_data["Probability_of_Complaint"],
            "TicketTitle": response_data["TicketTitle"],
            "Recommended_solution": response_data["Recommended_solution"]
        }

        return result
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON response: {e}")
        raise ValueError("Failed to parse JSON from model response.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise RuntimeError("An unexpected error occurred while formatting and sending the prompt.")
