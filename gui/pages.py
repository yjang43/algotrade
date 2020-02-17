from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyqtgraph import *

class PageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 400)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)


