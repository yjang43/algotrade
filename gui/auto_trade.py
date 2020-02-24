from gui.pages import *

class AutoTradePage(PageWidget):
    def __init__(self):
        self.drop_down_menu = None
        self.session = None
        super().__init__()
        self.layout().addWidget(self.set_panel1())
        self.layout().addWidget(self.set_panel2())
        self.layout().addWidget(self.set_panel3())

    def set_panel1(self):
        def display_option(menu_index, stack_widget:QStackedWidget):
            stack_widget.setCurrentIndex(menu_index)

        panel = QWidget()
        panel.setFixedSize(200, 400)
        panel.setLayout(QVBoxLayout())
        input_section = QStackedWidget()

        # drop down menu for algorithm to use
        algo_menu = QComboBox()
        algo_menu.addItem('ema/sma')
        algo_menu.addItem('granger causality')
        algo_menu.addItem('other algorithm')
        algo_menu.currentIndexChanged.connect(lambda: display_option(algo_menu.currentIndex(), input_section))

        # stack widgets to show unique input page for each algorithm
        input_section.setFixedSize(200, 200)

        ema_option = EmaOption()
        i = OptionSection()
        input_section.addWidget(ema_option)
        input_section.addWidget(i)
        input_section.setCurrentIndex(0)


        # trade button
        trade_btn = QPushButton("Invest")
        trade_btn.setFixedSize(150, 30)
        trade_btn.clicked.connect(lambda x: print(ema_option.get_parameters()))

        panel.layout().addWidget(algo_menu)
        panel.layout().addWidget(input_section)
        panel.layout().addWidget(trade_btn)

        return panel

    def set_panel2(self):
        panel = QWidget()
        panel.setFixedSize(400, 400)
        panel.setLayout(QVBoxLayout())

        # trade history label
        lb = QLabel("trade history")

        # trade history table
        tb = QTableWidget(20, 4)
        tb.setHorizontalHeaderLabels(['date', 'session#', 'buy/sell', 'price'])

        # add components
        panel.layout().addWidget(lb)
        panel.layout().addWidget(tb)

        return panel

    def set_panel3(self):
        panel = QWidget()
        panel.setFixedSize(200, 400)
        panel.setLayout(QVBoxLayout())
        session_lb = QLabel("Sessions")

        panel.layout().addWidget(session_lb)
        return panel


class OptionSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

    def get_parameters(self):
        parameters = list()
        children = [child for child in self.children() if type(child) == QTextEdit or type(child) == QCheckBox]
        for child in children:
            if type(child) == QTextEdit:
                param = child.toPlainText()
                parameters.append(param)
        return parameters

class EmaOption(OptionSection):
    def __init__(self):
        super().__init__()
        # ema period
        ema_day_lb = QLabel("ema day")
        ema_day_value = QTextEdit()
        ema_day_value.setFixedHeight(30)
        # risk high mid low
        risk_lb = QLabel("risk")
        risk_value = QTextEdit()
        risk_value.setFixedHeight(30)

        #layout
        self.layout().addWidget(ema_day_lb, 0, 0)
        self.layout().addWidget(risk_lb, 1, 0)
        self.layout().addWidget(ema_day_value, 0, 1)
        self.layout().addWidget(risk_value, 1, 1)

