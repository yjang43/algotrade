
import sys
from PyQt5.QtWidgets import *


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *


class Label(QLabel):
    def __init__(self):
        super().__init__()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        image  = QImage('img/bitcoin.png')
        image = image.scaled(50, 50)
        qp.drawImage(QPoint(), image)

        pen = QPen(Qt.red)
        pen.setWidth(2)
        qp.setPen(pen)

        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(24)
        qp.setFont(font)
        # qp.scale(100,100)


        qp.drawText(50, 50, "Hello World !")

        qp.end()

print("hello world")
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        label = Label()
        label.setFixedSize(200, 200)
        self.setCentralWidget(label)

        self.show()
        # login = LoginDialog()
        # login.exec()

# https://freeprog.tistory.com/373
app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()
