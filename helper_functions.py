import metatrader_interface
import discord_interaction
import concurrent.futures


# Function to get a list of symbols for a given platform
def get_symbols(platform: str) -> list:
    """
    Function to get a list of symbols for a given platform
    """
    # If the platform is MetaTrader 5
    if platform == 'MetaTrader 5':
        # Get the symbols from MetaTrader 5
        symbols = metatrader_interface.get_my_symbols()
    else:
        raise Exception("The platform is not supported")
    return symbols


# Function to start and test the Discord bot
def start_and_test_discord_bot(token: str) -> bool:
    """
    Function to start and test the Discord bot
    """
    # Start the Discord bot in a separate thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(discord_interaction.start_discord_bot, token)
    # Send a test message
    test_message = discord_interaction.test_message()
    return True

