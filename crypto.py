import ccxt
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

exchange = ccxt.binance()
markets = exchange.load_markets()
symbols = exchange.symbols
currencies = exchange.currencies

#authentication and login
exchange.apiKey = ''
exchange.secret = ''
pd.set_option('display.float_format', lambda x: '%.5f' % x)

def check():
    recentma = dfma.iloc[dfma.shape[0]-1]
    recentsma10 = recentma[0]
    recentema10 = recentma[1]
    recentema20 = recentma[2]
    recentema50 = recentma[3]
    buysignal = False
    sellsignal = False
    above50 = False
    above20 = False
    if(recentema10 > recentema50):
        above50 = True
    else:
        above50 = False

    if(above20 == False and above50 == True and recentema10 > recentema20):
        above20 = True
        buysignal = True
    elif(above20 == True and above50 == False and recentema10 < recentema20):
        above20 == False
        sellsignal = True
    elif(recentema10 > recentema20):
        above20 = True
    elif(recentema10 < recentema20):
        above20 = False

    #BUY : 9EMA over the 21 while already above 55
    #SELL : 9 crosses below 21 while already below 55

    return buysignal,sellsignal
    


if exchange.has['fetchOHLCV']:
    #time.sleep (exchange.rateLimit/500) # time.sleep wants seconds
    #print(exchange.fetch_ohlcv("BTC/KRW", '1d')) #gives the last 200 candlesticks
    #make a list of the past sma
    smalist = pd.Series()

    ohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1d')
    #ohlcvlist.reverse() #newest first
    print(len(ohlcvlist))

    plist = pd.Series(v[4] for v in ohlcvlist)
    sma10 = plist.rolling(window = 10).mean()
    ema10 = plist.ewm(span = 10).mean() #10 ewm
    ema20 = plist.ewm(span = 20).mean() #20 ewm
    ema50 = plist.ewm(span = 50).mean() #50 ewm

    #print(sma10.tail(20))

    dfma = pd.concat([sma10,ema10,ema20,ema50], axis = 1)
    dfma.columns = ['sma10', 'ema10', 'ema20', 'ema50']
    print(dfma)
    print(check())
    balance = exchange.fetch_balance()
    #print(balance)
    dfbalance = pd.Series(balance)
    #print(exchange.privateGetAccounts(params))
    #print(ccxt.exchanges)

# if exchange.has['fetchOrders']:
#     since = exchange.milliseconds () - 8640000  # -1 day from now
#     # alternatively, fetch from a certain starting datetime
#     # since = exchange.parse8601('2018-01-01T00:00:00Z')
#     all_orders = []
#     while since < exchange.milliseconds ():
#         symbol = "ICX/BTC"  # change for your symbol
#         limit = 10000000  # change for your limit
#         orders = exchange.fetch_orders(symbol, since, limit)
#         if len(orders): 
#             since = orders[len(orders) - 1]['timestamp']
#             all_orders += orders
#         else:
#             break
#     print(len(all_orders))

print("//////////////////////////////////////")

coinsowned = []
coinsownedamount = []
coinsinbtc = []
coinsinusd = []
percentagechange = []
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


dfcoinsowned = pd.DataFrame()
dfcoinsowned['balance'] = scoinsowned
dfcoinsowned['in btc'] = coinsinbtc
dfcoinsowned['in usd'] = coinsinusd
print(dfcoinsowned)

balanceinusd = 0
for val in dfcoinsowned["in usd"]:
    balanceinusd += val
print("Your total balance in USD : $" + str(balanceinusd))


print("//////////////////////////////////////")


#for fetching recent trade or trade orders
print("Your recent trades")
tradetime = []
tradesymbol = []
tradeamount = []
tradeside = []
if exchange.has['fetchMyTrades']:
    for val in coinsowned:
        if(val!= "BTC" and val!= "SBTC" and val != "VTHO" and val != "BCX"):
            tradess = exchange.fetch_my_trades (symbol = val + "/BTC", since = exchange.milliseconds () - 864000000, limit = 10, params = {})
            for trade in tradess:
                tradetime.append(trade.get("datetime"))
                tradesymbol.append(trade.get("symbol"))
                tradeamount.append(trade.get("amount"))
                tradeside.append(trade.get("side"))          
        #print("At " + trade.get("datetime") + " : " + trade.get("symbol") + " : " + str(trade.get("amount")) + " " + trade.get("side") + " at " + str(trade.get("price")))
dftrades = pd.DataFrame()
dftrades['tradetime'] = tradetime
dftrades['tradeside'] = tradeside
dftrades['tradesymbol'] = tradesymbol
dftrades['tradeamount'] = tradeamount

print(dftrades)

print("//////////////////////////////////////")

print("Your recent buys")
isbuy = dftrades['tradeside']=="buy"
dftradesbuy = dftrades[isbuy]
print(dftradesbuy)

print("Your recent sells")
issell = dftrades['tradeside']=="sell"
dftradessell = dftrades[issell]
print(dftradessell)

print("//////////////////////////////////////")





