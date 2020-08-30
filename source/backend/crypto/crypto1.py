class Crypto:
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    symbols = exchange.symbols
    currencies = exchange.currencies
    def login(self, public_key, private_key):
        try:
            exchange.apiKey = public_key
            exchange.secret = private_key
        except Exception:
            return -1
        return 0
    def logout(self):
        try:
            exchange.apiKey = None
            exchange.secret = None
        except Exception:
            return -1
        return 0
    def getBalance(self):
        coinsowned = []
        rate = exchange.fetch_ticker('BTC/USDT').get("bid")
        for items in dfbalance.items():  # print the coins that i own
            if isinstance(items[1].get("total"), float):
                if (items[1].get("total") > 0):
                    coinsowned.append(items[0])
                    coinsownedamount.append(items[1].get("total"))
                    if (items[0] == "BTC"):
                        priceinbtc = 1
                    elif (items[0] == "SBTC" or items[0] == "BCX" or items[0] == "VTHO"):
                        priceinbtc = 0
                    else:
                        priceinbtc = (exchange.fetch_ticker(items[0] + "/BTC").get("close") + exchange.fetch_ticker(
                            items[0] + "/BTC").get("open")) / 2.0
                    coinsinbtc.append(items[1].get("total") * priceinbtc)
                    coinsinusd.append(items[1].get("total") * priceinbtc * rate)
        scoinsowned = pd.Series(coinsownedamount, coinsowned, name='amount')
        dfcoinsowned = pd.DataFrame({
            'balance': scoinsowned,
            'in btc': coinsinbtc,
            'in usd': coinsinusd
        })
        print(dfcoinsowned)
        dfcoinsowned.to_csv(r'/Users/jae/Documents/Programming/algotrade/source/csv/coinsowned.csv', header=True)
        balanceinusd = 0
        for val in dfcoinsowned["in usd"]:
            balanceinusd += val
        print("Your total balance in USD : $" + str(balanceinusd))
        print("//////////////////////////////////////")
        return dfcoinsowned


    def getRecentTrades():
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

        return dftrades

    def getBuyTrades():
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

        isbuy = dftrades['tradeside']=="buy"
        dftradesbuy = dftrades[isbuy]
        return dftradesbuy


    def getSellTrades():
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

        issell = dftrades['tradeside']=="sell"
        dftradessell = dftrades[issell]
        return dftradessell

    # def buy():
    # def sell():

