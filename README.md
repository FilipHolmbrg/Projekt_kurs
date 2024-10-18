# Energy and Weather Data Analysis
This project explores how weather conditions, electricity prices and inflation data are connected, utilizing Python and R for data analysis and machine learning. Historical data on weather, electricity prices, and inflation is used to develop predictive models. The following is a breakdown of the files included in the project and their respective functions.
## Project Structure
### Data files
* `day_ahead_prices.csv`: Historical day-ahead prices, that will be used for analysis and predictions.
* `open-meteo-57.68N12.03E9m.xlsx`: Historical weather data for SE3, including temperature, precipitation and other weather conditions.
* `prc_hicp_manr_page_spreadsheet (1).xlsx`: Inflation rate data.
* `weather_price_data_vers3.db`: SQLite database that serves as the main data source for the project.
### Python Scripts
* `main.py`: The main script that loads, merges and prepares the data.
* `weather_data.py`: Script that fetches, cleanes and prepares weather data.
* `df_to_sql.py`: Script that coverts pandas DataFrames to SQL databases.
* `file_merger.py`: Merges the weather data and electricity prices into a dataset.
* `inflation_data.py`: Processes inflaion data and prepares it for integration with electricity price models.
* `price_data.py`: Electricity price data processing.
* `read_prices.py`: Reads data form the CSV file and preforms initial transformations.
### R Scripts
* `final_models.R`: Used for building regression models to predict electricity prices based on the weather and inflation data.
### Usage
1. __Setup__:
  * Ensure that the requiered Python libraries are installed. You can install the libraries using the `requierments.txt` or manually via `pip`:
  ``` 
  pip install pandas numpy scikit-learn sqlite3 openpyxl
  ```
  * Register for an account on [Entsoe](https://transparency.entsoe.eu/dashboard/show) and request an API key.
  * On row 8 in `price_data.py`, change `api_key` to your acquired API key from Entsoe.
2. __Data Preparation__:
  * Run the `main.py` script to load and merge data from the various sources.
  * The script will save the final dataset to an SQLite database for further analysis.
3. __Modeling__:
* After the dataset has been prepared, use the `final_models.R` script to build and evaluate regression models on the data. The R script is designed to handle the final cleaned dataset and train machine learning models (e.g., Random Forest, Linear Regression) to predict electricity prices.
