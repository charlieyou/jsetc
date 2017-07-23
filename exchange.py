import socket
import json

portfolio = {"AAPL": None, "BOND": None, "GOOG": None, "MSFT": None, "NOKFH": None, "NOKUS": None, "XLK": None}

class Exchange:
    def __init__(self, test, team_name='CHARLIETHEUNICORN', port=25000):
        if test:
            host_name = "test-exch-" + team_name
        else:
            host_name = "production"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host_name, port))
        self.stream = s.makefile('rw', 1)

        self.write({"type": "hello", "team": team_name})
        hello_exchange = self.read()
        assert hello_exchange['type'] == 'hello'

        self.order_id = 0

        # TODO keep track of current positions

    def read(self):
        data = self.stream.readline()
        if(data == ""):
            return None
        else:
            data = json.loads(data)
            self.last_data = data

            #update our local copy of the portfolio, so we know how many of each stock we have
            if(data['type']=='fill'):
                if(data['dir']=='BUY'):
                    portfolio[data['symbol']] += int(data['size'])
                elif(data['dir']=='SELL'):
                    portfolio[data['symbol']] -= int(data['size'])

            return data

    def write(self, data):
        json.dump(data, self.stream)
        self.stream.write("\n")

    def trade(self, buysell, symbol, price, size):
        trade = {'type': 'add', 'order_id': self.order_id, 'symbol': symbol,
                 'dir': buysell, 'price': price, 'size': size}
        self.order_id += 1
        print trade
        self.write(trade)

    def trade_batch(self, trades):
        # TODO check conflicts
        if(trades):
            '''
            for t in trades:
                if(len(t)==4):


            if(len(trades[0])==4):
                for buysell, symbol, price, size in trades:
                    if buysell and size > 0:
                        self.trade(buysell, symbol, price, size)
            elif(len(trades[0])==3):
                for buysell, symbol, size in trades:
                    if buysell and size > 0:
                        self.convert(buysell, symbol, size)
            '''

            for args in trades:
                if args[0]:
                    if len(args) == 4:
                        self.trade(args[0], args[1], args[2], args[3])
                    elif len(args) == 3:
                        self.convert(args[0], args[1], args[2])
    def convert(self, buysell, symbol, size):
        trade = {'type': 'convert', 'order_id': self.order_id,
                 'symbol': symbol, 'dir': buysell, 'size': size}
        self.order_id += 1
        print trade
        self.write(trade)
