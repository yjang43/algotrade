import sys
from PyQt5.QtWidgets import *
"""
    panel = QWidget()
    panel.setFixedSize(250, 400)
    panel.setLayout(QVBoxLayout())

    # user balance status
    user_tot_balance = QLabel("total balance")
    user_tot_balance.setFixedSize(250, 30)
    user_tot_balance_table = QTableWidget()
    user_tot_balance_table.setRowCount(1)
    user_tot_balance_table.setColumnCount(4)
    user_tot_balance_table.setFixedHeight(45)
    user_tot_balance_table.setHorizontalHeaderLabels(['buy power', 'asset', 'profit', '(%)'])
    user_tot_balance_table.setColumnWidth(0, 70)
    user_tot_balance_table.setColumnWidth(1, 50)
    user_tot_balance_table.setColumnWidth(2, 50)
    user_tot_balance_table.setColumnWidth(3, 40)
    for row in range(user_tot_balance_table.rowCount()):
        user_tot_balance_table.setRowHeight(row, 10)

    # coin status
    user_coin_title = QLabel('my coin')
    user_coin_title.setFixedSize(250, 30)
    user_coin_table = QTableWidget(10, 5)
    user_coin_table.setFixedSize(250, 100)
    user_coin_table.setFont(QFont("Times", 12))
    user_coin_table.setHorizontalHeaderLabels(['coin', 'value', 'invest', 'value', '(%)'])
    user_coin_table.setColumnWidth(0, 30)
    user_coin_table.setColumnWidth(1, 50)
    user_coin_table.setColumnWidth(2, 50)
    user_coin_table.setColumnWidth(3, 50)
    user_coin_table.setColumnWidth(4, 40)
    for row in range(user_coin_table.rowCount()):
        user_coin_table.setRowHeight(row, 10)
    panel.layout().addWidget(user_icon)
    panel.layout().addWidget(user_tot_balance)
    panel.layout().addWidget(user_tot_balance_table)
    panel.layout().addWidget(user_coin_title)
    panel.layout().addWidget(user_coin_table)
"""

import pandas as pd

app = QApplication(sys.argv)
col_header = {'coin':['btc', 'ith'], 'price':['100.00', '40.00'], 'invested':[1000.00, 2000.00], 'value':[1100.00, 1400.00], '%':['5%', '-30%']}
my_df = pd.DataFrame(col_header)
col_header = my_df.columns.to_list()
row_header = my_df.index.to_list()

user_coin_table = QTableWidget(row_header.__len__(), col_header.__len__())
user_coin_table.setHorizontalHeaderLabels(col_header)

for col_index in range(col_header.__len__()):
    for row_index in range(row_header.__len__()):
        e = my_df[col_header[col_index]][row_header[row_index]]
        user_coin_table.setItem(row_index, col_index, QTableWidgetItem(str(e)))


main_window = QMainWindow()
user_coin_table.setStyleSheet("background-color:black;")
main_window.setCentralWidget(user_coin_table)
main_window.show()

app.exec_()
