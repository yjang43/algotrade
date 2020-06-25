from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import ccxt


class LoginDialog(QDialog):
    is_login_correct = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Login')
        self.status = QLabel()
        self.status.setText("enter your account information")
        self.loginID = QTextEdit('Public Key here...')
        self.loginID.setFixedHeight(50)
        self.loginPW = QTextEdit('Private Key here...')
        self.loginPW.setFixedHeight(50)
        self.enter = QPushButton('Enter')
        self.enter.clicked.connect(self.check_account)
        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addWidget(self.loginID)
        layout.addWidget(self.loginPW)
        layout.addWidget(self.enter)
        self.setLayout(layout)

    def check_account(self):
        public_key = self.loginID.toPlainText()
        private_key = self.loginPW.toPlainText()
        exchange = ccxt.binance()
        exchange.apiKey = public_key
        exchange.secret = private_key

        try:
            exchange.fetch_balance()
            is_login_correct = True
        except ccxt.errors.AuthenticationError:
            is_login_correct = False

        if is_login_correct:
            self.status.setText("login successful!")
            self.status.repaint()
            self.close()
        else:
            self.status.setText("wrong credentials, try again")
            self.status.repaint()




