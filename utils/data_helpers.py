import logging

from pandas import DataFrame

logging.basicConfig(level=logging.INFO)


def get_offername_stat(df: DataFrame, offername: str):
    """
    Get the statistics for a specific offer name.

    :param (DataFrame) df: The dataframe containing the data
    :param (str) offername: The offer name to get statistics for
    :return: (DataFrame) The statistics for the offer name
    raises Exception: If an error occurs during processing
    """
    try:
        # Filter the dataframe for the specific offer name
        offer_df = df[df['OfferName'] == offername]
        
        # Fill NaN or empty 'TicketTitle' with a placeholder like 'No Title'
        offer_df['TicketTitle'] = offer_df['TicketTitle'].fillna('No Title').replace('', 'No Title')
        
        # Group by the necessary columns and count occurrences
        grouped_df = offer_df.groupby(['OfferName', 'MobileData', 'Complained', 'TicketTitle']).size().reset_index(name='Number of Records')
        
        return grouped_df
    except Exception as e:
        logging.error(f"Error in getting unique records: {e}")
        raise
