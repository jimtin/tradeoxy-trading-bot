import talib
import pandas


def calc_indicator(indicator_name: str, historical_data: pandas.DataFrame, **kwargs) -> dict:
    """
    Function to calculate a specified indicator
    :param indicator_name: The name of the indicator to calculate
    :param historical_data: The historical data to calculate the indicator from
    :param kwargs: Any additional arguments to pass to the indicator function
    """
    # Create a return dictionary
    return_dictionary = {
        "outcome": "unsuccessful",
        "indicator": indicator_name,
        "values": None,
        "indicator_outcome": None
    }

    # Get the name of the indicator from the indicator name
    indicator_name = indicator_name.lower()

    # Check for MACD
    if indicator_name == "macd":
        # Set the indicator to macd in the return dictionary
        return_dictionary["indicator"] = "macd"
        try:
            # Check the kwargs for the MACD fast period, MACD slow period and MACD signal period
            macd_fast_period = kwargs["macd_fast_period"]
            macd_slow_period = kwargs["macd_slow_period"]
            macd_signal_period = kwargs["macd_signal_period"]
            # Get the MACD values
            macd_data = calc_macd(
                historical_data=historical_data,
                macd_fast_period=macd_fast_period,
                macd_slow_period=macd_slow_period,
                macd_signal_period=macd_signal_period
            )
            # Set the values in the return dictionary
            return_dictionary["values"] = macd_data["values"]
            # Set the indicator outcome in the return dictionary
            return_dictionary["indicator_outcome"] = macd_data["indicator_outcome"]
            # Set the outcome to successful
            return_dictionary["outcome"] = "successful"

        except Exception as exception:
            print(f"An exception occurred when calculating the MACD: {exception}")
            raise exception
    elif indicator_name == "rsi":
        # Set the indicator to rsi in the return dictionary
        return_dictionary["indicator"] = "rsi"
        try:
            # Check the kwargs for the RSI period, rsi high and rsi low
            rsi_period = kwargs["rsi_period"]
            rsi_high = kwargs["rsi_high"]
            rsi_low = kwargs["rsi_low"]
            # Get the RSI values
            rsi_data = calc_rsi(
                historical_data=historical_data,
                rsi_period=rsi_period,
                rsi_high=rsi_high,
                rsi_low=rsi_low
            )
            # Set the values in the return dictionary
            return_dictionary["values"] = rsi_data["values"]
            # Set the indicator outcome in the return dictionary
            return_dictionary["indicator_outcome"] = rsi_data["indicator_outcome"]
            # Set the outcome to successful
            return_dictionary["outcome"] = "calculated"

        except Exception as exception:
            print(f"An exception occurred when calculating the RSI: {exception}")
            raise exception
    elif indicator_name == "bollinger":
        # Set the indicator to bollinger in the return dictionary
        return_dictionary["indicator"] = "bollinger"
        try:
            # Check the kwargs for the Bollinger Bands period and Bollinger Bands standard deviation
            bollinger_period = kwargs["bollinger_period"]
            bollinger_std = kwargs["bollinger_std"]
            # Get the Bollinger Bands values
            bollinger_data = calc_bollinger(
                historical_data=historical_data,
                bollinger_period=bollinger_period,
                bollinger_std=bollinger_std
            )
            # Set the values in the return dictionary
            return_dictionary["values"] = bollinger_data["values"]
            # Set the indicator outcome in the return dictionary
            return_dictionary["indicator_outcome"] = bollinger_data["indicator_outcome"]
            # Set the outcome to successful
            return_dictionary["outcome"] = "calculated"

        except Exception as exception:
            print(f"An exception occurred when calculating the Bollinger Bands: {exception}")
            raise exception
    # Add the Harami pattern
    elif indicator_name == "harami":
        # Set the indicator to harami in the return dictionary
        return_dictionary["indicator"] = "harami"
        try:
            # Get the Harami pattern
            harami_data = calc_harami(
                historical_data=historical_data
            )
            # Set the values in the return dictionary
            return_dictionary["values"] = harami_data["values"]
            # Set the indicator outcome in the return dictionary
            return_dictionary["indicator_outcome"] = harami_data["indicator_outcome"]
            # Set the outcome to successful
            return_dictionary["outcome"] = "calculated"

        except Exception as exception:
            print(f"An exception occurred when calculating the Harami pattern: {exception}")
            raise exception
    # If the indicator name not recognised, raise a ValueError
    else:
        raise ValueError(f"The indicator {indicator_name} is not recognised.")

    # Return the indicator values
    return return_dictionary


# Function to calculate the MACD technical indicator
def calc_macd(historical_data: pandas.DataFrame, macd_fast_period: int=12, macd_slow_period: int=26, macd_signal_period: int=9) -> dict:
    """
    Function to calculate the MACD technical indicator
    :param historical_data: The historical data to calculate the MACD from
    :param macd_fast_period: The MACD fast period
    :param macd_slow_period: The MACD slow period
    :param macd_signal_period: The MACD signal period
    """
    # Create a return dictionary
    return_dictionary = {
        "outcome": "unsuccessful",
        "indicator": "macd",
        "values": None,
        "indicator_outcome": None
    }

    # Check that the MACD fast period is greater than 0
    if macd_fast_period <= 0:
        raise ValueError("The MACD fast period must be greater than 0.")
    # Check that the MACD slow period is greater than 0
    if macd_slow_period <= 0:
        raise ValueError("The MACD slow period must be greater than 0.")
    # Check that the MACD signal period is greater than 0
    if macd_signal_period <= 0:
        raise ValueError("The MACD signal period must be greater than 0.")
    # Check that the MACD fast period is less than the MACD slow period
    if macd_fast_period >= macd_slow_period:
        raise ValueError("The MACD fast period must be less than the MACD slow period.")
    # Check that the MACD signal period is less than the MACD slow period
    if macd_signal_period >= macd_slow_period:
        raise ValueError("The MACD signal period must be less than the MACD slow period.")
    # Check that the length of the dataframe is greater than the MACD slow period
    if len(historical_data) < macd_slow_period:
        raise ValueError("The length of the dataframe must be greater than the MACD slow period.")

    try:
        # Get the MACD values
        macd_values, macd_signal_values, macd_histogram_values = talib.MACD(
            historical_data["candle_close"],
            fastperiod=macd_fast_period,
            slowperiod=macd_slow_period,
            signalperiod=macd_signal_period
        )
    except Exception as exception:
        print(f"An exception occurred when calculating the MACD: {exception}")
        raise exception
    
    # Add the MACD values to the historical data
    historical_data["macd"] = macd_values
    # Add the MACD signal values to the historical data
    historical_data["macd_signal"] = macd_signal_values
    # Add the MACD histogram values to the historical data
    historical_data["macd_histogram"] = macd_histogram_values

    # Create a column called "macd_indication"
    historical_data["macd_indication"] = "hold"
    # Set the macd_indication to overbought when the MACD is greater than the MACD signal
    historical_data.loc[historical_data["macd"] > historical_data["macd_signal"], "macd_indication"] = "overbought"
    # Set the macd_indication to oversold when the MACD is less than the MACD signal
    historical_data.loc[historical_data["macd"] < historical_data["macd_signal"], "macd_indication"] = "oversold"

    # Get the last row of the historical data and get the MACD indication. Set this to value of indicator_outcome in return_dictionary
    return_dictionary["indicator_outcome"] = historical_data["macd_indication"].iloc[-1]

    # Add the values to the return dictionary
    return_dictionary["values"] = historical_data
    # Set the outcome to successful
    return_dictionary["outcome"] = "successful"

    # Return the dictionary
    return return_dictionary


# Function to calculate the RSI
def calc_rsi(historical_data: pandas.DataFrame, rsi_period: int=14, rsi_high: int=70, rsi_low: int=30) -> dict:
    """
    Function to calculate the RSI
    :param historical_data: The historical data to calculate the RSI from
    :param kwargs: Any additional arguments to pass to the RSI function
    """
    # Create a return dictionary
    return_dictionary = {
        "outcome": "unsuccessful",
        "indicator": "rsi",
        "values": None,
        "indicator_outcome": None
    }

    # Check that the RSI period is greater than 0
    if rsi_period <= 0:
        raise ValueError("The RSI period must be greater than 0.")
    # Check that the length of the dataframe is greater than the RSI period
    if len(historical_data) < rsi_period:
        raise ValueError("The length of the dataframe must be greater than the RSI period.")

    try:
        # Get the RSI values
        rsi_values = talib.RSI(historical_data["candle_close"], timeperiod=rsi_period)
    except Exception as exception:
        print(f"An exception occurred when calculating the RSI: {exception}")
        raise exception

    # Add the RSI values to the historical data
    historical_data["rsi"] = rsi_values

    # Set the outcome to successful
    return_dictionary["outcome"] = "calculated"

    # Create a new column called rsi_signal and set the value to hold
    historical_data["rsi_signal"] = "hold"
    # Set the rsi_signal to oversold when the RSI is less than 30
    historical_data.loc[historical_data["rsi"] < rsi_low, "rsi_signal"] = "oversold"
    # Set the rsi_signal to overbought when the RSI is greater than 70
    historical_data.loc[historical_data["rsi"] > rsi_high, "rsi_signal"] = "overbought"

    # Get the last row of the historical data and get the RSI signal. Set this to value of indicator_outcome in return_dictionary
    return_dictionary["indicator_outcome"] = historical_data["rsi_signal"].iloc[-1]

    # Add the values to the return dictionary
    return_dictionary["values"] = historical_data

    # Return the dictionary
    return return_dictionary


# Function to calculate Bollinger Bands
def calc_bollinger(historical_data: pandas.DataFrame, bollinger_period: int=20, bollinger_std: int=2) -> dict:
    """
    Function to calculate Bollinger Bands
    :param historical_data: The historical data to calculate the Bollinger Bands from
    :param bollinger_period: The Bollinger Bands period
    :param bollinger_std: The Bollinger Bands standard deviation
    """
    # Create a return dictionary
    return_dictionary = {
        "outcome": "unsuccessful",
        "indicator": "bollinger",
        "values": None,
        "indicator_outcome": None
    }

    # Check that the Bollinger Bands period is greater than 0
    if bollinger_period <= 0:
        raise ValueError("The Bollinger Bands period must be greater than 0.")
    # Check that the length of the dataframe is greater than the Bollinger Bands period
    if len(historical_data) < bollinger_period:
        raise ValueError("The length of the dataframe must be greater than the Bollinger Bands period.")

    try:
        # Get the Bollinger Bands values
        upper_band, middle_band, lower_band = talib.BBANDS(
            historical_data["candle_close"],
            timeperiod=bollinger_period,
            nbdevup=bollinger_std,
            nbdevdn=bollinger_std
        )
    except Exception as exception:
        print(f"An exception occurred when calculating the Bollinger Bands: {exception}")
        raise exception

    # Add the Bollinger Bands values to the historical data
    historical_data["bollinger_upper_band"] = upper_band
    historical_data["bollinger_middle_band"] = middle_band
    historical_data["bollinger_lower_band"] = lower_band

    # Create a new column called bollinger_signal and set the value to hold
    historical_data["bollinger_signal"] = "hold"
    # Set the bollinger_signal to oversold when the candle_close is less than the lower_band
    historical_data.loc[historical_data["candle_close"] < lower_band, "bollinger_signal"] = "oversold"
    # Set the bollinger_signal to overbought when the candle_close is greater than the upper_band
    historical_data.loc[historical_data["candle_close"] > upper_band, "bollinger_signal"] = "overbought"
    
    # Get the last row of the historical data and get the Bollinger Bands signal. Set this to value of indicator_outcome in return_dictionary
    return_dictionary["indicator_outcome"] = historical_data["bollinger_signal"].iloc[-1]
    
    # Add the values to the return dictionary
    return_dictionary["values"] = historical_data
    
    # Set the outcome to successful
    return_dictionary["outcome"] = "calculated"
    
    # Return the dictionary
    return return_dictionary


# Calculate the Harami candlestick pattern
def calc_harami(historical_data: pandas.DataFrame) -> dict:
    """
    Function to calculate the Harami candlestick pattern
    :param historical_data: The historical data to calculate the Harami candlestick pattern from
    """
    # Create a return dictionary
    return_dictionary = {
        "outcome": "unsuccessful",
        "indicator": "harami",
        "values": None,
        "indicator_outcome": None
    }

    # Check that the length of the dataframe is greater than 1
    if len(historical_data) < 2:
        raise ValueError("The length of the dataframe must be greater than 1 to calculate the Harami candlestick pattern.")
    
    # Calculate the Harami pattern using the TA Lib function cdlharami
    harami_pattern = talib.CDLHARAMI(
        historical_data["candle_open"],
        historical_data["candle_high"],
        historical_data["candle_low"],
        historical_data["candle_close"]
    )
    
    # Add the Harami pattern to the historical data
    historical_data["harami_pattern"] = harami_pattern    
    
    # Create a new column called harami_signal and set the value to hold
    historical_data["harami_signal"] = "hold"
    
    # Set the harami_signal to bearish when the Harami pattern is less than 0
    historical_data.loc[historical_data["harami_pattern"] < 0, "harami_signal"] = "bearish"
    # Set the harami_signal to bullish when the Harami pattern is greater than 0
    historical_data.loc[historical_data["harami_pattern"] > 0, "harami_signal"] = "bullish"
    
    # Get the last row of the historical data and get the Harami signal. Set this to value of indicator_outcome in return_dictionary
    return_dictionary["indicator_outcome"] = historical_data["harami_signal"].iloc[-1]

    # Add the values to the return dictionary
    return_dictionary["values"] = historical_data

    # Set the outcome to successful
    return_dictionary["outcome"] = "calculated"

    # Return the dictionary
    return return_dictionary
