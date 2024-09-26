import streamlit
import discord_interaction
import metatrader_interface
import dotenv
import os
import helper_functions



# Function to get the data for button push
def get_data():
    """
    Function to get the data for button push
    """
    # Get the platform from the session state
    platform = streamlit.session_state['platform']
    # If the platform state is None, write an error message to the copilot container
    if platform is None:
        copilot_container.error("Please select a platform")
        return False
    else:
        # If the platform is MetaTrader 5, make sure the platform is MetaTrader5
        if platform == 'MetaTrader 5':
            platform = 'MetaTrader5'
    # Get the symbol and timeframe from the session state
    symbol = streamlit.session_state['symbol']
    # If the symbol state is None, write an error message to the copilot container
    if symbol is None:
        copilot_container.error("Please select a symbol")
        return False
    # Get the timeframe from the session state
    timeframe = streamlit.session_state['timeframe']
    # If the timeframe state is None, write an error message to the copilot container
    if timeframe is None:
        copilot_container.error("Please select a timeframe")
        return False
    # Run the get_data function from the helper_functions.py file
    try:
        data = helper_functions.get_data(
            platform=platform,
            symbol=symbol,
            timeframe=timeframe
        )
        # Write the dataframe to the copilot container
        copilot_container.write(data)
    except Exception as exception:
        copilot_container.error(f"An exception occurred when getting data: {exception}")
        return False
    return True


# Function to get information for a given platform
def get_platform_info():
    """
    Function to get information for a given platform
    :param platform: The platform to get information for
    :param container: The container to add the widgets to
    """
    # Set up branching variables
    platform_connected = False
    # Get the platform from the session state
    platform = streamlit.session_state['platform']
    # Get the settings file selection from the session state
    settings_file = streamlit.session_state['settings_file']
    # Get any required information based on the platform
    if platform == "MetaTrader 5":
        if settings_file == "Yes":
            # Load environment variables from the .env file
            dotenv.load_dotenv()
            # Get the MetaTrader 5 username, password, server, and filepath from the .env file
            mt5_username = os.getenv('metatrader_username')
            mt5_password = os.getenv('metatrader_password')
            mt5_server = os.getenv('metatrader_server')
            mt5_filepath = os.getenv('metatrader_filepath')
        else:
            # Add four text inputs to the third column
            mt5_username = trading_platform.text_input('Username', value='', max_chars=None, key=None, type='default')
            mt5_password = trading_platform.text_input('Password', value='', max_chars=None, key=None, type='password')
            mt5_server = trading_platform.text_input('Server', value='', max_chars=None, key=None, type='default')
            mt5_filepath = trading_platform.text_input('Filepath', value='', max_chars=None, key=None, type='default')
        # When all four text inputs are filled, try to open the terminal
        if mt5_username and mt5_password and mt5_server and mt5_filepath:
            try:
                # Start MetaTrader 5
                mt5_start = metatrader_interface.start_metatrader(
                    mt5_username=mt5_username, 
                    mt5_password=mt5_password, 
                    mt5_server=mt5_server, 
                    mt5_filepath=mt5_filepath
                )
                # If successful, log in to MetaTrader 5
                if mt5_start:
                    copilot_container.success("MetaTrader5 started successfully")
                    platform_connected = True
                else:
                    copilot_container.error(f"MetaTrader 5 failed to start. Reason: {mt5_start}")
            except Exception as exception:
                copilot_container.error(f"An exception occurred when starting MetaTrader 5: {exception}")   
    else:
        print(f"{platform} is not supported yet.")
    # Check if the platform is connected
    if platform_connected is False:
        raise Exception(f"Failed to connect to {platform}")
    # Get the platform information
    symbols, timeframes = helper_functions.get_platform_info('MetaTrader5', symbol_st, timeframe_st)
    # Update the symbol and timeframe selectboxes
    streamlit.session_state['symbols'] = symbols
    streamlit.session_state['timeframes'] = timeframes
    return True
        


if __name__ == '__main__':
    #### Streamlit Setup ####
    # Start the streamlit app
    streamlit.set_page_config(
        page_title='TradeOxy Terminal',
        page_icon='📈',
        layout='wide'
    )
    # Create the session states
    if "settings_file" not in streamlit.session_state:
        streamlit.session_state.settings_file = None
    if "platform" not in streamlit.session_state:
        streamlit.session_state.platform = None
    if "symbol" not in streamlit.session_state:
        streamlit.session_state.symbol = None
    if "timeframe" not in streamlit.session_state:
        streamlit.session_state.timeframe = None
    if "symbols" not in streamlit.session_state:
        streamlit.session_state.symbols = []
    if "timeframes" not in streamlit.session_state:
        streamlit.session_state.timeframes = []
    # Create the header
    streamlit.header('TradeOxy Terminal')
    # Create the header container
    header_container = streamlit.container()
    # Create four columns in the header container
    settings_choice, alert_listener, trading_platform, settings = header_container.columns(4)
    # Create a start_stop container
    start_stop = streamlit.container()
    start_button = False
    # Create a start button
    if start_button == False:
        # Create a start button that stretches across the page and is green
        start = start_stop.button(
            'Start', 
            use_container_width=True
            )
        start_button = True
    # Create a copilot container
    copilot_container = streamlit.container()
    # Add a title to the copilot container
    copilot_container.header(
        'TradeOxy Intelligence Copilot'
    )
    # Create three columns in the copilot container
    symbol_st, timeframe_st, strategy_st = copilot_container.columns(3)
    # Add an empty dropdown to symbol_st and timeframe_st
    symbol_st.selectbox(
        'Symbol',
        streamlit.session_state['symbols'],
        index=None,
        key='symbol'
    )
    timeframe_st.selectbox(
        'Timeframe',
        streamlit.session_state['timeframes'],
        index=None,
        key='timeframe'
    )
    # Add a button to the Copilot container
    copilot_container.button('Get Data', on_click=get_data, use_container_width=True)
    # Add an option to use a settings file
    settings_file = settings_choice.selectbox(
        'Use Settings File',
        ['Yes', 'No'],
        index=None,
        placeholder='Select an option', 
        key='settings_file'
    )
    # Configure the alert listener column #
    # Add a dropdown to the alert listener column
    alerting_option = alert_listener.selectbox(
        'Alert Listener', 
        ['Discord', 'Direct'], 
        index=None,
        placeholder='Select an alerting option'
    )
    if alerting_option == 'Discord':
        copilot_container.write('Connecting to Discord...')
        if settings_file:
            # Load environment variables from the .env file
            dotenv.load_dotenv()
            # Get the Discord key from the .env file
            discord_key = os.getenv('discord_key')
        else:
            # Add a text input to the alert listener column
            discord_key = alert_listener.text_input('Discord Key', value='', max_chars=None, key=None, type='default')
    # Add a dropdown to the trading platform column
    trading_platform_selection = trading_platform.selectbox(
        'Trading Platform', 
        ['Alpaca', 'MetaTrader 5', 'Binance', 'Coinbase'],
        index=None,
        placeholder='Select a trading platform',
        on_change=get_platform_info, 
        key='platform'
    )
    # Add a selectbox to the fourth column
    make_trades = settings.selectbox(
        'Make Trades', 
        ['Yes', 'No'],
        index=None,
        placeholder='Select an option'
    )
    
    
        
     
