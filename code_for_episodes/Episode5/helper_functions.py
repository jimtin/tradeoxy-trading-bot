import metatrader_interface
import discord_interaction
import concurrent.futures
import os
import json


# Function to get a list of symbols for a given platform
def get_symbols(platform: str) -> list:
    """
    Function to get a list of symbols for a given platform
    """
    # If the platform is MetaTrader 5
    if platform == 'MetaTrader5':
        # Get the symbols from MetaTrader 5
        symbols = metatrader_interface.get_my_symbols()
    else:
        raise Exception("The platform is not supported")
    return symbols


# Function to start and test the Discord bot
def start_and_test_discord_bot(token: str=None) -> bool:
    """
    Function to start and test the Discord bot
    """
    # If the token is not provided, get it from the .env file
    if not token:
        token = os.getenv('discord_key')
    # Start the Discord bot in a separate thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(discord_interaction.start_discord_bot, token)
        print(f"Discord bot started: {future.result()}")
    # Send a test message
    test_message = discord_interaction.test_message()
    return True


# Function to get a list of timeframes for a given platform
def get_timeframes(platform: str) -> list:
    """
    Function to get a list of timeframes for a given platform
    """
    # If the platform is MetaTrader 5
    if platform == 'MetaTrader5':
        # Read the timeframes from the JSON file
        with open('static_content/timeframes.json', 'r') as file:
            timeframes = json.load(file)
        # Retrieve the list of timeframes
        timeframes = timeframes['MetaTrader5']
    else:
        raise Exception("The platform is not supported")
    return timeframes

# Function to get a list of strategies for a given platform
def get_strategies(platform: str) -> list:
    """
    Function to get a list of strategies for a given platform
    """
    # Create the list of strategies
    strategies_list = []
    # If the platform is MetaTrader 5
    if platform == 'MetaTrader5':
        # Read the strategies from the JSON file
        with open('static_content/strategies.json', 'r') as file:
            strategies = json.load(file)
        # Iterate through the strategies
        for strategy in strategies['strategies']:
            # Get the list of platforms for the strategy
            strategy_platforms = strategy['platforms']
            # If the platform is supported
            for platform in strategy_platforms:
                if platform == 'MetaTrader5':
                    # Get the list of strategies for MetaTrader 5
                    strategies_list.append(strategy['name'])
    else:
        raise Exception("The platform is not supported")
    return strategies_list


# Function to get the information for a given platform
def get_platform_info(platform: str, st_symbol, st_timeframe):
    """
    Function to get the information for a given platform
    """
    # If the platform is MetaTrader 5
    if platform == 'MetaTrader5':
        # Get the symbols from MetaTrader 5
        symbols = get_symbols('MetaTrader5')
        # Get the timeframes from MetaTrader 5
        timeframes = get_timeframes('MetaTrader5')
        # Get the strategies from MetaTrader 5
        strategies = get_strategies('MetaTrader5')
    else:
        raise Exception("The platform is not supported")
   
    return symbols, timeframes, strategies


# Function to get data for a given platform
def get_data(platform: str, symbol: str, timeframe: str) -> bool:
    """
    Function to get data for a given platform
    """
    # If the platform is MetaTrader 5
    if platform == 'MetaTrader5':
        try:
            # Get the historic data from MetaTrader 5
            data = metatrader_interface.get_historic_data(symbol, timeframe)
        except Exception as exception:
            raise ValueError(f"An exception occurred when attempting to get data from MetaTrader 5. get_data in helper_functions: {exception}")
    else:
        raise Exception("The platform is not supported")
    return data
    
