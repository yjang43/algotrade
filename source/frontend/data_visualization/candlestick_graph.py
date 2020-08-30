"""Contains classes that render candlestick graph"""
import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import pandas as pd


class CandlestickGraph(pg.PlotWidget):
    """Generates candlestick graph with data in DataFrame"""

    def __init__(self, data, *args, **kwargs):
        """Initializes candlestick graph"""
        # self.data = data[['Time', 'Open', 'Close', 'High', 'Low']]
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

        super().__init__()
        # super().__init__(axisItems={'bottom': StringAxis(data['Time'], orientation='bottom')}, *args, **kwargs)
        # self.data = data[['Time', 'Open', 'Close', 'High', 'Low']]
        # self.time_range, self.price_range = self.get_range(data)      # look at 100 most recent values
        # # super().__init__(axisItems={'bottom': x_axis}, *args, **kwargs)
        # self.generate_candlesticks()
        # self.setRange(xRange=self.time_range, yRange=self.price_range, padding=0.01)

        size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(size_policy)
        self.setBackground('w')

    def get_range(self, data: pd.DataFrame):
        """Gets the range of data being visualized"""
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
        """Generates 500 candlesticks"""
        for i in range(500):
            d = self.data.iloc[i]
            candle_stick = CandlestickItem(d)
            candle_stick.setPos(i * CandlestickItem.CANDLESTICK_GAP - CandlestickItem.CANDLESTICK_WIDTH / 2, d['Open'])
            self.addItem(candle_stick)

    def update_candlesticks(self, data):
        """Updates candlestick"""
        # Todo: update axisItems
        # self.getPlotItem().setAxisItems(axisItems={'bottom': StringAxis(data['Time'])})
        self.data = data[['Time', 'Open', 'Close', 'High', 'Low']]
        self.clear()
        self.time_range, self.price_range = self.get_range(data)      # look at 100 most recent values
        self.generate_candlesticks()
        self.setAxisItems({'bottom': StringAxis(data['Time'], orientation='bottom')})
        self.setRange(xRange=self.time_range, yRange=self.price_range, padding=0.01)


class CandlestickItem(QGraphicsItem):
    """Contains description of each candlestick"""

    CANDLESTICK_GAP = 100
    CANDLESTICK_WIDTH = 30

    def __init__(self, data_bit, *args, **kwargs):
        """Initializes one candlestick instance"""
        super().__init__(*args, **kwargs)
        (self.t, self.open_price, self.close_price, self.max_price, self.min_price) = data_bit

    def boundingRect(self):
        """Bounds one candlestick instance"""
        return QRectF(0, 0, CandlestickItem.CANDLESTICK_WIDTH, self.max_price)

    def paint(self, painter, option, widget):
        """Render candlestick instance"""
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
    """Subclass of AxisItem that describes axis containing timeline"""

    def __init__(self, timeline, *args, **kwargs):
        """Initializes timeline of the graph"""
        super().__init__(*args, **kwargs)
        self.timeline = timeline

    def tickStrings(self, values, scale, spacing):
        """Puts string value to the Axis"""
        def convert_value(value):
            index = int(value / 100)
            if 0 <= index < self.timeline.shape[0]:
                return self.timeline.iloc[index]
            else:
                return 'nan'

        return [convert_value(value) for value in values]

# https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/customGraphicsItem.py
# https://stackoverflow.com/questions/31775468/show-string-values-on-x-axis-in-pyqtgraph
# https://freeprog.tistory.com/373
