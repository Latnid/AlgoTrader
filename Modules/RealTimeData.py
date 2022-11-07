from alpaca.data.live import CryptoDataStream
import Authorization
import asyncio

# Asign Key and secret value
API_KEY = Authorization.ALPACA_API_KEY
SECRET_KEY = Authorization.ALPACA_SECRET_KEY
# Initiate class
crypto_stream = CryptoDataStream(API_KEY, SECRET_KEY)


# define callback function to print the bar upon reciving.
async def bar_callback(bar):
    for property_name, value in bar: 
        print(f"\"{property_name}\": {value}")
        
# Subscribing to bar event 
symbol = "BTC/USD"
crypto_stream.subscribe_updated_bars(bar_callback, symbol)

crypto_stream.run()