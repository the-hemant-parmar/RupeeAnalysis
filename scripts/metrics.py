import pandas as pd


def calculate_rupee_strength(df: pd.DataFrame) -> float:
    pct_changes = df.drop(columns=["Date"]).pct_change().mean()
    avg_change = pct_changes.mean() * 100  # Convert to percentage
    return avg_change
