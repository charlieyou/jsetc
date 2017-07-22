import socket
import json
import fairValue as fV

#################### GLOBAL VARIABLES ####################
team_name = "CHARLIETHEUNICORN"
ORDER_ID = 0

# True if testing mode, False if production mode
test_switch = True
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
def trade(exchange):
    i = 0
    while True:
        data = read_exchange(exchange)
        if(data==None):
            i += 1
            print(i)
            continue
        fvTrades = fV.get_FVtrades(data)
        #print(fvTrades)
        for trade in fvTrades:
            make_trade(exchange, trade[0], trade[1], trade[2], trade[3])

def make_trade(exchange, buysell, symbol, price, size):
    write_exchange(exchange, {'type': 'add', 'order_id': order_id,
                              'symbol': symbol, 'dir': buysell, 'price': price,
                              'size': size})
    global order_id
    order_id += 1


#################### MAIN ####################
def main():
    exchange = connect()
    write_exchange(exchange, {"type": "hello", "team": team_name})
    hello_exchange = read_exchange(exchange)
    trade(exchange)

if __name__ == '__main__':
    while True:
        main()
