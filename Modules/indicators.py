from CleanData import get_data
import pandas_ta as ta
import hvplot.pandas
import pandas as pd

# Create indicator function
def add_indicators(Data_df):
    # Create bbands.
    Data_i_bbands = ta.bbands(Data_df['close'])
    # Create kdj
    Data_df_i_kdj = ta.kdj(high=Data_df['high'],low=Data_df['low'],close=Data_df['close'],length=9,signal=3,offset=3)
    # concat all indicatiors to Data_df
    ML_df = pd.concat([Data_df,Data_i_bbands,Data_df_i_kdj],axis = 1)
    return ML_df