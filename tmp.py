import sys
import json
import re

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
import ccxt


class CentralWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QHBoxLayout())
        self.setStyleSheet(
            "background-color: lightgray;"
        )
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        red = BabyWidget('red')
        button = QPushButton("hello")
        button.setFixedSize(100, 100)
        red.layout().addWidget(button)
        yellow = BabyWidget('yellow')
        green = BabyWidget('green')
        self.layout().addWidget(red)
        self.layout().addWidget(yellow)
        self.layout().addWidget(green)
        print(red.sizeHint())
        print(yellow.sizeHint())
        print(green.sizeHint())



class BabyWidget(QWidget):
    def __init__(self, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.layout().addWidget(QWidget(self))
        self.setStyleSheet(f"background-color: {color}")
        # self.setMaximumSize(300, 500)


class AssetContainer(QScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.exchange = ccxt.binance()
        self.exchange.apiKey = 'nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13'
        self.exchange.secret = '0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1'
        balance = self.exchange.fetch_balance()

        self.coins_owned = [coin_name for coin_name in balance['total'] if balance['total'][coin_name] != 0]
        for coin in self.coins_owned:
            print(coin)
            for section in balance[coin]:
                print(section, balance[coin][section])


        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setFixedHeight(150)

        self.container = QWidget()
        self.container.setLayout(QHBoxLayout())
        self.set_assets()

        self.setWidget(self.container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_price)
        self.timer.setInterval(10000)
        self.timer.start()

        self.set_event()

    def set_assets(self):
        with open('tmp.json', 'r') as f:
            coins = json.load(f)

        for coin in self.coins_owned:
            try:
                orderbook = self.exchange.fetch_order_book(f'{coin}/USDT')
            except ccxt.errors.BadSymbol:
                break
            bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
            ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
            spread = (ask - bid) if (bid and ask) else None
            print(self.exchange.id, 'market price', {'bid': bid, 'ask': ask, 'spread': spread})

            # label = QLabel(f"{coin}\n\t$1234")
            label = QLabel(str(bid))
            label.setFixedSize(200, 100)
            # # label.setPixmap(QPixmap("img/bitcoin.png"))
            # # label.setScaledContents(True)
            # label.setStyleSheet(
            #     f"background-image: url({coins[coin]['img']});"
            #     "background-repeat: no-repeat;"
            #     "background-position: center;"
            #     "color: black;"
            #     "font-size: 20pt;"
            # )

            # # label.setStyleSheet("border-image: url(img/bitcoin.png);")
            self.container.layout().addWidget(label)

    def update_price(self):
        print("update")
        labels: QLabel = [c for c in self.widget().children() if type(c) == QLabel]
        print(labels)
        for l in labels:
            price = float(l.text())
            price += 1
            l.setText(str(price))

    def set_event(self):
        scroll_bar = self.horizontalScrollBar()

        def print_bar_val():
            print(scroll_bar.value())
        print(scroll_bar.value())
        self.t = QTimer()
        self.t.timeout.connect(print_bar_val)
        self.t.setInterval(1000)
        self.t.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setCentralWidget(CentralWidget(parent=self))

        central_widget = QWidget()
        central_widget.setLayout(QVBoxLayout())
        label = QLabel("Demo")
        label.setFixedHeight(40)

        central_widget.layout().addWidget(label)
        central_widget.layout().addWidget(AssetContainer())

        self.setCentralWidget(central_widget)
        self.setFixedSize(300, 400)
        self.show()


class AssetCard(QLabel):
    def __init__(self, asset_name: str, *args):
        super().__init__(*args)
        with open('tmp.json', 'r') as f:
            data = json.load(f)
        print(data[asset_name]['img'])




app = QApplication(sys.argv)
AssetCard("bitcoin")
main_window = MainWindow()
app.exec_()


