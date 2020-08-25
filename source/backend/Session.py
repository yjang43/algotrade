import ccxt
import threading
import time
import pandas as pd

#define exchange locally

exchange = ccxt.binance()
markets = exchange.load_markets()
symbols = exchange.symbols
currencies = exchange.currencies

exchange.apiKey = 'nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13'
exchange.secret = '0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1'

#base currency and quote currency

class Session(threading.Thread):

    def __init__(self, session_id, order_queue, initial_investment, currency):
        threading.Thread.__init__(self, daemon= True)
        self.session_id = session_id
        self.order_queue = order_queue
        self.counter = 0
        self.initial_investment = initial_investment
        self.total = initial_investment
        self.totalcoin = 0
        self.totalcash = initial_investment
        self.totalprofit = 0
        self.currency = currency
        self.termination_flag = False

    def trade_update(self, trade_structure):
        if(int(trade_structure.session_id) != self.session_id):
            print("wrong match")
        else:
            if(trade_structure.side == "buy"):
                self.totalcoin += trade_structure.amount * trade_structure.price
                self.totalcash -= trade_structure.amount
            elif(trade_structure.side == "sell"):
                self.totalcoin -= trade_structure.amount * trade_structure.price
                self.totalcash += trade_structure.amount
        print("Updated balance")
        self.calc_profit()
        print(self.totalprofit)

    def calc_balance(self):
        #calculates the current valuation
        current_balance = 0
        current_balance += self.totalcash
        current_balance += self.totalcoin * self.fetch_price()
        self.total = current_balance
        return self.total

    def fetch_price(self):
        #fetches the latest bid price from exchange
        orderbook = exchange.fetch_order_book (self.currency)
        bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None #highest price a buyer will pay for security
        ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None #lowest price a seller will accept for security
        return ask

    def calc_profit(self):
        #returns profit in percentage
        self.totalprofit = (self.calc_balance()-self.initial_investment)/self.initial_investment * 100

    def kill_session(self):
        self.termination_flag = True