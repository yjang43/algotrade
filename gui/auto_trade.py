#import
from gui.pages import *


class AutoTradePage(PageWidget):
    def __init__(self):
        super().__init__()

        # instance member that needs communication in between
        self.drop_down_menu = None
        self.session = None
        self.tb: QTableWidget = None
        self.current_algorithm = thread_control.process

        # panel setting
        self.panel1 = self.set_panel1()
        self.panel2 = self.set_panel2()
        self.panel3 = self.set_panel3()
        self.layout().addWidget(self.panel1)
        self.layout().addWidget(self.panel2)
        self.layout().addWidget(self.panel3)

        # add QTimer to update table
        self.timer_status = QTimer()
        self.timer_status.timeout.connect(self.update_all_views)
        self.timer_status.setInterval(10000)
        self.timer_status.start()

        # thread manager
        self.thread_manager = thread_control.ThreadManager()

    def update_all_views(self):
        """
        updates trade history and session uploaded
        need to implement session update part later
        :return: updates trade history and session upload
        """
        self.update_trade_history()

    def update_trade_history(self):
        """
        upload most recent data from gui/trade_history.csv into trade
        history table
        :return: update trade history
        """
        # upload DataFrame from the file
        df = pd.read_csv('gui/trade_history.csv')

        # refresh panel2
        self.panel2.hide()
        self.panel2 = self.set_panel2()
        self.layout().insertWidget(1, self.panel2)

    def set_panel1(self):
        """
        sets widgets in panel1
        :return: panel1
        """
        def display_option(menu_index, stack_widget: QStackedWidget):
            """
            display algorithm input options
            :param menu_index: index of the stack widget
            :param stack_widget: stacks of input section
            :return: sets index of input section as menu_index
            """
            stack_widget.setCurrentIndex(menu_index)

        def invest_clicked():
            """
            once Invest button is clicked, program runs an automated trade in
            the background, add session addition to trade history, and add session
            :return: calls functions to update status
            """
            # add session addition history to trade history
            # df: pd.DataFrame = pd.read_csv('gui/trade_history.csv')
            # d = {'Date': [cur_datetime()], 'Session#': ['session'], 'Buy/Sell': [''], 'Price': ['']}    # session data
            # df_to_add = pd.DataFrame(d)
            # df = df_to_add.append(df, ignore_index=False)
            # df.to_csv('gui/trade_history.csv', index=False)

            # update trade_history table to show user session is created
            # self.panel2.hide()
            # self.panel2 = self.set_panel2()
            # self.layout().insertWidget(1, self.panel2)

            # receive input from user input
            # it's just printing for now
            parameter = ema_option.get_parameters()

            # algorithm runs in the back
            algorithm_process = thread_control.BackgroundProcess(self.current_algorithm, parameter)
            self.thread_manager.start_process(algorithm_process)
            # self.algorithm = AlgoFunc(count)
            # self.algorithm.run_algo()


        # set panel general attribute
        panel = QWidget()
        panel.setFixedSize(200, 400)
        panel.setLayout(QVBoxLayout())
        input_section = QStackedWidget()

        # drop down menu for algorithm to use
        algo_menu = QComboBox()
        algo_menu.addItem('ema/sma')
        algo_menu.addItem('granger causality')
        algo_menu.addItem('other algorithm')
        algo_menu.currentIndexChanged.connect(lambda: display_option(algo_menu.currentIndex(), input_section))  # signal

        # stack widgets to show unique input page for each algorithm
        input_section.setFixedSize(200, 200)
        # option pages
        ema_option = EmaOption()   # each option section will require its own class
        i = OptionSection()
        input_section.addWidget(ema_option)
        input_section.addWidget(i)
        input_section.setCurrentIndex(0)

        # trade button
        trade_btn = QPushButton("Invest")
        trade_btn.setFixedSize(150, 30)
        trade_btn.clicked.connect(invest_clicked)

        # add components
        panel.layout().addWidget(algo_menu)
        panel.layout().addWidget(input_section)
        panel.layout().addWidget(trade_btn)

        return panel

    def set_panel2(self):
        # set panel2 general attribute
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
    """
    general option input section for algorithms in panel 1
    """
    def __init__(self):
        super().__init__()
        layout = QGridLayout()  # grid layout for flexible widget layout
        self.setLayout(layout)

    def get_parameters(self):
        """
        get user inputs of the algorithm
        :return: parameters in list
        """
        parameters = list()
        children = ([child for child in self.children()
                     if type(child) == QTextEdit or type(child) == QCheckBox])  # retrieve QTextEdit and QCheckBox types
        for child in children:
            if type(child) == QTextEdit:
                param = child.toPlainText()
                parameters.append(param)
        return parameters


class EmaOption(OptionSection):
    """
    option input section for ema algorithm
    """
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

        # layout
        self.layout().addWidget(ema_day_lb, 0, 0)
        self.layout().addWidget(risk_lb, 1, 0)
        self.layout().addWidget(ema_day_value, 0, 1)
        self.layout().addWidget(risk_value, 1, 1)


def cur_datetime():
    """
    return string of current date time
    this function is general so need to be in different file
    :return: string of current date time
    """
    cur_date = datetime.now().strftime("%d/%m/%y")
    cur_time = datetime.now().strftime("%H:%M:%S")
    ret = (str(cur_date) + "-" + str(cur_time))
    print(ret)
    return ret
