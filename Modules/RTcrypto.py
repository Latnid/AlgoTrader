# Crypto RealTime Data using websocket.
import Authorization
from ConnectDB import *
from websocket import create_connection
import simplejson as json
import pprint
import pandas as pd

# Asign Key and secret value
API_KEY = Authorization.ALPACA_API_KEY
SECRET_KEY = Authorization.ALPACA_SECRET_KEY

# Connect DataBase
con,cur = connect_data_base()

url = 'wss://stream.data.alpaca.markets/v1beta2/crypto'
ws = create_connection(url)
print(json.loads(ws.recv())) #print the connection message

auth_message = {"action": "auth", "key": API_KEY, "secret": SECRET_KEY}
ws.send(json.dumps(auth_message))
print(json.loads(ws.recv())) # print the authenticated message

subscription = {"action":"subscribe","trades":["BTC/USD"],"quotes":["BTC/USD"],"bars":["BTC/USD"]}
ws.send(json.dumps(subscription))
print(json.loads(ws.recv())) # print the subscribed message

while True:
    # Receive and print data.
    data = json.loads(ws.recv())
    pprint.pprint(data[0])
    print('*********************')
    
    # Data organized.
    if data[0]['T'] == 'q':        
        Symbol = data[0]['S']
        Type = data[0]['T']
        Ask = data[0]['ap']
        Ask_size = data[0]['as']
        Bid = data[0]['bp']
        Bid_size = data[0]['bs']
        Time = data[0]['t']
        # Convert to NewYork Time
        Newyork_time = pd.Timestamp(Time, tz="America/New_York").isoformat().split('T')[0]
        # prepare table_name as today's date
        quote_table_name = "_" + Newyork_time.replace('-', '_') + '_crypto_quote'
        # Create table if not esists,
        cur.execute(
        "CREATE TABLE IF NOT EXISTS %s (symbol TEXT, time TIMESTAMPTZ, type TEXT, ask NUMERIC,\
        ask_size NUMERIC, bid NUMERIC, bid_size NUMERIC);" %quote_table_name)
        # excute SQL command
        con.commit()
        # Insert all data to database and excute.  
        cur.execute("INSERT INTO {} (symbol, Time, Type, Ask, Ask_size, Bid, Bid_size) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(quote_table_name),
        (Symbol, Time, Type, Ask, Ask_size, Bid, Bid_size))
        # excute query
        con.commit()
    
    elif data[0]['T'] == 't':
        Symbol = data[0]['S']
        Type = data[0]['T']
        Trade_id = data[0]['i']
        Trade_price = data[0]['p']
        Trade_size = data[0]['s']
        Taker_side  = data[0]['tks']
        Time = data[0]['t']
        # Convert to NewYork Time
        Newyork_time = pd.Timestamp(Time, tz="America/New_York").isoformat().split('T')[0]
        # prepare table_name as today's date
        trade_table_name = "_" + Newyork_time.replace('-', '_') + '_crypto_trade'
        # Create table if not esists
        cur.execute(
        "CREATE TABLE IF NOT EXISTS %s (symbol TEXT, time TIMESTAMPTZ, type TEXT, id NUMERIC,\
        price NUMERIC, size NUMERIC, side TEXT);" %trade_table_name)
        # excute SQL command
        con.commit()
        # Insert all data to database and excute.  
        cur.execute("INSERT INTO {} (symbol, time, type, id, price, size, side) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(trade_table_name),
        (Symbol, Time, Type, Trade_id, Trade_price, Trade_size, Taker_side))
        con.commit()
        
    elif data[0]['T'] == 'b':
        Symbol = data[0]['S']
        Type = data[0]['T']
        Close_price = data[0]['c']
        High_price = data[0]['h']
        Low_price = data[0]['l']
        Trade_count  = data[0]['n']
        Open_price = data[0]['o']
        Time = data[0]['t']
        Volume = data[0]['v']
        Vwap = data[0]['vw']
        # Convert to NewYork Time
        Newyork_time = pd.Timestamp(Time, tz="America/New_York").isoformat().split('T')[0]
        # Convert to NewYork Time
        bar_table_name = "_" + Newyork_time.replace('-', '_')+ '_crypto_bar'
        # Create table if not esists
        cur.execute(
        "CREATE TABLE IF NOT EXISTS %s (symbol TEXT, time TIMESTAMPTZ, type TEXT, close NUMERIC,\
         high NUMERIC, low NUMERIC,open NUMERIC, trade NUMERIC, volume NUMERIC, vwap NUMERIC);" %bar_table_name)
        # excute SQL command
        con.commit()
        # Insert all data to database and excute.  
        cur.execute("INSERT INTO {} (symbol, time, type, close, high, low, open, trade, volume, vwap) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(bar_table_name),
        (Symbol, Time, Type, Close_price, High_price, Low_price, Open_price, Trade_count, Volume, Vwap))
        con.commit()        
    else:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


