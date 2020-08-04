#import
from source.gui.pages import *
from source.back_processing.algorithm_wrapper import run_algorithm, emaalgorithm
import source.back_processing.thread_control as thread_control
from beta.backend_driver import BackendDriver


class AutoTradePage(PageWidget):
    def __init__(self):
        super().__init__()

        # instance member that needs communication in between
        self.drop_down_menu = None
        self.session = None
        self.tb: QTableWidget = None
        self.algo_menu = None
        self.current_algorithm = None
        self.session_num_clicked = -1
        self.session_df_row = -1

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
        # TODO: replace thread_manager with backend_driver
        self.thread_manager = thread_control.ThreadManager()
        self.backend_driver = BackendDriver()

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
        df = pd.read_csv('source/gui/trade_history.csv')

        # refresh panel2
        self.panel2.hide()
        self.panel2 = self.set_panel2()
        self.layout().insertWidget(1, self.panel2)

    def update_session(self):
        # upload DataFrame from the file
        df = pd.read_csv('source/back_processing/sessions.csv')

        # refresh panel2
        self.panel3.hide()
        self.panel3 = self.set_panel3()
        self.layout().insertWidget(2, self.panel3)


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
            print(self.algo_menu.currentText())

        def invest_clicked():
            """
            once Invest button is clicked, program runs an automated trade in
            the background, add session addition to trade history, and add session
            :return: calls functions to update status
            """
            # receive input from user input
            parameter = ema_option.get_parameters()
            # this will be put in to Session info
            print(parameter)
            # self.current_algorithm = run_algorithm(self.algo_menu.currentText(), parameters=parameter,
            #                                        process_id=thread_control.BackgroundProcess.process_id_count + 1)
            self.current_algorithm = emaalgorithm
            print(self.current_algorithm)

            # algorithm runs in the back
            algorithm_process = thread_control.BackgroundProcess(self.current_algorithm, parameter)
            self.thread_manager.start_process(algorithm_process)
            # self.algorithm = AlgoFunc(count)
            # self.algorithm.run_algo()

            # add session addition history to sessions
            df: pd.DataFrame = pd.read_csv('source/back_processing/sessions.csv')
            d = {'date': [thread_control.cur_datetime()], 'session_num': [algorithm_process.process_id],
                 'algorithm': ["algorithm"], 'profit': ['']}    # session data
            df_to_add = pd.DataFrame(d)
            df = df_to_add.append(df, ignore_index=False)
            df.to_csv('source/back_processing/sessions.csv', index=False)
            self.update_session()


        # set panel general attribute
        panel = QWidget(parent=self)
        panel.setMinimumSize(200, 400)
        panel.setMaximumWidth(400)
        panel.setLayout(QVBoxLayout())
        input_section = QStackedWidget()

        # drop down menu for algorithm to use
        self.algo_menu = QComboBox()
        self.algo_menu.addItem('ema/sma')
        self.algo_menu.addItem('granger causality')
        self.algo_menu.addItem('other algorithm')
        self.algo_menu.currentIndexChanged.connect(lambda: display_option(self.algo_menu.currentIndex(), input_section))  # signal

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
        panel.layout().addWidget(self.algo_menu)
        panel.layout().addWidget(input_section)
        panel.layout().addWidget(trade_btn)

        return panel

    def set_panel2(self):
        # set panel2 general attribute
        panel = QWidget(parent=self)
        panel.setMinimumSize(400, 400)
        panel.setLayout(QVBoxLayout())

        # trade history label
        lb = QLabel("trade history")
        lb.setFixedHeight(20)

        # trade history table
        df = pd.read_csv('source/gui/trade_history.csv')
        self.tb = df_to_table(df)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.tb.setSizePolicy(size_policy)

        # add components
        panel.layout().addWidget(lb)
        panel.layout().addWidget(self.tb)

        return panel

    def set_panel3(self):
        panel = QWidget(parent=self)
        panel.setMinimumSize(200, 400)
        panel.setLayout(QVBoxLayout())
        session_lb = QLabel("Sessions")
        session_lb.setFixedHeight(30)
        # date, session #. algorithm, benefit
        session_df = pd.read_csv("source/back_processing/sessions.csv")
        if session_df.shape[0] > 5:
            raise ValueError("there cannot be more than five sessions")
        session_table = df_to_table(session_df)
        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        session_table.setSizePolicy(size_policy)
        session_table.setRowCount(5)

        def set_session_clicked(row, col):
            print(str(row) + str(col))
            item = session_table.item(row, 1)
            if item is not None:
                self.session_num_clicked = int(session_table.item(row, 1).text())
                self.session_df_row = row
            print(self.session_num_clicked)

        def kill_session_clicked():
            if self.session_df_row == -1:
                print("invalid row clicked")
                return
            df = pd.read_csv("source/back_processing/sessions.csv")
            df = session_df.drop(self.session_df_row, axis='index')
            df = df.reset_index(drop=True)
            df.to_csv("source/back_processing/sessions.csv", index=False)
            self.thread_manager.kill_process(self.session_num_clicked)
            self.session_df_row = -1
            self.session_num_clicked = -1
            self.update_session()

        session_table.cellClicked.connect(set_session_clicked)

        session_terminate_button = QPushButton("terminate")
        session_terminate_button.clicked.connect(kill_session_clicked)

        status = QLabel("status")
        status.setFixedSize(200, 200)

        panel.layout().addWidget(session_lb)
        panel.layout().addWidget(session_table)
        panel.layout().addWidget(session_terminate_button)
        panel.layout().addWidget(status)
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
        :return: parameters that converted from str to int in list
        """
        parameters = list()
        children = ([child for child in self.children()
                     if type(child) == QTextEdit or type(child) == QCheckBox])  # retrieve QTextEdit and QCheckBox types
        for child in children:
            if type(child) == QTextEdit:
                param: str = child.toPlainText()
                if param.isdigit():
                    param = int(param)
                else:
                    param = -1  # sentinel value
                parameters.append(param)
        return parameters


class EmaOption(OptionSection):
    """
    option input section for ema algorithm
    """
    def __init__(self):
        super().__init__()
        # ema period
        ema_day_lb = QLabel("investment")
        ema_day_value = QTextEdit()
        ema_day_value.setFixedHeight(30)
        # risk high mid low
        risk_lb = QLabel("risk")
        risk_value = QTextEdit()
        risk_value.setFixedHeight(30)

        # input
        investment_lb = QLabel("investment")
        investment_val = QTextEdit()
        period_lb = QLabel("period")
        period_val = QTextEdit()
        short_term_lb = QLabel("short term")
        short_term_val = QTextEdit()
        medium_term_lb = QLabel("medium term")
        medium_term_val = QTextEdit()
        long_term_lb = QLabel("long term")
        long_term_val = QTextEdit()

        # layout
        self.layout().addWidget(investment_lb, 0, 0)
        self.layout().addWidget(investment_val, 0, 1)
        self.layout().addWidget(period_lb, 1, 0)
        self.layout().addWidget(period_val, 1, 1)
        self.layout().addWidget(short_term_lb, 2, 0)
        self.layout().addWidget(short_term_val, 2, 1)
        self.layout().addWidget(medium_term_lb, 3, 0)
        self.layout().addWidget(medium_term_val, 3, 1)
        self.layout().addWidget(long_term_lb, 4, 0)
        self.layout().addWidget(long_term_val, 4, 1)


