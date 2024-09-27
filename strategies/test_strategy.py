import helper_functions as helpers


# Function test function
def run_strategy(platform, symbol, timeframe):
    """
    Function to test the strategy
    :param platform: The trading platform
    :param symbol: The trading symbol
    :param timeframe: The trading timeframe
    """
    # Define the platforms this strategy is compatible with
    platforms = ['MetaTrader5']
    # If the platform is not supported, raise an exception
    if platform not in platforms:
        raise ValueError('The platform is not supported')
    # Define a signal variable
    signal = {
        'decision': 'hold',
        'entry': None,
        'exit': None
    }
    # Retrieve the data for the symbol and timeframe
    dataframe = helpers.get_data(
        platform=platform,
        symbol=symbol,
        timeframe=timeframe
    )
    # Get the last row of the dataframe
    last_row = dataframe.iloc[-1]
    # Get the close price from the last row
    close = last_row['candle_close']
    # Get the second last row of the dataframe
    second_last_row = dataframe.iloc[-2]
    # Get the close price from the second last row
    second_last_close = second_last_row['candle_close']
    # If the second last close price is greater than the close price
    if second_last_close > close:
        # Return a buy signal with an entry price 1% above the close price and an exit price 2% above the close price
        signal['decision'] = 'buy'
        signal['entry'] = close * 1.01
        signal['exit'] = close * 1.02
    # If the second last close price is less than the close price
    elif second_last_close < close:
        # Return a sell signal with an entry price 1% below the close price and an exit price 2% below the close price
        signal['decision'] = 'sell'
        signal['entry'] = close * 0.99
        signal['exit'] = close * 0.98
    # If the second last close price is equal to the close price
    else:
        # Return a hold signal
        signal['decision'] = 'hold'
    return signal
