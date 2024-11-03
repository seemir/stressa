# -*- coding: utf-8 -*-
"""
Module containing logic for table with Ad History

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame

from PyQt5.QtCore import Qt, QObject, pyqtSlot  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QHeaderView  # pylint: disable=no-name-in-module
from source.util import Assertor

from .table_model import TableModel
from .model import Model


class AdHistoryModel(Model):
    """
    Implementation of model for Ad history

    """

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent      : QObject
                      Parent view for which the model in to be linked

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent)
        self.keys = None
        self.values = None

    @pyqtSlot()
    def add_ad_history(self, postfix: str):
        """
        method for adding Finn ad history to front end

        Parameters
        ----------
        postfix     : str
                      index if used in naming of widgets

        """
        Assertor.assert_data_types([postfix], [str])
        grandparent = self.parent.parent
        history_data = {}
        ad_key = "annonse_historikk"

        if grandparent.finn_model.finn_data:
            for key, val in grandparent.finn_model.finn_data.items():
                if key[:-len(postfix)] == ad_key:
                    history_data.update(
                        {key: val.to_dict() if isinstance(val, DataFrame) else val})
        self.data.update(history_data)
        if ad_key + postfix in self.data.keys() and self.data[ad_key + postfix]:
            ad_history_data_model = TableModel(
                DataFrame(self.data[ad_key + postfix]), alignment=Qt.AlignCenter)
            self.parent.ui_form.table_view_annonse_historikk.setModel(
                ad_history_data_model)
            self.parent.ui_form.table_view_annonse_historikk.horizontalHeader() \
                .setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.parent.ui_form.table_view_annonse_historikk.horizontalHeader() \
                .setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.parent.ui_form.table_view_annonse_historikk.horizontalHeader() \
                .setSectionResizeMode(2, QHeaderView.Stretch)

    @pyqtSlot()
    def clear_ad_history(self, postfix: str):
        """
        method for clearing finn ad history from line_edit and graphics

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        self.clear_finn_data('ad_history' + postfix)

    def clear_finn_data(self, full_key):
        """
        helper method for clearing inputted Finn data

        """
        grandparent = self.parent.parent.finn_model
        if full_key in self.data.keys():
            self.data.pop(full_key)
        if full_key in grandparent.data.keys():
            grandparent.data.pop(full_key)
        if full_key in grandparent.finn_data.keys():
            grandparent.finn_data.pop(full_key)
