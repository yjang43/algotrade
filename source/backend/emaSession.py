import ccxt
import threading
import time
import pandas as pd

class Session(threading.Thread):

  def __init__(self, sessionID, name):
    threading.Thread.__init__(self)
    self.sessionID = sessionID
    self.name = name
    self.counter = 0
    self.total = 0
    self.totalcoin = 0
    self.totalcash = 0
    self.totalprofit = 0
    self.currency = ""
    self.exitFlag = 0

class EmaSession(Session):

  def __init__(self, sessionID, name, exchange, orderQueue, initialInvestment = 100, currency = "BTC/USDT", shortterm = 5, mediumterm = 10, longterm = 20):
    Session.__init__(self, sessionID, name)
    self.exchange = exchange
    self.orderQueue = orderQueue
    self.initialInvestment = initialInvestment
    self.currency = currency
    self.shortterm = shortterm
    self.mediumterm = mediumterm
    self.longterm = longterm

    self.total = initialInvestment
    self.totalcash = initialInvestment

  def run(self):
    print("Starting ", self.sessionID)
    #run algorithm that checks ema every 10seconds
    self.execute()
    print("Exiting ", self.sessionID)

  def changeTerms(self, shortterm, mediumterm, longterm):
    self.shortterm = shortterm
    self.mediumterm = mediumterm
    self.longterm = longterm

  def execute(self):
    #execute respective session
    #buy in
    while True : 
      print("Session ID : ", self.sessionID, " counter : " , self.counter)
      checkresult = self.emacheck(self.shortterm, self.mediumterm, self.longterm)
      if(checkresult[0]):
          #BUY, account for price slippage
          buyamount = (1/2) * self.totalcash
          #once bought, subtract the amount from balance
          buyorder = {
            "sessionID" : self.sessionID,
            "order_structure": {
              "symbol": self.currency, # market symbol
              "side": "buy",   # buy/sell
              "amount": buyamount
            }
          } 
          self.orderQueue.put(buyorder)
          # mytrade = exchange.fetch_my_trades (symbol = currency, since = None, limit = None, params = {})
          # if(success, retrieve transaction history and make according changes to balance):
          # self.totalcash -= mytrade.cost
          # self.totalcoin += mytrade.amount
          print("BUY")
      elif(checkresult[1]):
          #SELL
          sellamount = (1/2) * self.totalcoin
          sellorder = {
            "sessionID" : self.sessionID,
            "order_structure": {
              "symbol": self.currency, # market symbol
              "side": "sell",   # buy/sell
              "amount": sellamount
            }
          }
          self.orderQueue.put(sellorder)
          # mytrade = exchange.fetch_my_trades (symbol = currency, since = None, limit = None, params = {})
          # if(success, retrieve transaction history and make according changes to balance):
          # self.totalcoin -= mytrade.amount
          # self.totalcash += mytrade.cost
          print("SELL")
      else:
         print("PASS")
      print("total : ", self.total)
      print("total cash : ", self.totalcash)
      print("total coin : ", self.totalcoin)
      print("total profit : ", self.totalprofit)
      time.sleep(10) #check every 10 seconds
      self.counter = self.counter + 1

  def emaFetch(self):
    dohlcvlist = self.exchange.fetch_ohlcv("BTC/USDT", '1d')
    dfohlcv = pd.DataFrame.from_records(dohlcvlist) #convert to dataframe
    dfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
    #print(dfohlcv)
    dfohlcv['Time'] = pd.to_datetime(dfohlcv['Time'], unit='ms') #convert time to ms
    plist = pd.Series(v[4] for v in dohlcvlist)

    shortma = plist.rolling(window = self.shortterm).mean()
    shortema = plist.ewm(span = self.shortterm).mean() #10 ewm
    mediumema = plist.ewm(span = self.mediumterm).mean() #20 ewm
    longema = plist.ewm(span = self.longterm).mean() #50 ewm

    dfma = pd.concat([shortma,shortema,mediumema,longema], axis = 1)
    dfma.columns = ['Short-term MA (MA' + str(self.shortterm) + ')', 'Short-term EMA (EMA' + str(self.shortterm) + ')', 'Medium-term EMA (EMA' + str(self.mediumterm) + ')', 'Long-term EMA (EMA' + str(self.longterm) + ')']
    dfma.to_csv (r'/Users/jae/Documents/Programming/algotrade/source/data/1dayma.csv', header=True)
    return dfma

  def emacheck(self, shortterm, mediumterm, longterm):
    buysignal = False
    sellsignal = False

    dfma = self.emaFetch()
    #locate most recent ema values
    recentma = dfma.iloc[dfma.shape[0]-1]
    recentshortema = recentma[1]
    recentmediumema = recentma[2]
    recentlongema = recentma[3]
    #locate next recent ema values
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

