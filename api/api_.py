import flask
from flask import request, jsonify
import asyncio
import os
import sys
import time

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Example
output = ""
out = ""

# Create some test data for our catalog in the form of a list of dictionaries.
#ticker = 234.44

loop = asyncio.get_event_loop()

async def get_ticker(exchange,sym):
# def get_ticker(exchange):
    btcusdticker = exchange.fetch_ticker("BTC/USDT")
    btcusdrate = btcusdticker['last']
    ticker = exchange.fetch_ticker(sym.upper())
    symboltousd = btcusdrate * ticker['last']
    global output
    # output += 'LAST PRICE (' + symbol.upper() + '): ' + str(ticker['last']) + '\nBTCUSD rate: ' + str(btcusdrate) + '\n' + symbol.upper() + ' rate to USD:' + str(symboltousd)
    output += str(symboltousd)
    # return str(symboltousd)
    # return str(sym)
    return output


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Cabbage Farm Custom Ticker API</h1>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/<exch>/<quote>/<base>', methods=['GET'])
def multiple(exch,quote,base):
    global out
    exchange = getattr(ccxt, exch)()
    sym = quote + "/" + base
    out = exch + " - " + sym
    # out += str(fetcher(exch, sym))



    return get_ticker(exchange,sym)

    # out += str(get_ticker(exch, symbol))

    # return output

app.run()