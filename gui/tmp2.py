from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time
import sys

pool = QThreadPool()
class Process(QRunnable):

    def __init__(self, function):
        super().__init__()
        self.function = function

    @pyqtSlot()
    def run(self):
        result = self.function()
        self.started.emit("process started")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.b = QPushButton("button")
        self.b.clicked.connect(self.b_clicked)
        self.setCentralWidget(self.b)

    def b_clicked(self):
        process = Process(count)
        pool.start(process)

    def started_statement(self, statement):
        print(statement)


def count():
    for n in range(5):
        time.sleep(1)
        print(n)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()

app.exec_()
