import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import pandas as pd

# Load the required config from .env file under root directory.
load_dotenv()

# acquire all info and assign variables.
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

#Function for paper trading api or data only api
def api_access(type):
    if type == 'paper':
        try:
            api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, 'https://paper-api.alpaca.markets')
            account = api.get_account()
            status = account.status
            print(f"Paper API connected")
            return api
        except:
            raise Exception("Please configur the .env file under root directory")
    elif type == 'data':
        try:
            api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, 'https://data.alpaca.markets')
            start_date = pd.Timestamp("2020-06-01", tz="America/New_York").isoformat()
            end_date = pd.Timestamp("2020-06-05", tz="America/New_York").isoformat()
            api.get_bars("AAPL",timeframe = "1Day",start = start_date,end = end_date)
            print('Data API connected')
            return api
        except:
            raise Exception("Please configur the .env file under root directory")
            
