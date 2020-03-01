from PyQt5.QtCore import *
from typing import List, Dict
import time
import random
import pandas as pd


class BackgroundProcess(QThread):
    trade = pyqtSignal(dict)
    process_id_count = 0

    def __init__(self, process, *args, **kwargs):
        super().__init__()
        self.process = process
        self.args = args
        self.kwargs = kwargs
        self.kwargs['trade_info'] = self.trade
        BackgroundProcess.process_id_count += 1
        self.process_id = BackgroundProcess.process_id_count
        self.kwargs['process_id'] = self.process_id

    def run(self):
        self.process(*self.args, **self.kwargs)


class ThreadManager(QObject):
    def __init__(self):
        super().__init__()
        self.threads = dict()

    def start_process(self, background_process: BackgroundProcess):
        background_process.trade.connect(self.trade_history_update)
        while True:
            process_number = background_process.process_id
            if not self.threads.__contains__(process_number):
                break
        self.threads[process_number] = background_process
        background_process.start()

    def trade_history_update(self, trade_info: Dict):
        # date, session, buy/sell, price
        # dictionary of strings
        df: pd.DataFrame = pd.read_csv('gui/trade_history.csv')
        d = trade_info
        print(d)
        for key in d:
            d[key] = d[key].split()
        df_to_add = pd.DataFrame(d)
        df = df_to_add.append(df, ignore_index=False)
        df.to_csv('gui/trade_history.csv', index=False)

    def get_process(self, process_number):
        return self.threads.get(process_number)

    def kill_process(self, process_number):
        process = self.threads.pop(process_number)
        process.terminate()
        process.wait()


# class MainWindow(QMainWindow):
#     def run_process(self):
#         background_process = BackgroundProcess(self.function, self.parameters)
#         self.thread_manager.start_process(background_process)
#
#     def kill_process(self):
#         process = self.thread_manager.threads.popitem()
#         process[1].terminate()
#         process[1].wait()
#

def process(parameters: List, trade_info: pyqtSignal, process_id):
    for n in range(5):
        time.sleep(1)
        print(n)
    trade_info.emit({'Date': 'today', 'Session#': str(process_id), 'Buy/Sell': 'buy', 'Price': '1$'})

