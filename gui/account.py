from gui.pages import *


class AccountPage(PageWidget):
    class CoinGraph(PlotWidget):
        def __init__(self, data_input_x, data_input_y, title):
            super().__init__()
            self.setFixedSize(250, 140)
            self.plot(data_input_x, data_input_y)
            self.showAxis('top', False)
            self.setBackground('w')
            self.setTitle(title)

    def __init__(self):
        super().__init__()
        self.layout().addWidget(self.set_panel1())
        self.layout().addWidget(self.set_panel2())
        self.layout().addWidget(self.set_panel3())

    def set_panel1(self):
        panel = QWidget()
        panel.setFixedSize(250, 400)
        panel.setLayout(QVBoxLayout())

        # user icon
        user_icon = QLabel()
        icon_image = QPixmap('gui/profileIcon.png')
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
        user_coin_table = QTableWidget(10, 5)
        user_coin_table.setFixedSize(250, 100)
        user_coin_table.setFont(QFont("Times", 12))
        user_coin_table.setHorizontalHeaderLabels(['coin', 'value', 'invest', 'value', '(%)'])
        user_coin_table.setColumnWidth(0, 30)
        user_coin_table.setColumnWidth(1, 50)
        user_coin_table.setColumnWidth(2, 50)
        user_coin_table.setColumnWidth(3, 50)
        user_coin_table.setColumnWidth(4, 40)
        for row in range(user_coin_table.rowCount()):
            user_coin_table.setRowHeight(row, 10)
        panel.layout().addWidget(user_icon)
        panel.layout().addWidget(user_tot_balance)
        panel.layout().addWidget(user_tot_balance_table)
        panel.layout().addWidget(user_coin_title)
        panel.layout().addWidget(user_coin_table)

        return panel

    def set_panel2(self):
        page = QWidget()
        page.setFixedSize(250, 450)
        page.setLayout(QVBoxLayout())
        history_label = QLabel("Log")
        history_label.setFixedSize(250, 30)
        history = QListWidget()
        history.setFixedSize(250, 400)
        history.addItems(['bought million dollar amount of btc', 'b'])
        history.setSizePolicy(5, 5)
        page.layout().addWidget(history_label)
        page.layout().addWidget(history)
        return page

    def set_panel3(self):
        page = QWidget()
        page.setFixedSize(250, 450)
        page.setLayout(QVBoxLayout())
        bitcoin_graph = self.CoinGraph([1,2,3, 4],[1,2,3, 3], 'btc')
        coin_graph = self.CoinGraph([1, 3, 2], [1,2,3], 'coin')

        page.layout().addWidget(bitcoin_graph)
        page.layout().addWidget(coin_graph)
        return page

