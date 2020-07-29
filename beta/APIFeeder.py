import threading
from typing import TYPE_CHECKING
import queue
from requests import HTTPError
from pprint import pprint

if TYPE_CHECKING:
    from beta.communicator import Communicator


class APIFeeder(threading.Thread):

    def __init__(self):
        super().__init__()
        self.caller: Communicator = threading.current_thread()
        self.caller.alarm.clear()
        self.queue: queue.Queue = None
        self.session_container = None

    def run(self):
        # clear up the internal flag of the Event
        self.order_from_queue()
        # self.fetch_trades_with_symbol('VET/USDT')
        self.fetch_trades()

        print("alarm is clear now")

    def fetch_trades(self):
        print("HERE FETCH OCCURS")
        print("symbol tracker:", self.caller.symbol_tracker)
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
            order = self.caller.exchange.fetch_order(order_id, symbol)  # binance addtionally requires symbol parameter
            session_id = order['clientOrderId']
            # TODO: Find the corresponding session and call function to update balance
            #       We need to integrate session_container (or current_session) with APIFeeder
            """required trade structure
            {
                session_id: string,
                order_id: string,
                symbol: string,
                side: string,
                price: float,
                amount: float
            }
            """
            trade_structure = {
                'session_id': session_id,
                'order_id': order_id,
                'symbol': symbol,
                'side': trade['side'],
                'price': trade['price'],
                'amount': trade['amount']
            }
            pprint(trade_structure)

        pass

    def order_from_queue(self):
        if not self.queue:
            raise QueueNotSet("queue is not set yet, set queue by APIFeeder.set_queue(<QUEUE>)")
        """queue is a list of dictionary form
        {
            session_id: string,
            order_structure: {
                symbol: string, # market symbol
                side: string,   # buy/sell
                amount: float
            }
        }
        """
        # TODO:
        #   just in case the order gets accepted continuously,
        #   if each order takes long because of traffic, then it can cause double order
        #   need another data structure that move queued data to
        queue_length = self.queue.qsize()
        try:
            while queue_length:
                # just double check if queue is not empty
                if not self.queue.empty():
                    order = self.queue.get()
                    session_id = order['session_id']
                    order_info = order['order_info']
                    # self.caller.exchange.create_order(order_info['symbol'], 'market', order_info['side'],
                    #                                   order_info['amount'], {'clientOrderId': session_id})
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


