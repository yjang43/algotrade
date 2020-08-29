from PyQt5.QtWidgets import *
import time

from backend.account_management.my_exchange import Account


class LoginDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Login')
        self.status = QLabel()
        self.status.setText("enter your account information")
        self.loginID = QTextEdit('Public Key here...')
        self.loginID = QTextEdit('nOK54jyAMTSkrCicsBtqZErob8SORYj3qXjrIull8PSgkSs4dVxSbVz9HIYkpv13')
        self.loginID.setFixedHeight(50)
        self.loginPW = QTextEdit('Private Key here...')
        self.loginPW = QTextEdit('0l93ZNwaAzHaWGSiphrKvFJw0w9BH3nT5NlcLvQbfXotx4tbdOW5sTfqBAbwgON1')
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
        # for develop purpose I bring keys from "tmp_do_not_add.py"
        public_key = self.loginID.toPlainText()
        private_key = self.loginPW.toPlainText()
        # exchange = ccxt.binance()
        # exchange.apiKey = public_key
        # exchange.secret = private_key
        #
        # try:
        #     exchange.fetch_balance()
        #     is_login_correct = True
        # except ccxt.errors.AuthenticationError:
        #     is_login_correct = False
        is_login_correct = Account.login(public_key, private_key)
        print("login correct: ", is_login_correct)

        if is_login_correct:
            self.status.setText("login successful!")
            self.status.repaint()
            time.sleep(2)
            self.close()
        else:
            self.status.setText("wrong credentials, try again")
            self.status.repaint()




