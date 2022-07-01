# -*- coding: utf-8 -*-
"""
Module containing logic for the graphics know simply as BarChartWithLine

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import warnings

from numpy import percentile, insert, array

from pyqtgraph import PlotDataItem, PlotWidget, TextItem, mkPen
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import Qt

from source.util import Assertor
from .chart import Chart

warnings.filterwarnings('ignore')


class BarChartWithLine(Chart):
    """
    Implementation of the Bar chart with line graphics

    """

    def __init__(self, x_val: list, y_val: list, graphics_view: PlotWidget, table_view: QTableView,
                 legend: str = "", width=0.5, reverse=True):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        x_val           : list
                          x-values
        y_val           : list
                          y-values
        graphics_view   : PlotWidget
                          graphics view to place chart
        table_view      : QTableView
                          table view to link graphics_view
        legend          : HTML str
                          legend
        width           : int, float
                          width of bars
        reverse         : bool
                          reverse selection in table

        """
        Assertor.assert_data_types([x_val, y_val, graphics_view, table_view, legend, width],
                                   [list, list, PlotWidget, QTableView, str, (int, float)])
        super().__init__()
        self.x_val = x_val
        self.y_val = y_val
        self.graphics_view = graphics_view
        self.table_view = table_view
        self.label = TextItem()
        self.width = width
        self.reverse = reverse
        self.legend = legend

        place = percentile(insert(array(self.x_val), 0, 0), 2)
        self.label.setPos(place, int(max(y_val) * 1.5))

        self.label.setHtml(self.legend)
        self.graphics_view.addItem(self.label)

        pen = mkPen(color="#d2e5f5", style=Qt.DotLine, width=2)
        self.graphics_view.plot(x=self.x_val, y=self.y_val, pen=pen)

        self.graphics_view.plotItem.vb.setLimits(xMin=min(self.x_val) - width,
                                                 xMax=max(self.x_val) + width)

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

            pen_1 = mkPen(color="#69a8de", style=Qt.DotLine, width=2)
            chart_item = PlotDataItem(x=self.x_val, y=self.y_val, pen=pen_1)

            pen = mkPen(color="#d2e5f5", style=Qt.DotLine, width=2)
            self.graphics_view.plot(x=self.x_val, y=self.y_val, pen=pen)

            row = len(self.x_val) - 1 - item.row() if self.reverse else item.row()
            clicked_item = PlotDataItem(x=[self.x_val[row]], y=[self.y_val[row]],
                                        pen=pen_1, symbol='+', symbolSize=14)
            self.graphics_view.addItem(chart_item)
            self.graphics_view.addItem(clicked_item)

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
