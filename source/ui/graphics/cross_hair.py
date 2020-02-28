# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import numpy as np

from pyqtgraph import TextItem, InfiniteLine, SignalProxy, mkPen
from PyQt5.QtCore import Qt

from source.domain import Amount


def cross_hair(x_1, x_2, y_1, y_2, plot_widget_1, plot_widget_2, labels):
    pen_1 = mkPen(color="#4c96d7", style=Qt.SolidLine, width=1)
    vertical_line_1 = InfiniteLine(angle=90, movable=False, pen=pen_1)
    vertical_line_2 = InfiniteLine(angle=90, movable=False, pen=pen_1)
    plot_widget_1.addItem(vertical_line_1, ignoreBounds=True)
    plot_widget_2.addItem(vertical_line_2, ignoreBounds=True)
    view_box_1 = plot_widget_1.getViewBox()
    view_box_2 = plot_widget_2.getViewBox()
    label_1 = TextItem()
    label_2 = TextItem()
    label_1.setPos(0, int(max(y_1) * 1.10))
    label_2.setPos(0, int(max(y_2) * 1.10))
    plot_widget_1.addItem(label_1)
    plot_widget_2.addItem(label_2)

    pen_2 = mkPen(color="b", style=Qt.DotLine, width=2)
    average_line_1 = InfiniteLine(angle=90, movable=False, pen=pen_2)
    average_line_2 = InfiniteLine(angle=90, movable=False, pen=pen_2)
    average_line_1.setPos(np.average(x_1, weights=y_1))
    average_line_2.setPos(np.average(x_2, weights=y_2))
    plot_widget_1.addItem(average_line_1)
    plot_widget_2.addItem(average_line_2)

    def mouse_moved(evt):
        pos = evt[0]
        if plot_widget_1.sceneBoundingRect().contains(
                pos) or plot_widget_2.sceneBoundingRect().contains(pos):
            mouse_point_1 = view_box_1.mapSceneToView(pos)
            mouse_point_2 = view_box_2.mapSceneToView(pos)
            x_val_1 = int(round(mouse_point_1.x(), -3))
            x_val_2 = int(round(mouse_point_2.x(), -3))
            x_idx_1 = np.where(x_1 == x_val_1)
            x_idx_2 = np.where(x_2 == x_val_2)
            y_val_1 = int(y_1[x_idx_1]) if y_1[x_idx_1] else 0
            y_val_2 = int(y_2[x_idx_2]) if y_2[x_idx_2] else 0
            vertical_line_1.setPos(mouse_point_1.x())
            vertical_line_2.setPos(mouse_point_2.x())

            if 0 < x_val_1 < max(x_1) and 0 < x_val_2 < max(x_2):
                label_1.setText(
                    "{} \n{} \n({})".format(labels[0],
                                            Amount.format_amount(str(x_val_1)) + " kr/m²",
                                            Amount.format_amount(str(y_val_1)) + " salg"))
                label_2.setText(
                    "{} \n{} \n({})".format(labels[1],
                                            Amount.format_amount(str(x_val_2)) + " kr/m²",
                                            Amount.format_amount(str(y_val_2)) + " salg"))
            else:
                label_1.setText(
                    "{} \n{} \n({})".format(labels[0],
                                            Amount.format_amount(str(0)) + " kr/m²",
                                            Amount.format_amount(str(0)) + " salg"))
                vertical_line_1.setPos(0)
                label_2.setText(
                    "{} \n{} \n({})".format(labels[1],
                                            Amount.format_amount(str(0)) + " kr/m²",
                                            Amount.format_amount(str(0)) + " salg"))
                vertical_line_2.setPos(0)

    proxy_mouse_moved_1 = SignalProxy(plot_widget_1.scene().sigMouseMoved, rateLimit=60,
                                      slot=mouse_moved)
    proxy_mouse_moved_2 = SignalProxy(plot_widget_2.scene().sigMouseMoved, rateLimit=60,
                                      slot=mouse_moved)
    plot_widget_1.proxy = proxy_mouse_moved_1
    plot_widget_2.proxy = proxy_mouse_moved_2
