# -*- coding: utf-8 -*-
"""
Module containing logic for the graphics know simply as BarChartWithLine

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pyqtgraph as pg
from pyqtgraph import BarGraphItem, PlotDataItem, PlotWidget, TextItem
from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import Qt, QObject

from source.util import Assertor


class BarChartWithLine(QObject):
    """
    Implementation of the Bar chart with line graphics

    """

    def __init__(self, x: list, y: list, graphics_view: PlotWidget, table_view: QTableView,
                 legend: str = ""):
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
        table_view      : QTableView
                          table view to link graphics_view
        legend          : str
                          legend

        """
        Assertor.assert_data_types([x, y, graphics_view, table_view, legend],
                                   [list, list, PlotWidget, QTableView, str])
        super().__init__(parent=None)
        self.x = x
        self.y = y
        self.graphics_view = graphics_view
        self.table_view = table_view
        self.legend = TextItem()
        self.legend.setPos(0, int(max(y) * 1.10))
        self.legend.setText(legend)
        self.graphics_view.addItem(self.legend, ignore_bounds=True)

        self.bar_item = BarGraphItem(x=self.x, height=self.y, width=0.50, brush="#d2e5f5")
        self.graphics_view.addItem(self.bar_item)
        pen = pg.mkPen(color="#d2e5f5", style=Qt.DotLine, width=2)
        self.graphics_view.plot(x=self.x, y=self.y, pen=pen, symbol='+', symbolSize=14)
        self.graphics_view.setMenuEnabled(False)

    def table_view_mapping(self):
        """
        method for mapping table rows to chart bars

        """
        self.table_view.clicked.connect(self.row_clicked)

    def row_clicked(self, item):
        """
        method for accessing row in table_view

        """
        row = len(self.x) - 1 - item.row()
        bar_item = BarGraphItem(x=self.x, height=self.y, width=0.50, brush="#d2e5f5")
        clicked_item = BarGraphItem(x=[self.x[row]], height=self.y[row], width=0.50,
                                    brush="#69a8de")
        pen = pg.mkPen(color="#69a8de", style=Qt.DotLine, width=2)
        chart_item = PlotDataItem(x=self.x, y=self.y, pen=pen,
                                  symbol='+', symbolSize=14)
        self.graphics_view.addItem(bar_item)
        self.graphics_view.addItem(clicked_item)
        self.graphics_view.addItem(chart_item)

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
        graphics_view.clear()
