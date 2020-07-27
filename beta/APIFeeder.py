import threading
import ccxt
from typing import TYPE_CHECKING
import queue
from requests import HTTPError

if TYPE_CHECKING:
    from beta.communicator import Communicator


class APIFeeder(threading.Thread):

    def __init__(self):
        super().__init__()
        self.caller: Communicator = threading.current_thread()
        self.caller.alarm.clear()
        self.queue: queue.Queue = None

    def run(self):
        # clear up the internal flag of the Event
        self.order_from_queue()
        self.fetch_trade('VET/USDT')

        print("alarm is clear now")

    # def fetch_data(self):
    #     exchange: ccxt.Exchange = self.caller.exchange
    #     try:
    #         balance_data = exchange.fetch_balance()
    #         coins_owned = [coin for coin in balance_data['total'] if balance_data['total'][coin] != 0.0]
    #         balance = {coin: balance_data[coin] for coin in coins_owned}
    #         order = exchange.fetch_orders(symbol='BTC/USDT')
    #         trades = exchange.fetch_my_trades(symbol='BTC/USDT')
    #         # print(order)
    #         print(balance)
    #         # print(trades)
    #     except ccxt.errors.AuthenticationError as e:
    #         print(f"The operation requires public and private key")
    #     except AttributeError as e:
    #         print(f"Current exchange does not support fetch_balance, {e}")

    def fetch_trade(self, symbol: str):
        # update since value when fetching trade is done
        if symbol not in self.caller.since:     # set since
            self.caller.since[symbol] = self.caller.since['default']

        # TODO: uncomment next line this and delete a line below
        trades = self.caller.exchange.fetch_my_trades(symbol=symbol, since=self.caller.since[symbol])
        # trades = self.caller.exchange.fetch_my_trades(symbol=symbol)
        print(f'TRADE TEST: \n {trades}')

        if trades:
            self._update_since(trades[-1], symbol)  # last trade is an end element of trades

    def _update_since(self, last_trade, symbol):
        # logic here is check the last trade, find timestamp and find since +1 from it
        # last_trade follows trade structure from ccxt
        since = last_trade['timestamp'] + 1
        self.caller.since[symbol] = since

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
        # just in case the order gets accepted continuously,
        # if each order takes long because of traffic, then it can cause double order
        # set current length as target length for current period
        queue_length = self.queue.qsize()
        try:
            while queue_length:
                # just double check if queue is not empty
                if not self.queue.empty():
                    session_id, order_info = self.queue.get()
                    order_return = self.caller.exchange.create_order(order_info['symbol'], 'market',
                                                                     order_info['side'], order_info['amount'])
                    # save session_id and order id pair
                    self.caller.order_track.append({order_return['id']: session_id})
                    queue_length -= 1
                    print(f"ORDER RESULT:\n"
                          f"session id: {session_id}"
                          f"order info: {order_info}"
                          f"order track: {self.caller.order_track}"
                          f"order return: {order_return}")
        except HTTPError:
            # an error was caused when there is so little money traded
            print("Due to a limit that was set by the exchange,"
                  "you need to trade bigger amount.\n"
                  "reverting trade process")
            # self.caller.order_track.pop()

    def cancel_order(self):
        # TODO: work on this function later
        pass

    # getters and setters here
    def set_queue(self, order_queue):
        self.queue = order_queue


class QueueNotSet(Exception):
    pass


