import ccxt
apiKey = ''
secret = ''

# exchange = ccxt.binance()
# balance = exchange.fetch_balance()
#
# coins_owned = [coin_name for coin_name in balance['total'] if balance['total'][coin_name] != 0]
# print(coins_owned)
# for coin in coins_owned:
#     print(coin)
#     for section in balance[coin]:
#         print(section, balance[coin][section])
#
# # print(exchange.load_markets())
# print(exchange.market('BTC/USDT').keys())
# orderbook = exchange.fetch_order_book ('BTC/USDT')
# bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
# ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
# spread = (ask - bid) if (bid and ask) else None
# print (exchange.id, 'market price', { 'bid': bid, 'ask': ask, 'spread': spread })