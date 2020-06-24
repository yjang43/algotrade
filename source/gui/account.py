"""Renders account page

The script covers every gist of graphical component in account page
"""
import pandas as pd

from source.gui.pages import *
from source.gui.candlestick_graph import CandlestickGraph


class AccountPage(PageWidget):
    """PageWidget that holds components related to account management"""

    def __init__(self):
        """Initialize two panels"""
        super().__init__()
        self.layout().addWidget(self.set_panel1())
        self.layout().addWidget(self.set_panel2())

    def set_panel1(self):
        """Creates sections fits into panel1"""
        panel = QWidget()
        panel.setFixedSize(250, 400)
        panel.setLayout(QVBoxLayout())

        # user icon
        user_icon = QLabel()
        icon_image = QPixmap('source/gui/profileIcon.png')
        user_icon.setPixmap(icon_image)
        user_icon.setScaledContents(True)
        user_icon.setFixedSize(100, 100)

        # user balance status
        user_tot_balance = QLabel("total balance")
        user_tot_balance.setFixedSize(250, 30)
        user_tot_balance_table = QTableWidget()
        user_tot_balance_table.setRowCount(1)
        user_tot_balance_table.setColumnCount(4)
        user_tot_balance_table.setFixedHeight(45)
        user_tot_balance_table.setHorizontalHeaderLabels(['buy power', 'asset', 'profit', '(%)'])
        user_tot_balance_table.setColumnWidth(0, 70)
        user_tot_balance_table.setColumnWidth(1, 50)
        user_tot_balance_table.setColumnWidth(2, 50)
        user_tot_balance_table.setColumnWidth(3, 40)
        for row in range(user_tot_balance_table.rowCount()):
            user_tot_balance_table.setRowHeight(row, 10)

        # coin status
        user_coin_title = QLabel('my coin')
        user_coin_title.setFixedSize(250, 30)
        user_coin_table = df_to_table(pd.read_csv('source/data/coinsowned.csv'))
        for row in range(user_coin_table.rowCount()):
            user_coin_table.setRowHeight(row, 10)

        panel.layout().addWidget(user_icon)
        panel.layout().addWidget(user_tot_balance)
        panel.layout().addWidget(user_tot_balance_table)
        panel.layout().addWidget(user_coin_title)
        panel.layout().addWidget(user_coin_table)

        return panel

    def set_panel2(self):
        """Set components fit into panel2"""
        page = QWidget()
        page.setFixedSize(500, 450)
        page.setLayout(QVBoxLayout())

        notification_label = QLabel("Notification")
        notification_label.setFixedSize(500, 30)
        notification_file_path = "source/gui/notification.txt"
        notification = NotificationLog(notification_file_path)

        page.layout().addWidget(notification_label)
        page.layout().addWidget(notification)
        return page




class NotificationLog(QListWidget):
    def __init__(self, file_path):
        super().__init__()
        self.setFixedSize(500, 400)
        self.setSizePolicy(5, 5)
        self.load_notification(file_path)
    
    def load_notification(self, file_path):
        notification_list = list()
        with open(file_path) as f:
            for line in f:
                notification_list.insert(0, line.rstrip())
        self.addItems(notification_list)



