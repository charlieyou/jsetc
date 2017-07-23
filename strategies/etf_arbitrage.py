import exchange

def trade(exchange):
    # trade = ('BUY'/'SELL'/None, symbol, price, size)
    trades = []
    mean_values = {"AAPL": [None,None], "BOND": [None,None], "GOOG": [None,None], "MSFT": [None,None]}
    data = exchange.last_read
    
    if(data['type'] != 'book'):
        return trades
    if(data['symbol'] != 'BOND' or data['symbol'] != 'AAPL' or data['symbol'] != 'MSFT' or data['symbol'] != 'GOOG', data['symbol'] != 'XLK'):
        return trades
    
    symb = data['symbol']
    exp_buy, exp_sell = exp_etf_val(data, symb, mean_values)
    exp_avg = sum(exp_buy + exp_sell)/2

    if symb == 'XLK':
        for price, size in data['sell']:
            if exp_avg > price:
                trades.append(['BUY', symb, price, size])
            else:
                break
        for price, size in data['buy']:
            if exp_avg > price:
                trades.append(['SELL', symb, price, size])
            else:
                break

    return trades
            
def comb_stock_val(data, symb, mean_values):
    buys = data['buy']
    sells = data['sell']

    if len(buys) > 0:
        mean_values[symb][0] = sum([int(price) for price, size in buys]) / len(buys)
    if len(sells) > 0:
        mean_values[symb][1] = sum([int(price) for price, size in sells]) / len(sells)

    exp_buy = 0
    exp_sell = 0
    for stock in mean_values:
        if mean_values[0] is None or mean_values[1] is None:
            return None
        exp_buy += mean_values[0]
        exp_sell += mean_values[1]

    return exp_buy, exp_sell



