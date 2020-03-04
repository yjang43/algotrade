from PyQt5.QtCore import *
from datetime import datetime
import ccxt
import random
import time
import numpy as np
import pandas as pd
import random
from time import sleep

exchange = ccxt.binance()

def emaalgorithm(trade_info:pyqtSignal, process_id, investment = 0, period = 60, shortterm = 10, mediumterm = 20, longterm = 50): #run for an hour
    timecount = 0
    while True :
        checkresult = emacheck(shortterm, mediumterm, longterm)
        if(checkresult[0]):
            #BUY
            print("BUY")
        elif(checkresult[1]):
            #SELL
            print("SELL")
        else:
            print("PASS")
            trade_info.emit({'date': cur_datetime(), 'session_num': str(process_id), 'buy_sell': 'buy', 'amount': '1$'})
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
    dfma.to_csv (r'source/csv/1dayma.csv', header=True)
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
    elif(prevshortema > prevlongema and prevshortema < prevmediumema and recentshortema > recentlongema and recentshortema > recentmediumema):
        sellsignal = True
    else:
        pass

    return buysignal,sellsignal
algorithms = {'ema/sma': emaalgorithm}

# how to put list as parameters in python
# https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists


def run_algorithm(algorithm_key: str, parameters: list, process_id):

    algorithms[algorithm_key](date=cur_datetime(), session_num='session_num')
    # algorithms[algorithm_key](*parameters, date=cur_datetime(), session_num='session_num')

# add this to jay's function!!!
def send_signal(trade_info: pyqtSignal, kwargs: dict, buy_sell = 0, amount = 0):
    emit_dict = kwargs
    emit_dict['buy_sell'] = buy_sell
    emit_dict['amount'] = amount
    trade_info.emit(emit_dict)

def cur_datetime():
    """
    return string of current date time
    this function is general so need to be in different file
    :return: string of current date time
    """
    cur_date = datetime.now().strftime("%d/%m/%y")
    cur_time = datetime.now().strftime("%H:%M:%S")
    ret = (str(cur_date) + "-" + str(cur_time))
    print(ret)
    return ret


