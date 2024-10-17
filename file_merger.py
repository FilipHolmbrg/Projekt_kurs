import pandas as pd

def merge_file(df_1: pd.DataFrame, df_2: pd.DataFrame, df_3: pd.DataFrame) -> pd.DataFrame: 
    """Function to merge two DataFrames"""   
    price_df = df_1
    weather_df = df_2
    inflation_df = df_3
    # print(price_df.head())
    # print()
    # print(weather_df.head())
    # print()
    # print(inflation_df.head())
    # print()
    
    # price_df['date'] = pd.to_datetime(price_df['date'])
    # weather_df['date'] = pd.to_datetime(weather_df['date'])
    # inflation_df['date'] = pd.to_datetime(weather_df['date'])
    
    # merged_df = pd.merge(price_df, weather_df, inflation_df, on='date', how='inner')
    merged_df = pd.merge(price_df, weather_df, on='date', how='inner')
    merged_df = pd.merge(merged_df, inflation_df, on='date', how='inner')
    merged_df = merged_df.sort_values(by='date')
    
    # merged_df.to_excel(r'merged_data.xlsx', index=False)
    return merged_df