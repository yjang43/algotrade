import ccxt
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from threading import Timer
from time import sleep

class RepeatedTimer(object):
    def __init__(self, interval, function):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function()

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



def emacheck():
    if exchange.has['fetchOHLCV']:
        #time.sleep (exchange.rateLimit/500) # time.sleep wants seconds
        #print(exchange.fetch_ohlcv("BTC/KRW", '1d')) #gives the last 200 candlesticks
        #make a list of the past sma
        ohlcvlist = exchange.fetch_ohlcv("ETH/BTC", '1d')
        #ohlcvlist.reverse() #newest first
        #print((ohlcvlist))

        dfohlcv = pd.DataFrame.from_records(ohlcvlist)
        dfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
        dfohlcv.to_csv (r'/Users/jae/Documents/Programming/algotrade/csv/ohlcv.csv', header=True)

        plist = pd.Series(v[4] for v in ohlcvlist)
        sma10 = plist.rolling(window = 10).mean()
        ema10 = plist.ewm(span = 10).mean() #10 ewm
        ema20 = plist.ewm(span = 20).mean() #20 ewm
        ema50 = plist.ewm(span = 50).mean() #50 ewm


        dfma = pd.concat([sma10,ema10,ema20,ema50], axis = 1)
        dfma.columns = ['sma10', 'ema10', 'ema20', 'ema50']
        print(dfma)
        dfma.to_csv (r'/Users/jae/Documents/Programming/algotrade/csv/1dayma.csv', header=True)

    recentma = dfma.iloc[dfma.shape[0]-1]
    recentsma10 = recentma[0]
    recentema10 = recentma[1]
    recentema20 = recentma[2]
    recentema50 = recentma[3]
    prevma = dfma.iloc[dfma.shape[0]-2]
    prevsma10 = prevma[0]
    prevema10 = prevma[1]
    prevema20 = prevma[2]
    prevema50 = prevma[3]

    if(prevema10 > prevema50):
        above50 = True
    else:
        above50 = False

    if(prevema10 > prevema20):
        above20 = True
    else:
        above20 = False

    buysignal = False
    sellsignal = False
    
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
    print(buysignal, sellsignal)
    if(buysignal):
        buy()
    elif(sellsignal):
        sell()

    return buysignal,sellsignal


def buy():
    print("BUY")
    # exchange.createMarketBuyOrder("ETH/BTC", 0.01)
def sell():
    print("SELL")
    # exchange.createMarketBuyOrder("ETH/BTC", 0.01)


exchange = ccxt.binance()
markets = exchange.load_markets()
symbols = exchange.symbols
currencies = exchange.currencies

#authentication and login
exchange.apiKey = ''
exchange.secret = ''
pd.set_option('display.float_format', lambda x: '%.5f' % x)


balance = exchange.fetch_balance()
dfbalance = pd.Series(balance)
#print(exchange.privateGetAccounts(params))
#print(ccxt.exchanges)

if exchange.has['fetchClosedOrders']:
    since = exchange.milliseconds () - 8640000  # -1 day from now
    # alternatively, fetch from a certain starting datetime
    # since = exchange.parse8601('2018-01-01T00:00:00Z')
    all_orders = []
    while since < exchange.milliseconds ():
        symbol = "ICX/BTC"  # change for your symbol
        limit = 10000000  # change for your limit
        orders = exchange.fetch_orders(symbol, since, limit)
        if len(orders): 
            since = orders[len(orders) - 1]['timestamp']
            all_orders += orders
        else:
            break
    print("Order Length : ")
    print(len(all_orders))

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


dfcoinsowned = pd.DataFrame({
        'balance' : scoinsowned,
        'in btc' : coinsinbtc,
        'in usd' : coinsinusd
    })
print(dfcoinsowned)
dfcoinsowned.to_csv (r'/Users/jae/Documents/Programming/algotrade/csv/coinsowned.csv', header=True)


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
            trades = exchange.fetch_my_trades (symbol = val + "/BTC", since = exchange.milliseconds () - 864000000, limit = 10, params = {})
            for trade in trades:
                tradetime.append(trade.get("datetime"))
                tradesymbol.append(trade.get("symbol"))
                tradeamount.append(trade.get("amount"))
                tradeside.append(trade.get("side"))          
        #print("At " + trade.get("datetime") + " : " + trade.get("symbol") + " : " + str(trade.get("amount")) + " " + trade.get("side") + " at " + str(trade.get("price")))
dftrades = pd.DataFrame({
        'tradetime': tradetime,
        'tradeside': tradeside,
        'tradesymbol': tradesymbol,
        'tradeamount': tradeamount,
    })
dftrades = dftrades.sort_values(by = ['tradetime'], ascending = False)


dftrades.to_csv (r'/Users/jae/Documents/Programming/algotrade/csv/trades.csv', header=True)
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

print("starting...")
rt = RepeatedTimer(60, emacheck) # it auto-starts, no need of rt.start(), CHECK EVERY MINUTE
# try:
#     sleep() # your long-running job goes here...
# finally:
#     rt.stop() # better in a try/finally block to make sure the program ends!



