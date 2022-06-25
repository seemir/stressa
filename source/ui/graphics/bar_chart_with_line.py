# -*- coding: utf-8 -*-
"""
Module containing logic for the graphics know simply as BarChartWithLine

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import warnings

from numpy import percentile, insert, array

from pyqtgraph import BarGraphItem, PlotDataItem, PlotWidget, TextItem, mkPen
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

        place = percentile(insert(array(self.x_val), 0, 0), 2)
        self.label.setPos(place, int(max(y_val) * 1.5))

        self.label.setHtml(legend)
        self.graphics_view.addItem(self.label, ignore_bounds=True)

        self.bar_item = BarGraphItem(x=self.x_val, height=self.y_val, width=self.width,
                                     brush="#d2e5f5")
        self.graphics_view.addItem(self.bar_item)
        pen = mkPen(color="#d2e5f5", style=Qt.DotLine, width=2)
        self.graphics_view.plot(x=self.x_val, y=self.y_val, pen=pen, symbol='+', symbolSize=14)

        self.graphics_view.plotItem.vb.setLimits(xMin=min(self.x_val) - width,
                                                 xMax=max(self.x_val) + width)
        self.graphics_view.setMenuEnabled(False)
        self.graphics_view.getViewBox().enableAutoRange()

    def table_view_mapping(self):
        """
        method for mapping table rows to chart bars

        """
        self.table_view.clicked.connect(self.row_clicked)

    def row_clicked(self, item):
        """
        method for accessing row in table_view

        """
        pen_1 = mkPen(color="#69a8de", style=Qt.DotLine, width=2)
        pen_2 = mkPen(color="#d2e5f5", style=Qt.DotLine, width=2)
        bar_item = BarGraphItem(x=self.x_val, height=self.y_val, width=self.width, brush="#d2e5f5")
        chart_item = PlotDataItem(x=self.x_val, y=self.y_val, pen=pen_1, symbol='+', symbolSize=14)
        clear_line = PlotDataItem(x=self.x_val, y=self.y_val, pen=pen_2, symbol='+', symbolSize=14)

        if item.row() < len(self.x_val):
            row = len(self.x_val) - 1 - item.row() if self.reverse else item.row()

            clicked_item = BarGraphItem(x=[self.x_val[row]], height=self.y_val[row],
                                        width=self.width,
                                        brush="#69a8de")
            self.graphics_view.addItem(bar_item)
            self.graphics_view.addItem(clicked_item)
            self.graphics_view.addItem(chart_item)
        else:
            self.graphics_view.addItem(bar_item)
            self.graphics_view.addItem(clear_line)

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
