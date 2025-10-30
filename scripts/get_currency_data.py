import pandas as pd
import os

DATA_PATH = "data/currency_data.csv"

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import os

CURRENCY_TICKERS = {
    "USD": "USDINR=X",
    "EUR": "EURINR=X",
    "JPY": "JPYINR=X",
    "GBP": "GBPINR=X",
}


def get_currency_data(days: int = 365):
    end_date = datetime.today()
    start_date = end_date - timedelta(days)

    all_data = []
    for name, ticker in CURRENCY_TICKERS.items():
        df = yf.download(
            ticker, start=start_date, end=end_date, progress=False, auto_adjust=True
        )
        df = df[["Close"]].rename(columns={"Close": f"{name}_INR"})  # type: ignore
        all_data.append(df)

    merged_data = pd.concat(all_data, axis=1)
    merged_data.columns = merged_data.columns.droplevel(1)
    merged_data.reset_index(inplace=True)
    merged_data = merged_data.astype(
        {
            "Date": str,
            "USD_INR": float,
            "EUR_INR": float,
            "JPY_INR": float,
            "GBP_INR": float,
        }
    )

    # Keep only latest required days
    merged_data["Date"] = pd.to_datetime(merged_data["Date"])
    merged_data = merged_data.iloc[-days:]
    return merged_data
