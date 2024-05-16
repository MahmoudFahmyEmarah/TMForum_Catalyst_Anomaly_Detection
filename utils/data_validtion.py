class DataValidationError(Exception):
    @staticmethod
    def validate_order_details(order_details: dict) -> bool:
        """
        Validates the structure and content of the order details.

        :param order_details: The order details to validate.
        :type order_details: dict
        :return: True if the order details are valid, False otherwise.
        :rtype: bool
        """
        # Check if the top-level keys are present
        if not all(key in order_details for key in ["OrderId", "productOrderItem"]):
            return False

        # Check if 'productOrderItem' is a list
        if not isinstance(order_details["productOrderItem"], list):
            return False

        # Check each item in the 'productOrderItem' list
        for item in order_details["productOrderItem"]:
            # Check if the necessary keys are present
            if not all(key in item for key in ["OfferName", "productOffering", "action", "orderItemId"]):
                return False

            # Check if 'action' is either 'delete' or 'add'
            if item["action"] not in ["delete", "add"]:
                return False

            # If 'action' is 'add', check if the necessary keys are present
            if str(item["action"]).lower() == "add":
                if not all(key in item for key in ["MobileData", "MobileVoice", "Text", "Price"]):
                    return False

        # If all checks passed, the order details are valid
        return True
