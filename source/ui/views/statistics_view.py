# -*- coding: utf-8 -*-
"""
StatisticsView which contains the GUI for the Statistics from home ads

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from random import randint

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

from source.util import Assertor

from .images_view import ImagesView
from .meta_view import MetaView
from .map_view import MapView

from ..models import StatisticsModel


class StatisticsView(QDialog):
    """
    Statistics view

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view for the SifoView

        """
        Assertor.assert_data_types([parent], [QWidget])
        super().__init__(parent=parent)
        up = os.path.dirname

        self.ui = loadUi(os.path.join(up(__file__), "forms/statistics_form.ui"), self)
        self.ui.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self._parent = parent
        self._statistics_model = StatisticsModel(self)
        self._meta_view = MetaView(self)
        self._map_view = MapView(self)
        self._images_view = ImagesView(self)

        self.ui.push_button_grunnboka.setIcon(
            QIcon(up(up(os.path.abspath(__file__))) + '/images/grunnboka.svg'))

        self.ui.push_button_meta_data.clicked.connect(self.meta_view.display)
        self.ui.push_button_oppdater.clicked.connect(self.update)
        self.ui.push_button_avbryt.clicked.connect(self.close)
        self.ui.push_button_show_in_map_1.clicked.connect(self.map_view.show)
        self.ui.push_button_show_in_map_2.clicked.connect(self.map_view.show)
        self.ui.push_button_show_in_map_3.clicked.connect(self.map_view.show)
        self.ui.push_button_show_in_map_4.clicked.connect(self.map_view.show)
        self.ui.push_button_show_in_map_5.clicked.connect(self.map_view.show)
        self.ui.push_button_show_in_map_6.clicked.connect(self.map_view.show)

        self.postfix = None

        self.ui.push_button_grunnboka.clicked.connect(
            lambda: self.parent.grunnboka_view.add_grunnboka_data(self.postfix))
        self.ui.push_button_eierskifte_historikk.clicked.connect(
            lambda: self.parent.history_view.add_finn_history(self.postfix))

        self.ui.push_button_images.clicked.connect(self.images_view.show)

    @property
    def parent(self):
        """
        parent getter

        Returns
        -------
        out     : QObject
                  active parent view for the StatisticsView

        """
        return self._parent

    @property
    def statistics_model(self):
        """
        StatisticsModel getter

        Returns
        -------
        out     : StatisticsModel
                  active StatisticsModel

        """
        return self._statistics_model

    @property
    def meta_view(self):
        """
        MetaView getter

        Returns
        -------
        out     : MetaView
                  View with the metadata for the Statistics view

        """
        return self._meta_view

    @property
    def map_view(self):
        """
        MapView getter

        Returns
        -------
        out     : MapView
                  View with the mapdata for the Statistics view

        """
        return self._map_view

    @property
    def images_view(self):
        """
        ImagesView getter

        Returns
        -------
        out     : ImagesView
                  View with the images data for the Statistics view

        """
        return self._images_view

    def add_statistics_info(self, postfix):
        """
        method for displaying StatisticsView

        """
        self.postfix = postfix
        self.ui.tab_widget_statistics.setCurrentIndex(0)
        self.statistics_model.add_statistics_info(postfix)
        self.show_progress_bar()
        self.show()

    def update(self):
        """
        method for updating

        """
        finn_code = getattr(self.ui, "line_edit_finnkode").text()
        finn_code_1 = getattr(self.parent.ui, "line_edit_finnkode_1").text().strip()
        if finn_code_1 and finn_code:
            getattr(self.ui, "progress_bar_statistics").setValue(randint(5, 25))
            self.parent.finn_model.process_finn_data(finn_code_1, "_1")
            getattr(self.ui, "progress_bar_statistics").setValue(30)

    def show_progress_bar(self):
        """
        method for progress bar display

        """
        finn_code = getattr(self.ui, "line_edit_finnkode").text()
        finn_code_1 = getattr(self.parent.ui, "line_edit_finnkode_1").text().strip()
        finn_code_2 = getattr(self.parent.ui, "line_edit_finnkode_2").text().strip()
        finn_code_3 = getattr(self.parent.ui, "line_edit_finnkode_3").text().strip()
        if finn_code_1 and finn_code:
            getattr(self.ui, "progress_bar_statistics").setValue(30)
        elif finn_code_2 and finn_code:
            getattr(self.ui, "progress_bar_statistics").setValue(30)
        elif finn_code_3 and finn_code:
            getattr(self.ui, "progress_bar_statistics").setValue(30)
        else:
            getattr(self.ui, "progress_bar_statistics").setValue(0)
