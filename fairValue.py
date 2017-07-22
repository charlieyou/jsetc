from __future__ import division

fvList = {"AAPL": [None,None], "BOND": [None,None], "GOOG": [None,None], "MSFT": [None,None], "NOKFH": [None,None], "NOKUS": [None,None], "XLK": [None,None]}

def updateValues(data, symb):
	buys = data['buy']
	sells = data['sell']
	# TODO median
	if(len(buys) > 0):
		mean_buy = sum([price for price, size in buys]) / len(buys)
		if(fvList[symb][0] == None):
			fvList[symb][0] = mean_buy
		else:
			fvList[symb][0] = (fvList[symb][0] + mean_buy)/2
	if(len(sells) > 0):
		mean_sell = sum([price for price, size in sells])/ len(sells)
		if(fvList[symb][1] == None):
			fvList[symb][1] = mean_sell
		else:
			fvList[symb][1] = (fvList[symb][0] + mean_sell)/2

def get_FVtrades(data):
	"""Given the data in the book, decides whether we should make a trade.
	Returns a list of trades (buy/sell, symbol, price, size).
	"""
	trades = []
	if(data['type'] != 'book'):
		return trades

	symb = data['symbol'] #we've confirmed that it's a book, so it must have a symb
	fv = fvList[symb]
	if(fv[0] == None or fv[1] == None):
		return trades
	
	updateValues(data, symb)
	fv = fvList[symb]
	fv = sum(fv)/2
        
        print data['buy']	
	for entry in data['buy']:
		if(entry['price'] > fv):
			trades.append(['SELL', symb, entry['price'], entry['size']])
	for entry in data['sell']:
		if(entry['price']<fv):
			trades.append(['BUY', symb, entry['price'], entry['size']])
	return trades

