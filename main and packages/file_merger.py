import pandas as pd

def merge_file(df_1: pd.DataFrame, df_2: pd.DataFrame, df_3: pd.DataFrame) -> pd.DataFrame: 
    """Function to merge two DataFrames"""   
    price_df = df_1
    weather_df = df_2
    inflation_df = df_3

    merged_df = pd.merge(price_df, weather_df, on='date', how='inner')
    merged_df = pd.merge(merged_df, inflation_df, on='date', how='inner')
    merged_df = merged_df.sort_values(by='date')
    
    return merged_df