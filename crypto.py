import ccxt
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

upbit = ccxt.upbit()
markets = upbit.load_markets()
symbols = upbit.symbols
currencies = upbit.currencies

# def sma(clist, n):  #simple moving average function, n = number of days
# 	psum = 0
# 	ohlcvlist = clist
# 	for i in range(n):
# 		psum+=ohlcvlist[i][3]
# 	#	print(psum)
# 	return (psum)/n

# def ema(clist, n): #exponential moving average function, n = number of days
# 	#print(ohlcvlist)
# 	if(len(clist) == 1):
# 		return clist[0]
# 	else:
# 		temp = clist[0]
# 		clist = clist[1:]
# 		weight = 2/(n+1)
# 		return weight * temp + (1-weight) * ema(clist,n)

above50 = False
above20 = False

def checkabove50(data):
	if(data.iloc[-1]['ema50']<data.iloc[-1]['ema10']):
		print('hi')
		return True
	else :
		return False

def checkabove20(data):
	if(data.iloc[-1]['ema20']<data.iloc[-1]['ema10']):
	    print('hi')
	    return True
	else :
		return False

#uptrend
#10EMA over 20 while already above 50

def checkuptrend(data, above20, above50):
    if(checkabove50(s3)):
        above50 = True
        if((not above20) and checkabove20(s3)):
            above20 = True
            return True #BUY
    return False

def checkdowntrend(data, above20, above50):
    if(checkabove50(s3) == False):
        above50 = False
        if(above20 and (not checkabove20(s3))):
            above20 = False
            return True #SELL
    return False

#authentication
upbit.apiKey = ''
upbit.secret = ''
pd.set_option('display.float_format', lambda x: '%.5f' % x)


if upbit.has['fetchOHLCV']:
    #time.sleep (upbit.rateLimit/500) # time.sleep wants seconds
    #print(upbit.fetch_ohlcv("BTC/KRW", '1d')) #gives the last 200 candlesticks
    #make a list of the past sma
    smalist = pd.Series()

    ohlcvlist = upbit.fetch_ohlcv("BTC/KRW", '1d')
    #ohlcvlist.reverse() #newest first
    print(len(ohlcvlist))

    plist = pd.Series(v[4] for v in ohlcvlist)
    sma10 = plist.rolling(window = 10).mean()
    ema10 = plist.ewm(span = 10).mean() #10 ewm
    ema20 = plist.ewm(span = 20).mean() #20 ewm
    ema50 = plist.ewm(span = 50).mean() #50 ewm

    #print(sma10.tail(20))

    s3 = pd.concat([sma10,ema10,ema20,ema50], axis = 1)
    s3.columns = ['sma10', 'ema10', 'ema20', 'ema50']
    print(s3)

    print(checkuptrend(s3))
    print(checkdowntrend(s3))
 

    #downtrend
    #10EMA below 20 while already below 50





