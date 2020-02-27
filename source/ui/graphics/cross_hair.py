# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import numpy as np

from pyqtgraph import TextItem, InfiniteLine, SignalProxy, mkPen
from PyQt5.QtCore import Qt

from source.domain import Amount


def cross_hair(x, y, plot_widget, legend, labels=("x", "y")):
    pen = mkPen(color="#4c96d7", style=Qt.SolidLine, width=1)
    vertical_line = InfiniteLine(angle=90, movable=False, pen=pen)
    plot_widget.addItem(vertical_line, ignoreBounds=True)
    view_box = plot_widget.getViewBox()
    label = TextItem()
    label.setPos(0, int(max(y) * 1.10))
    plot_widget.addItem(label, ignore_bounds=True)

    def mouse_moved(evt):
        pos = evt[0]
        if plot_widget.sceneBoundingRect().contains(pos):
            mouse_point = view_box.mapSceneToView(pos)
            x_val = int(round(mouse_point.x(), -3))
            x_idx = np.where(x == x_val)
            y_val = int(y[x_idx]) if y[x_idx] else 0
            label.setText(
                "{} \n{}: {} \n({} {})".format(legend, labels[0],
                                               Amount.format_amount(str(x_val)) + " kr/m²",
                                               Amount.format_amount(str(y_val)), labels[1]))
            vertical_line.setPos(mouse_point.x())

    plot_widget.getViewBox().setAutoVisible(y=True)
    proxy_mouse_moved = SignalProxy(plot_widget.scene().sigMouseMoved, rateLimit=60,
                                    slot=mouse_moved)
    plot_widget.proxy = proxy_mouse_moved
