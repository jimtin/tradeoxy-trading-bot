import os
import requests
import pandas
import datetime

# Set the Alpaca.Markets API Key
API_KEY = os.getenv('ALPACA_API')
API_SECRET = os.getenv('ALPACA_SECRET_API')


# Base function for querying the Alpaca.Markets API
def query_alpaca_api(url: str, params: dict) -> dict:
    """
    Base function for querying the Alpaca.Markets API
    :param url: The URL to query
    :param params: The parameters to pass to the API
    """
    # Check that the API Key and Secret are not None
    if API_KEY is None:
        raise ValueError("The API Key is not set.")
    if API_SECRET is None:
        raise ValueError("The API Secret is not set.")
    
    # Set the header information
    headers = {
        'accept': 'application/json',
        'APCA-API-KEY-ID': API_KEY,
        'APCA-API-SECRET-KEY': API_SECRET
    }

    try:
        # Get the response from the API endpoint
        response = requests.get(url, headers=headers, params=params)
    except Exception as exception:
        print(f"An exception occurred when querying the URL {url} with the parameters {params}: {exception}")
        raise exception
    # Get the response code
    response_code = response.status_code
    # If the response code is 403, print that the API key and or secret are incorrect
    if response_code == 403:
        print("The API key and or secret are incorrect.")
        raise ValueError("The API key and or secret are incorrect.")
    # Convert the response to JSON
    json_response = response.json()

    # Return the JSON response
    return json_response


# Function to retrieve historical candlestick data from Alpaca.Markets
def get_historic_bars(symbols: list, timeframe: str, limit: int, start_date: datetime, end_date: datetime) -> pandas.DataFrame:
    """
    Function to retrieve historical candlestick data from Alpaca.Markets
    :param symbols: The symbols to retrieve the historical data for
    :param timeframe: The timeframe to retrieve the historical data for
    :param limit: The number of bars to retrieve
    :param start_date: The start date for the historical data
    :param end_date: The end date for the historical data
    """

    # Check that the start_date and end_date are datetime objects
    if not isinstance(start_date, datetime.datetime):
        print("The start_date must be a datetime object.")
        raise ValueError("The start_date must be a datetime object.")
    if not isinstance(end_date, datetime.datetime):
        raise ValueError("The end_date must be a datetime object.")

    # Check that the end date is not in the future
    if end_date > datetime.datetime.now():
        print("The end date is in the future. Setting the end date to now.")
        end_date = datetime.datetime.now()

    # Check that the start date is not after the end date
    if start_date > end_date:
        raise ValueError("The start date cannot be after the end date.")
    
    # Convert the symbols list to a comma-separated string
    symbols_joined = ",".join(symbols)

    # Set the start and end dates to the correct format - they should only include days
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    # Create the params dictionary
    params = {
        "symbols": symbols_joined,
        "timeframe": timeframe,
        "limit": limit,
        "start": start_date,
        "end": end_date,
        "adjustment": "raw",
        "feed": "iex",
        "sort": "asc"
    }
    
    # Set the API endpoint
    url = f"https://data.alpaca.markets/v2/stocks/bars"
    # Send to the base function to query the API
    try:
        json_response = query_alpaca_api(url, params)
    except Exception as exception:
        print(f"An exception occurred in the function get_historic_bars() with the parameters {params}: {exception}")
        raise exception

    # Extract the bars from the JSON response
    json_response = json_response["bars"]

    # Create an empty parent dataframe
    bars_df = pandas.DataFrame()

    # Iterate through the symbols list
    for symbol in symbols:
        # Extract the bars for the symbol
        symbol_bars = json_response[symbol]

        # Convert the bars to a dataframe
        symbol_bars_df = pandas.DataFrame(symbol_bars)

        # Add the symbol column
        symbol_bars_df["symbol"] = symbol

        # Modify the following column names to be more descriptive:
        # o -> candle_open
        # h -> candle_high
        # l -> candle_low
        # c -> candle_close
        # v -> candle_volume
        # t -> candle_timestamp
        # vw -> vwap
        # Rename the columns
        symbol_bars_df = symbol_bars_df.rename(
            columns={
                "o": "candle_open", 
                "h": "candle_high", 
                "l": "candle_low", 
                "c": "candle_close", 
                "v": "candle_volume", 
                "t": "candle_timestamp", 
                "vw": "vwap"
            }
        )

        # Add the symbol bars to the parent dataframe
        bars_df = pandas.concat([bars_df, symbol_bars_df])

    # Return the historical bars
    return bars_df
