# -*- coding: utf-8 -*-
"""
Module containing logic for the DoubleBarChart

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from numpy import arange, cumsum, asarray

from pyqtgraph import BarGraphItem, PlotWidget, SignalProxy

from source.util import Assertor

from .double_cross_hair import DoubleCrossHair
from .chart import Chart


class DoubleBarChart(Chart):
    """
    Implementation of DoubleBarChart

    """

    def __init__(self, x_1: list, y_1: list, x_2: list, y_2: list, x_3: list, y_3: list,
                 graphics_view_1: PlotWidget, graphics_view_2: PlotWidget, labels: tuple,
                 units: tuple, width=0.4):
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
        x_3               : list
                            x-values
        y_3               : list
                            y-values
        graphics_view_1   : PlotWidget
                            graphics view to place chart
        graphics_view_2   : PlotWidget
                            graphics view to place chart
        labels            : tuple
                            labels to be used in chart
        units             : tuple
                            measurement units
        width             : int, float
                            width of any bars

        """
        Assertor.assert_data_types(
            [x_1, y_1, x_2, y_2, graphics_view_1, graphics_view_2, width],
            [list, list, list, list, PlotWidget, PlotWidget, (int, float)])
        super().__init__()
        self.x_1 = list(arange(1, len(x_1) + 1, 1))
        self.y_1 = y_1
        self.x_2 = self.x_1
        self.y_2 = y_2
        self.x_3 = x_3
        self.y_3 = y_3

        self.graphics_view_1 = graphics_view_1
        self.graphics_view_2 = graphics_view_2

        self.bar_item_1 = BarGraphItem(x=self.x_1, height=self.y_1, width=width,
                                       brush="#a8ccec")
        self.graphics_view_1.addItem(self.bar_item_1)
        self.bar_item_2 = BarGraphItem(x=self.x_1, height=self.y_2, width=width,
                                       brush="#d2e5f5")
        self.graphics_view_1.addItem(self.bar_item_2)

        self.bar_item_3 = BarGraphItem(x=self.x_1, height=self.y_3, width=width,
                                       brush="#a8ccec")
        self.graphics_view_2.addItem(self.bar_item_3)

        self.bar_item_4 = BarGraphItem(x=self.x_1, height=cumsum(self.y_2), width=width,
                                       brush="#d2e5f5")
        self.graphics_view_2.addItem(self.bar_item_4)

        self.cross_hair = DoubleCrossHair(asarray(self.x_1), asarray(self.y_1), asarray(self.x_2),
                                          asarray(self.y_3), self.graphics_view_1,
                                          self.graphics_view_2, labels, units=units, width=width,
                                          x_labels=x_1)

        self.graphics_view_1.plotItem.vb.setLimits(xMin=0, xMax=max(self.x_1) + 1)
        self.graphics_view_2.plotItem.vb.setLimits(xMin=0, xMax=max(self.x_2) + 1)
        self.graphics_view_1.setMenuEnabled(False)
        self.graphics_view_2.setMenuEnabled(False)

        self.connection_chart = None
        self.graphics_view_3 = None

    def connect(self, chart, plot_widget):
        """
        method for connecting from external chart

        """
        self.connection_chart = chart
        self.graphics_view_3 = plot_widget
        self.add_cross_hair_to_chart()

    def add_cross_hair_to_chart(self):
        """
        method for adding crosshair to the charts

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
        method for tracking movement of mouse

        """
        self.cross_hair.mouse_moved(evt)
        pos = evt[0]
        if self.graphics_view_3 and self.graphics_view_3.sceneBoundingRect().contains(pos):
            self.connection_chart.mouse_moved(evt)
