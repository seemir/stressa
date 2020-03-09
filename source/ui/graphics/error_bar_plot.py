# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from numpy import arange, array, percentile, where, insert

from pyqtgraph import ErrorBarItem, mkPen, PlotWidget, TextItem, InfiniteLine
from PyQt5.QtCore import Qt

from source.util import Assertor
from source.domain import Amount

from .chart import Chart


class ErrorBarPlot(Chart):

    def __init__(self, y: list, top: list, bottom: list, graphics_view: PlotWidget, labels: str,
                 units=None, x=None, x_time=None):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        y               : list
                          y-values
        top             : list
                          top values
        bottom          : list
                          bottom values
        graphics_view   : PlotWidget
                          widget to add items
        labels          : str
                          legend labels
        units           : tuple
                          measurement units for tuple
        x               : list
                          x-values, optional, default is list of range of y-values
        x_time          : array-like
                          array of dates, i.e. time-period

        """
        super().__init__()
        Assertor.assert_data_types([y, top, bottom, graphics_view, labels, units, x, x_time],
                                   [list, list, list, PlotWidget, str, (type(None), tuple),
                                    (type(None), list), (type(None), list)])

        self.y = array(y)
        self.x = arange(1, len(y) + 1, 1) if not x else array(x)
        self.top = array(top)
        self.bottom = array(bottom)
        self.graphics_view = graphics_view
        self.labels = labels
        self.units = units if units else tuple(["" for _ in range(10)])
        self.x_time = x_time

        pen_1 = mkPen(color="#ffffff", style=Qt.SolidLine, width=1)
        self.error_bar_1 = ErrorBarItem(x=self.x, y=self.y, top=self.top, bottom=self.bottom,
                                        beam=2, pen=pen_1)
        self.graphics_view.addItem(self.error_bar_1)

        pen_2 = mkPen(color="#4c96d7", style=Qt.SolidLine, width=1)
        self.error_bar_2 = ErrorBarItem(x=self.x, y=self.y, top=self.top, bottom=self.bottom,
                                        beam=0.4, pen=pen_2)

        self.graphics_view.addItem(self.error_bar_2)
        pen_3 = mkPen(color="#4c96d7", style=Qt.DotLine, width=2)
        self.graphics_view.plot(x=self.x, y=self.y, pen=pen_3, symbol="o", symbolSize=6,
                                symbolBrush=(105, 168, 222))

        self.label = TextItem()
        pen = mkPen(color="#4c96d7", style=Qt.SolidLine, width=1)
        self.vertical_line = InfiniteLine(angle=90, movable=False, pen=pen)
        self.graphics_view.addItem(self.vertical_line)

        self.view_box = self.graphics_view.getViewBox()
        self.configure_cross_hair()

        self.graphics_view.plotItem.vb.setLimits(xMin=0, xMax=max(self.x) + 1)
        self.graphics_view.setMenuEnabled(False)

    def configure_cross_hair(self):
        """
        method for configuring cross hair

        """
        place = percentile(array(insert(self.x, 0, 0)), 10)

        self.label.setPos(place, int((max(self.y) + max(self.top)) * 1.6))
        self.graphics_view.addItem(self.label)

    def move_vertical_lines(self, pos):
        """
        method for moving the vertical lines on the plot

        """
        mouse_point = self.view_box.mapSceneToView(pos)

        x_val = int(round(mouse_point.x()))
        x_idx = where(self.x == x_val)
        y_val = int(self.y[x_idx]) if self.y[x_idx] else 0
        top_val = y_val + int(self.top[x_idx]) if self.top[x_idx] else 0
        bottom_val = y_val - int(self.bottom[x_idx]) if self.bottom[x_idx] and self.bottom[
            x_idx] > 0 else 0

        self.vertical_line.setPos(x_val)

        return x_val, y_val, top_val, bottom_val

    def mouse_moved(self, evt):
        """
        method for moving the vertical lines based on mouse placement

        """
        pos = evt[0]
        x_val, y_val, top_val, bottom_val = self.move_vertical_lines(pos)
        x_label_idx = where(array(self.x) == x_val)[0]
        x_label = self.x_time[x_label_idx.item()] if \
            self.x_time and x_label_idx.size != 0 else Amount.format_amount(
            str(x_val)) + self.units[0]
        y_label = Amount.format_amount(str(y_val)) + self.units[1]
        top_label = Amount.format_amount(str(top_val)) + self.units[1]
        bottom_label = Amount.format_amount(str(bottom_val)) + self.units[1]

        if min(self.x) <= x_val <= max(self.x):
            self.label.setText(
                "{} \n{} \n({}) \nØvre: {}, \nNedre: {}".format(self.labels, x_label, y_label,
                                                                top_label, bottom_label))
