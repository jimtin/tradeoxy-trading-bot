import alpaca_markets as alpaca
import datetime
import indicators

# List of symbols
symbols = ["AAPL"]
max_number_of_candles = 1000
timeframe = "1hour"
indicator = "adx"

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
    #### Calculate the an indicator ####
    for symbol in symbols:
        # Save the symbol text
        symbol_text = symbol
        # Convert symbol to a list
        symbol = [symbol]
        # Get the historical data for the symbol
        symbol_historical_data = alpaca.get_historic_bars(
            symbols=symbol, 
            timeframe=timeframe, 
            start_date=start_date, 
            end_date=end_date, 
            limit=max_number_of_candles
        )
        # Calculate the specified indicator
        print(f"Calculating the {indicator} for {symbol_text}")
        indicator_result = indicators.calc_indicator(
            indicator_name=indicator,
            historical_data=symbol_historical_data,
            adx_period=14 
        )
        # Branch based on indicator_result
        if indicator_result["outcome"] == "calculated":
            # Print succcess
            print(f"The {indicator} was successfully calculated for {symbol_text}")
            # Extract the values
            values_dataframe = indicator_result["values"]
            print(values_dataframe)
            
        else:
            # Print and error
            print(f"An error occurred when calculating the {indicator} for {symbol_text}")
            # Print the full message
            print(indicator_result)
        


# Main function for program
if __name__ == "__main__":
    auto_run_trading_bot()
