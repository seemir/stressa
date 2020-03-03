# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import numpy as np

from pyqtgraph import TextItem, InfiniteLine, SignalProxy, mkPen, PlotWidget, BarGraphItem
from PyQt5.QtCore import Qt, QObject

from source.util import Assertor
from source.domain import Amount


class CrossHair(QObject):

    def __init__(self, x: list, y: list, plot_widget: PlotWidget, labels: str, x_time: list = None):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        x                 : list
                            x-values
        y                 : list
                            y-values
        plot_widget       : PlotWidget
                            graphics view to place cross hair
        labels            : str
                            label for legend
        x_time            : list
                            date values, if supplied

        """
        super().__init__(parent=None)
        Assertor.assert_data_types([x, y, plot_widget, labels, x_time],
                                   [list, list, PlotWidget, str, (type(None), list)])
        self.x, self.y = x, y
        self.plot_widget = plot_widget
        self.labels = labels
        self.bar_item = None
        self.label = TextItem()
        self.x_time = x_time

        pen = mkPen(color="#4c96d7", style=Qt.SolidLine, width=1)
        self.vertical_line = InfiniteLine(angle=90, movable=False, pen=pen)

        self.plot_widget.addItem(self.vertical_line, ignoreBounds=True)
        self.view_box = self.plot_widget.getViewBox()
        self.configure_cross_hair()

    def configure_cross_hair(self):
        """
        method for configuring cross hair

        """
        place = np.percentile(np.array(self.x), 75)

        self.label.setPos(place, int(max(self.y) * 1.25))
        self.plot_widget.addItem(self.label)

    def move_vertical_lines(self, pos):
        """
        method for moving the vertical lines on the plot

        """
        mouse_point = self.view_box.mapSceneToView(pos)

        x_val = int(round(mouse_point.x()))
        x_idx = np.where(np.array(self.x) == x_val)[0]

        if x_idx.size != 0:
            y_val = self.y[x_idx.item()]
        else:
            y_val = 0

        self.vertical_line.setPos(x_val)
        return x_val, y_val

    def highlight_bar_items(self, x_val, y_val):
        """
        method for highlighting bar items

        """
        self.plot_widget.removeItem(self.bar_item)
        self.bar_item = BarGraphItem(x=[x_val], height=y_val, width=0.5, brush="#69a8de")
        self.plot_widget.addItem(self.bar_item)

    def mouse_moved(self, evt):
        """
        method for moving the vertical lines based on mouse placement

        """
        pos = evt[0]
        if self.plot_widget.sceneBoundingRect().contains(pos):
            x_val, y_val = self.move_vertical_lines(pos)

            x_label_idx = np.where(np.array(self.x) == x_val)[0]
            x_label = self.x_time[x_label_idx.item()] \
                if self.x_time and x_label_idx.size != 0 else ""
            y_label = "({} klikk)".format(Amount.format_amount(str(y_val))) if x_label else ""
            legend_label = "{} \n{} \n{}".format(self.labels, x_label, y_label)
            self.label.setText(legend_label)
            if len(self.plot_widget.getViewBox().allChildren()) > 3:
                self.highlight_bar_items(x_val, y_val)

    def add_cross_hair_to_chart(self):
        """
        method for adding cross hair to the charts

        """
        proxy_mouse_moved = SignalProxy(self.plot_widget.scene().sigMouseMoved, rateLimit=60,
                                        slot=self.mouse_moved)
        self.plot_widget.proxy = proxy_mouse_moved
