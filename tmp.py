from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import Qt
import sys


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


from source.gui.login import LoginDialog
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
<<<<<<< HEAD
        self.setCentralWidget(CentralWidget(parent=self))
        self.setMinimumSize(800, 500)
=======
        self.setContentsMargins(0, 0, 0, 0)

        self.coins = QLineEdit("coin symbol...")
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.coins.setCompleter(completer)
        self.coins.textChanged.connect(lambda x: print(x))
        self.coins.returnPressed.connect(self.enter_pressed)

        self.setCentralWidget(self.coins)
>>>>>>> b5aa1508237fbd32d9c876f965568f24d5154d42
        self.show()
        # login = LoginDialog()
        # login.exec()


<<<<<<< HEAD

=======
>>>>>>> b5aa1508237fbd32d9c876f965568f24d5154d42
app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()


