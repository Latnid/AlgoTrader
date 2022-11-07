#import require libraries
from Authorization import api_access

def go_long(symbol,qty,limit_price,take_profit_price,stop_loss_price):
    """
    Use when going long only
    symbol: str,
    qty: float,
    limit_price: float,
    stop_loss_price: float,
    take_profit_price: float
    """
    API = api_access('paper')
    long_order = API.submit_order(
        symbol = symbol,
        qty = qty,
        side = 'buy',
        type = 'limit',
        time_in_force = 'day',
        limit_price = limit_price,
        order_class = 'bracket',
        take_profit = {
        "limit_price": take_profit_price
      },
        stop_loss = {
        "stop_price": stop_loss_price,
        "limit_price": stop_loss_price*0.99
      },
    )
    long_order = long_order._raw
    print (f"Go long order submitted:\nOrder ID: {long_order['id']}\nEntry point: {long_order['limit_price']}\nTake profit point: {long_order['legs'][0]['limit_price']}\nStop loss point: {long_order['legs'][1]['limit_price']}")
    return long_order

def go_short(symbol,qty,limit_price,take_profit_price,stop_loss_price):
    """
    Use when going short only
    symbol: str,
    qty: float,
    limit_price: float,
    stop_loss_price: float,
    take_profit_price: float
    """
    API = api_access('paper')
    short_order = API.submit_order(
        symbol = symbol,
        qty = qty,
        side = 'sell',
        type = 'limit',
        time_in_force = 'day',
        limit_price = limit_price,
        order_class = 'bracket',
        take_profit = {
        "limit_price": take_profit_price
      },
        stop_loss = {
        "stop_price": stop_loss_price,
        "limit_price": stop_loss_price*1.01
      },
    )
    short_order = short_order._raw
    print (f"Short selling order submitted:\nOrder ID: {short_order['id']}\nEntry point: {short_order['limit_price']}\nTake profit point: {short_order['legs'][0]['limit_price']}\nStop loss point: {short_order['legs'][1]['limit_price']}")
    return short_order
    