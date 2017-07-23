from __future__ import division
import exchange

fvList = {"AAPL": [None,None], "BOND": [None,None], "GOOG": [None,None], "MSFT": [None,None], "NOKFH": [None,None], "NOKUS": [None,None], "XLK": [None,None]}

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
	"""
	Should return a list of trades to do.
	"""
	trades = []

	#get fair values
	nokus = fvList['NOKUS']
	nokfh = fvList['NOKFH']
	print(fvList)
	if(nokus[0]==None or nokus[1]==None or nokfh[0]==None or nokfh[1]==None):
		return trades

	nokusFair = sum(nokus)/2
	nokfhFair = sum(nokfh)/2

	data = exchange.last_data
	if(data['type']!='book'):
		return trades
	symb = data['symbol']
	if(symb!='NOKUS' and symb!='NOKFH'):
		return trades
	#calculating the arbitrage
	bsymb = 'NOKUS'
	topFair = nokfhFair
	if nokusFair>nokfhFair:
		bsymb = 'NOKFH'
		topFair = nokusFair

	print(nokusFair + " " + nokfhFair)
	if(abs(nokfhFair-nokusFair)>2):
		if(data['symbol']==bsymb):
			for sell_price, size in data['sell']:
				#if we can buy the lower worth for under the fair value of the higher, then we will
				if sell_price < btick:
					trades.append(['BUY', bsymb, sell_price, size])
		trades.append(['SELL', bsymb, max(portfolio[NOKFH], 10)])