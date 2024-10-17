import pandas as pd

def read_inflation_data() -> pd.DataFrame:
    """Function to read inflation data saved localy as .xlsx file in working directory"""
    file_path = r'./example_data/prc_hicp_manr_page_spreadsheet (1).xlsx'
    df = pd.read_excel(file_path, skiprows=lambda x: x in list(range(0, 9)), sheet_name='Sheet 1')
    return df

def transform_inflation_data(df: pd.DataFrame) -> pd.DataFrame:
    """Function to clean and transform inflation data"""
    df.rename(columns={'Unnamed: 1': 'inflation'}, inplace=True)
    df.replace({':': None, 'not available': None}, inplace=True)
    df_cleaned = df.dropna(subset = 'inflation')
    df = df_cleaned.drop(columns=['Unnamed: 2'])
    df['TIME'] = pd.to_datetime(df['TIME'], format='%Y-%m')

    def expand_month(row: int) -> pd.DataFrame:
        """Function to expand each month to all dates in that month"""
        # Generate a date range for the entire month
        dates = pd.date_range(start=row['TIME'], end=row['TIME'] + pd.offsets.MonthEnd(0), freq='D')
        # Create a DataFrame for these dates, repeating the inflation value
        return pd.DataFrame({'date': dates, 'inflation': row['inflation']})
    
    df_expanded = pd.concat([expand_month(row) for _, row in df.iterrows()], ignore_index=True)
    df_expanded['date'] = pd.to_datetime(df_expanded['date']) # Transform into datetime
    return df_expanded