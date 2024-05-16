import pandas as pd
import logging

from services.main_service import main_service

logging.basicConfig(level=logging.INFO)


def main():
    df = pd.read_csv("data/Mismatched_Data.csv")
    try:
        main_service(df)
    except Exception as e:
        logging.error(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
