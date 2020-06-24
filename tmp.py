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


from source.gui.login import LoginDialog
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.coins = QLineEdit("coin symbol...")
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.coins.setCompleter(completer)
        self.coins.textChanged.connect(lambda x: print(x))
        self.coins.returnPressed.connect(self.enter_pressed)

        self.setCentralWidget(self.coins)
        self.show()
        # login = LoginDialog()
        # login.exec()


app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()


