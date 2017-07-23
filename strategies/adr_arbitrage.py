from fair_value import fvList
import exchange

#[buy, sell]
NOKUS_FAIR = fvList['NOKUS']
NOKFH_FAIR = fvList['NOKFH']

def trade(exchange):
	"""
	Should return a list of trades to do.
	"""
	trades = []

	#update fair values
	NOKUS_FAIR = fvList['NOKUS']
	NOKFH_FAIR = fvList['NOKFH']

	data = exchange.last_data
	if(data['type']!='book'):
		return trades
	symb = data['symbol']
	if(symb!='NOKUS' or symb!='NOKFH'):
		return trades

	#calculating the arbitrage
	bsymb = 'NOKUS'
	topFair = NOKFH_FAIR
	if NOKUS_FAIR>NOKFH_FAIR:
		bsymb = 'NOKFH'
		topFair = NOKUS_FAIR

	if(abs(NOKFH_FAIR-NOKUS_FAIR)>10):
		for sell_price, size in data['sell']:
			#if we can buy the lower worth for under the fair value of the higher, then we will
			if sell_price < btick:
				trades.append(['BUY', bsymb, sell_price, size])
		trades.append(['SELL', bsymb, portfolio[NOKFH]])