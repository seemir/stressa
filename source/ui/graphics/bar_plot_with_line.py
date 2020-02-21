# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pyqtgraph as pg
from pyqtgraph import BarGraphItem, PlotDataItem
from PyQt5.QtCore import Qt, QObject


class BarPlotWithLine(QObject):

    def __init__(self, x, y, graphics_view, table_view):
        super().__init__(parent=None)
        self.x = x
        self.y = y
        self.graphics_view = graphics_view
        self.table_view = table_view

        self.bar_item = BarGraphItem(x=self.x, height=self.y, width=0.50, brush="#d2e5f5")
        self.graphics_view.addItem(self.bar_item)
        pen = pg.mkPen(color="#d2e5f5", style=Qt.DotLine, width=2)
        self.graphics_view.plot(x=self.x, y=self.y, pen=pen, symbol='+', symbolSize=14)

    def table_view_mapping(self):
        self.table_view.clicked.connect(self.row_clicked)

    def row_clicked(self, item):
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

    def add_legend(self, legend, title, subtitle, subsubtitle):
        legend.setParentItem(self.graphics_view.graphicsItem())
        legend.addItem(self.bar_item, title)
        legend.addItem(self.bar_item, subtitle)
        legend.addItem(self.bar_item, subsubtitle)

    @staticmethod
    def clear_graphics(graphics_view, table_view):
        table_view.setModel(None)
        graphics_view.clear()
        for item in graphics_view.childItems():
            if isinstance(item, pg.LegendItem):
                graphics_view.scene().removeItem(item)
