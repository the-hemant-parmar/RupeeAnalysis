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

OUTPUT_PATH = "../data/currency_data.csv"


def fetch_data(days: int = 365):
    end_date = datetime.today()
    start_date = end_date - timedelta(days)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    all_data = []
    for name, ticker in CURRENCY_TICKERS.items():
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        df = df[["Close"]].rename(columns={"Close": f"{name}_INR"})  # type: ignore
        all_data.append(df)

    merged_data = pd.concat(all_data, axis=1)
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
    merged_data.to_csv(OUTPUT_PATH, index=False)
