from gui.algorithms import emaalgorithm
from PyQt5.QtCore import *


# dictionary of algorithms
# 'tag of algorithm name in combo box menu: algorithm function
algorithms = {'ema/sma': emaalgorithm}

# how to put list as parameters in python
# https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists


def run_algorithm(algorithm_key: str, parameters: list, process_id):
    return algorithms[algorithm_key]
    # algorithms[algorithm_key](*parameters, date=cur_datetime(), session_num='session_num')


# add this to jay's function!!!
def send_signal(trade_info: pyqtSignal, kwargs: dict, buy_sell = 0, amount = 0):
    emit_dict = kwargs
    emit_dict['buy_sell'] = buy_sell
    emit_dict['amount'] = amount
    trade_info.emit(emit_dict)




