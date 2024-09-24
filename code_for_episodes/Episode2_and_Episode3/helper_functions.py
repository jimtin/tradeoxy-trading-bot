import metatrader_interface


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

