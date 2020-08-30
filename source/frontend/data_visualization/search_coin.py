from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import ccxt

from .setting_button import SettingButton


class SearchCoin(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(600, 50)

        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)

        self.current_coin_searched = 'BTC/USDT'
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.exchange = ccxt.binance()
        self.exchange.load_markets()
        self.coin_list = self.exchange.markets.keys()

        self.search_bar = self.create_search_bar()
        self.search_button = self.create_search_button()

        setting = SettingButton('settings')

        layout.addWidget(self.search_bar)
        layout.addWidget(self.search_button)
        layout.addWidget(setting)

    def create_search_bar(self):
        search_bar = QLineEdit('search...')
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        search_bar.setSizePolicy(size_policy)

        # set autocomplete when user starts an input
        completer = QCompleter(self.coin_list)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        search_bar.setCompleter(completer)
        search_bar.textChanged.connect(lambda x: print(x))
        return search_bar

    def create_search_button(self):
        def set_current_coin():
            self.current_coin_searched = self.search_bar.text()
            print('current coin searched: ', self.current_coin_searched)
        search_button = QPushButton('search')
        search_button.setFixedWidth(100)
        search_button.clicked.connect(set_current_coin)

        return search_button
