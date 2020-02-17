from gui.pages import *


class AutoTradePage(PageWidget):
    class InputSection(QWidget):
        def __init__(self):
            super().__init__()
            layout = QVBoxLayout()
            self.setLayout(layout)
            risk_lb = QLabel("risk")
            risk_txt = QTextEdit("risk")
            option2_lb = QLabel("option2")
            option2_txt = QTextEdit("option2")
            option3_lb = QLabel("option3")
            option3_txt = QTextEdit("option2")
            option4_lb = QLabel("option4")
            option4_check = QCheckBox()

            layout.addWidget(risk_lb)
            layout.addWidget(risk_txt)
            layout.addWidget(option2_lb)
            layout.addWidget(option2_txt)
            layout.addWidget(option3_lb)
            layout.addWidget(option3_txt)
            layout.addWidget(option4_lb)
            layout.addWidget(option4_check)

        def get_inputs(self):
            inputs = dict()
            for child in self.children():
                print(child)
            return inputs

    def __init__(self):
        self.drop_down_menu = None
        self.session = None
        super().__init__()
        self.layout().addWidget(self.set_panel1())
        self.layout().addWidget(self.set_panel2())
        self.layout().addWidget(self.set_panel3())

    def set_panel1(self):
        panel = QWidget()
        panel.setFixedSize(200, 400)
        panel.setLayout(QVBoxLayout())

        # drop down menu for algorithm to use
        algo_menu = QComboBox()
        algo_menu.addItem('ema/sma')
        algo_menu.addItem('granger causality')
        algo_menu.addItem('other algorithm')

        # stack widgets to show unique input page for each algorithm
        input_section = QStackedWidget()
        input_section.setFixedSize(200, 200)

        j = self.InputSection()
        i = self.InputSection()
        input_section.addWidget(i)
        input_section.addWidget(j)
        input_section.setCurrentIndex(0)


        # trade button
        trade_btn = QPushButton("trade")
        trade_btn.setFixedSize(150, 30)
        trade_btn.clicked.connect(lambda x: i.get_inputs())

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

