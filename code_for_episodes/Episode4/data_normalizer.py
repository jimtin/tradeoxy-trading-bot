import pandas


# Function to normalize the data for a given platform
def normalize_data_format(data: pandas.DataFrame, platform) -> pandas.DataFrame:
    """
    Function to normalize the data for a given platform
    """
    # If the platform is MetaTrader 5
    if platform == 'MetaTrader5':
        # Rename the columns to match the expected format
        # time -> timestamp
        # open -> candle_open
        # high -> candle_high
        # low -> candle_low
        # close -> candle_close
        data = data.rename(columns={
            'time': 'timestamp',
            'open': 'candle_open',
            'high': 'candle_high',
            'low': 'candle_low',
            'close': 'candle_close',
        })
        # Convert the timestamp to a datetime object
        data['timestamp'] = pandas.to_datetime(data['timestamp'], unit='s')
    else:
        raise Exception("The platform is not supported")
    # Return the normalized data
    return data
