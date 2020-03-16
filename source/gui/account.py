from gui.pages import *
import pandas as pd
from CandlestickGraph import CandlestickGraph

class AccountPage(PageWidget):

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
        user_coin_table = df_to_table(pd.read_csv('csv/coinsowned.csv'))
        # user_coin_table = QTableWidget(10, 5)
        # user_coin_table.setFixedSize(250, 100)
        # user_coin_table.setFont(QFont("Times", 12))
        # user_coin_table.setHorizontalHeaderLabels(['coin', 'value', 'invest', 'value', '(%)'])
        # user_coin_table.setColumnWidth(0, 30)
        # user_coin_table.setColumnWidth(1, 50)
        # user_coin_table.setColumnWidth(2, 50)
        # user_coin_table.setColumnWidth(3, 50)
        # user_coin_table.setColumnWidth(4, 40)
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
        notification_label = QLabel("Notification")
        notification_label.setFixedSize(250, 30)
        notification_file_path = "gui/notification.txt"
        notification = NotificationLog(notification_file_path)
        page.layout().addWidget(notification_label)
        page.layout().addWidget(notification)
        return page

    def set_panel3(self):
        page = QWidget()
        page.setFixedSize(250, 450)
        page.setLayout(QVBoxLayout())
        df = pd.read_csv("csv/ohlcv.csv")
        # bitcoin_graph = CoinGraph(title='btc', labels={'left': 'price', 'bottom': 'time'})
        # bitcoin_graph.getPlotItem().addItem(GraphData(df))
        bitcoin_graph = CandlestickGraph(df)
        coin_graph = CoinGraph(title='other coin', labels={'left': 'price', 'bottom': 'time'})
        coin_graph.getPlotItem().addItem(GraphData(df))
        pdi = PlotDataItem()
        pdi.setData(df[['Time', 'Volume']].to_numpy())
        coin_graph.getPlotItem().addItem(pdi)
        tmp = df['Time']
        coin_graph.getPlotItem().setXRange(tmp.loc[1], tmp.loc[30])
        page.layout().addWidget(bitcoin_graph)
        page.layout().addWidget(coin_graph)
        return page


class GraphData(PlotDataItem):
    def __init__(self, df: pd.DataFrame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        price_data = self.open_price(df)
        self.setData(price_data)

    def open_price(self, df: pd.DataFrame):
        # time and open price
        price:pd.DataFrame = df[['Time', 'Open']]
        price = price.to_numpy()
        return price

class NotificationLog(QListWidget):
    def __init__(self, file_path):
        super().__init__()
        self.setFixedSize(250, 400)
        self.setSizePolicy(5, 5)
        self.load_notification(file_path)
    
    def load_notification(self, file_path):
        notification_list = list()
        with open(file_path) as f:
            for line in f:
                notification_list.insert(0, line.rstrip())
        self.addItems(notification_list)

    
    
class CoinGraph(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(250, 130)
        self.showAxis('top', False)
        self.setBackground('w')


