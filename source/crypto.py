import ccxt
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
from threading import Timer
from algorithm import ema
from algorithm import arima


#Classes  :

class RepeatedTimer(object): #Class for repeated checking
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

#functions


def ohlcvsave(): #function for saving ohclv csv files
    mohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1m')
    hohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1h')
    dohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1d')
    Mohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1M')
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
    mdfohlcv.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/minuteohlcv.csv', header=True)
    hdfohlcv.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/hourohlcv.csv', header=True)
    ddfohlcv.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/dayohlcv.csv', header=True)
    Mdfohlcv.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/monthohlcv.csv', header=True)


def testemacheck(dfsignal, testUSDbalance,testBTCbalance):
    shortterm = 10
    mediumterm = 20
    longterm = 50

    if exchange.has['fetchOHLCV']:
        #time.sleep (exchange.rateLimit/500) # time.sleep wants seconds
        #print(exchange.fetch_ohlcv("BTC/KRW", '1d')) #gives the last 200 candlesticks
        #make a list of the past sma
        ohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1m')
        # '1m': '1minute',
        # '1h': '1hour',
        # '1d': '1day',
        # '1M': '1month',
        # '1y': '1year',

        #ohlcvlist.reverse() #newest first
        #print((ohlcvlist))

        dfohlcv = pd.DataFrame.from_records(ohlcvlist)
        dfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
        dfohlcv.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/ohlcv.csv', header=True)

        plist = pd.Series(v[4] for v in ohlcvlist)
        shortma = plist.rolling(window = shortterm).mean()
        shortema = plist.ewm(span = shortterm).mean() #10 ewm
        mediumema = plist.ewm(span = mediumterm).mean() #20 ewm
        longema = plist.ewm(span = longterm).mean() #50 ewm


        dfma = pd.concat([shortma,shortema,mediumema,longema], axis = 1)
        dfma.columns = ['Short-term MA (MA' + str(shortterm) + ')', 'Short-term EMA (EMA' + str(shortterm) + ')', 'Medium-term EMA (EMA' + str(mediumterm) + ')', 'Long-term EMA (EMA' + str(longterm) + ')']
        print(dfma)
        dfma.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/1dayma.csv', header=True)

        recentma = dfma.iloc[dfma.shape[0]-1]
        recentshortema = recentma[1]
        recentmediumema = recentma[2]
        recentlongema = recentma[3]
        prevma = dfma.iloc[dfma.shape[0]-2]
        prevshortema = prevma[1]
        prevmediumema = prevma[2]
        prevlongema = prevma[3]

    buysignal = False
    sellsignal = False

    if(prevshortema < prevlongema and prevshortema > prevmediumema and recentshortema < recentlongema and recentshortema < recentmediumema):
        sellsignal = True
    elif(prevshortema > prevlongema and prevshortema < prevmediumema and recentshortema > recentlongema and recentshortema > recentmediumema):
        buysignal = True
    else:
        buysignal = False
        sellsignal = False 

    #BUY : 9EMA over the 21 while already above 55
    #SELL : 9 crosses below 21 while already below 55
    print("//////////////////////////////////////")


    print("Your test USD Balance : " + str(testUSDbalance))
    print("Your test BTC Balance : " + str(testBTCbalance))
    ohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1m')
    dfohlcv = pd.DataFrame.from_records(ohlcvlist)
    dfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    totalb = testUSDbalance + (testBTCbalance*(dfohlcv.iloc[-1][4]))
    print("Your total balance : " + str(totalb))
    change = (totalb - 1000)/1000.0 * 100
    ss = pd.Series([buysignal, sellsignal, totalb, testUSDbalance,testBTCbalance, str(change) + "%"], index = ['buy', 'sell', 'total balance', 'usd balance', 'btc balance', 'change'])
    print(ss)
    dfsignal = dfsignal.append(ss, ignore_index = True)
    print(dfsignal)
    dfsignal.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/0.5signal.csv', header=True)

    if(buysignal):
        return(testbuy(dfsignal, testUSDbalance, testBTCbalance))
    elif(sellsignal):
        return(testsell(dfsignal, testUSDbalance, testBTCbalance))
    else:
        return(dfsignal, testUSDbalance, testBTCbalance)



def getBalance(): 
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
    dfcoinsowned.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/coinsowned.csv', header=True)


    balanceinusd = 0
    for val in dfcoinsowned["in usd"]:
        balanceinusd += val
    print("Your total balance in USD : $" + str(balanceinusd))
    print("//////////////////////////////////////")

def getRecentTrades():
    tradetime = []
    tradesymbol = []
    tradeamount = []
    tradeside = []
    print("Your recent trades")
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


    dftrades.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/csv/trades.csv', header=True)
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


def testbuy(dfsignal, testUSDbalance, testBTCbalance):
    print("BUY")
    ohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1d')
    dfohlcv = pd.DataFrame.from_records(ohlcvlist)
    dfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    testBTCbalance = testBTCbalance + ((0.5 * testUSDbalance)/(dfohlcv.iloc[-1][4]))
    testUSDbalance = 0.5 * testUSDbalance
    return(dfsignal, testUSDbalance,testBTCbalance)

    # exchange.createMarketBuyOrder("ETH/BTC", 0.01) ONLY ENABLE FOR ACTUAL TESTING, WILL ACTUALLY PLACE ORDER
def testsell(dfsignal, testUSDbalance, testBTCbalance):
    print("SELL")
    ohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1d')
    dfohlcv = pd.DataFrame.from_records(ohlcvlist)
    dfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    testUSDbalance = testUSDbalance + 0.5 * testBTCbalance*(dfohlcv.iloc[-1][4])
    testBTCbalance = 0.5 * testBTCbalance
    return(dfsignal, testUSDbalance,testBTCbalance)

    # exchange.createMarketBuyOrder("ETH/BTC", 0.01) ONLY ENABLE FOR ACTUAL TESTING, WILL ACTUALLY PLACE ORDER


def test():
    testUSDbalance = 1000
    testBTCbalance = 0
    count = 0
    dfsignal = pd.DataFrame(columns = ['buy', 'sell', 'total balance', 'usd balance', 'btc balance', 'change'])

    while True : 
        lol = testemacheck(dfsignal, testUSDbalance,testBTCbalance)
        dfsignal = lol[0]
        testUSDbalance = lol[1]
        testBTCbalance = lol[2]
        time.sleep(60)
        count = count + 1
        print(count)
        if(count > 10):
            break
    #rt = RepeatedTimer(5, testemacheck, testUSDbalance,testBTCbalance)


#main.py

exchange = ccxt.binance()
markets = exchange.load_markets()
symbols = exchange.symbols
currencies = exchange.currencies

#authentication and login
exchange.apiKey = 'nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13'
exchange.secret = '0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1'
pd.set_option('display.float_format', lambda x: '%.5f' % x)

balance = exchange.fetch_balance()
dfbalance = pd.Series(balance)

coinsowned = []
coinsownedamount = []
coinsinbtc = []
coinsinusd = []
percentagechange = []

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
    # print("Order Length : ")
    # print(len(all_orders))

print("//////////////////////////////////////")
#getBalance()

#for fetching recent trade or trade orders
#getRecentTrades()

print("starting...")
ohlcvsave()
#ema.emaalgorithm()
arima.ARIMAalgorithm()


#rt = RepeatedTimer(60, test) # it auto-starts, no need of rt.start(), CHECK EVERY MINUTE
# try:
#     sleep() # your long-running job goes here...
# finally:
#     rt.stop() # better in a try/finally block to make sure the program ends!



