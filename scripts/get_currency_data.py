import pandas as pd
import os

DATA_PATH = "data/currency_data.csv"


def get_currency_data(days: int = 365):
    """Return cached data."""

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
        df = df.drop(columns=["CNY_INR"])
        # Drop the first row if it's headers repeated as data
        df = df.iloc[1:]
        df = df.astype(
            {
                "Date": str,
                "USD_INR": float,
                "EUR_INR": float,
                "JPY_INR": float,
                "GBP_INR": float,
            }
        )
        return df
