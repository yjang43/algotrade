import ccxt
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from EmaSession import EmaSession
from threading import Timer
import queue



exchange = ccxt.binance()
markets = exchange.load_markets()
symbols = exchange.symbols
currencies = exchange.currencies

#authentication and login
exchange.apiKey = 'nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13'
exchange.secret = '0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1'

pd.set_option('display.float_format', lambda x: '%.5f' % x) #pandas display option

balance = exchange.fetch_balance()
dfbalance = pd.Series(balance)

#basic data parameters
coinsowned = []
coinsownedamount = []
coinsinbtc = []
coinsinusd = []
percentagechange = []
sessions = []



def setkey(apikey, secretkey):
    exchange.apiKey = apikey
    exchange.secret = secretkey


def ohlcvsave(currency = "BTC/USDT"): #function for saving ohclv csv files
    mohlcvlist = exchange.fetch_ohlcv(currency, '1m')
    hohlcvlist = exchange.fetch_ohlcv(currency, '1h')
    dohlcvlist = exchange.fetch_ohlcv(currency, '1d')
    Mohlcvlist = exchange.fetch_ohlcv(currency, '1M')
    # '1m': '1minute',
    # '1h': '1hour',
    # '1d': '1day',
    # '1M': '1month',
    # '1y': '1year',

    mdfohlcv = pd.DataFrame.from_records(mohlcvlist)
    hdfohlcv = pd.DataFrame.from_records(hohlcvlist)
    ddfohlcv = pd.DataFrame.from_records(dohlcvlist)
    Mdfohlcv = pd.DataFrame.from_records(Mohlcvlist)
    mdfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    hdfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    ddfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    Mdfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    mdfohlcv['Time'] = pd.to_datetime(mdfohlcv['Time'], unit='ms')
    hdfohlcv['Time'] = pd.to_datetime(hdfohlcv['Time'], unit='ms')
    ddfohlcv['Time'] = pd.to_datetime(ddfohlcv['Time'], unit='ms')
    Mdfohlcv['Time'] = pd.to_datetime(Mdfohlcv['Time'], unit='ms')
    mdfohlcv.to_csv (r'data/minuteohlcv.csv', header=True)
    hdfohlcv.to_csv (r'data/hourohlcv.csv', header=True)
    ddfohlcv.to_csv (r'data/dayohlcv.csv', header=True)
    Mdfohlcv.to_csv (r'data/monthohlcv.csv', header=True)

def getBalance(): 
    balance = exchange.fetch_balance()

    dfbalance = pd.Series(balance)
    rate = exchange.fetch_ticker('BTC/USDT').get("bid")
    for items in dfbalance.items(): #print the coins that i own
        if isinstance(items[1].get("total"), float):
            if (items[1].get("total") > 0):
                coinsowned.append(items[0])
                coinsownedamount.append(items[1].get("total"))
                if(items[0] == "BTC"):
                    priceinbtc = 1
                elif(items[0] == "SBTC" or items[0] == "BCX" or items[0] == "VTHO"):
                    priceinbtc = 0
                else:
                    priceinbtc = (exchange.fetch_ticker(items[0] + "/BTC").get("close") + exchange.fetch_ticker(items[0] + "/BTC").get("open"))/2.0
                coinsinbtc.append(items[1].get("total") * priceinbtc)
                coinsinusd.append(items[1].get("total") * priceinbtc * rate)
    scoinsowned = pd.Series(coinsownedamount, coinsowned, name = 'amount')


    dfcoinsowned = pd.DataFrame({
            'balance' : scoinsowned,
            'in btc' : coinsinbtc,
            'in usd' : coinsinusd
        })
    print(dfcoinsowned)
    dfcoinsowned.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/data/coinsowned.csv', header=True)

    balanceinusd = 0
    for val in dfcoinsowned["in usd"]:
        balanceinusd += val
    print("Your total balance in USD : $" + str(balanceinusd))
    print("//////////////////////////////////////")
    return(dfcoinsowned) #returns dataframe

orderQueue = queue.Queue() # a queue of dictionary

x = EmaSession(1, "session-1", exchange, orderQueue)
y = EmaSession(2, "session-2", exchange, orderQueue)
x.start()
y.start()

# print(exchange.fetch_my_trades("VET/USDT"))
print("///////")
# print(exchange.fetch_order(210442184, "VET/USDT"))
# exchange.create_market_sell_order("VET/USDT", 1000, {'newClientOrderId': 'World'})

#take dictionary values from dictionary and make according buy or sell
# if(True): #clock signal
#     while not orderQueue.empty():
#         val = orderQueue.dequeue()
        





