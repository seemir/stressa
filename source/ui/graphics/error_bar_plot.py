# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from numpy import arange, array

from pyqtgraph import ErrorBarItem, mkPen, PlotWidget
from PyQt5.QtCore import Qt

from source.util import Assertor

from .chart import Chart


class ErrorBarPlot(Chart):

    def __init__(self, y: list, top: list, bottom: list, graphics_view: PlotWidget, x=None):
        super().__init__()
        Assertor.assert_data_types([y, top, bottom, graphics_view, x],
                                   [list, list, list, PlotWidget, (type(None), list)])

        self.y = array(y)
        self.x = arange(1, len(y) + 1, 1) if not x else array(x)
        self.top = top
        self.bottom = bottom
        self.graphics_view = graphics_view

        pen_1 = mkPen(color="#ffffff", style=Qt.SolidLine, width=1)
        self.error_bar_1 = ErrorBarItem(x=self.x, y=self.y, top=self.top, bottom=self.bottom,
                                        beam=1.5, pen=pen_1)
        self.graphics_view.addItem(self.error_bar_1)

        pen_2 = mkPen(color="#a8ccec", style=Qt.SolidLine, width=1)
        self.error_bar_2 = ErrorBarItem(x=self.x, y=self.y, top=self.top, bottom=self.bottom,
                                        beam=0.4, pen=pen_2)
        self.graphics_view.addItem(self.error_bar_2)

        pen_3 = mkPen(color="#d2e5f5", style=Qt.DotLine, width=2)
        self.graphics_view.plot(x=self.x, y=self.y, pen=pen_3, symbol="o", symbolSize=4,
                                symbolBrush=(105, 168, 222))

        self.graphics_view.plotItem.vb.setLimits(xMin=0, xMax=max(self.x) + 1)
        self.graphics_view.setMenuEnabled(False)
