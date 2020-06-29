"""Renders account page

The script covers every gist of graphical component in account page
"""
import pandas as pd

from source.gui.pages import *
from source.gui.candlestick_graph import CandlestickGraph
from source.gui.login import LoginDialog
from source.account_management.my_exchange import Account


class AccountPage(PageWidget):
    """PageWidget that holds components related to account management"""

    def __init__(self):
        """Initialize two panels"""
        super().__init__()
        self.layout().addWidget(self.set_panel1())
        self.layout().addWidget(self.set_panel2())

    def set_panel1(self):
        panel = QWidget(parent=self)
        panel.setMinimumSize(250, 400)
        panel.setMaximumWidth(800)
        panel.setLayout(QVBoxLayout())

        # set welcome box
        #   - if logged in, welcome
        #   - if not logged in, warn user use of this app will be limitted
        welcome_text = QLabel()
        welcome_text.setTextFormat(Qt.RichText)
        if Account.is_login_correct:
            welcome_text.setText(
                "<h1>Welcome User</h1>"
            )
        else:
            welcome_text.setText(
                "<h1>Welcome User</h1>"
                "As you have not successfully logged in,"
                "some services will be limited"
            )

        asset_table = AssetTable()

        panel.layout().addWidget(welcome_text)
        panel.layout().addWidget(asset_table)

        return panel

    def set_panel2(self):
        """Set components fit into panel2"""
        page = QWidget(parent=self)
        page.setMinimumSize(500, 450)
        page.setLayout(QVBoxLayout())

        notification_label = QLabel("Notification")
        notification_label.setFixedHeight(30)
        notification_file_path = "source/gui/notification.txt"
        notification = NotificationLog(notification_file_path)

        page.layout().addWidget(notification_label)
        page.layout().addWidget(notification)
        return page


class NotificationLog(QListWidget):
    def __init__(self, file_path):
        super().__init__()
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)
        self.load_notification(file_path)

    def load_notification(self, file_path):
        notification_list = list()
        with open(file_path) as f:
            for line in f:
                notification_list.insert(0, line.rstrip())
        self.addItems(notification_list)


class AssetTable(QTableWidget):
    def __init__(self, *args):
        self.asset_df = self.df_init()

        row_num = self.asset_df.shape[0]
        col_num = self.asset_df.shape[1]
        super().__init__(row_num, col_num, *args)

        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)
        self.table_init()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(10000)
        self.timer.start()

    def df_init(self):
        coins_owned = Account.get_coin_list()
        coins_data = []
        for coin in coins_owned:
            coin_price = Account.get_coin_price(coin)
            coin_balance = Account.get_coin_balance(coin)
            coin_data = [coin, f"{coin_price: .2f}", f"{coin_balance: .2f}", f"{coin_price * coin_balance: .2f}"]
            coins_data.append(coin_data)

        return pd.DataFrame(coins_data, columns=['Name', 'Currency', 'Coin Balance', 'USD Value'])

    def table_init(self):
        column_names = self.asset_df.columns.to_list()
        self.setHorizontalHeaderLabels(column_names)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                value = QTableWidgetItem()
                self.setItem(i, j, value)
                value.setText(str(self.asset_df.iloc[i, j]))

    def update(self):
        for i in range(self.rowCount()):
            coin = self.item(i, 0).text()
            coin_price = Account.get_coin_price(coin)
            coin_balance = Account.get_coin_balance(coin)
            self.item(i, 1).setText(f"{coin_price: .2f}")
            self.item(i, 2).setText(f"{coin_balance: .2f}")
            self.item(i, 3).setText(f"{coin_price * coin_balance: .2f}")

            # self.item(i, 3).setText("updated value")

        super().update()




