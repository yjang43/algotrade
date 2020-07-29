import threading
import time
from datetime import datetime

import ccxt

from beta.APIFeeder import APIFeeder
from beta.clock import Clock
from beta.tmp import order_queue


class Communicator(threading.Thread):

    def __init__(self):
        super().__init__()

        self.exchange = ccxt.binance()
        self.exchange.apiKey = "nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13"
        self.exchange.secret = "0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1"

        self.is_program_running = True
        self.count = 0

        self.caller = threading.current_thread()
        self.alarm = threading.Event()
        self.since = {'default': int(datetime.now().timestamp() * 1000)}    # since for each symbol

        self.symbol_tracker = set()

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
            api_feeder.set_queue(order_queue)
            api_feeder.start()
            print(f"since value right now is: {self.since}")
            # # need to set it as join for now
            # # or need to update since in a different way
            # api_feeder.join()

    def set_exchange(self, exchange_id: str, public: str, private: str):
        for exchange in ccxt.exchanges:
            if exchange['id'] == exchange_id:
                self.exchange = exchange
                self.exchange.apiKey = public
                self.exchange.secret = private
                return True
        return False




