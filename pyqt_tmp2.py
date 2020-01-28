from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

ACCOUNT = 'account'


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        main_widget = QWidget()
        main_widget_layout = QVBoxLayout()
        main_widget.setLayout(main_widget_layout)

        # add widgets to stack_widget
        page_buttons = PageButtons()
        page_each_button = [button for button in page_buttons.children() if type(button) is PageButtons.PageButton]
        page_each_button[0].clicked.connect(lambda x: self.display(page_each_button[0]))
        page_each_button[1].clicked.connect(lambda x: self.display(page_each_button[1]))
        page_each_button[2].clicked.connect(lambda x: self.display(page_each_button[2]))


        main_widget_layout.addWidget(page_buttons)
        self.stack_widget = QStackedWidget(self)

        main_widget_layout.addWidget(self.stack_widget)
        page1 = PageWidget()
        page1.set_color('red')
        page2 = PageWidget()
        page2.set_color('green')
        page3 = PageWidget()
        page3.set_color('yellow')

        self.stack_widget.addWidget(page1)
        self.stack_widget.addWidget(page2)
        self.stack_widget.addWidget(page3)

        main_widget.setMinimumSize(800, 450)
        self.setCentralWidget(main_widget)
        self.resize(800, 450)

    def display(self, button_clicked):
        if button_clicked.name == 'account':
            self.stack_widget.setCurrentIndex(0)
        elif button_clicked.name == 'data visualization':
            self.stack_widget.setCurrentIndex(1)
        else:
            self.stack_widget.setCurrentIndex(2)




class PageWidget(QWidget):
    def __init__(self):
        super().__init__()

    def set_color(self, color: str):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)



class PageButtons(QWidget):
    class PageButton(QPushButton):
        def __init__(self, name):
            super().__init__(name)
            self.name = name
            self.setFixedSize(150, 30)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(450, 30)
        account_page_button = self.PageButton('account')
        data_visualization_button = self.PageButton('data visualization')
        auto_trade_button = self.PageButton('auto trade')

        page_buttons_layout = QHBoxLayout()
        page_buttons_layout.setContentsMargins(0, 0, 0, 0)
        page_buttons_layout.setSpacing(0)
        page_buttons_layout.addWidget(account_page_button)
        page_buttons_layout.addWidget(data_visualization_button)
        page_buttons_layout.addWidget(auto_trade_button)
        self.setLayout(page_buttons_layout)


app = QApplication(sys.argv)
a = PageWidget()
main_window = MainWindow()
main_window.show()

app.exec_()

