import socket
import json


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

    def read(self):
        data = self.stream.readline()
        if(data == ""):
            return None
        else:
            return json.loads(data)

    def write(self, data):
        json.dump(data, self.stream)
        self.stream.write("\n")

    def trade(self, buysell, symbol, price, size):
        trade = {'type': 'add', 'order_id': self.order_id, 'symbol': symbol,
                 'dir': buysell, 'price': price, 'size': size}
        print trade
        self.write(trade)

    def trade_batch(self, trades):
        # TODO check conflicts
        for buysell, symbol, price, size in trades:
            if buysell and size != 0:
                self.trade(buysell, symbol, price, size)
