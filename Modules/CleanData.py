from Authorization import api_access
import pandas as pd
import numpy as np
import hvplot.pandas


def get_data(type,Symbol,timeframe,start = None,end = None):
    # get api access
    paper_api = api_access(type)
    
    # Set timezone as required
    if start != None:            
        start = pd.Timestamp(start, tz="America/New_York").isoformat()
    if end != None:
        end = pd.Timestamp(end, tz="America/New_York").isoformat()
    # Request data.
    print(f'requesting {Symbol} data')
    data_df = paper_api.get_bars(Symbol,timeframe,start,end).df
    #Convert received data time zone the same as WallStreet
    data_df.index = data_df.index.tz_convert('America/New_York')
    # drop NA
    data_df = data_df.dropna()
    # show success retrieved data message.
    print(f'{Symbol} data was retrieved successfully')
    return data_df
