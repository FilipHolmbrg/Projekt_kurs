import pandas as pd

def read_weather_data() -> pd.DataFrame:
    """Function to read historical weather data saved localy as .xlsx file"""
    file_path = r'open-meteo-57.68N12.03E9m (3).xlsx'
    df = pd.read_excel(file_path, skiprows=lambda x: x in list(range(0, 10)))
    return df

def transform_weather_data(data: pd.DataFrame) -> pd.DataFrame:
    """Function to create mean of city locations."""
    df = data.groupby([data['time'].dt.date]).mean() # Calculate mean for each date based of city locations
    df['sunshine_duration (min)'] = df['sunshine_duration (s)'].apply(lambda x: float(x/60)) # Convert seconds into min.
    df.drop(columns=['sunshine_duration (s)', 'location_id', 'weather_code (wmo code)', 'time'], inplace=True) # Drop columns
    df.reset_index(inplace=True) # Reset index to turn the date index into a column
    df = df.rename(columns={'time': 'date'}) # Rename
    df['date'] = pd.to_datetime(df['date']) #transform to datetime
    return df



