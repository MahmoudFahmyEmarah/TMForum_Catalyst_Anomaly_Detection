import pandas as pd
import json
import time
from kafka import KafkaProducer
import config
import logging

TOPIC_NAME = "complains"

def read_data():
    df = pd.read_csv("data/Mismatched_Data.csv")
    df = df[df['Complained'] == 1]
    selected_columns = df.loc[:, ['OrderId', 'CustomerId', 'OfferName',
                                  'MobileData', 'MobileVoice', 'Text',
                                  'Price']]

    return selected_columns.itertuples(index=False)


def send_row_to_kafka(row):
    try:
        # message = row._asdict()
        # produce_complaint(TOPIC_NAME, message)

        producer = KafkaProducer(
            bootstrap_servers=[config.KAFKA_BROKER_URL],
        )
        message = json.dumps(row._asdict()).encode('utf-8')
        producer.send(TOPIC_NAME, message)
        producer.flush()
    except Exception as e:
        logging.error(f"Failed to produce message: {e}")
        raise


def send_data_to_kafka():
    rows_generator = read_data()
    for row in rows_generator:
        print("Complain produced")
        send_row_to_kafka(row)
        time.sleep(10)


send_data_to_kafka()
