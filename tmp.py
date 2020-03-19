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
        self.setContentsMargins(0, 0, 0, 0)

        main = QWidget()
        main.setFixedSize(250, 180)
        main.setContentsMargins(0, 0, 0, 0)

        ml = QHBoxLayout()
        main.setLayout(ml)
        w = QWidget()

        b = QPushButton("hello")
        panel = QWidget()
        ml.addWidget(w)
        ml.addWidget(panel)

        panel.setFixedSize(150, 180)
        layout = QGridLayout()
        panel.setLayout(layout)
        # label = QLabel("123")
        check1 = QCheckBox('check1')
        check1.setFixedSize(100, 30)
        check1.setContentsMargins(0, 0, 0, 0)
        print(check1.size())
        check2 = QCheckBox('check2')
        check2.setFixedSize(100, 30)
        check2.setContentsMargins(0, 0, 0, 0)
        check3 = QCheckBox('check3')
        check3.setFixedSize(100, 30)
        check3.setContentsMargins(0, 0, 0, 0)
        check4 = QCheckBox('check4')
        check4.setFixedSize(100, 30)
        check4.setContentsMargins(0, 0, 0, 0)
        check5 = QCheckBox('check5')
        check5.setFixedSize(100, 30)
        check5.setContentsMargins(0, 0, 0, 0)
        check6 = QCheckBox('check6')
        check6.setFixedSize(100, 30)
        check6.setContentsMargins(0, 0, 0, 0)

        # layout.addWidget(label)
        layout.addWidget(check1, 0, 0)
        layout.addWidget(check2, 1, 0)
        layout.addWidget(check3, 2, 0)
        layout.addWidget(check4, 3, 0)
        layout.addWidget(check5, 4, 0)
        layout.addWidget(check6, 5, 0)
        self.setCentralWidget(main)
        self.show()

    def settext(self):
        self.l.setText('abcd')
        self.l.repaint()
# https://freeprog.tistory.com/373
app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()


