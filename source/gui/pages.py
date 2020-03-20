from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
from typing import List, Dict
from datetime import datetime
import source.back_processing.thread_control

class PageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 400)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)


def df_to_table(df: pd.DataFrame):
    column_names: List = df.columns.to_list()
    table_row = df.shape[0]
    table_col = df.shape[1]
    if df.shape[0] >= 10:
        table_row = 10
    table_size = (table_row, table_col)
    table = QTableWidget(table_size[0], table_size[1])
    table.setFont(QFont("Times", 12))
    table.setHorizontalHeaderLabels(column_names)
    for col in range(table_size[1]):
        series = df[column_names[col]]
        for row in range(table_size[0]):
            value = QTableWidgetItem()
            table.setItem(row, col, value)
            value.setText(str(series[row]))
    return table
