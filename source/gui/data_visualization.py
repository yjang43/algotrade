from source.gui.pages import *
from source.gui.candlestick_graph import CandlestickGraph

class DataVisualizationPage(PageWidget):
    def __init__(self):
        super().__init__()
        self.layout().addWidget(self.data_visualization_panel())
        self.layout().addWidget(self.data_analysis_panel())


    def data_visualization_panel(self):
        panel = QWidget()
        panel.setContentsMargins(0, 0, 0, 0)
        graph_layout = QVBoxLayout()
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.setSpacing(0)
        panel.setLayout(graph_layout)

        bar = self.option_bar()
        bar.setFixedSize(600, 50)

        df = pd.read_csv("source/data/dayohlcv.csv")
        bitcoin_graph = CandlestickGraph(df)
        bitcoin_graph.setFixedSize(600, 300)

        graph_layout.addWidget(bar)
        graph_layout.addWidget(bitcoin_graph)

        return panel

    def option_bar(self):
        bar = QWidget()
        bar_layout = QHBoxLayout()
        bar.setLayout(bar_layout)

        options = QComboBox()
        options.addItem("1")
        options.addItem("2")
        options.currentIndexChanged.connect(self.set_algo_visual)

        curr_option_label = QLabel("current option")

        help_button = QPushButton("H")
        # help_button.clicked.connect(print("clicked"))

        bar_layout.addWidget(options)
        bar_layout.addWidget(curr_option_label)
        bar_layout.addWidget(help_button)

        return bar

    def set_algo_visual(self):
        return

    def data_analysis_panel(self):
        panel = QWidget()
        panel.setFixedSize(150, 300)
        panel.setContentsMargins(0, 0, 0, 0)
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        panel.setLayout(layout)
        # label = QLabel("123")
        check1 = QCheckBox('check1')
        check1.setFixedSize(100, 30)
        check1.setContentsMargins(0, 0, 0, 0)
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
        return panel








