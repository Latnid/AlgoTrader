import Trade
from ConnectDB import *
import datetime
import pytz
import pandas as pd

# Check database connection,if not connected, connect it.
try:
    con
except NameError:
    # Connect to database
    con,cur = connect_data_base()
    print('Initial connection to PostgreSQL DataBase')
    print(con.closed)
else:
    if con.closed !=0:
    # Connect to database
        con,cur = connect_data_base()
        print('Reconnected to PostgreSQL DataBase')
    else:
        print(f'PostgreSQL DataBase connection is normal.{con.closed}')

# Fuction for acquiring data from database.
def get_data(data_type = 'stock_bar'):
    con,cur = connect_data_base()    
    # acquire wall street date
    def get_wall_street_date():
        """
        return wall street date
        """
        tz = pytz.timezone('America/New_York')
        return datetime.datetime.now(tz).strftime('%Y-%m-%d')

    # acquire latest data from realtime database (last 60 minites)
    wall_street_date = get_wall_street_date()
    table_name = "_" + wall_street_date.replace('-','_') + f'_{data_type}'
    cur.execute("SELECT * FROM {} ORDER BY time DESC LIMIT 60".format(table_name))
    data = cur.fetchall()

    # Acquire table columns names
    cur.execute("SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}'".format(table_name))
    rows = cur.fetchall()
    table_columns = []
    for row in rows:
        table_columns.append(row[3])

    # finish dataframe then return dataframe
    data_df = pd.DataFrame(data,columns= table_columns)
    return data_df