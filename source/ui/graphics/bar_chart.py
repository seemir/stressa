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

    def __init__(self, x_1: list, y_1: list, x_2: list, y_2: list, graphics_view_1: PlotWidget,
                 graphics_view_2: PlotWidget, labels: tuple):
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

        """
        Assertor.assert_data_types(
            [x_1, y_1, x_2, y_2, graphics_view_1, graphics_view_2, labels],
            [list, list, list, list, PlotWidget, PlotWidget, tuple])
        super().__init__(parent=None)
        self.y_1, self.x_1 = self.create_bins(x_1, y_1, bins=x_1)
        self.y_2, self.x_2 = self.create_bins(x_2, y_2, bins=x_2)
        self.graphics_view_1 = graphics_view_1
        self.graphics_view_2 = graphics_view_2
        self.bar_item_1 = BarGraphItem(x=self.x_1[:-1], height=self.y_1, width=1000,
                                       brush="#d2e5f5")
        self.bar_item_2 = BarGraphItem(x=self.x_2[:-1], height=self.y_2, width=1000,
                                       brush="#d2e5f5")
        self.graphics_view_1.addItem(self.bar_item_1)
        self.graphics_view_2.addItem(self.bar_item_2)
        cross_hair(self.x_1[:-1], self.x_2[:-1], self.y_1, self.y_2, self.graphics_view_1,
                   self.graphics_view_2, labels)

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
