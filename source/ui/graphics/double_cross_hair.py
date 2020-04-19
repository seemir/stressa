# -*- coding: utf-8 -*-
"""
Module containing logic for double cross hairs on plots

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from numpy import percentile, ndarray, array, where, insert

from pyqtgraph import TextItem, InfiniteLine, mkPen, PlotWidget, BarGraphItem
from PyQt5.QtCore import Qt, QObject

from source.domain import Amount
from source.util import Assertor


class DoubleCrossHair(QObject):
    """
    Double cross hair implementation

    """

    def __init__(self, x_1: ndarray, y_1: ndarray, x_2: ndarray, y_2: ndarray,
                 plot_widget_1: PlotWidget, plot_widget_2: PlotWidget, labels: tuple, units=None,
                 precision=0, width=1, x_time=None):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        x_1               : np.ndarray
                            x-values
        y_1               : np.ndarray
                            y-values
        x_2               : np.ndarray
                            x-values
        y_2               : np.ndarray
                            y-values
        plot_widget_1     : PlotWidget
                            graphics view to place chart
        plot_widget_2     : PlotWidget
                            graphics view to place chart
        labels            : tuple
                            labels for legend
        precision         : int
                            precision for rounding, default is zero
        width             : int, float
                            width of any bars
        x_time            : array-like
                            array of dates, i.e. time-period

        """
        super().__init__(parent=None)
        Assertor.assert_data_types(
            [x_1, y_1, x_2, y_2, plot_widget_1, plot_widget_2, labels, precision, width],
            [ndarray, ndarray, ndarray, ndarray, PlotWidget,
             PlotWidget, tuple, int, (int, float)])
        self.x_1, self.y_1 = x_1, y_1
        self.x_2, self.y_2 = x_2, y_2

        self.plot_widget_1 = plot_widget_1
        self.plot_widget_2 = plot_widget_2
        self.precision = precision
        self.width = width
        self.x_time = x_time

        self.bar_item_1 = None
        self.bar_item_2 = None

        pen = mkPen(color="#4c96d7", style=Qt.SolidLine, width=1)
        self.vertical_line_1 = InfiniteLine(angle=90, movable=False, pen=pen)
        self.vertical_line_2 = InfiniteLine(angle=90, movable=False, pen=pen)
        self.label_1, self.label_2 = TextItem(), TextItem()
        self.labels = labels
        self.units = units if units else tuple(["" for _ in range(10)])

        self.plot_widget_1.addItem(self.vertical_line_1, ignoreBounds=True)
        self.plot_widget_2.addItem(self.vertical_line_2, ignoreBounds=True)
        self.view_box_1 = self.plot_widget_1.getViewBox()
        self.view_box_2 = self.plot_widget_2.getViewBox()
        self.configure_cross_hair()

    def configure_cross_hair(self):
        """
        method for configuring cross hair

        """
        place = percentile(insert(array(self.x_1), 0, 0), 10)

        self.label_1.setPos(place, int(abs(max(self.y_1, key=abs)) * 1.4))
        self.label_2.setPos(place, int(abs(max(self.y_2, key=abs)) * 1.4))
        self.plot_widget_1.addItem(self.label_1)
        self.plot_widget_2.addItem(self.label_2)

    def move_vertical_lines(self, pos):
        """
        method for moving the vertical lines on the plot

        """
        mouse_point_1 = self.view_box_1.mapSceneToView(pos)
        mouse_point_2 = self.view_box_2.mapSceneToView(pos)

        x_val_1 = int(round(mouse_point_1.x(), self.precision))
        x_val_2 = int(round(mouse_point_2.x(), self.precision))
        x_idx_1 = where(self.x_1 == x_val_1)
        x_idx_2 = where(self.x_2 == x_val_2)
        y_val_1 = int(self.y_1[x_idx_1]) if self.y_1[x_idx_1] else 0
        y_val_2 = int(self.y_2[x_idx_2]) if self.y_2[x_idx_2] else 0

        self.vertical_line_1.setPos(x_val_1)
        self.vertical_line_2.setPos(x_val_1)

        limits = min(self.x_1) <= x_val_1 <= max(self.x_1)

        if len(self.plot_widget_1.getViewBox().allChildren()) > 3 and limits:
            self.highlight_bar_items(x_val_1, y_val_1, x_val_2, y_val_2)

        return x_val_1, y_val_1, x_val_2, y_val_2, limits

    def highlight_bar_items(self, x_val_1, y_val_1, x_val_2, y_val_2):
        """
        method for highlighting bar items

        """
        self.plot_widget_1.removeItem(self.bar_item_1)
        self.plot_widget_2.removeItem(self.bar_item_2)
        self.bar_item_1 = BarGraphItem(x=[x_val_1], height=y_val_1, width=self.width,
                                       brush="#69a8de")
        self.bar_item_2 = BarGraphItem(x=[x_val_2], height=y_val_2, width=self.width,
                                       brush="#69a8de")
        self.plot_widget_1.addItem(self.bar_item_1)
        self.plot_widget_2.addItem(self.bar_item_2)

    def mouse_moved(self, evt):
        """
        method for moving the vertical lines based on mouse placement

        """
        pos = evt[0]
        if self.plot_widget_1.sceneBoundingRect().contains(
                pos) or self.plot_widget_2.sceneBoundingRect().contains(pos):
            x_val_1, y_val_1, x_val_2, y_val_2, limits = self.move_vertical_lines(pos)

            x_label_idx = where(array(self.x_1) == x_val_1)[0]
            x_label_1 = self.x_time[x_label_idx.item()] if \
                self.x_time and x_label_idx.size != 0 else Amount.format_amount(
                str(x_val_1)) + self.units[0]
            y_label_1 = Amount.format_amount(str(y_val_1)) + self.units[1]

            x_label_2 = self.x_time[x_label_idx.item()] if \
                self.x_time and x_label_idx.size != 0 else Amount.format_amount(
                str(x_val_2)) + self.units[2]
            y_label_2 = Amount.format_amount(str(y_val_2)) + self.units[3]

            if limits:
                self.label_1.setText(
                    "{} \n{} \n({})".format(self.labels[0], x_label_1, y_label_1))
                self.label_2.setText(
                    "{} \n{} \n({})".format(self.labels[1], x_label_2, y_label_2))
