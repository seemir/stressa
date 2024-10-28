# -*- coding: utf-8 -*-
"""
Module with logic for the View that handles the Ownership History

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.uic import loadUi  # pylint: disable=no-name-in-module
from PyQt5.QtCore import pyqtSlot, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog, QWidget, \
    QHeaderView  # pylint: disable=no-name-in-module

from source.util import Assertor

from ..models import HistoryModel


class HistoryView(QDialog):
    """
    Implementation of model for Ownership history view

    """

    def __init__(self, parent: QWidget):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QWidget
                  parent view of the HistoryView

        """
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QWidget])
        self.parent = parent
        self.ui_form = loadUi(
            os.path.join(os.path.dirname(__file__), "forms/history_form.ui"),
            self)
        self.ui_form.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.ui_form.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.ui_form.table_view_historikk.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self._history_model = HistoryModel(self)

    @property
    def history_model(self):
        """
        HistoryModel getter

        Returns
        -------
        out     : HistoryModel
                  Model containing all the logic of the OwnershipHistory

        """
        return self._history_model

    @pyqtSlot()
    def add_finn_history(self, postfix: str):
        """
        method for adding ownership history to view

        Parameters
        ----------
        postfix     : str
                      index if used in naming of widgets

        """
        Assertor.assert_data_types([postfix], [str])
        self.history_model.add_finn_history(postfix)
        self.show()
