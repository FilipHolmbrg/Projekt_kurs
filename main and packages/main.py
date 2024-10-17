# Imports
from read_prices import get_prices #används för csv
from weather_data import read_weather_data, transform_weather_data
from inflation_data import read_inflation_data, transform_inflation_data
from price_data import read_prices, transform_prices #används för api
from file_merger import merge_file
from df_to_sql import save_data

def main():
    """main script to execute ETL"""
    
    #Load weather, day-ahead price and inflation data into DataFrames.
    inflation_data = read_inflation_data()
    weather_data = read_weather_data()
    # price_data = read_prices() #används för API
    price_data = get_prices() #används för csv
    
    # Transform data
    inflation_df = transform_inflation_data(inflation_data)
    weather_df = transform_weather_data(weather_data)
    price_df = transform_prices(price_data)
    
    # Merge dataframes for storage
    merged_df = merge_file(price_df, weather_df, inflation_df)
    
    print(merged_df)
    
    # Save DataFrame in SQlite3 db
    # save_data(merged_df)
    
if __name__ == '__main__':
    main()
