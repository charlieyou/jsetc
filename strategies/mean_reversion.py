from statistics import mean, variance


length = 10
n = 5
values = {'AAPL': [], 'GOOG': [], 'MSFT': [], 'NOKFH': [], 'NOKUS': [],
          'XLK': []}


def update_values(data, symbol):
    if symbol in values:
        last_trades = values[symbol]
        if len(last_trades) >= length:
            last_trades = last_trades[1:]
        last_trades.append(data['price'])


def trade(exchange):
    trades = []
    data = exchange.last_data

    if data['type'] == 'trade':
        symbol = data['symbol']
        update_values(data, symbol)

    if data['type'] == 'book':
        symbol = data['symbol']
        if symbol in values and len(values[symbol]) > length:
            sma = mean(values[symbol])
            var = variance(values[symbol], sma)
            for price, size in data['buy']:
                # TODO handle case where we hit buy/hold limit
                # TODO order quantity based on difference (multiple of std?)
                if price > sma + n * var:
		    print sma
		    print var
                    trades.append(('SELL', symbol, price, size))
                else:
                    break

            for price, size in data['sell']:
                # TODO handle case where we hit buy/hold limit
                # TODO order quantity based on difference (multiple of std?)
                if price < sma - n * var:
		    print sma
		    print var
                    trades.append(('BUY', symbol, price, size))
                else:
                    break

    return trades
