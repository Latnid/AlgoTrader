# #Use the Stream API
# from alpaca.data.live import StockDataStream
# import Authorization
# import asyncio
# from ConnectDB import *
# import time

# # Asign Key and secret value
# API_KEY = Authorization.ALPACA_API_KEY
# SECRET_KEY = Authorization.ALPACA_SECRET_KEY
# # Initiate class
# stock_stream = StockDataStream(API_KEY, SECRET_KEY)

# # Connect DataBase
# con,cur = connect_data_base()
# # prepare table_name as today's date
# table_name = "stockdata_" + datetime.date.today().strftime('%Y_%m_%d')
# # Create table if not esists.
# cur.execute("CREATE TABLE IF NOT EXISTS %s (symbol TEXT, timestamp TIMESTAMPTZ, open NUMERIC,high NUMERIC,low NUMERIC,close NUMERIC,volume NUMERIC,trade_count INTEGER,vwap NUMERIC);" %table_name)
# # excute SQL command
# con.commit()

# # define callback function to print the bar upon reciving.
# async def bar_callback(bar):
# # handle each property.
#     print(type(bar))
#     print(bar)

#     cur.execute("INSERT INTO %s (%s) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" %(table_name, bar.symbol, time.mktime(time.strptime(str(bar.timestamp), "%Y-%m-%d %H:%M:%S-05:00")), bar.open, bar.high, bar.low, bar.close, bar.volume, bar.trade_count, bar.vwap))

#     con.commit()
#     # for property_name, value in bar: 
#     #     if property_name == 'symbol':
#     #         print(f"\"{property_name}\": {value}")
#     #         symbol_value = value
#     #     elif property_name == 'timestamp':
#     #         date_str = str(value)
#     #         date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
#     #         timestamp_value = date_obj.timestamp()
#     #     elif property_name == 'open':
#     #         open_value = value
#     #     elif property_name == 'high':
#     #         high_value = value
#     #     elif property_name == 'low':
#     #         low_value = value
#     #     elif property_name == 'close':
#     #         close_vlaue = value
#     #     elif property_name == 'volume':
#     #         volume_value = value
#     #     elif property_name == 'trade_count':
#     #         trade_count_value = value
#     #     elif property_name == 'vwap':
#     #         vwap_value = value

# # Insert all data to database and excute.        

#     # cur.execute("INSERT INTO %s (symbol, timestamp, open, high, low, close, volume, trade_count, vwap) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" %(table_name, symbol_value, timestamp_value, open_value, high_value, low_value, close_vlaue, volume_value, trade_count_value, vwap_value))

#     # con.commit()
    
# # Subscribing to bar event 
# symbol = 'GOOGL'
# stock_stream.subscribe_bars(bar_callback, symbol)

# stock_stream.run()


# # Use websocket straight
# import Authorization

# from websocket import create_connection
# import simplejson as json
# import pprint

# API_KEY = Authorization.ALPACA_API_KEY
# SECRET_KEY = Authorization.ALPACA_SECRET_KEY

# url = 'wss://stream.data.alpaca.markets/v2/iex'
# ws = create_connection(url)
# print(json.loads(ws.recv())) #print the connection message

# auth_message = {"action": "auth", "key": API_KEY, "secret": SECRET_KEY}
# ws.send(json.dumps(auth_message))
# print(json.loads(ws.recv())) # print the authenticated message

# subscription = {"action":"subscribe","trades":["TSLA","MU"],"quotes":["TSLA","MU"],"bars":["TSLA","MU"]}
# ws.send(json.dumps(subscription))
# print(json.loads(ws.recv())) # print the subscribed message

# while True:
#     data = json.loads(ws.recv())
#     pprint.pprint(data[0])
#     print('*********************')



#Use the Stream API
from alpaca.data.live import CryptoDataStream
import Authorization
import asyncio
from ConnectDB import *
import time
import hvplot.pandas
import pandas as pd


# Asign Key and secret value
API_KEY = Authorization.ALPACA_API_KEY
SECRET_KEY = Authorization.ALPACA_SECRET_KEY
# Subscribing to bar event 
ticker = "BTC/USD"

# Initiate class
crypto_stream = CryptoDataStream(API_KEY, SECRET_KEY)
#df = pd.DataFrame(data=[], columns=['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'trade_count', 'vwap'])
# Connect DataBase
con,cur = connect_data_base()
# prepare table_name as today's date
table_name = "cryptodata_" + datetime.date.today().strftime('%Y_%m_%d')
# Create table if not esists.
cur.execute("CREATE TABLE IF NOT EXISTS %s (symbol TEXT, timestamp TIMESTAMPTZ, open NUMERIC,high NUMERIC,low NUMERIC,close NUMERIC,volume NUMERIC,trade_count INTEGER,vwap NUMERIC);" %table_name)
# excute SQL command
con.commit()

def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df

import hvplot.streamz



# define callback function to print the bar upon reciving.
async def bar_callback(bar):
    # for property_name, value in bar:
    #     print(f"\"{property_name}\": {value}")

    print(f"Data received !\n{type(bar)}\n{bar}")
     
    #  #Connect DataBase
    #  con,cur = connect_data_base()
    #  cur.execute("INSERT INTO %s (symbol, timestamp, open, high, low, close, volume, trade_count, vwap) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" %(table_name, bar.symbol, time.mktime(time.strptime(str(bar.timestamp), "%Y-%m-%d %H:%M:%S+00:00")), bar.open, bar.high, bar.low, bar.close, bar.volume, bar.trade_count, bar.vwap))
    #  cur.execute("INSERT INTO {} (symbol, timestamp, open, high, low, close, volume, trade_count, vwap) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {})".format(table_name, str(bar.symbol), time.mktime(time.strptime(str(bar.timestamp), "%Y-%m-%d %H:%M:%S+00:00")), bar.open, bar.high, bar.low, bar.close, bar.volume, bar.trade_count, bar.vwap))
    cur.execute("INSERT INTO {} (symbol, timestamp, open, high, low, close, volume, trade_count, vwap) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)".format(table_name),(bar.symbol, bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume, bar.trade_count,bar.vwap))
    #  cur.execute(f"""
    #     INSERT INTO {table_name} (symbol, timestamp, open, high, low, close, volume, trade_count, vwap) VALUES ({bar.symbol}, {str(bar.timestamp)}, {bar.open}, {bar.high}, {bar.low}, {bar.close}, {bar.volume}, {bar.trade_count}, {bar.vwap})
    #  """)
    con.commit()
    #  con.close()
    #df = postgresql_to_dataframe(conn=con, select_query="SELECT * FROM cryptodata_2022_11_09", column_names=['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'trade_count', 'vwap'])
    # cur.execute("SELECT * FROM cryptodata_2022_11_09 ORDER BY timestamp DESC LIMIT 60")
    #4 spaces or 1 tab
    # tupples = cur.fetchall()
    # df = pd.DataFrame(data=tupples, columns=['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'trade_count', 'vwap'])
    # print(df)
    # df.hvplot()
    

if __name__ == "__main__":
    # Connect DataBase
    # con,cur = connect_data_base()
    crypto_stream.subscribe_bars(bar_callback, ticker)
    crypto_stream.run()