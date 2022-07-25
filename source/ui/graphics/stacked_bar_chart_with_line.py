# -*- coding: utf-8 -*-
"""
Module containing logic for the graphics know simply as BarChartWithLine

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import warnings

from numpy import percentile, insert, array

from pyqtgraph import PlotWidget, TextItem, BarGraphItem
from PyQt5.QtWidgets import QTableView

from source.util import Assertor
from .chart import Chart

warnings.filterwarnings('ignore')


class StackedBarChartWithLine(Chart):
    """
    Implementation of the Bar chart with line graphics

    """

    def __init__(self, x_val: list, y_val_1: list, y_val_2: list, graphics_view: PlotWidget,
                 table_view: QTableView, legend: str = "", reverse=True, y_max=None):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        x_val           : list
                          x-values
        y_val_1         : list
                          y-values
        y_val_2         : list
                          y-values
        graphics_view   : PlotWidget
                          graphics view to place chart
        table_view      : QTableView
                          table view to link graphics_view
        legend          : HTML str
                          legend
        reverse         : bool
                          reverse selection in table
        y_max           : int
                          y_axis max value

        """
        Assertor.assert_data_types([x_val, y_val_1, y_val_2, graphics_view, table_view, legend],
                                   [list, list, list, PlotWidget, QTableView, str])
        super().__init__()
        self.x_val = x_val
        self.y_val_1 = y_val_1
        self.y_val_2 = y_val_2
        self.graphics_view = graphics_view
        self.table_view = table_view
        self.label = TextItem()

        self.width = 0.8

        self.reverse = reverse
        self.legend = legend

        place = percentile(insert(array(self.x_val), 0, 0), 2)
        self.label.setPos(place, int(max(y_val_1) * 1.5))

        self.label.setHtml(self.legend)
        self.graphics_view.addItem(self.label)

        self.bar_item_1 = BarGraphItem(x=self.x_val, height=self.y_val_1, width=self.width,
                                       brush="#d2e5f5")
        self.graphics_view.addItem(self.bar_item_1)

        self.bar_item_2 = BarGraphItem(x=self.x_val, height=self.y_val_2, width=self.width,
                                       brush="#A8B7C4")
        self.graphics_view.addItem(self.bar_item_2)

        if y_max:
            self.graphics_view.setYRange(0, y_max, padding=0)

    def table_view_mapping(self):
        """
        method for mapping table rows to chart bars

        """
        self.table_view.clicked.connect(self.row_clicked)

    def row_clicked(self, item):
        """
        method for accessing row in table_view

        """
        if item.row() < len(self.x_val):
            self.graphics_view.clear()

            self.label.setHtml(self.legend)
            self.graphics_view.addItem(self.label)

            row = len(self.x_val) - 1 - item.row() if self.reverse else item.row()

            bar_item_1 = BarGraphItem(x=self.x_val, height=self.y_val_1, width=self.width,
                                      brush="#d2e5f5")
            bar_item_2 = BarGraphItem(x=self.x_val, height=self.y_val_2, width=self.width,
                                      brush="#A8B7C4")
            clicked_bar_1 = BarGraphItem(x=[self.x_val[row]], height=[self.y_val_1[row]],
                                         width=self.width, brush="#8aa7c0")
            clicked_bar_2 = BarGraphItem(x=[self.x_val[row]], height=[self.y_val_2[row]],
                                         width=self.width, brush="#517797")
            self.graphics_view.addItem(bar_item_1)
            self.graphics_view.addItem(bar_item_2)

            self.graphics_view.addItem(clicked_bar_1)
            self.graphics_view.addItem(clicked_bar_2)

    @staticmethod
    def clear_graphics(graphics_view: PlotWidget, table_view: QTableView):
        """
        static method for clearing content in all graphics

        Parameters
        ----------
        graphics_view   : PlotWidget
                          graphics view to place chart
        table_view      : QTableView
                          table view to link graphics_view

        """
        Assertor.assert_data_types([graphics_view, table_view], [PlotWidget, QTableView])
        table_view.setModel(None)
        table_view.clearSpans()
        graphics_view.clear()
