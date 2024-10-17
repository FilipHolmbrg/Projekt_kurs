import pandas as pd

def get_prices() -> pd.DataFrame:
    """Function to read CSV into DataFrame"""
    df_daily_price = pd.read_csv("day_ahead_prices.csv")
    return df_daily_price