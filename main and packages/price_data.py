import pandas as pd
from entsoe import EntsoePandasClient
import time

def read_prices() -> pd.DataFrame:

    api_key = 'INSER API KEY HERE' #"35424227-10de-45bc-bfd9-1647821c1d5f"
    client = EntsoePandasClient(api_key = api_key)

    area = "SE_3"
    timezone = "Europe/Stockholm"

    dataframes = []

    for year in range (2015, 2025):
        if year == 2024:
            start = pd.Timestamp(f"{year}-01-01", tz = "Europe/Stockholm")
            end = pd.Timestamp(f"{year}-09-30", tz = "Europe/Stockholm")
                
            df_year = client.query_day_ahead_prices(area, start = start, end = end)
            dataframes.append(df_year)
            time.sleep(10)
                
        else:
            start = pd.Timestamp(f"{year}-01-01", tz = "Europe/Stockholm")
            end = pd.Timestamp(f"{year}-12-31", tz = "Europe/Stockholm")
        
            df_year = client.query_day_ahead_prices(area, start = start, end = end)
            dataframes.append(df_year)
            time.sleep(10)
        
    df_all_year = pd.concat(dataframes)
    
    return df_all_year

def electric_price_convert(mw_per_euro: pd.Series, exchange_rate_sek: float = 11.35) -> pd.Series:
    """Function to convert Euro/Mwh to öre/kwh"""
    kw_per_ore = ((mw_per_euro / 1000) * exchange_rate_sek) * 100    
    return round(kw_per_ore, 2)

def transform_prices(data: pd.DataFrame) -> pd.DataFrame:
    """Function to transform prices to öre/kwh"""
    mw_per_euro = data["price"]
    
    kw = electric_price_convert(mw_per_euro)
    data["price_kw/ore"] = kw
    df_kw_ore = data.drop(["price"], axis = 1)
    
    df_kw_ore['date'] = pd.to_datetime(df_kw_ore['date']) #transform to datetime
    
    return df_kw_ore
    
