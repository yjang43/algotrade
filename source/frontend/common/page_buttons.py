from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class PageButtons(QWidget):
    class PageButton(QPushButton):
        def __init__(self, name):
            super().__init__(name)
            self.name = name
            self.setFixedSize(150, 30)

    def __init__(self, pages):
        super().__init__()
        # button group general setting
        self.setFixedSize(450, 30)
        page_buttons_layout = QHBoxLayout()
        page_buttons_layout.setSpacing(0)
        page_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(page_buttons_layout)

        # add buttons to button group
        for page in pages:
            page_button = self.PageButton(str(page))
            page_buttons_layout.addWidget(page_button)



