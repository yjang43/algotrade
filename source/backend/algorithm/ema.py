import ccxt
import random
import time
import numpy as np
import pandas as pd
import random
from time import sleep

exchange = ccxt.binance()

def emaalgorithm(investment = 0, period = 60, shortterm = 10, mediumterm = 20, longterm = 50): #run for an hour
    timecount = 0
    counter = 1
    while True : 
        checkresult = emacheck(shortterm, mediumterm, longterm)
        if(True):
            #BUY
            print(getBalance())
            buyamount = ((1/2)**(counter)) 
            #exchange.createMarketBuyOrder("BTC/KRW", 0.01) ONLY ENABLE FOR ACTUAL TESTING, WILL ACTUALLY PLACE ORDER
            print("BUY")
            counter+=1
        elif(checkresult[1]):
            #SELL
            sellamount = ((1/2)**(counter)) 
            print("SELL")
            counter+=1
        else:
            print("PASS")
        time.sleep(10)
        timecount = timecount + 1
        print("counter : " , timecount)
        if(timecount > period):
            break

def emacheck(shortterm, mediumterm, longterm):
    buysignal = False
    sellsignal = False

    dohlcvlist = exchange.fetch_ohlcv("BTC/USDT", '1d')

    ddfohlcv = pd.DataFrame.from_records(dohlcvlist)
    ddfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    ddfohlcv['Time'] = pd.to_datetime(ddfohlcv['Time'], unit='ms')
    plist = pd.Series(v[4] for v in dohlcvlist)

    shortma = plist.rolling(window = shortterm).mean()
    shortema = plist.ewm(span = shortterm).mean() #10 ewm
    mediumema = plist.ewm(span = mediumterm).mean() #20 ewm
    longema = plist.ewm(span = longterm).mean() #50 ewm


    dfma = pd.concat([shortma,shortema,mediumema,longema], axis = 1)
    dfma.columns = ['Short-term MA (MA' + str(shortterm) + ')', 'Short-term EMA (EMA' + str(shortterm) + ')', 'Medium-term EMA (EMA' + str(mediumterm) + ')', 'Long-term EMA (EMA' + str(longterm) + ')']
    dfma.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/data/1dayma.csv', header=True)
    print(dfma)

    recentma = dfma.iloc[dfma.shape[0]-1]
    recentshortema = recentma[1]
    recentmediumema = recentma[2]
    recentlongema = recentma[3]
    prevma = dfma.iloc[dfma.shape[0]-2]
    prevshortema = prevma[1]
    prevmediumema = prevma[2]
    prevlongema = prevma[3]

    #BUY : 9EMA over the 21 while already above 55
    #SELL : 9 crosses below 21 while already below 55

    if(prevshortema < prevlongema and prevshortema > prevmediumema and recentshortema < recentlongema and recentshortema < recentmediumema):
        buysignal = True
        sellsignal = False
    elif(prevshortema > prevlongema and prevshortema < prevmediumema and recentshortema > recentlongema and recentshortema > recentmediumema):
        sellsignal = True
        buysignal = False
    else:
        pass

    return buysignal,sellsignal