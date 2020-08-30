import threading
from typing import TYPE_CHECKING

import ccxt

if TYPE_CHECKING:
    from backend.beta.communicator import Communicator


class BalanceFeeder(threading.Thread):
    def __init__(self):
        super().__init__()
        self.caller: Communicator = threading.current_thread()
        self.raw_balance = self.caller.exchange.fetch_balance()
        self.balance = self.caller.balance          # most important part of this thread

    def run(self):
        print("BALANCE FEEDER INVOKED")
        for coin_name in self.get_coin_list():
            self.balance[coin_name] = {
                'price': self.get_coin_price(coin_name),
                'amount': self.get_coin_amount(coin_name)
            }

    def get_coin_list(self):
        coins_owned = [coin_name for coin_name in self.raw_balance['total'] if self.raw_balance['total'][coin_name] != 0]
        return coins_owned

    def get_coin_price(self, coin: str):
        try:
            orderbook = self.caller.exchange.fetch_order_book(f"{coin}/USDT")
        except ccxt.errors.BadSymbol:
            # print("BAD SYMBOL BOOKORDER FETCHED")
            # TODO: need to handle this exception properly so that correct USD value is shown
            return -1
        bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
        ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
        return (bid + ask) / 2

    def get_coin_amount(self, coin: str):
        return self.raw_balance[coin]['total']
