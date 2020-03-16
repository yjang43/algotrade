from PyQt5.QtCore import *
from typing import List, Dict
import time
from datetime import datetime
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
        df: pd.DataFrame = pd.read_csv('source/gui/trade_history.csv')
        d = trade_info
        print(d)
        for key in d:
            d[key] = d[key].split()
        df_to_add = pd.DataFrame(d)
        df = df_to_add.append(df, ignore_index=False)
        df.to_csv('source/gui/trade_history.csv', index=False)

    def get_process(self, process_number):
        return self.threads.get(process_number)

    def kill_process(self, process_number):
        print(self.threads)
        print(process_number)
        if not self.threads.__contains__(process_number):
            return
        process = self.threads.pop(process_number)
        process.terminate()
        print("process terminated")
        process.wait()


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


def process(parameters: List, trade_info: pyqtSignal, process_id):
    for n in range(60):
        if n % 10 == 0:
            cur_time = cur_datetime()
            trade_info.emit({'date': cur_time, 'session_num': str(process_id), 'buy_sell': 'buy', 'amount': '1$'})
        time.sleep(1)
        print(n)

