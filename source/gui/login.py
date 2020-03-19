from PyQt5.QtWidgets import *


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

    def check_account(self):
        print("clicked")
        if self.loginID.toPlainText() == 'Admin' and self.loginPW.toPlainText() == 'Admin':
            self.status.setText("login successful!")
            self.status.repaint()




