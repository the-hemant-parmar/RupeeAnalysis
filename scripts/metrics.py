import pandas as pd


def calculate_rupee_strength(df: pd.DataFrame) -> float:
    """
    Compute the average percentage change across all numeric columns excluding the "Date" column.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing a "Date" column and one or more numeric columns whose percentage changes should be measured.
    
    Returns:
        float: The mean of per-column percentage changes multiplied by 100 (overall average percentage change).
    """
    pct_changes = df.drop(columns=["Date"]).pct_change().mean()
    avg_change = pct_changes.mean() * 100  # Convert to percentage
    return avg_change


def calculate_normalized_change(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize each non-`Date` column to a base value of 100 using the first row as the baseline.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame containing a `Date` column and one or more numeric series to normalize.
            The `Date` column is preserved unchanged; all other columns are scaled so their first-row value becomes 100.
    
    Returns:
        pd.DataFrame: A DataFrame with the same shape as `df` where each non-`Date` column value is `(value / first_row_value) * 100`.
    """
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