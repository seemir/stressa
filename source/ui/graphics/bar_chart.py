# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import numpy as np
from itertools import chain

import pyqtgraph as pg
from pyqtgraph import BarGraphItem, PlotWidget
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import QObject

from source.util import Assertor

from ..graphics import cross_hair


class BarChart(QObject):

    def __init__(self, x: list, y: list, graphics_view: PlotWidget, legend: str, labels=("x", "y")):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        x               : list
                          x-values
        y               : list
                          y-values
        graphics_view   : PlotWidget
                          graphics view to place chart

        """
        Assertor.assert_data_types([x, y, graphics_view, legend, labels],
                                   [list, list, PlotWidget, str, (type(None), tuple)])
        super().__init__(parent=None)
        self.y, self.x = self.create_bins(x, y, bins=x)
        self.graphics_view = graphics_view
        self.legend = pg.LegendItem()

        self.bar_item = BarGraphItem(x=self.x[:-1], height=self.y, width=1000,
                                     brush="#d2e5f5")
        self.graphics_view.addItem(self.bar_item)
        cross_hair(self.x, self.y, self.graphics_view, legend, labels)

    @staticmethod
    def clear_graphics(graphics_view: PlotWidget):
        """
        static method for clearing content in all graphics

        Parameters
        ----------
        graphics_view   : PlotWidget
                          graphics view to place chart

        """
        Assertor.assert_data_types([graphics_view], [PlotWidget, QTableView])
        graphics_view.clear()
        for item in graphics_view.childItems():
            if isinstance(item, pg.LegendItem):
                graphics_view.scene().removeItem(item)

    @staticmethod
    def create_bins(x, y, bins):
        bin_array = []
        for i, value in enumerate(x):
            if y[i] != 0:
                bin_array.append([value] * y[i])
            else:
                bin_array.append([0])
        return np.histogram(list(chain(*bin_array)), bins=bins)
