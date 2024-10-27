# -*- coding: utf-8 -*-
"""
Module containing logic for RatioChart

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from numpy import percentile, array, insert, where

from pyqtgraph import PlotWidget, BarGraphItem, TextItem, InfiniteLine, mkPen
from PyQt5.QtCore import Qt

from source.domain import Amount, Percent
from source.util import Assertor

from .chart import Chart


class RatioChart(Chart):
    """
    Implementation of the RatioChart graphics used for visualizing the ratio between sqm-prices
    in area vs municipality.

    """

    def __init__(self, x_val: list, y_1: list, y_2: list, graphics_view: PlotWidget, labels: str,
                 units=None, x_labels=None, precision=0, width=1000):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        x_val           : list
                          x-values
        y_1             : np.ndarray
                          y-values
        y_2             : np.ndarray
                          y-values
        graphics_view   : PlotWidget
                          widget to add items
        labels          : str
                          legend labels
        units           : tuple
                          measurement units for tuple
        x_labels        : array-like
                          array of x_labels
        precision       : int
                          precision for rounding, default is zero
        width           : int, float
                          width of any bars

        """
        Assertor.assert_data_types(
            [x_val, y_1, y_2, graphics_view, labels, units, x_labels, precision, width],
            [list, list, list, PlotWidget, str, (type(None), tuple), (type(None), list),
             (float, int), (float, int)])
        super().__init__()
        self.y_1, self.x_val = self.create_bins(x_val, y_1, bins=x_val)
        self.y_2, self.x_val = self.create_bins(x_val, y_2, bins=x_val)

        self.x_val = self.x_val[:-1]

        self.labels = labels
        self.units = units if units else ("", "")
        self.precision = precision

        self.ratio = (self.y_1 / self.y_2) * 100
        self.x_labels = x_labels if x_labels else self.ratio

        self.graphics_view = graphics_view
        self.view_box = self.graphics_view.getViewBox()

        self.width = width
        self.label = TextItem()
        self.bar_item_1 = BarGraphItem(x=self.x_val, height=self.ratio, width=self.width,
                                       brush="#a8ccec")
        self.graphics_view.addItem(self.bar_item_1)
        self.configure_cross_hair()

        self.bar_item_2 = None
        pen = mkPen(color="#4c96d7", style=Qt.SolidLine, width=1)
        self.vertical_line = InfiniteLine(angle=90, movable=False, pen=pen)
        self.graphics_view.addItem(self.vertical_line)

        self.graphics_view.plotItem.vb.setLimits(xMin=min(self.x_val) - width,
                                                 xMax=max(self.x_val) + width)
        self.graphics_view.setMenuEnabled(False)

    def configure_cross_hair(self):
        """
        method for configuring cross hair

        """
        place = percentile(array(insert(self.x_val, 0, 0)), 2)

        self.label.setPos(place, int(abs(max(self.ratio, key=abs)) * 1.5))
        self.graphics_view.addItem(self.label)

    def move_vertical_lines(self, pos):
        """
        method for moving the vertical lines on the plot

        """
        mouse_point = self.view_box.mapSceneToView(pos)

        x_val = int(round(mouse_point.x(), self.precision))
        x_idx = where(self.x_val == x_val)

        y_val = self.ratio[x_idx] if self.ratio[x_idx] else 0
        self.vertical_line.setPos(x_val)
        limits = min(self.x_val) <= x_val <= max(self.x_val)

        if len(self.graphics_view.getViewBox().allChildren()) > 3 and limits:
            self.highlight_bar_items(x_val, y_val)

        return x_val, y_val

    def highlight_bar_items(self, x_val, y_val):
        """
        method for highlighting bar items

        """
        self.graphics_view.removeItem(self.bar_item_2)
        self.bar_item_2 = BarGraphItem(x=[x_val], height=y_val, width=self.width,
                                       brush="#69a8de")
        self.graphics_view.addItem(self.bar_item_2)

    def mouse_moved(self, evt):
        """
        method for moving the vertical lines based on mouse placement

        """
        pos = evt[0]
        if self.graphics_view.sceneBoundingRect().contains(pos):
            x_val, y_val = self.move_vertical_lines(pos)

            percent = Percent(str(y_val / 100).replace("[", "").replace("]", ""))

            if min(self.x_val) <= x_val <= max(self.x_val):
                self.label.setHtml(f'<div style="text-align: center">'
                                   f'<span style="font-size: 10pt">{self.labels}</span><br>'
                                   f'<span style="font-size: 10pt">{Amount(str(x_val)).amount} '
                                   f'{self.units[0]}</span><br>'
                                   f'<span style="font-size: 10pt">({percent.value})</span>'
                                   f'</div>')
