from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Login')
        self.status = QLabel()
        self.status.setText("enter your account information")
        self.loginID = QTextEdit('ID here...')
        self.loginID.setFixedHeight(50)
        self.loginPW = QTextEdit('PW here...')
        self.loginPW.setFixedHeight(50)
        self.enter = QPushButton('Enter')
        self.enter.clicked.connect(self.check_account)
        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.loginID)
        layout.addWidget(self.loginPW)
        layout.addWidget(self.enter)
        self.setLayout(layout)
        login = LoginDialog(self)

    def check_account(self):
        print("clicked")
        if self.loginID.toPlainText() == 'Admin' and self.loginPW.toPlainText() == 'Admin':
            self.status.setText("login successful!")
            self.status.repaint()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        d = LoginDialog()
        d.exec_()
        layout = QVBoxLayout()
        b = QPushButton('enter')
        b.clicked.connect(self.settext)
        self.l = QLabel('abc', self)
        self.l.setFixedSize(100, 100)
        layout.addWidget(self.l)
        layout.addWidget(b)
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.show()

    def settext(self):
        self.l.setText('abcd')
        self.l.repaint()
# https://freeprog.tistory.com/373
# app = QApplication(sys.argv)
# main_window = MainWindow()
# app.exec_()

