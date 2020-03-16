from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
from pyqtgraph import *
import sys
import time

CANDLESTICK_GAP = 40
CANDLESTICK_WIDTH = 10

"""
make graph, right top will show status in which generates open close high low volume stuff
"""


class CandlestickGraph(PlotWidget):
    def __init__(self, data, *args, **kwargs):
        """
        generate candlestick graph with data in DataFrame
        :param data: DataFrame with ['Time', 'Open', 'Close', 'High', 'Low']
        """
        super().__init__(axisItems={'bottom': StringAxis(orientation='bottom')}, *args, **kwargs)
        self.setFixedSize(500, 250)
        self.setBackground('w')
        self.data = data[['Time', 'Open', 'Close', 'High', 'Low']]
        self.candlestick_width = 10
        self.generate_candlesticks()

    def generate_candlesticks(self):
        for i in range(20):
            d = self.data.iloc[i]
            print(d)
            candle_stick = CandlestickItem(d)
            candle_stick.setPos(i * 40 - self.candlestick_width / 2, d['Open'])
            self.addItem(candle_stick)

    def set_axis(self):
        x_axis_data = {i: i for i in range(20)}
        x_axis = self.getAxis('bottom')
        x_axis.setTicks(x_axis_data)


class StringAxis(AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def tickStrings(self, values, scale, spacing):
        return [time.strftime("%H:%M:%S", time.localtime(local_time)) for local_time in values]


class CandlestickItem(QGraphicsItem):
    """
    when we put the candle, in which position is it going to go
    """
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        (self.t, self.open_price, self.close_price, self.max_price, self.min_price) = data
        self.candlestick_width = 10

    def boundingRect(self):
        return QRectF(0, 0, self.candlestick_width, self.max_price)

    def paint(self, painter, option, widget):
        candle_color = QColor()
        candle = QRect(0, 0, self.candlestick_width, self.close_price - self.open_price)
        if self.open_price > self.close_price:
            candle_color.setNamedColor('red')
        else:
            candle_color.setNamedColor('green')
        painter.drawLine(QPointF(self.candlestick_width / 2.0, self.min_price - self.open_price),
                         QPointF(self.candlestick_width / 2.0, self.max_price - self.open_price))
        painter.fillRect(candle, candle_color)


class ParentItem(QGraphicsItem):
    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-10 - penWidth / 2, -10 - penWidth / 2,
                      20 + penWidth, 10 + penWidth)


class SimpleItem(QGraphicsItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def boundingRect(self):
        penWidth = 1.0
        return QRectF(-10 - penWidth / 2, -10 - penWidth / 2,
                      20 + penWidth, 20 + penWidth)

    def paint(self, painter, option, widget):
        rect = QRect(0, 0, 20, 20)
        painter.fillRect(rect, QColor(255, 0, 0, 127))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        scene = QGraphicsScene()
        background = ParentItem()
        candle_width = 10

        data_set = pd.read_csv("csv/ohlcv.csv")
        # , Time, Open, High, Low, Close, Volume
        data_set = data_set[['Time', 'Open', 'Close', 'High', 'Low']]
        # for i in range(30):
        #     data = data_set.iloc[i]
        #     candle_stick = CandlestickItem(data, parent=background)
        #     candle_stick.setPos(i * 40 - candle_width / 2, data['Open'])

        # tmp = SimpleItem(parent=background)
        # tmp.setPos(5, 5)
        # tmp2 = SimpleItem(parent=background)
        # tmp3 = CandlestickItem([1,20,80,1,100], parent=background)
        # scene.addItem(background)
        # view = QGraphicsView()
        # view.setScene(scene)
        graph = CandlestickGraph(data_set)
        graph.setBackground('w')
        self.setCentralWidget(graph)
        self.show()

app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()


# https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/customGraphicsItem.py
# https://stackoverflow.com/questions/31775468/show-string-values-on-x-axis-in-pyqtgraph
# https://freeprog.tistory.com/373
