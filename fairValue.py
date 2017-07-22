import strategy

class FairValue(Strategy):

	def __init__(self):
		return

	def findValue(data):
		return (sum(data['buy'])/len(data['buy']) + sum(data['sell'])/len(data['sell']))/2

	def trade(data):
		"""Given the data in the book, decides whether we should make a trade.
		Returns a list of trades (buy/sell, symbol, price, size).
		"""
		trades = []
		fairValue = findValue(data)
		for entry in data['buy']:
			if(entry['price']>fairValue):
				trades += ['SELL', data['symb'], entry['price'], entry['size']]
		for entry in data['sell']:
			if(entry['price']<fairValue):
				trades += ['BUY', data['symb'], entry['price'], entry['size']]
		return trades