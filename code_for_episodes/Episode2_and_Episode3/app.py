import streamlit
import discord_interaction
import metatrader_interface
import dotenv
import os
import helper_functions



if __name__ == '__main__':
    #### Streamlit Setup ####
    # Start the streamlit app
    streamlit.set_page_config(
        page_title='TradeOxy Terminal',
        page_icon='📈',
        layout='wide'
    )
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
    # Add an option to use a settings file
    settings_file = settings_choice.selectbox(
        'Use Settings File',
        ['Yes', 'No'],
        index=None,
        placeholder='Select an option'
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
        ['Alpaca', 'MetaTrader 5'],
        index=None,
        placeholder='Select a trading platform'
    )
    # Branch based on the trading platform selection
    if trading_platform_selection == 'MetaTrader 5':
        if settings_file == 'Yes':
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
                    copilot_container.success("MetaTrader 5 started successfully")
                    # Load the symbols from MetaTrader 5
                    symbols = helper_functions.get_symbols('MetaTrader 5')
                    # Populate the symbols dropdown
                    symbol = copilot_container.selectbox(
                        'Symbol', 
                        symbols, 
                        index=None, 
                        key=None, 
                        help=None, 
                        on_change=None, 
                        args=None, 
                        kwargs=None
                    )
                else:
                    copilot_container.error(f"MetaTrader 5 failed to start. Reason: {mt5_start}")
            except Exception as exception:
                copilot_container.error(f"An exception occurred when starting MetaTrader 5: {exception}")
    elif trading_platform_selection == 'Alpaca':
        if settings_file == 'Yes':
            # Load environment variables from the .env file
            dotenv.load_dotenv()
            # Get the Alpaca API key and secret key from the .env file
            alpaca_api_key = os.getenv('alpaca_api_key')
            alpaca_api_secret_key = os.getenv('alpaca_api_secret_key')
        else:
            # Add a text input to the third column
            alpaca_api_key = trading_platform.text_input('API Key', value='', max_chars=None, key=None, type='default')
            # Add a text input to the fourth column
            alpaca_api_secret_key = trading_platform.text_input('Secret Key', value='', max_chars=None, key=None, type='password')
    # Add a selectbox to the fourth column
    make_trades = settings.selectbox(
        'Make Trades', 
        ['Yes', 'No'],
        index=None,
        placeholder='Select an option'
    )
    
