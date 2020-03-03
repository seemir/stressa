# -*- coding: utf-8 -*-
"""
Module containing logic for the DoubleBarChart

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from numpy import arange

from pyqtgraph import BarGraphItem, PlotWidget

from source.util import Assertor

from .cross_hair import CrossHair
from .chart import Chart


class DoubleBarChart(Chart):
    """
    Implementation of DoubleBarChart

    """

    def __init__(self, x_1: list, y_1: list, x_2: list, y_2: list, graphics_view: PlotWidget):
        Assertor.assert_data_types(
            [x_1, y_1, x_2, y_2, graphics_view], [list, list, list, list, PlotWidget])
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

        """
        self.x_1 = list(arange(1, len(x_1) + 1, 1))
        self.y_1 = y_1
        self.x_2 = self.x_1
        self.y_2 = [sum(element) for element in zip(self.y_1, y_2)]

        self.graphics_view = graphics_view
        self.bar_item_1 = BarGraphItem(x=self.x_2, height=self.y_2, width=0.5,
                                       brush="#a8ccec")
        self.graphics_view.addItem(self.bar_item_1)
        self.bar_item_2 = BarGraphItem(x=self.x_1, height=self.y_1, width=0.5,
                                       brush="#d2e5f5")
        self.graphics_view.addItem(self.bar_item_2)
        self.graphics_view.setMenuEnabled(False)
        self.cross_hair = CrossHair(self.x_2, self.y_2, self.graphics_view,
                                    labels="Klikk på annonsen",
                                    x_time=x_1)

        self.cross_hair.add_cross_hair_to_chart()
        self.graphics_view.plotItem.vb.setLimits(xMin=0, xMax=max(self.x_1) + 1)
        self.graphics_view.setMenuEnabled(False)
