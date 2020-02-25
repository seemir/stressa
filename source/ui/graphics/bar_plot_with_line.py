# -*- coding: utf-8 -*-
"""
Module containing logic for the graphics know simply as BarPlotWithLine

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pyqtgraph as pg
from pyqtgraph import BarGraphItem, PlotDataItem, PlotWidget
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QTableView

from source.util import Assertor

pg.setConfigOption('background', 'w')


class BarPlotWithLine(QObject):
    """
    Implementation of the Bar plot with line graphics

    """

    def __init__(self, x: list, y: list, graphics_view: PlotWidget, table_view: QTableView):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        x               : list
                          x-values
        y               : list
                          y-values
        graphics_view   : PlotWidget
                          graphics view to place plot
        table_view      : QTableView
                          table view to link graphics_view

        """
        Assertor.assert_data_types([x, y, graphics_view, table_view],
                                   [list, list, PlotWidget, QTableView])
        super().__init__(parent=None)
        self.x = x
        self.y = y
        self.graphics_view = graphics_view
        self.table_view = table_view
        self.legend = pg.LegendItem()

        self.bar_item = BarGraphItem(x=self.x, height=self.y, width=0.50, brush="#d2e5f5")
        self.graphics_view.addItem(self.bar_item)
        pen = pg.mkPen(color="#d2e5f5", style=Qt.DotLine, width=2)
        self.graphics_view.plot(x=self.x, y=self.y, pen=pen, symbol='+', symbolSize=14)

    def table_view_mapping(self):
        """
        method for mapping table rows to plot bars

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
        plot_item = PlotDataItem(x=self.x, y=self.y, pen=pen,
                                 symbol='+', symbolSize=14)
        self.graphics_view.addItem(bar_item)
        self.graphics_view.addItem(clicked_item)
        self.graphics_view.addItem(plot_item)

    def add_legend(self, title: str, subtitle: str, subsubtitle: str):
        """
        method for adding legend to plot

        Parameters
        ----------
        title           : str
                          name of title
        subtitle        : str
                          name of subtitle / second title
        subsubtitle     : str
                          name of subsubtitle / third title

        """
        Assertor.assert_data_types([title, subtitle, subsubtitle], [str, str, str])
        self.legend.setParentItem(self.graphics_view.graphicsItem())
        self.legend.addItem(self.bar_item, title)
        self.legend.addItem(self.bar_item, subtitle)
        self.legend.addItem(self.bar_item, subsubtitle)

    @staticmethod
    def clear_graphics(graphics_view: PlotWidget, table_view: QTableView):
        """
        static method for clearing content in all graphics

        Parameters
        ----------
        graphics_view   : PlotWidget
                          graphics view to place plot
        table_view      : QTableView
                          table view to link graphics_view

        """
        Assertor.assert_data_types([graphics_view, table_view], [PlotWidget, QTableView])
        table_view.setModel(None)
        graphics_view.clear()
        for item in graphics_view.childItems():
            if isinstance(item, pg.LegendItem):
                graphics_view.scene().removeItem(item)
