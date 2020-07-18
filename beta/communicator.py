import threading
import time

import ccxt


class Communicator(threading.Thread):
    exchange = ccxt.binance()
    exchange.apiKey = "nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13"
    exchange.secret = "0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1"

    def __init__(self):
        super().__init__()

        self.is_program_running = True
        self.count = 0

        self.caller = threading.current_thread()
        self.alarm = threading.Event()

    def run(self):
        while self.is_program_running:
            # init clock
            Clock(3).start()
            while not self.alarm.is_set():
                time.sleep(1)
                self.count += 1
                print(f"communicator count is {self.count}")
            print("alarm alarm!")
            api_feeder = APIFeeder()
            api_feeder.start()
            api_feeder.join()

    @classmethod
    def set_exchange(cls, exchange_id: str, public: str, private: str):
        for exchange in ccxt.exchanges:
            if exchange['id'] == exchange_id:
                cls.exchange = exchange
                cls.exchange.apiKey = public
                cls.exchange.secret = private
                return True
        return False


class APIFeeder(threading.Thread):

    def __init__(self):
        super().__init__()
        self.caller: Communicator = threading.current_thread()

    def run(self):
        # clear up the internal flag of the Event
        self.fetch_data()
        print("alarm is clear now")
        self.caller.alarm.clear()

    @staticmethod
    def fetch_data():
        exchange: ccxt.Exchange = Communicator.exchange
        try:
            balance_data = exchange.fetch_balance()
            coins_owned = [coin for coin in balance_data['total'] if balance_data['total'][coin] != 0.0]
            balance = {coin: balance_data[coin] for coin in coins_owned}
            order = exchange.fetch_orders(symbol='BTC/USDT')
            trades = exchange.fetch_my_trades(symbol='BTC/USDT')
            # print(order)
            print(balance)
            # print(trades)
        except ccxt.errors.AuthenticationError as e:
            print(f"The operation requires public and private key")
        except AttributeError as e:
            print(f"Current exchange does not support fetch_balance, {e}")


class Clock(threading.Timer):
    def __init__(self, interval):
        super().__init__(interval, self.time_up)
        self.caller: Communicator = threading.current_thread()
        if type(self.caller) != Communicator:
            raise TypeError("Clock's caller is not Communicator")

    def time_up(self):
        print("clock time's up!")
        self.caller.alarm.set()


com = Communicator()
com.start()


