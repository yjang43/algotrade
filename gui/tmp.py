# algorithm function background runner
# https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
# need to take care of terminating algorithm!!!

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time

thread_pool = QThreadPool()


class FunctionSignals(QObject):
    # simple termination statement
    finished = pyqtSignal()
    # simple error statement
    error = pyqtSignal()
    # algorithm functions returns dictionary
    result = pyqtSignal(dict)
    # buy/sell dictionary
    progress = pyqtSignal(dict)


class FunctionRunner(QRunnable):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = FunctionSignals()

        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        try:
            result = self.function(*self.args, **self.kwargs)
        except Exception:
            self.signals.error.emit()
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()


class AlgoFunc():
    def __init__(self, func):
        print("runner init")
        self.func = func
        self.runner = FunctionRunner(self.func)

    def run_algo(self):
        self.runner.signals.error.connect(self.error_statement)
        self.runner.signals.result.connect(self.result_statement)
        self.runner.signals.finished.connect(self.finshed_statement)
        self.runner.signals.progress.connect(self.progress_statement)
        thread_pool.start(self.runner)
        print("started")

    def error_statement(self):
        print(str(self.func) + ": ERROR OCCURRED")

    def result_statement(self, result_dict):
        for key in result_dict:
            print(str(key) + ": " + str(result_dict[key]))

    def finshed_statement(self):
        print("\nprocess finished")

    def progress_statement(self, progress_dict):
        for key in progress_dict:
            print(str(key) + ": " + str(progress_dict[key]))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.b = QPushButton("push")
        # weird bug, if I don't use self, it doesn't do anything
        self.algorithm = AlgoFunc(self.count)
        print(self.algorithm.run_algo())
        self.b.clicked.connect(self.algorithm.run_algo)
        layout = QVBoxLayout()

        self.setCentralWidget(self.b)
        self.show()


def count(progress_callback):
    for n in range(5):
        print("count here")
        time.sleep(1)
        progress_callback.emit({'progress': n})
    return {"a": "abc"}

