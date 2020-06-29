
import sys
from PyQt5.QtWidgets import *

print("hello world")
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(QLabel('abc'))

        self.show()
        # login = LoginDialog()
        # login.exec()

# https://freeprog.tistory.com/373
app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()
