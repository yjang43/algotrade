import ccxt
import pickle
from pprint import pprint
import time


exchange = ccxt.binance()
exchange.apiKey = "nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13"
exchange.secret = "0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1"

exchange.load_markets()


def get_balance(e):
    balance_data = e.fetch_balance()
    coins_owned = [coin for coin in balance_data['total'] if balance_data['total'][coin] != 0.0]
    balance = {coin: balance_data[coin] for coin in coins_owned}
    return balance


def get_since():
    with open("beta/time.pickle", 'rb') as f:
        since = pickle.load(f)
    return since


# symbol to trade VET/USDT
# order_info = exchange.create_order('VET/USDT', 'market', 'buy', 1000)
# print('ORDER INFO')
# pprint(order_info)

# time.sleep(0.2)
# order = exchange.fetch_order(order_id)
# print("CHECK ORDER")
# pprint(order)
#
# time.sleep(0.2)
# order = exchange.fetch_order(order_id)
# print("CHECK ORDER")
# pprint(order)
#
# time.sleep(0.2)
# order = exchange.fetch_order(order_id)
# print("CHECK ORDER")
# pprint(order)

# pprint(exchange.fees)

# print("TRADES")
# pprint(exchange.fetch_my_trades('VET/USDT'))
# print("ORDER")
# pprint(exchange.fetch_order('207962552', symbol='VET/USDT'))
