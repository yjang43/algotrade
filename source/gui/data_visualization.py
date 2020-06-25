from source.gui.pages import *
from source.gui.candlestick_graph import CandlestickGraph
import ccxt


class DataVisualizationPage(PageWidget):
    def __init__(self):
        super().__init__()
        self.layout().addWidget(self.data_visualization_panel())
        self.layout().addWidget(self.data_analysis_panel())

    def data_visualization_panel(self):
        panel = QWidget()
        panel.setContentsMargins(0, 0, 0, 0)
        panel.setMinimumSize(600, 450)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        panel.setSizePolicy(size_policy)

        graph_layout = QVBoxLayout()
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.setSpacing(0)
        panel.setLayout(graph_layout)

        # search bar
        bar = SearchCoin()
        bar.setSizePolicy(size_policy)

        # candlestick graph
        df = pd.read_csv("source/data/dayohlcv.csv")
        self.bitcoin_graph = CandlestickGraph(df)
        self.bitcoin_graph.setMinimumSize(600, 300)

        graph_layout.addWidget(bar)
        graph_layout.addWidget(self.bitcoin_graph)

        return panel

    def option_bar(self):
        def update_graph():
            self.bitcoin_graph.update_candlesticks(pd.read_csv("source/data/minuteohlcv.csv"))
        bar = QWidget()
        bar_layout = QHBoxLayout()
        bar.setLayout(bar_layout)

        options = QComboBox()
        options.addItem("1")
        options.addItem("2")
        options.currentIndexChanged.connect(self.set_algo_visual)

        curr_option_label = QLabel("current option")

        help_button = QPushButton("H")
        help_button.clicked.connect(update_graph)
        # help_button.clicked.connect(print("clicked"))

        bar_layout.addWidget(options)
        bar_layout.addWidget(curr_option_label)
        bar_layout.addWidget(help_button)

        return bar

    def set_algo_visual(self):
        return

    def data_analysis_panel(self):
        panel = QWidget()
        panel.setMinimumSize(150, 300)
        panel.setMaximumWidth(200)
        panel.setContentsMargins(0, 0, 0, 0)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        panel.setSizePolicy(size_policy)

        layout = QGridLayout()
        panel.setLayout(layout)

        # options
        check1 = QCheckBox('check1')
        check1.setFixedHeight(30)
        check1.setContentsMargins(0, 0, 0, 0)
        check2 = QCheckBox('check2')
        check2.setFixedHeight(30)
        check2.setContentsMargins(0, 0, 0, 0)

        # layout.addWidget(label)
        layout.addWidget(check1, 0, 0)
        layout.addWidget(check2, 1, 0)

        return panel


class SearchCoin(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(600, 50)

        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)

        self.current_coin_searched = 'BTC/USDT'
        layout = QHBoxLayout()
        self.setLayout(layout)

        exchange = ccxt.binance()
        exchange.load_markets()
        self.coin_list = exchange.markets.keys()

        self.search_bar = self.create_search_bar()
        self.search_button = self.create_search_button()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.search_button)

    def create_search_bar(self):
        search_bar = QLineEdit('search...')
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        search_bar.setSizePolicy(size_policy)

        # set autocomplete when user starts an input
        completer = QCompleter(self.coin_list)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        search_bar.setCompleter(completer)
        search_bar.textChanged.connect(lambda x: print(x))
        return search_bar

    def create_search_button(self):
        def set_current_coin():
            self.current_coin_searched = self.search_bar.text()
            print('current coin searched: ', self.current_coin_searched)
        search_button = QPushButton('search')
        search_button.setFixedWidth(100)
        search_button.clicked.connect(set_current_coin)

        return search_button



