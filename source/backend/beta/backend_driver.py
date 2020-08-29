"""The code helps integration with the main program. It is a driver for
running session, controlling session, and communication with APIs
"""

from typing import List

import pandas as pd

from backend.beta.communicator import Communicator
from backend.emaSession import EmaSession
from backend.beta.tmp import order_queue, session_container


class BackendDriver:
    def __init__(self):
        self.session_container = session_container
        self.order_queue = order_queue
        self.communicator = Communicator()
        self.communicator.set_order_queue(self.order_queue)
        self.communicator.set_session_container(self.session_container)
        self.communicator.start()
        self.algorithm_session_map = {
            'ema': EmaSession,
            # ...
        }
        self.session_count = 0

    @staticmethod
    def start_session(session):
        session.start()

    def create_session(self, class_name, options: List):
        # get Session class that was mapped in algorithm_session_map
        session_class = self.algorithm_session_map[class_name]
        session_id = str(self._session_number_generator())
        session = session_class(session_id, self.order_queue, *options)
        self.session_container[session.session_id] = session
        return session

    def kill_session(self, session_id):
        self.session_container[session_id].kill_session()
        self.session_container.pop(session_id)
        pass

    def _session_number_generator(self):
        # generate un-repetitive value
        session_number = self.session_count
        self.session_count += 1
        return session_number

    def get_balance_df(self):
        """This function returns currently owned coins' data table
        """
        balance_info = self.communicator.balance
        coins_data = []
        for coin_name in balance_info:
            coin_price = balance_info[coin_name]['price']
            coin_amount = balance_info[coin_name]['amount']
            coin_data = [coin_name, f"{coin_price: .2f}", f"{coin_amount: .2f}", f"{coin_price * coin_amount: .2f}"]
            coins_data.append(coin_data)
        return pd.DataFrame(coins_data, columns=['NAME', 'PRICE(USD)', 'AMOUNT', 'VALUE(USD)'])

