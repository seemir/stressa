# -*- coding: utf-8 -*-
"""
Module containing logic for the DoubleBarChart

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from numpy import arange, cumsum, asarray

from PyQt5.QtCore import Qt
from pyqtgraph import BarGraphItem, PlotWidget, PlotDataItem, mkPen

from source.util import Assertor

from .double_cross_hair import DoubleCrossHair
from .chart import Chart


class DoubleBarChart(Chart):
    """
    Implementation of DoubleBarChart

    """

    def __init__(self, x_1: list, y_1: list, x_2: list, y_2: list, graphics_view_1: PlotWidget,
                 graphics_view_2: PlotWidget, width=0.4):
        Assertor.assert_data_types(
            [x_1, y_1, x_2, y_2, graphics_view_1, graphics_view_2, width],
            [list, list, list, list, PlotWidget, PlotWidget, (int, float)])
        super().__init__()
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
        graphics_view     : PlotWidget
                            graphics view to place chart
        width             : int, float
                            width of any bars 

        """
        self.x_1 = list(arange(1, len(x_1) + 1, 1))
        self.y_1 = y_1
        self.x_2 = self.x_1
        self.y_2 = [sum(element) for element in zip(self.y_1, y_2)]

        self.graphics_view_1 = graphics_view_1
        self.graphics_view_2 = graphics_view_2

        self.bar_item_1 = BarGraphItem(x=self.x_1, height=self.y_2, width=width,
                                       brush="#a8ccec")
        self.graphics_view_1.addItem(self.bar_item_1)
        self.bar_item_2 = BarGraphItem(x=self.x_1, height=self.y_1, width=width,
                                       brush="#d2e5f5")
        self.graphics_view_1.addItem(self.bar_item_2)

        self.bar_item_3 = BarGraphItem(x=self.x_1, height=cumsum(self.y_2), width=width,
                                       brush="#a8ccec")
        self.graphics_view_2.addItem(self.bar_item_3)

        self.bar_item_4 = BarGraphItem(x=self.x_1, height=cumsum(self.y_1), width=width,
                                       brush="#d2e5f5")
        self.graphics_view_2.addItem(self.bar_item_4)

        self.cross_hair = DoubleCrossHair(asarray(self.x_1), asarray(self.y_2), asarray(self.x_2),
                                          asarray(cumsum(self.y_2)), self.graphics_view_1,
                                          self.graphics_view_2, ("Klikk på annonsen (per dag)",
                                                                 "Klikk på annonsen (akkumulert)"),
                                          units=(" ", " klikk", "", " klikk"), width=width,
                                          x_time=x_1)
        self.cross_hair.add_cross_hair_to_chart()

        self.graphics_view_1.plotItem.vb.setLimits(xMin=0, xMax=max(self.x_1) + 1)
        self.graphics_view_2.plotItem.vb.setLimits(xMin=0, xMax=max(self.x_2) + 1)
        self.graphics_view_1.setMenuEnabled(False)
        self.graphics_view_2.setMenuEnabled(False)