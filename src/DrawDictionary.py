from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QSizePolicy
import numpy as np
# https://www.cnblogs.com/Arago/p/7765510.html

class DrawDictionary(FigureCanvas):
    def __init__(self, dic, parent=None, width=4, height=5, dpi=100):
        self.fig = Figure(figsize= (width,height), dpi= dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.dictionary = dic

        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = self.figure.add_subplot()
        self.drawDic()
    def drawDic(self):
        self.ax.cla()
        x, y = self.dictionary.get7DaysWordNumber()

        self.ax.bar(x, y, color='orange', lw=1, ec='orange')

        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Words')
        self.ax.tick_params(axis='x', labelrotation=30)
        if max(y) > 30:
            self.ax.set_yticks(np.arange(0, max(y), 10))
            self.ax.set_yticks(np.arange(0, max(y), 5), minor=True)
        elif max(y) > 10:
            self.ax.set_yticks(np.arange(0, max(y), 5))
            self.ax.set_yticks(np.arange(0, max(y), 1), minor=True)
        else:
            self.ax.set_yticks(np.arange(0, max(y), 1))
        self.ax.set_title("Numbers of Word\n Learned Last Week")
        self.draw()
        self.flush_events()
