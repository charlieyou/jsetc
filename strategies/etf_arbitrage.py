import common


def trade(exchange):
    # trade = ('BUY'/'SELL'/None, symbol, price, size)
    trades = []
    true_bid, true_ask = get_true_etf_value(exchange)
    book_bid = common.get_bid(exchange, 'XLK')
    book_ask= common.get_ask(exchange, 'XLK')

    if true_bid - 10

    if t

    return trades


def get_true_etf_value(exchange):

