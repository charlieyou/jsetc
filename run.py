import argparse
import time

import errno
from socket import error as socket_error

from exchange import Exchange
from bot import Bot


def main(strategies, test):
    exchange = Exchange(test)
    print "Connected to exchange"
    bot = Bot(exchange, strategies)
    print "Bot initialized"
    bot.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('strategies')
    parser.add_argument('--test', action='store_true', default=False)
    args = parser.parse_args()

    strategies = args.strategies.split(',')
    while True:
        try:
            main(strategies, args.test)
        except socket_error as serr:
            if serr.errno != errno.ECONNREFUSED:
                raise serr
            # TODO metrics for each round
            print "Sleeping..."
            time.sleep(1)
