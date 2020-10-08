from quart import Quart

# import keys
import os
import sys
import time
import asyncio

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt.async_support as ccxt  # noqa: E402

# Example
output = ""
out = ""

# Create some test data for our catalog in the form of a list of dictionaries.
#ticker = 234.44

# loop = asyncio.get_event_loop()

async def get_ticker(exchange,symbola,symbolb):
# def get_ticker(exchange):
    triticker = await exchange.fetch_ticker(symbolb.upper())
    trirate = triticker['last']
    ticker = await exchange.fetch_ticker(symbola.upper())
    symboltousd = trirate * ticker['last']
    #clsoe the connection
    await exchange.close()
    # global output
    # output += 'LAST PRICE (' + symbol.upper() + '): ' + str(ticker['last']) + '\nBTCUSD rate: ' + str(btcusdrate) + '\n' + symbol.upper() + ' rate to USD:' + str(symboltousd)
    # output += str(symboltousd)
    return str(symboltousd)
    # return str(sym)
    # return output

async def run_request(exchange, symbola, symbolb):
    try:

        id = exchange # get exchange id from command line arguments

        # check if the exchange is supported by ccxt
        exchange_found = id in ccxt.exchanges

        if exchange_found:
            #dump('Instantiating', green(id))

            # instantiate the exchange by id
            # executor = ThreadPoolExecutor()
            # await loop.run_in_executor(executor, work)
            exchange = getattr(ccxt, id)()

            # load all markets from the exchange
            # markets = exchange.load_markets()

            # output all symbols
            #dump(green(id), 'has', len(exchange.symbols), 'symbols:', yellow(', '.join(exchange.symbols)))

            try:
                return await get_ticker(exchange, symbola, symbolb)
                # return output
            except ccxt.DDoSProtection as e:
                return 'DDoS Protection (ignoring)'
            except ccxt.RequestTimeout as e:
                return 'Request Timeout (ignoring)'
            except ccxt.ExchangeNotAvailable as e:
                return 'Exchange Not Available due to downtime or maintenance (ignoring)'
            except ccxt.AuthenticationError as e:
                return 'Authentication Error (missing API keys, ignoring)'
        else:
            return str('Exchange ' + id + ' not found')
            # print_usage()

    except Exception as e:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        return template.format(type(e).__name__, e.args)
        # return "Error..."

app = Quart(__name__)

@app.route("/api/v1/<exchange>/<quote>/<base>/<tri>")
async def notify(exchange,quote,base,tri):
    global output
    symbola = quote + "/" + base
    symbolb = base + "/" + tri
    result = await run_request(exchange,symbola,symbolb)
    # return exchange + " " + symbol + " : " + result
    return result

if __name__ == "__main__":
    app.run(debug=False)