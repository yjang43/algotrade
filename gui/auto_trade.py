from gui.pages import *

class AutoTradePage(PageWidget):
    def __init__(self):
        self.drop_down_menu = None
        self.session = None
        self.tb: QTableWidget = None
        super().__init__()
        self.panel1 = self.set_panel1()
        self.panel2 = self.set_panel2()
        self.panel3 = self.set_panel3()
        self.layout().addWidget(self.panel1)
        self.layout().addWidget(self.panel2)
        self.layout().addWidget(self.panel3)

        # 2.25 add QTimer to update table
        self.timer_status = QTimer()
        self.timer_status.timeout.connect(self.update_all_views)
        self.timer_status.setInterval(10000)
        self.timer_status.start()

    def update_all_views(self):
        self.update_trade_history()

    def update_trade_history(self):
        df = pd.read_csv('gui/trade_history.csv')

        df.to_csv('gui/trade_history.csv', index=False)
        # self.tb.setItem(0, 0, QTableWidgetItem('test'))
        self.panel2.hide()
        # self.layout().removeWidget(self.panel1)
        print(self.layout().count)
        self.panel2 = self.set_panel2()
        self.layout().insertWidget(1, self.panel2)

    def set_panel1(self):
        def display_option(menu_index, stack_widget:QStackedWidget):
            stack_widget.setCurrentIndex(menu_index)

        def invest_clicked():
            df: pd.DataFrame = pd.read_csv('gui/trade_history.csv')
            # df_to_add = pd.DataFrame(columns=df.columns)
            # df_to_add = df_to_add.append({'Date': '-', 'Session#': '-', 'Buy/Sell': '-', 'Price': '-'})
            d = {'Date': ['date'], 'Session#': ['session'], 'Buy/Sell': ['buy'], 'Price': ['price']}
            df_to_add = pd.DataFrame(d)
            # print(df_to_add)
            df = df_to_add.append(df, ignore_index=False)
            df.to_csv('gui/trade_history.csv', index=False)
            # self.panel2 = self.set_panel2()
            print(ema_option.get_parameters())
            # need to implement QTimer!!!!!!


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
        trade_btn.clicked.connect(lambda x: invest_clicked())

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
        df = pd.read_csv('gui/trade_history.csv')
        self.tb = df_to_table(df)

        # add components
        panel.layout().addWidget(lb)
        panel.layout().addWidget(self.tb)

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



def cur_datetime():
    cur_date = datetime.now().strftime("%d/%m/%y")
    cur_time = datetime.now().strftime("%H:%M:%S")
    ret = (str(cur_date) + "-" + str(cur_time))
    print(ret)
    return ret
