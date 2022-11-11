import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import dash_table
import pandas as pd
from ConnectDB import *
import warnings

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
warnings.filterwarnings("ignore")

con,cur = connect_data_base()
app = dash.Dash(__name__)
cur.execute("SELECT * FROM cryptodata_2022_11_10 ORDER BY timestamp DESC LIMIT 60")
tupples = cur.fetchall()
df = pd.DataFrame(data=tupples, columns=['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'trade_count', 'vwap'])

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
    cur.execute("SELECT * FROM cryptodata_2022_11_10 ORDER BY timestamp DESC LIMIT 60")
    tupples = cur.fetchall()
    df = pd.DataFrame(data=tupples, columns=['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'trade_count', 'vwap'])
    return df.to_dict('records')
#Input("ticker", "value"))

@app.callback(
    Output("time-series-chart", "figure"),
    Input("time-series-update", "n_intervals"))
def display_time_series(n):
    cur.execute("SELECT * FROM cryptodata_2022_11_10 ORDER BY timestamp DESC LIMIT 60")
    tupples = cur.fetchall()
    df = pd.DataFrame(data=tupples, columns=['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'trade_count', 'vwap']) # replace with your own data source
    fig = px.line(df, x='timestamp', y=df['close'])
    return fig

if __name__ == '__main__':
     app.run_server(debug=True, port=8080)