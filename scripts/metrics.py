import pandas as pd


def calculate_rupee_strength(df: pd.DataFrame) -> float:
    pct_changes = df.drop(columns=["Date"]).pct_change().mean()
    avg_change = pct_changes.mean() * 100  # Convert to percentage
    return avg_change


def calculate_normalized_change(df: pd.DataFrame) -> pd.DataFrame:
    pct_change = df.copy()
    for col in df.columns:
        if col != "Date":
            pct_change[col] = df[col].pct_change() * 100

    cum_change = pct_change.copy()
    for col in df.columns:
        if col != "Date":
            cum_change[col] = pct_change[col].cumsum()

    norm = df.copy()
    for col in df.columns:
        if col != "Date":
            norm[col] = (df[col] / df[col].iloc[0]) * 100

    return norm
