# -*- coding: utf-8 -*-

import os
import sys
import time
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402


def dump(*args):
    print(' '.join([str(arg) for arg in args]))

output = ""

def print_ticker(exchange, symbol):
    btcusdticker = exchange.fetch_ticker("BTC/USDT")
    btcusdrate = btcusdticker['last']
    ticker = exchange.fetch_ticker(symbol.upper())
    symboltousd = btcusdrate * ticker['last']
    global output
    # output += 'LAST PRICE (' + symbol.upper() + '): ' + str(ticker['last']) + '\nBTCUSD rate: ' + str(btcusdrate) + '\n' + symbol.upper() + ' rate to USD:' + str(symboltousd)
    output += str(symboltousd)
    return output

try:

    id = sys.argv[1]  # get exchange id from command line arguments

    # check if the exchange is supported by ccxt
    exchange_found = id in ccxt.exchanges

    if exchange_found:
        #dump('Instantiating', green(id))

        # instantiate the exchange by id
        exchange = getattr(ccxt, id)()

        # load all markets from the exchange
        # markets = exchange.load_markets()

        # output all symbols
        #dump(green(id), 'has', len(exchange.symbols), 'symbols:', yellow(', '.join(exchange.symbols)))

        try:
            if len(sys.argv) > 2:  # if symbol is present, get that symbol only

                symbol = sys.argv[2]
                output += str(print_ticker(exchange, symbol))
                print(output)


        except ccxt.DDoSProtection as e:
            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
        except ccxt.RequestTimeout as e:
            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
        except ccxt.ExchangeNotAvailable as e:
            print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
        except ccxt.AuthenticationError as e:
            print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
    else:
        dump('Exchange ' + red(id) + ' not found')
        # print_usage()

except Exception as e:

    print(type(e).__name__, e.args, str(e))
    #print(output)
#    print_usage()