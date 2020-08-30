import threading
import time
from datetime import datetime
from pprint import pprint

import ccxt

from backend.beta.APIFeeder import APIFeeder
from backend.beta.balance_feeder import BalanceFeeder
from backend.beta.clock import Clock


class Communicator(threading.Thread):

    def __init__(self):
        super().__init__(daemon=True)

        self.exchange = ccxt.binance()
        self.exchange.apiKey = "nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13"
        self.exchange.secret = "0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1"

        self.is_program_running = True
        self.count = 0

        self.caller = threading.current_thread()
        self.alarm = threading.Event()
        self.since = {'default': int(datetime.now().timestamp() * 1000)}    # since for each symbol

        self.symbol_tracker = set()

        self.order_queue = None         # need to be set outside
        self.session_container = None   # need to be set outside

        self.balance = {}

    def run(self):
        while self.is_program_running:
            # init clock
            print(f'CURRENT THREAD NUMBER: {threading.active_count()}')
            Clock(5).start()
            while not self.alarm.is_set():
                time.sleep(0.2)
            self.alarm.clear()                      # reset alarm

            balance_feeder = BalanceFeeder()        # start balance feeder
            balance_feeder.start()
            pprint(self.balance)

            api_feeder = APIFeeder()                # start api feeder
            if self.order_queue is None or self.session_container is None:
                print("NEED TO CALL SETTERS FOR ORDER_QUEUE AND SESSION_CONTAINER")
            api_feeder.set_queue(self.order_queue)
            api_feeder.set_session_container(self.session_container)
            api_feeder.start()
            # print(f"since value right now is: {self.since}")
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

    def set_session_container(self, session_container):
        self.session_container = session_container

    def set_order_queue(self, order_queue):
        self.order_queue = order_queue


