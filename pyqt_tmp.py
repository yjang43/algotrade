from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

ACCOUNT = 'account'
DATA_VISUALIZATION = 'data visualization'
AUTO_TRADE = 'auto trade'

pages = []


class MainWindow(QMainWindow):
    class PageButtons(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            button_layout = QHBoxLayout()
            self.add_buttons(button_layout)
            self.setFixedSize(600, 50)
            self.setLayout(button_layout)

        @staticmethod
        def add_buttons(button_layout):
            """
            add account, data visualization, auto trade tabs
            """
            account_button = QPushButton(ACCOUNT)
            account_button.setFixedSize(200, 30)
            account_button.clicked.connect(lambda x: pages[0].hide())
            data_visualization_button = QPushButton(DATA_VISUALIZATION)
            auto_trade_button = QPushButton(AUTO_TRADE)
            button_layout.addWidget(account_button)
            button_layout.addWidget(data_visualization_button)
            button_layout.addWidget(auto_trade_button)

    class PageWidget(QWidget):
        def __init__(self, widget_name:str,  *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setMinimumSize(600, 400)
            self.resize(100, 100)
            self.widget_name = widget_name
            self.setAutoFillBackground(True)
            palette = self.palette()
            palette.setColor(QPalette.Window, QColor('red'))
            self.setPalette(palette)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        account_page = self.PageWidget('page')
        pages.append(account_page)

        main_widget = QWidget()
        main_widget_layout = QVBoxLayout()

        # main widget layout setting
        main_widget_layout.setContentsMargins(0, 0, 0, 0)
        main_widget_layout.setSpacing(0)

        main_widget.setLayout(main_widget_layout)
        main_widget_layout.addWidget(self.PageButtons())
        main_widget_layout.addWidget(account_page)
        self.setCentralWidget(main_widget)
        self.resize(800, 450)


app = QApplication(sys.argv)
main_window = MainWindow()

#main_window.show()
main_window.PageWidget('a').show()
app.exec_()
