"""Renders account page

The script covers every gist of graphical component in account page
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer

from backend.account_management.my_exchange import Account
from frontend.common.pages import PageWidget
from frontend.common.df_to_table import DataFrameTable
from .notification_log import NotificationLog


class AccountPage(PageWidget):
    """PageWidget that holds components related to account management"""

    def __init__(self, *args, **kwargs):
        """Initialize two panels"""
        super().__init__(*args, **kwargs)
        self.layout().addWidget(self.set_panel1())
        self.layout().addWidget(self.set_panel2())
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(5000)
        self.timer.start()

    def update(self):
        self.asset_table.set_data(self.main_window.backend_driver.get_balance_df())

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

        # asset_table = AssetTable()
        self.asset_table = DataFrameTable(self.main_window.backend_driver.get_balance_df())

        panel.layout().addWidget(welcome_text)
        panel.layout().addWidget(self.asset_table)

        return panel

    def set_panel2(self):
        """Set components fit into panel2"""
        page = QWidget(parent=self)
        page.setMinimumSize(500, 450)
        page.setLayout(QVBoxLayout())

        notification_label = QLabel("Notification")
        notification_label.setFixedHeight(30)
        notification_file_path = "backend/notification.txt"
        notification = NotificationLog(notification_file_path)

        page.layout().addWidget(notification_label)
        page.layout().addWidget(notification)
        return page

    def __str__(self):
        return 'Account'





