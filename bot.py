import socket
import json
import fairValue as fV

#################### GLOBAL VARIABLES ####################
team_name = "CHARLIETHEUNICORN"
ORDER_ID = 0

# True if testing mode, False if production mode
test_switch = False
port = 25000

if test_switch:
    host_name = "test-exch-" + team_name
else:
    host_name = "production"


#################### EXCHANGE CONNECTION ####################
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host_name, port))
    return s.makefile('rw', 1)

def write_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_exchange(exchange):
    data = exchange.readline()
    if(data == ""):
        return None
    else:
        return json.loads(data)


#################### TRADING ALGORITHM ####################
def trade(data):
    while True:
        data = read_exchange(exchange)
        bond_trade(exchange)
        fvTrades = fV.get_FVtrades(data)
        for trade in fvTrades:
            make_trade(exchange, trade[0], trade[1], trade[2], trade[3])

def bond_trade(exchange):
    data = read_exchange(exchange)
    while data:
        buy, sell = bond_helper
        if buy:
            buy_price, buy_size = buy
            if buy_size > 0:
                make_trade(exchange, 'BUY', 'BOND', buy_price, buy_size)
        if sell:
            sell_price, sell_size = sell
            if sell_size > 0:
                make_trade(exchange, 'SELL', 'BOND', sell_price, sell_size)
        data = read_exchange(exchange)

def bond_helper(data):
    buy = sell = None
    if data['type'] == 'book' and data['symbol'] == 'BOND':
        bids = data['buy']
        sell = [1001, 0]
        for price, size in bids:
            if price > 1000:
                sell[1] += size

        asks = data['sell']
        buy = [999, 0]
        for price, size in asks:
            if price < 1000:
                buy[1] += size
    return buy, sell

def make_trade(exchange, buysell, symbol, price, size):
    write_exchange(exchange, {'type': 'add', 'order_id': ORDER_ID,
                              'symbol': symbol, 'dir': buysell, 'price': price,
                              'size': size})
    global ORDER_ID
    ORDER_ID += 1


#################### MAIN ####################
def main():
    exchange = connect()
    write_exchange(exchange, {"type": "hello", "team": team_name})
    hello_exchange = read_exchange(exchange)
    trade(exchange)

if __name__ == '__main__':
    while True:
        main()
