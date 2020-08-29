import threading
from typing import TYPE_CHECKING
from requests import HTTPError
from pprint import pprint
from datetime import datetime

import pandas as pd

if TYPE_CHECKING:
    from backend.beta.communicator import Communicator


class APIFeeder(threading.Thread):

    def __init__(self):
        super().__init__()
        self.caller: Communicator = threading.current_thread()
        self.queue = None
        self.session_container = None

    def run(self):
        print("API FEEDER INVOKED")
        self.order_from_queue()
        self.fetch_trades()

    def fetch_trades(self):
        print("FETCH OCCURS")
        # TODO: optimization needed
        #       delete unnecessary symbols when the trade is done
        for symbol in self.caller.symbol_tracker:
            self.fetch_trades_with_symbol(symbol)

    def fetch_trades_with_symbol(self, symbol: str):
        # update since value when fetching trade is done
        if symbol not in self.caller.since:     # set since
            self.caller.since[symbol] = self.caller.since['default']

        trades = self.caller.exchange.fetch_my_trades(symbol=symbol, since=self.caller.since[symbol])
        print(f'TRADE TEST')
        pprint(trades)

        if trades:
            self._update_since(trades[-1], symbol)  # last trade is an end element of trades
            self._send_trade_notice(trades, symbol)

    def _update_since(self, last_trade, symbol):
        # logic here is check the last trade, find timestamp and find since +1 from it
        # last_trade follows trade structure from ccxt
        since = last_trade['timestamp'] + 1
        self.caller.since[symbol] = since

    def _send_trade_notice(self, trades, symbol: str):
        for trade in trades:
            order_id = trade['order']
            order = self.caller.exchange.fetch_order(order_id, symbol)  # binance additionally requires symbol parameter
            session_id = order['clientOrderId']
            trade_structure = {
                'session_id': session_id,
                'order_id': order_id,
                'symbol': symbol,
                'side': trade['side'],
                'price': trade['price'],
                'amount': trade['amount']
            }
            pprint(trade_structure)

            self.session_container[session_id].trade_update(trade_structure)
            self._add_trade_history(trade_structure)

    @staticmethod
    def _add_trade_history(trade_structure):
        print("ADDING TRADE HISTORY")
        cur_date = datetime.now().strftime("%d/%m/%y")
        cur_time = datetime.now().strftime("%H:%M:%S")
        cur = (str(cur_date) + "-" + str(cur_time))
        df: pd.DataFrame = pd.read_csv('backend/trade_history.csv')
        d = {'date': [cur], 'session_num': [trade_structure['session_id']],
             'buy_sell': [trade_structure['side']],
             'amount': [f"{trade_structure['amount']*trade_structure['price']}$"]}  # session data
        print(d)
        df_to_add = pd.DataFrame(d)
        df = df_to_add.append(df, ignore_index=False)
        df.to_csv('backend/trade_history.csv', index=False)

    def order_from_queue(self):
        if not self.queue:
            raise QueueNotSet("queue is not set yet, set queue by APIFeeder.set_queue(<QUEUE>)")
        queue_length = self.queue.qsize()
        try:
            while queue_length:
                # just double check if queue is not empty
                if not self.queue.empty():
                    order = self.queue.get()
                    session_id = order['session_id']
                    order_info = order['order_info']
                    print('HOW THE FUCK THAT HAPPENED')
                    self.caller.exchange.create_order(order_info['symbol'], 'market', order_info['side'],
                                                      order_info['amount'], params={'clientOrderId': session_id})
                    self.add_symbol_to_tracker(order_info['symbol'])
                queue_length -= 1
        except HTTPError:
            # an error was caused when there is so little money traded
            # TODO: Need to revert logic in sessions
            print("Due to a limit that was set by the exchange,"
                  "you need to trade bigger amount.\n"
                  "reverting trade process")

    def cancel_order(self):
        # TODO: work on this function later
        pass

    # getters and setters here
    def set_queue(self, order_queue):
        self.queue = order_queue

    def set_session_container(self, session_container):
        self.session_container = session_container

    def add_symbol_to_tracker(self, symbol):
        self.caller.symbol_tracker.add(symbol)

    def remove_symbol_from_tracker(self, symbol):
        self.caller.symbol_tracker.remove(symbol)


class QueueNotSet(Exception):
    pass


