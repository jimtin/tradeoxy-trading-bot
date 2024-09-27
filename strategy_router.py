from strategies import test_strategy


# How the strategy file works
# 1. Passes it to the strategy function
# 2. The strategy function returns a signal
# 3. The signal is used to make a trading decision


def strategy_router(platform, symbol, timeframe, strategy_name):
    """
    Function to route the strategy based on the platform
    :param platform: The trading platform
    :param symbol: The trading symbol
    :param timeframe: The trading timeframe
    :param strategy_name: The name of the strategy
    """
    # Return an error if platform, symbol, or timeframe is None
    if platform is None:
        raise ValueError('The platform is None')
    if symbol is None:
        raise ValueError('The symbol is None')
    if timeframe is None:
        raise ValueError('The timeframe is None')
    if strategy_name == 'Test Strategy':
        try:
            # Get the trading signal from the test strategy
            signal = test_strategy.run_strategy(
                platform=platform,
                symbol=symbol,
                timeframe=timeframe
            )
        except Exception as exception:
            raise ValueError(f"An exception occurred when attempting to run the test strategy: {exception}")
    else:
        raise ValueError('Invalid strategy name')
    # If the signal['decision'] is buy, return a buy signal
    if signal['decision'] == 'buy':
        return 'buy'
    # If the signal['decision'] is sell, return a sell signal
    elif signal['decision'] == 'sell':
        return 'sell'
    # If the signal['decision'] is hold, return a hold signal
    elif signal['decision'] == 'hold':
        return 'hold'
    else:
        raise ValueError('Invalid signal decision')
