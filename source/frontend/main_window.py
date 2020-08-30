from PyQt5.QtWidgets import *


from .common import PageButtons
from .account import AccountPage
from .auto_trade import AutoTradePage
from .data_visualization import DataVisualizationPage
from .login import LoginDialog
from backend.beta.backend_driver import BackendDriver


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._execute_login()
        self._init_backend_driver()

        pages = [AccountPage(parent=self), DataVisualizationPage(parent=self), AutoTradePage(parent=self)]
        self._init_main_widget(pages)

    def _init_backend_driver(self):
        self.backend_driver = BackendDriver()

    def _init_main_widget(self, pages):
        # main widget general setting
        main_widget = QWidget()
        main_widget.setMinimumSize(800, 450)
        main_widget_layout = QVBoxLayout()
        main_widget.setLayout(main_widget_layout)
        self.setCentralWidget(main_widget)

        # main widget add components
        self.page_buttons = PageButtons(pages)
        self.stack_widget = QStackedWidget()
        for page in pages:
            self.stack_widget.addWidget(page)

        self._connect_page_buttons()
        main_widget_layout.addWidget(self.page_buttons)
        main_widget_layout.addWidget(self.stack_widget)

    def _connect_page_buttons(self):
        page_each_button = [button for button in self.page_buttons.children() if type(button) is PageButtons.PageButton]
        for index, page in enumerate(page_each_button):
            page.clicked.connect(self._show_page(index))

    def _execute_login(self):
        # login process page
        login_dialog = LoginDialog(self)
        login_dialog.move(500, 300)
        login_dialog.exec()

    def _show_page(self, index):
        return lambda x: self._lambda(index)

    def _lambda(self, index):
        self.stack_widget.setCurrentIndex(index)
        self.repaint()

