import ccxt


class Account:
    exchange = ccxt.binance()
    is_login_correct = False
    balance = None

    def __init__(self):
        super().__init__()

    @classmethod
    def login(cls, public_key, private_key):
        cls.exchange.apiKey = public_key
        cls.exchange.secret = private_key

        try:
            cls.exchange.fetch_balance()
            cls.is_login_correct = True
        except ccxt.errors.AuthenticationError:
            cls.is_login_correct = False

        return cls.is_login_correct

    @classmethod
    def get_coin_price(cls, coin: str):
        try:
            orderbook = cls.exchange.fetch_order_book(f"{coin}/USDT")
        except ccxt.errors.BadSymbol:
            print("BAD SYMBOL BOOKORDER FETCHED")
            # TODO: need to handle this exception properly so that correct USD value is shown
            return 0
        bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        # spread = (ask - bid) if (bid and ask) else None
        # print(cls.exchange.id, 'market price', { 'bid': bid, 'ask': ask, 'spread': spread })
        return (bid + ask) / 2

    @classmethod
    def get_coin_list(cls):
        if not cls.is_login_correct:
            raise ccxt.errors.AuthenticationError()
        cls.balance = cls.exchange.fetch_balance()
        coins_owned = [coin_name for coin_name in cls.balance['total'] if cls.balance['total'][coin_name] != 0]
        return coins_owned

    @classmethod
    def get_coin_balance(cls, coin: str):
        if not cls.is_login_correct:
            raise ccxt.errors.AuthenticationError()
        cls.balance = cls.exchange.fetch_balance()
        return cls.balance[coin]['total']

    @classmethod
    def get_markets(cls):
        return cls.exchange.markets.keys()



