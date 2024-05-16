class KafkaHelper:
    @staticmethod
    def parse_response(order_details):
        """
        Parses the response from the Kafka message.

        :param (dict) order_details: The order details from the Kafka message
        :return: (dict) The parsed order details
        """
        try:
            flattened = {
                "OrderId": order_details["OrderId"],
            }

            found_add_action = False
            for item in order_details.get("productOrderItem", []):
                if item.get("action") == "add":
                    found_add_action = True
                    flattened.update({
                        "OfferName": item.get("OfferName", ""),
                        "orderItemId": item.get("orderItemId", ""),
                        "productOffering": item.get("productOffering", ""),
                        "MobileData": item.get("MobileData", ""),
                        "MobileVoice": item.get("MobileVoice", ""),
                        "Text": item.get("Text", ""),
                        "Price": f"€{item.get('Price', '')}"
                    })
                    break

            if not found_add_action:
                raise ValueError("No productOrderItem with action 'ADD' found.")

        except KeyError as e:
            return f"Key error: {str(e)} - required key not found in the input."
        except Exception as e:
            return f"An error occurred: {str(e)}"

        return flattened
