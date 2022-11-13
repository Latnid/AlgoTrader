import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import dash_table
import pandas as pd
from ConnectDB import *
import warnings
from RTdata import get_data
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
warnings.filterwarnings("ignore")

# def sql_connection_keeper():
# # Check database connection,if not connected, connect it.
#     try:
#         con
#     except NameError:
#         # Connect to database
#         con,cur = connect_data_base()
#         print('Initial connection to PostgreSQL DataBase')
#         print(con.closed)
#         return con,cur
#     else:
#         if con.closed !=0:
#         # Connect to database
#             con,cur = connect_data_base()
#             print('Reconnected to PostgreSQL DataBase')
#             return con,cur
#         else:
#             print(f'PostgreSQL DataBase connection is normal.{con.closed}')
        
app = dash.Dash(__name__)
# cur.execute("SELECT * FROM _2022_11_11_stock_quote ORDER BY time DESC LIMIT 60")
# tupples = cur.fetchall()
# df = pd.DataFrame(data=tupples, columns=['symbol', 'time', 'type', 'ask', 'ask_size','ask_exchange', 'aid', 'aid_size', 'bid_exchange', 'quote_condition', 'tape'])
con,cur = connect_data_base()
df = get_data('crypto_bar')

app.layout = html.Div([
    html.H4('Dashboard'),
    dcc.Interval('time-series-update', interval = 30000,n_intervals = 0),
    dcc.Graph(id="time-series-chart"),
    dcc.Interval('graph-update', interval = 2000, n_intervals = 0),
    dash_table.DataTable(
          id = 'table',
          data = df.to_dict('records'),
          columns=[{"name": i, "id": i} for i in df.columns])])
 


@app.callback(
        dash.dependencies.Output('table','data'),
        [dash.dependencies.Input('graph-update', 'n_intervals')])
def updateTable(n):
    """ Query database 
    """
    # con,cur = connect_data_base()
    # cur.execute("SELECT * FROM _2022_11_11_stock_quote ORDER BY time DESC LIMIT 60")
    # tupples = cur.fetchall()
    # df = pd.DataFrame(data=tupples, columns=['symbol', 'time', 'type', 'ask', 'ask_size','ask_exchange', 'aid', 'aid_size', 'bid_exchange', 'quote_condition', 'tape'])
    ccon,cur = connect_data_base()
    df = get_data('crypto_bar')
    return df.to_dict('records')
#Input("ticker", "value"))

@app.callback(
    Output("time-series-chart", "figure"),
    Input("time-series-update", "n_intervals"))
def display_time_series(n):
    # cur.execute("SELECT * FROM _2022_11_11_stock_quote ORDER BY time DESC LIMIT 60")
    # tupples = cur.fetchall()
    # df = pd.DataFrame(data=tupples, columns=['symbol', 'time', 'type', 'ask', 'ask_size','ask_exchange', 'aid', 'aid_size', 'bid_exchange', 'quote_condition', 'tape']) # replace with your own data source
    con,cur = connect_data_base()
    df = get_data('crypto_bar')
    fig = px.line(df, x='time', y=df['close'])
    return fig

if __name__ == '__main__':
    con,cur = connect_data_base()
    app.run_server(debug=True, port=8080)