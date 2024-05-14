import pandas as pd
from kafka_client import consumer_service
import logging

logging.basicConfig(level=logging.INFO)


def main():
    df = pd.read_csv("data/Mismatched_Data.csv")
    try:
        consumer_service(df)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
