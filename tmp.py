from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import Qt
import sys
import json


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
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setFixedHeight(150)

        self.container = QWidget()
        self.container.setLayout(QHBoxLayout())
        self.set_assets()

        self.setWidget(self.container)

    def set_assets(self):
        with open('tmp.json', 'r') as f:
            coins = json.load(f)

        for coin in coins:
            label = QLabel(f"{coin}\n\t$1234")
            label.setFixedSize(200, 100)
            # label.setPixmap(QPixmap("img/bitcoin.png"))
            # label.setScaledContents(True)
            label.setStyleSheet(
                f"background-image: url({coins[coin]['img']});"
                "background-repeat: no-repeat;"
                "background-position: center;"
                "background-size: contain;"
                "color: black;"
                "font-size: 20pt;"
            )

            # label.setStyleSheet("border-image: url(img/bitcoin.png);")
            self.container.layout().addWidget(label)
        pass



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


