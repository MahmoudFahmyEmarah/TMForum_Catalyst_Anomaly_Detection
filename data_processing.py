import logging

logging.basicConfig(level=logging.INFO)


def get_unique_records(df, offername):
    try:
        offer_df = df[df['OfferName'] == offername]
        grouped_df = offer_df.groupby(['OfferName', 'MobileData', 'Complained', 'TicketTitle']).size().reset_index(
            name='Number of Records')
        return grouped_df
    except Exception as e:
        logging.error(f"Error in getting unique records: {e}")
        raise
