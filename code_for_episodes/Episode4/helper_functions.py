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
    else:
        raise Exception("The platform is not supported")
   
    return symbols, timeframes


# Function to get data for a given platform
def get_data(platform: str, symbol: str, timeframe: str) -> bool:
    """
    Function to get data for a given platform
    """
    # If the platform is MetaTrader 5
    if platform == 'MetaTrader5':
        # Get the historic data from MetaTrader 5
        data = metatrader_interface.get_historic_data(symbol, timeframe)
    else:
        raise Exception("The platform is not supported")
    return data
