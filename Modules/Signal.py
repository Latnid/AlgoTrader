from RTdata import get_data
from indicators import add_indicators
from Trade import go_long, go_short
import time
from ConnectDB import *

# Connect postgresql
con,cur = connect_data_base()
# Create data acquire function:
def clean_data():
    data_df = get_data(cur=cur, data_type="crypto_bar")
    # Set 'time' index
    data_index_df = data_df.set_index('time')

    #Transfer datatype
    data_index_df[['symbol','type']]= data_index_df[['symbol','type']].astype('str')
    data_index_df[['close', 'high', 'low', 'open','trade','volume','vwap']] = data_index_df[['close', 'high', 'low', 'open','trade','volume','vwap']].astype('float')
    # Add indicators.
    data_indicators_df = add_indicators(data_index_df)
    return data_indicators_df

# Set Condition to excute trade.
def trade_condition_check(qty):
    while True:
        # get clean data.
        data_indicators_df = clean_data()
        # Go long condition 1 BOLL: close <= BBL
        if data_indicators_df['close'][0] <= data_indicators_df['BBL_5_2.0'][4]:
            # set current price as low price
            low_price_point = data_indicators_df['low']
            print(f'Low price point: {low_price_point}')
            if data_indicators_df['D_9_3'][15] < 20:
                if data_indicators_df['K_9_3'][13] > data_indicators_df['D_9_3'][15]:
                    if data_indicators_df['J_9_3'][15] < 10: 
                        symbol = data_indicators_df['symbol'][0]
                        limit_price = data_indicators_df['low'][0]
                        take_profit_price = limit_price * 1.01
                        stop_loss_price = limit_price * 0.99
                        go_long(symbol,qty,limit_price,take_profit_price,stop_loss_price)
                        print('Trade placed')
                        break
        # Go short condition 1 BOLL: close >= BBL
        elif data_indicators_df['close'][0] >= data_indicators_df['BBU_5_2.0'][4]:
            high_price_point = data_indicators_df['high']
            print(f'High price point: {high_price_point}')
            # Go Short condition 2 - KDJ 
            if data_indicators_df['D_9_3'][15] > 80:
                if data_indicators_df['K_9_3'][13] < data_indicators_df['D_9_3'][15]:
                    if data_indicators_df['J_9_3'][15] > 100:
                        # prepare trade detail
                        symbol = data_indicators_df['symbol'][0]
                        limit_price = data_indicators_df['high'][0]
                        take_profit_price = limit_price * 0.99
                        stop_loss_price = limit_price * 1.01
                        # submit trade
                        go_short(symbol,qty,limit_price,take_profit_price,stop_loss_price)
                        print('Trade placed')
                        break
        else:
            print(f"***Monitoring trade condition***\n"
                  f"Ticker: {data_indicators_df['symbol'][0]}\n"
                  f"Close: {data_indicators_df['close'][0]}\n"
                  f"High: {data_indicators_df['high'][0]}\n"
                  f"Low: {data_indicators_df['low'][0]}\n"
                  f"BBL: {data_indicators_df['BBL_5_2.0'][4]}\n"
                  f"BBU: {data_indicators_df['BBU_5_2.0'][4]}\n"
                  f"K: {data_indicators_df['K_9_3'][13]}\n"
                  f"D: {data_indicators_df['D_9_3'][15]}\n"
                  f"J: {data_indicators_df['K_9_3'][13]}"
                 )

            
        time.sleep(30)

if __name__ == "__main__":
    trade_condition_check(1.01)