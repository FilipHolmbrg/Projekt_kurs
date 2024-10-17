import sqlite3
import pandas as pd

def save_data(df_data: pd.DataFrame) -> None:
    """Function to save weather and price data in a database"""
    con = sqlite3.connect("./example_data/weather_price_data.db")
    df_data.to_sql("weather_price_table", con, if_exists = "replace", index = False)
    con.commit()
    con.close()    

            
