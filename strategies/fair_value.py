from __future__ import division
from common import fvList


def updateValues(data, symb):
    buys = data['buy']
    sells = data['sell']

    if(len(buys) > 0):
        mean_buy = sum([int(price) for price, size in buys]) / len(buys)
        if(fvList[symb][0] == None):
            print(fvList)
            fvList[symb][0] = mean_buy
        else:
            fvList[symb][0] = (fvList[symb][0] + mean_buy)/2
    if(len(sells) > 0):
        mean_sell = sum([int(price) for price, size in sells])/ len(sells)
        if(fvList[symb][1] == None):
            fvList[symb][1] = mean_sell
        else:
            fvList[symb][1] = (fvList[symb][1] + mean_sell)/2

def trade(exchange):
    """Given the data in the book, decides whether we should make a trade.
    Returns a list of trades (buy/sell, symbol, price, size).
    """
    data = exchange.read()
    trades = []
    if(data==None or data['type'] != 'book'):
        return trades
    symb = data['symbol']
    fv = fvList[symb]

    updateValues(data, symb)
    if(fv[0] == None or fv[1] == None):
        return trades

    fv = fvList[symb]
    fv = sum(fv)/2
    diff = fv / 200

    for entry in data['buy']:
        if(int(entry[0]) > fv + diff):
            trades.append(['SELL', symb, entry[0], entry[1]])
    for entry in data['sell']:
        if(int(entry[0]) < fv - diff):
            trades.append(['BUY', symb, entry[0], entry[1]])
    return trades

