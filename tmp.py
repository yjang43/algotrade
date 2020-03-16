from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph import *
import sys
import pandas as pd
from datetime import datetime
class StringAxis(AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel("time")
    def tickStrings(self, values, scale, spacing):
        ret = []
        for v in values:
            if v%2 == 0:
                ret.append('a')
            elif v%2 == 1:
                ret.append('b')
            else:
                ret.append(' ')
        return ret
# https://stackoverflow.com/questions/31775468/show-string-values-on-x-axis-in-pyqtgraph
class CandlestickItemXP(GraphicsObject):
    def __init__(self, data):
        self.data = data
# https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/customGraphicsItem.py
class CandlestickItem(GraphicsWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data  ## data must have fields: time, open, close, min, max
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(mkBrush('r'))
            else:
                p.setBrush(mkBrush('g'))
            p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        graph = PlotWidget()

        cur_time = datetime.utcnow()
        df = pd.read_csv("csv/ohlcv.csv")
        df['Time'] = df['Time'].div(10**12)
        df: pd.DataFrame = df[['Time', 'Open', 'Close', 'Low', 'High']]
        data: np.ndarray = df.to_numpy(float)
        print(data)
        data = data.tolist()
        item = CandlestickItem(data)
        # graph.addItem(item)
        graph.setBackground('w')

        plot_item: ViewBox = graph.getPlotItem()
        plot_item.setClipToView(True)
        plot_item.setXRange(data[0][0], data[20][0])

        xdict = {1:'a', 2:'b', 3:'c'}
        xax = graph.getAxis('bottom')
        xax.setTicks(xdict)
        # string_axis = AxisItem(orientation='bottom')
        # string_axis.setTicks([xdict.items()])
        # my_plot = PlotItem(title="coin graph", axisItems={'bottom':string_axis})
        # candle = my_plot.plot([1,2,3], [1,2,3])
        # graph.addItem(candle)
        tmp_w = PlotWidget(axisItems={'bottom': StringAxis(orientation='bottom')})
        item = PlotDataItem([1,2,3],[1,2,3])
        tmp_w.addItem(item)

        # self.setCentralWidget(graph)
        self.setCentralWidget(tmp_w)
        self.show()
# https://freeprog.tistory.com/373
app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()


