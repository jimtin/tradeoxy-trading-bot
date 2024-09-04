import streamlit
import discord_interaction
import metatrader_interface


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
    alert_listener, trading_platform, col3, col4 = header_container.columns(4)
    # Create a copilot container
    copilot_container = streamlit.container()
    # Configure the alert listener column #
    # Add a dropdown to the alert listener column
    alerting_option = alert_listener.selectbox(
        'Alert Listener', 
        ['Discord', 'Direct'], 
        index=None,
        placeholder='Select an alerting option'
    )
    if alerting_option == 'Discord':
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
        # Add four text inputs to the third column
        mt5_username = col3.text_input('Username', value='', max_chars=None, key=None, type='default')
        print(mt5_username)
        mt5_password = col3.text_input('Password', value='', max_chars=None, key=None, type='password')
        print(mt5_password)
        mt5_server = col3.text_input('Server', value='', max_chars=None, key=None, type='default')
        print(mt5_server)
        mt5_filepath = col3.text_input('Filepath', value='', max_chars=None, key=None, type='default')
        print(mt5_filepath)
        # When all four text inputs are filled, try to open the terminal
        if mt5_username and mt5_password and mt5_server and mt5_filepath:
            # Write a message to the copilot container
            copilot_container.write('Starting MetaTrader 5...')
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
                    mt5_login = MetaTrader5.login(
                        login=mt5_username,
                        password=mt5_password,
                        server=mt5_server
                    )
                    if mt5_login:
                        print("Logged in to MetaTrader 5")
                    else:
                        print("MetaTrader 5 failed to log in")
            except Exception as exception:
                copilot_container.error(f"An exception occurred when starting MetaTrader 5: {exception}")
    elif trading_platform_selection == 'Alpaca':
        # Add a text input to the third column
        alpaca_api_key = col3.text_input('API Key', value='', max_chars=None, key=None, type='default')
        # Add a text input to the fourth column
        alpaca_api_secret_key = col3.text_input('Secret Key', value='', max_chars=None, key=None, type='password')
    # Add a selectbox to the fourth column
    make_trades = col4.selectbox(
        'Make Trades', 
        ['Yes', 'No'],
        index=None,
        placeholder='Select an option'
    )
    # Add a button to the fourth column
    col4.button('Begin')
    
        
     
