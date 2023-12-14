import alpaca_interactions as alpaca
import datetime

# List of symbols
symbols = ["AAPL"]
max_number_of_candles = 1000
timeframe = "30min"

# Function to run the trading bot
def auto_run_trading_bot():
    """
    Function to run the trading bot
    """
    # Print Welcome to your very own trading bot
    print("Welcome to your very own trading bot")
    # Set the end date to yesterday
    end_date = datetime.datetime.now() - datetime.timedelta(days=1) # Note that if you have a premium subscription you can remove this restriction
    # Set the start date to one year ago
    start_date = end_date - datetime.timedelta(days=365)
    # Get the historical data
    historical_data = alpaca.get_historic_bars(
        symbols=symbols, 
        timeframe=timeframe, 
        start_date=start_date, 
        end_date=end_date, 
        limit=max_number_of_candles
    )
    # Print the historical data
    print(historical_data)


# Main function for program
if __name__ == "__main__":
    auto_run_trading_bot()
