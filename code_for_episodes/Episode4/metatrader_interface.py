import os
import dotenv
import MetaTrader5
import pandas
import data_normalizer

# Load environment variables
dotenv.load_dotenv()

# Function to start MetaTrader 5
def start_metatrader(mt5_username=None, mt5_password=None, mt5_server=None, mt5_filepath=None):
    """
    Function to start MetaTrader 5
    """
    # If any the variables are None, try to get them from the .env file
    if not mt5_username or not mt5_password or not mt5_server or not mt5_filepath:
        uname = os.getenv(metatrader_username)
        pword = os.getenv(metatrader_password)
        server = os.getenv(metatrader_server)
        terminal64filepath = os.getenv(metatrader_filepath)
    # Otherwise, assign the variables
    else:
        uname = mt5_username
        pword = mt5_password
        server = mt5_server
        terminal64filepath = mt5_filepath
    # Check if the terminal64 file exists
    if not os.path.exists(terminal64filepath):
        raise Exception(f"The terminal64 file does not exist at the specified path {terminal64filepath}")
    # Convert the inputs to the right data types
    # Uname is a integer
    uname = int(uname)
    # Pword is a string
    pword = str(pword)
    # Server is a string
    server = str(server)
    # Filepath is a string
    terminal64filepath = str(terminal64filepath)
    # Try to start MetaTrader 5
    try:
        mt5_start = MetaTrader5.initialize(
            login=uname,
            password=pword,
            server=server,
            path=terminal64filepath
        )
    except Exception as exception:
        raise Exception(f"An exception occurred when starting MetaTrader 5: {exception}")
    # If successful, log in to MetaTrader 5
    if mt5_start:
        try:
            login = MetaTrader5.login(
                login=uname,
                password=pword,
                server=server
            )
        except Exception as exception:
            raise exception
        # If successful, return True
        if login:
            return True
        # If not successful, raise an exception
        else:
            print("MetaTrader 5 failed to log in")
            raise Exception("MetaTrader 5 failed to log in")
    else:
        print("MetaTrader 5 failed to start")
        raise Exception("MetaTrader 5 failed to start")


# Function to get a list of all the symbols in MetaTrader 5
def get_my_symbols():
    """
    Function to get a list of all the symbols in MetaTrader 5
    """
    # Get the symbols
    try:
        symbols = MetaTrader5.symbols_get()
    except Exception as exception:
        raise Exception(f"An exception occurred when getting the symbols for MetaTrader 5: {exception}")
    all_symbols = []
    # Iterate through the symbols and get the names
    for symbol in symbols:
        all_symbols.append(symbol.name)
    # Otherwise, return the symbols
    return all_symbols


# Function to get data from MetaTrader 5
def get_historic_data(symbol, timeframe):
    """
    Function to get data from MetaTrader 5
    """
    # Convert the timeframe to something MT5 friendly
    timeframe = convert_to_mt5_timeframe(timeframe)
    # Get the data
    try:
        data = MetaTrader5.copy_rates_from_pos(symbol, timeframe, 0, 10)
    except Exception as exception:
        raise Exception(f"An exception occurred when getting the data for MetaTrader 5: {exception}")
    # Convert the data to a DataFrame
    data = pandas.DataFrame(data)
    # Pass the data to the data normalizer
    data = data_normalizer.normalize_data_format(data, 'MetaTrader5')
    # Return the data
    return data


# Function to convert the timeframe to something MT5 friendly
def convert_to_mt5_timeframe(timeframe: str):
    """
    Function to convert the timeframe to something MT5 friendly
    """
    if timeframe == "M1":
        return MetaTrader5.TIMEFRAME_M1
    elif timeframe == "M2":
        return MetaTrader5.TIMEFRAME_M2
    elif timeframe == "M3":
        return MetaTrader5.TIMEFRAME_M3
    elif timeframe == "M4":
        return MetaTrader5.TIMEFRAME_M4
    elif timeframe == "M5":
        return MetaTrader5.TIMEFRAME_M5
    elif timeframe == "M6":
        return MetaTrader5.TIMEFRAME_M6
    elif timeframe == "M10":
        return MetaTrader5.TIMEFRAME_M10
    elif timeframe == "M12":
        return MetaTrader5.TIMEFRAME_M12
    elif timeframe == "M15":
        return MetaTrader5.TIMEFRAME_M15
    elif timeframe == "M20":
        return MetaTrader5.TIMEFRAME_M20
    elif timeframe == "M30":
        return MetaTrader5.TIMEFRAME_M30
    elif timeframe == "H1":
        return MetaTrader5.TIMEFRAME_H1
    elif timeframe == "H2":
        return MetaTrader5.TIMEFRAME_H2
    elif timeframe == "H3":
        return MetaTrader5.TIMEFRAME_H3
    elif timeframe == "H4":
        return MetaTrader5.TIMEFRAME_H4
    elif timeframe == "H6":
        return MetaTrader5.TIMEFRAME_H6
    elif timeframe == "H8":
        return MetaTrader5.TIMEFRAME_H8
    elif timeframe == "H12":
        return MetaTrader5.TIMEFRAME_H12
    elif timeframe == "D1":
        return MetaTrader5.TIMEFRAME_D1
    elif timeframe == "W1":
        return MetaTrader5.TIMEFRAME_W1
    elif timeframe == "MN1":
        return MetaTrader5.TIMEFRAME_MN1
    else:
        raise Exception("The timeframe is not supported")
