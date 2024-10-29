# -*- coding: utf-8 -*-
"""
Module with logic for the View that handles the Ad history data

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.uic import loadUi  # pylint: disable=no-name-in-module
from PyQt5.QtCore import pyqtSlot, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog, QWidget, \
    QHeaderView  # pylint: disable=no-name-in-module

from source.util import Assertor

from ..models import AdHistoryModel


class AdHistoryView(QDialog):
    """
    Implementation of model for Ad history view

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view of the AdHistoryView

        """
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QWidget])
        self.parent = parent
        self.ui_form = loadUi(
            os.path.join(os.path.dirname(__file__), "forms/ad_history_form.ui"),
            self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui_form.table_view_annonse_historikk.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self._ad_history_model = AdHistoryModel(self)

    @property
    def ad_history_model(self):
        """
        AdHistoryModel getter

        Returns
        -------
        out     : AdHistoryModel
                  Model containing all the logic of the ad history

        """
        return self._ad_history_model

    @pyqtSlot()
    def add_ad_history(self, postfix: str):
        """
        method for adding ad history to view

        Parameters
        ----------
        postfix     : str
                      index if used in naming of widgets

        """
        Assertor.assert_data_types([postfix], [str])
        self.ad_history_model.add_ad_history(postfix)
        self.show()
