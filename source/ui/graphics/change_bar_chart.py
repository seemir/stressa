# -*- coding: utf-8 -*-
"""
Module containing logic for chart type ChangeBarChart

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from numpy import array, percentile, where, insert, asarray, arange

from pyqtgraph import BarGraphItem, mkPen, PlotWidget, TextItem, InfiniteLine
from PyQt5.QtCore import Qt

from source.util import Assertor
from source.domain import Amount

from .chart import Chart


class ChangeBarChart(Chart):
    """
    ChangeCarChart chart type

    """

    def __init__(self, x_val: list, y_val: list, graphics_view: PlotWidget, labels: str,
                 units=None, x_labels=None, width=0.4):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        x_val           : list
                          x-values
        y_val           : list
                          y-values
        graphics_view   : PlotWidget
                          widget to add items
        labels          : str
                          legend labels
        units           : tuple
                          measurement units for tuple
        width           : int, float
                          width of any bars
        x_labels        : array-like
                          array of dates, i.e. time-period

        """
        super().__init__()
        Assertor.assert_data_types([x_val, y_val, graphics_view, labels, units, x_labels, width],
                                   [list, list, PlotWidget, str, (type(None), tuple),
                                    (type(None), list), (float, int)])
        self.x_val = asarray(arange(1, len(x_val) + 1, 1))
        self.y_val = asarray(
            [float(val.replace(" ", "").replace("%", "")) if val else 0 for val in y_val])
        self.graphics_view = graphics_view
        self.labels = labels
        self.units = units if units else ("" for _ in range(10))
        self.x_time = x_labels
        self.width = width

        self.bar_item_1 = BarGraphItem(x=self.x_val, height=self.y_val, width=self.width,
                                       brush="#a8ccec")
        self.graphics_view.addItem(self.bar_item_1)
        self.bar_item_2 = None

        self.label = TextItem()
        pen = mkPen(color="#4c96d7", style=Qt.SolidLine, width=1)
        self.vertical_line = InfiniteLine(angle=90, movable=False, pen=pen)
        self.graphics_view.addItem(self.vertical_line)

        self.view_box = self.graphics_view.getViewBox()
        self.configure_cross_hair()

        self.graphics_view.plotItem.vb.setLimits(xMin=0, xMax=max(self.x_val) + 1)
        self.graphics_view.setMenuEnabled(False)

    def configure_cross_hair(self):
        """
        method for configuring cross hair

        """
        place = percentile(array(insert(self.x_val, 0, 0)), 2)

        self.label.setPos(place, int(abs(max(self.y_val, key=abs)) * 1.5))
        self.graphics_view.addItem(self.label)

    def move_vertical_lines(self, pos):
        """
        method for moving the vertical lines on the plot

        """
        mouse_point = self.view_box.mapSceneToView(pos)

        x_val = int(round(mouse_point.x_val()))
        x_idx = where(self.x_val == x_val)

        y_val = int(self.y_val[x_idx]) if self.y_val[x_idx] else 0
        self.vertical_line.setPos(x_val)
        limits = min(self.x_val) <= x_val <= max(self.x_val)
        if len(self.graphics_view.getViewBox().allChildren()) > 3 and limits:
            self.highlight_bar_items(x_val, y_val)

        return x_val, y_val

    def highlight_bar_items(self, x_val, y_val):
        """
        method for highlighting bar items

        """
        self.graphics_view.removeItem(self.bar_item_2)
        self.bar_item_2 = BarGraphItem(x=[x_val], height=y_val, width=self.width,
                                       brush="#69a8de")
        self.graphics_view.addItem(self.bar_item_2)

    def mouse_moved(self, evt):
        """
        method for moving the vertical lines based on mouse placement

        """
        pos = evt[0]
        x_val, y_val = self.move_vertical_lines(pos)

        x_label_idx = where(array(self.x_val) == x_val)[0]
        x_label = self.x_time[x_label_idx.item()] if \
            self.x_time and x_label_idx.size != 0 else \
            Amount(str(x_val)).amount + self.units[0]
        y_label = str(y_val) + self.units[1]

        if min(self.x_val) <= x_val <= max(self.x_val):
            self.label.setHtml('<div style="text-align: center">'
                               '<span style="font-size: 10pt">{}</span><br>'
                               '<span style="font-size: 10pt">{}</span><br>'
                               '<span style="font-size: 10pt">({})</span>'
                               '</div>'.format(self.labels, x_label, y_label))
