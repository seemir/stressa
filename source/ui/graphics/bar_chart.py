# -*- coding: utf-8 -*-
"""
Module with logic for the BarChart implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import numpy as np

from pyqtgraph import BarGraphItem, PlotWidget, mkPen, InfiniteLine, SignalProxy, LinearRegionItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt

from source.util import Assertor

from .double_cross_hair import DoubleCrossHair
from .chart import Chart


class BarChart(Chart):
    """
    Implementation of BarChart graphics

    """

    def __init__(self, x_1: list, y_1: list, x_2: list, y_2: list, graphics_view_1: PlotWidget,
                 graphics_view_2: PlotWidget, labels: tuple, units=None, precision=0, width=1,
                 average=None):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        x_1               : list
                            x-values
        y_1               : list
                            y-values
        x_2               : list
                            x-values
        y_2               : list
                            y-values
        graphics_view_1   : PlotWidget
                            graphics view to place chart
        graphics_view_2   : PlotWidget
                            graphics view to place chart
        labels            : tuple
                            labels for legend
        units             : tuple, optional
                            measurement units got labels
        precision         : int
                            precision for rounding, default is zero
        width             : int
                            width of any bars, default is 1
        average           : str
                            average sqm-price

        """
        Assertor.assert_data_types(
            [x_1, y_1, x_2, y_2, graphics_view_1, graphics_view_2, labels, precision, average],
            [list, list, list, list, PlotWidget, PlotWidget, tuple, int, (type(None), str)])
        super().__init__()
        self.y_1, self.x_1 = self.create_bins(x_1, y_1, bins=x_1)
        self.y_2, self.x_2 = self.create_bins(x_2, y_2, bins=x_2)

        self.graphics_view_1 = graphics_view_1
        self.graphics_view_2 = graphics_view_2
        self.connection_chart = None
        self.graphics_view_3 = None
        self.average = float(average)

        self.bar_item_1 = BarGraphItem(x=self.x_1[:-1], height=self.y_1, width=1000,
                                       brush="#d2e5f5")
        self.bar_item_2 = BarGraphItem(x=self.x_2[:-1], height=self.y_2, width=1000,
                                       brush="#d2e5f5")

        self.graphics_view_1.addItem(self.bar_item_1)
        self.graphics_view_2.addItem(self.bar_item_2)
        self.units = units if units else ("", "", "", "")
        if self.average:
            self.draw_average_line()

        self.cross_hair = DoubleCrossHair(self.x_1[:-1], self.y_1, self.x_2[:-1], self.y_2,
                                          self.graphics_view_1, self.graphics_view_2, labels,
                                          self.units, precision, width)
        self.add_cross_hair_to_chart()

        self.graphics_view_1.plotItem.vb.setLimits(xMin=min(self.x_1), xMax=max(self.x_1))
        self.graphics_view_2.plotItem.vb.setLimits(xMin=min(self.x_2), xMax=max(self.x_2))
        self.graphics_view_1.setMenuEnabled(False)
        self.graphics_view_2.setMenuEnabled(False)

    def connect(self, chart: Chart, plot_widget: PlotWidget):
        """
        method for connecting to other plot

        Parameters
        ----------
        chart           : Chart
                          chart object
        plot_widget     : PlotWidget
                          plot widget to connect

        """
        self.connection_chart = chart
        self.graphics_view_3 = plot_widget
        self.add_cross_hair_to_chart()

    def draw_average_line(self):
        """
        method for drawing average lines on plot widget

        """
        pen_1 = mkPen(color="#4c96d7", style=Qt.DotLine, width=2)
        average_line_1 = InfiniteLine(angle=90, movable=False, pen=pen_1)
        average_line_2 = InfiniteLine(angle=90, movable=False, pen=pen_1)

        average_1 = np.average(self.x_1[:-1], weights=self.y_1)
        average_2 = np.average(self.x_1[:-1], weights=self.y_2)

        pen_2 = mkPen(color="#4c96d7", style=Qt.SolidLine, width=2)
        average_line_3 = InfiniteLine(angle=90, movable=False, pen=pen_2)
        average_line_4 = InfiniteLine(angle=90, movable=False, pen=pen_2)

        brush = QBrush(QColor(0, 0, 255, 20))
        linear_region_1 = LinearRegionItem([average_1, self.average], movable=False,
                                           brush=brush)
        linear_region_2 = LinearRegionItem([average_2, self.average], movable=False,
                                           brush=brush)
        self.graphics_view_1.addItem(linear_region_1)
        self.graphics_view_2.addItem(linear_region_2)

        average_line_1.setPos(average_1)
        average_line_2.setPos(average_2)
        self.graphics_view_1.addItem(average_line_1)
        self.graphics_view_2.addItem(average_line_2)

        average_line_3.setPos(self.average)
        average_line_4.setPos(self.average)
        self.graphics_view_1.addItem(average_line_3)
        self.graphics_view_2.addItem(average_line_4)

    def add_cross_hair_to_chart(self):
        """
        method for adding cross hair to the charts

        """
        proxy_mouse_moved_1 = SignalProxy(self.graphics_view_1.scene().sigMouseMoved, rateLimit=60,
                                          slot=self.mouse_moved)
        proxy_mouse_moved_2 = SignalProxy(self.graphics_view_2.scene().sigMouseMoved, rateLimit=60,
                                          slot=self.mouse_moved)
        self.graphics_view_1.proxy = proxy_mouse_moved_1
        self.graphics_view_2.proxy = proxy_mouse_moved_2

        if self.graphics_view_3:
            proxy_mouse_moved_3 = SignalProxy(self.graphics_view_3.scene().sigMouseMoved,
                                              rateLimit=60, slot=self.mouse_moved)
            self.graphics_view_3.proxy = proxy_mouse_moved_3

    def mouse_moved(self, evt):
        """
        method for tracing mouse movement

        """
        self.cross_hair.mouse_moved(evt)
        pos = evt[0]
        if self.graphics_view_3 and self.graphics_view_3.sceneBoundingRect().contains(pos):
            self.connection_chart.mouse_moved(evt)
