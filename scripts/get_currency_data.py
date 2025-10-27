import pandas as pd
import os

DATA_PATH = "data/currency_data.csv"


def get_currency_data(days: int = 365):
    """
    Load cached currency exchange rates from the local CSV and return up to `days` rows.
    
    Parameters:
    	days (int): Number of rows to include from the file, starting after the first row (default 365).
    
    Returns:
    	pd.DataFrame or None: DataFrame containing columns `Date`, `USD_INR`, `EUR_INR`, `JPY_INR`, and `GBP_INR` (with `Date` as string and the currency columns as float) when the data file exists; `None` if the file is missing.
    """

    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
        # Drop the first row if it's headers repeated as data
        df = df.iloc[1:days]
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