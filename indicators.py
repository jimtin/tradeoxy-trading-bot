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

    # Branch based on the indicator name
    if indicator_name == "rsi":
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
    # If the indicator name not recognised, raise a ValueError
    else:
        raise ValueError(f"The indicator {indicator_name} is not recognised.")

    # Return the indicator values
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
        rsi_values = talib.RSI(historical_data["close"], timeperiod=rsi_period)
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

    # Return the dictionary
    return return_dictionary
