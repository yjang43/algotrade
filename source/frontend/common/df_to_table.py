from typing import List

import pandas as pd
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont



def df_to_table(df: pd.DataFrame):
    column_names: List = df.columns.to_list()
    table_row = df.shape[0]
    table_col = df.shape[1]
    # if df.shape[0] >= 10:
    #     table_row = 10
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


# def update_table(table: QTableWidget, data: pd.DataFrame):
#     table.setRowCount(data.shape[0])
#     table_row = data.shape[0]
#     table_col = data.shape[1]
#     table_size = (table_row, table_col)
#
#     for col in range(table_size[1]):
#         series = data[column_names[col]]
#         for row in range(table_size[0]):
#             value = QTableWidgetItem()
#             table.setItem(row, col, value)
#             value.setText(str(series[row]))
#     pass

class DataFrameTable(QTableWidget):
    def __init__(self, df, *args):
        super().__init__(*args)
        self.setColumnCount(len(df.columns))
        self.setHorizontalHeaderLabels(df.columns.to_list())
        self.df = df

        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)

        self.set_data()

    def set_data(self, new_df=None):
        if new_df is not None:
            self.df = new_df
        table_row = self.df.shape[0]
        table_col = self.df.shape[1]
        self.setRowCount(table_row)
        self.setColumnCount(table_col)
        for row in range(table_row):
            for col in range(table_col):
                item = QTableWidgetItem(self.df.iloc[row, col])
                self.setItem(row, col, item)

