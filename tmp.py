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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(CentralWidget(parent=self))
        self.setMinimumSize(800, 500)
        self.show()


app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()


