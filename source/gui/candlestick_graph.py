from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import pyqtgraph as pg
import sys
import time



"""
make graph, right top will show status in which generates open close high low volume stuff
"""


class CandlestickGraph(pg.PlotWidget):
    """
    generate candlestick graph with data in DataFrame
    """

    def __init__(self, data, *args, **kwargs):
        self.data = data[['Time', 'Open', 'Close', 'High', 'Low']]
        # timeline = self.data['Time']
        # timeline_list = list()
        # for t in timeline:
        #     timeline_list.append(t)
        # timeline_dict = dict()
        # for i in range(timeline_list.__len__()):
        #     timeline_dict[40 * i + 35] = timeline_list[i]
        # x_axis = AxisItem(orientation='bottom')
        # x_axis.setTicks([timeline_dict.items()])
        # x_axis.setTickSpacing([(3, 0), (1, 0), (0.25, 0)])

        super().__init__(axisItems={'bottom': StringAxis(data['Time'], orientation='bottom')}, *args, **kwargs)
        self.data = data[['Time', 'Open', 'Close', 'High', 'Low']]
        self.time_range, self.price_range = self.get_range(data)      # look at 100 most recent values
        # super().__init__(axisItems={'bottom': x_axis}, *args, **kwargs)
        self.generate_candlesticks()
        self.setRange(xRange=self.time_range, yRange=self.price_range, padding=0.01)


        self.setFixedSize(500, 250)
        self.setBackground('w')

    def get_range(self, data: pd.DataFrame):
        visible_offset = 30

        # timeline = data['Time'].iloc[data.shape[0] - visible_offset: data.shape[0]]
        time_from = (data.shape[0] - visible_offset) * CandlestickItem.CANDLESTICK_GAP
        time_to = data.shape[0] * CandlestickItem.CANDLESTICK_GAP

        low_prices = data['Low'].iloc[data.shape[0] - visible_offset: data.shape[0]]
        high_prices = data['High'].iloc[data.shape[0] - visible_offset: data.shape[0]]

        price_low = low_prices.min()
        price_high = high_prices.max()
        return (time_from, time_to), (price_low, price_high)

    def generate_candlesticks(self):
        for i in range(500):
            d = self.data.iloc[i]
            candle_stick = CandlestickItem(d)
            candle_stick.setPos(i * CandlestickItem.CANDLESTICK_GAP - CandlestickItem.CANDLESTICK_WIDTH / 2, d['Open'])
            self.addItem(candle_stick)

    def update_candlesticks(self, data):
        self.data = data[['Time', 'Open', 'Close', 'High', 'Low']]
        self.clear()
        self.time_range, self.price_range = self.get_range(data)      # look at 100 most recent values
        self.generate_candlesticks()
        self.setRange(xRange=self.time_range, yRange=self.price_range, padding=0.01)


class CandlestickItem(QGraphicsItem):
    CANDLESTICK_GAP = 100
    CANDLESTICK_WIDTH = 30
    """
    when we put the candle, in which position is it going to go
    """
    def __init__(self, data_bit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        (self.t, self.open_price, self.close_price, self.max_price, self.min_price) = data_bit

    def boundingRect(self):
        return QRectF(0, 0, CandlestickItem.CANDLESTICK_WIDTH, self.max_price)

    def paint(self, painter, option, widget):
        candle_color = QColor()
        candle = QRect(0, 0, CandlestickItem.CANDLESTICK_WIDTH, self.close_price - self.open_price)
        if self.open_price > self.close_price:
            candle_color.setNamedColor('red')
        else:
            candle_color.setNamedColor('green')
        painter.drawLine(QPointF(CandlestickItem.CANDLESTICK_WIDTH / 2.0, self.min_price - self.open_price),
                         QPointF(CandlestickItem.CANDLESTICK_WIDTH / 2.0, self.max_price - self.open_price))
        painter.fillRect(candle, candle_color)


class StringAxis(pg.AxisItem):
    def __init__(self, timeline, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timeline = timeline

    def tickStrings(self, values, scale, spacing):
        def convert_value(value):
            index = int(value / 100)
            if 0 <= index < self.timeline.shape[0]:
                return self.timeline.iloc[index]
            else:
                return 'nan'
        print(values)
        print(scale)
        print(spacing)
        print([int(value / 100) for value in values])
        return [convert_value(value) for value in values]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        data_set = pd.read_csv("source/data/hourohlcv.csv")
        # , Time, Open, High, Low, Close, Volume
        data_set = data_set[['Time', 'Open', 'Close', 'High', 'Low']]
        graph = CandlestickGraph(data_set)
        self.setCentralWidget(graph)
        self.show()

# app = QApplication(sys.argv)
# main_window = MainWindow()
# app.exec_()


# https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/customGraphicsItem.py
# https://stackoverflow.com/questions/31775468/show-string-values-on-x-axis-in-pyqtgraph
# https://freeprog.tistory.com/373
