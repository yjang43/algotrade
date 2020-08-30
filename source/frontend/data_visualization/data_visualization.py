"""The script is responsible for rendering components in data visualization page"""
from PyQt5.QtWidgets import *
import pandas as pd

from ..common.pages import PageWidget
from .candlestick_graph import CandlestickGraph
from .search_coin import SearchCoin


class DataVisualizationPage(PageWidget):
    """PageWidget that holds components within data visualization page"""

    def __init__(self, *args, **kwargs):
        """Initializes instance"""
        super().__init__(*args, **kwargs)
        self.layout().addWidget(self.data_visualization_panel())
        # self.layout().addWidget(self.data_analysis_panel())

    def data_visualization_panel(self):
        """Creates data visualization panel"""

        def update_graph():
            """Updates the graph when needed"""
            dohlcvlist = self.bar.exchange.fetch_ohlcv(self.bar.current_coin_searched, '1d')
            ddfohlcv = pd.DataFrame.from_records(dohlcvlist)
            ddfohlcv.columns = ['Time', 'Open', 'High', "Low", "Close", "Volume"]
            print(ddfohlcv['Time'])
            ddfohlcv['Time'] = pd.to_datetime(ddfohlcv['Time'], unit='ms')
            new_df = ddfohlcv
            self.bitcoin_graph.update_candlesticks(new_df)

        panel = QWidget()
        panel.setContentsMargins(0, 0, 0, 0)
        panel.setMinimumSize(600, 450)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        panel.setSizePolicy(size_policy)

        graph_layout = QVBoxLayout()
        panel.setLayout(graph_layout)

        # search bar
        self.bar = SearchCoin()
        self.bar.setSizePolicy(size_policy)
        self.bar.search_button.clicked.connect(update_graph)
        self.bar.search_bar.editingFinished.connect(update_graph)

        # candlestick graph
        df = pd.read_csv("backend/data/dayohlcv.csv")
        self.bitcoin_graph = CandlestickGraph(df)
        self.bitcoin_graph.setMinimumSize(600, 300)

        graph_layout.addWidget(self.bar)
        graph_layout.addWidget(self.bitcoin_graph)

        return panel

    def option_bar(self):
        def update_graph():
            self.bitcoin_graph.update_candlesticks(pd.read_csv("backend/data/minuteohlcv.csv"))
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

        # layout = QGridLayout()
        # panel.setLayout(layout)
        #
        # # options
        # check1 = QCheckBox('check1')
        # check1.setFixedHeight(30)
        # check1.setContentsMargins(0, 0, 0, 0)
        # check2 = QCheckBox('check2')
        # check2.setFixedHeight(30)
        # check2.setContentsMargins(0, 0, 0, 0)
        #
        # # layout.addWidget(label)
        # layout.addWidget(check1, 0, 0)
        # layout.addWidget(check2, 1, 0)
        layout = QVBoxLayout()
        panel.setLayout(layout)
        algo_list = QComboBox()
        algo_list.addItems(['algorithm1', 'algorithm2', 'algorithm3'])

        layout.addWidget(algo_list)
        layout.addWidget(self.analysis())
        layout.addWidget(self.analysis_result())

        return panel

    def analysis(self):
        algo_options = QStackedWidget()
        algo_options.addWidget(QLabel('algorithm1'))
        algo_options.addWidget(QLabel('algorithm2'))
        algo_options.addWidget(QLabel('algorithm3'))
        return algo_options


    def analysis_result(self):
        result_section = QLabel("analysis result:")
        return result_section

    def __str__(self):
        return "Visualization"



class EmaAnalysis(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        c1 = QCheckBox('c1')
        layout.addWidget(c1, 0, 0)

