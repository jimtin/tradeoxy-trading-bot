import pandas
import indicators


# Function to branch based on the strategy name
def calc_strategy(strategy_name: str, historical_data: pandas.DataFrame, **kwargs) -> dict:
    """
    Function to calculate a specified strategy
    :param strategy_name: The name of the strategy to calculate
    :param historical_data: The historical data to calculate the strategy from
    :param kwargs: Any additional arguments to pass to the strategy function
    """
    # Create a return dictionary
    return_dictionary = {
        "outcome": "unsuccessful",
        "strategy": strategy_name,
        "values": None,
        "strategy_outcome": None
    }

    # Get the name of the strategy from the strategy name
    strategy_name = strategy_name.lower()

    # Branch based on the strategy name
    if strategy_name == "rsi_high_low":
        try:
            # Check the kwargs for the RSI period, rsi high and rsi low
            rsi_period = kwargs["rsi_period"]
            rsi_high = kwargs["rsi_high"]
            rsi_low = kwargs["rsi_low"]
            # Get the RSI values
            rsi_data = calc_rsi_high_low_strategy(
                historical_data=historical_data,
                rsi_period=rsi_period,
                rsi_high=rsi_high,
                rsi_low=rsi_low
            )
            # Set the values in the return dictionary
            return_dictionary["values"] = rsi_data["values"]
            # Set the strategy outcome in the return dictionary
            return_dictionary["strategy_outcome"] = rsi_data["strategy_outcome"]
            # Set the outcome to successful
            return_dictionary["outcome"] = "successful"

        except Exception as exception:
            print(f"An exception occurred when calculating the RSI High Low strategy: {exception}")
            raise exception

    return return_dictionary


# Simple RSI strategy that uses the RSI High and Low values to determine when to buy and sell
def calc_rsi_high_low_strategy(historical_data: pandas.DataFrame, rsi_period: int, rsi_high: int, rsi_low: int) -> dict:
    """
    Function to calculate the RSI High Low strategy
    :param historical_data: The historical data to calculate the strategy from
    :param rsi_period: The RSI period to use
    :param rsi_high: The RSI high value
    :param rsi_low: The RSI low value
    """
    # Create a return dictionary
    return_dictionary = {
        "outcome": "unsuccessful",
        "strategy": "rsi_high_low",
        "values": None,
        "strategy_outcome": None
    }

    try:
        # Calculate the RSI
        rsi_data = indicators.calc_rsi(
            historical_data=historical_data,
            rsi_period=rsi_period,
            rsi_high=rsi_high,
            rsi_low=rsi_low
        )
        # Extract the rsi values from rsi_data
        rsi_values = rsi_data["values"]
        # Add in a column for entry, stop loss and take profit prices
        rsi_values["entry_price"] = None
        rsi_values["stop_loss_price"] = None
        rsi_values["take_profit_price"] = None
        # Set the entry_price to be the candle_close plus 1%
        rsi_values["entry_price"] = rsi_values["candle_close"] * 1.01
        # Set the stop_loss to be the close price
        rsi_values["stop_loss_price"] = rsi_values["candle_close"]
        # Set the take_profit to be the entry_price plus 3% of the close price
        rsi_values["take_profit_price"] = rsi_values["entry_price"] * 1.03
        # Set the values in the return dictionary
        return_dictionary["values"] = rsi_data["values"]
        # Set the strategy outcome in the return dictionary
        return_dictionary["strategy_outcome"] = rsi_data["indicator_outcome"]
        # Set the outcome to successful
        return_dictionary["outcome"] = "successful"

    except Exception as exception:
        print(f"An exception occurred when calculating the RSI High Low strategy: {exception}")
        raise exception

    return return_dictionary
