# -*- coding: utf-8 -*-
"""
Module containing logic for table and graph with Ownership History

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame

from PyQt5.QtCore import QObject, pyqtSlot
from source.util import Assertor

from .table_model import TableModel
from .model import Model

from ..graphics import BarChartWithLine


class HistoryModel(Model):
    """
    Implementation of model for Ownership history

    """
    _finn_history_keys = ["finn_adresse", "eieform", "kommunenr", "gardsnr", "bruksnr",
                          "bruksenhetsnr", "seksjonsnr", "historikk"]

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
        self.bar_plot = None

    @pyqtSlot()
    def add_finn_history(self, postfix: str):
        """
        method for adding Finn ownership history to front end

        Parameters
        ----------
        postfix     : str
                      index if used in naming of widgets

        """
        Assertor.assert_data_types([postfix], [str])
        grandparent = self.parent.parent
        history_data = {}
        if grandparent.finn_model.finn_data:
            for key, val in grandparent.finn_model.finn_data.items():
                if key[:-len(postfix)] in self._finn_history_keys:
                    if key[:-len(postfix)] == "historikk":
                        history_data.update(
                            {key: val.to_dict() if isinstance(val, DataFrame) else val})
                    else:
                        history_data.update({key: val})
        self.data.update(history_data)
        for key in self._finn_history_keys:
            if key == "historikk":
                BarChartWithLine.clear_graphics(self.parent.ui_form.graphics_view_historikk,
                                                self.parent.ui_form.table_view_historikk)
                if key + postfix in self.data.keys() and self.data["historikk" + postfix]:
                    # table
                    history_data_model = TableModel(DataFrame(self.data[key + postfix]))
                    self.parent.ui_form.table_view_historikk.setModel(history_data_model)

                    # bar chart
                    history = self.data["historikk" + postfix]["Pris"]

                    self.keys = [int(key) + 0.5 for key in list(history.keys())]
                    self.values = [int(val.replace("kr", "").replace(" ", "").replace("\xa0", ""))
                                   for val in history.values()][::-1]
                    finn_code = grandparent.finn_model.data["finnkode" + postfix]
                    bolig_type = grandparent.finn_model.data["boligtype" + postfix]
                    status = grandparent.finn_model.data["status" + postfix]
                    self.bar_plot = BarChartWithLine(
                        self.keys, self.values,
                        self.parent.ui_form.graphics_view_historikk,
                        self.parent.ui_form.table_view_historikk,
                        legend='<div style="text-align: center">'
                               '<span style="font-size: 10pt">FINN kode:{}</span><br>'
                               '<span style="font-size: 10pt">Boligtype: {}</span><br>'
                               '<span style="font-size: 10pt">(Status: {})</span>'
                               '</div>'.format(finn_code, bolig_type, status))
                    self.bar_plot.table_view_mapping()
            else:
                getattr(self.parent.ui_form, "line_edit_" + key).clear()
                if key + postfix in self.data.keys():
                    getattr(self.parent.ui_form, "line_edit_" + key).setText(
                        self.data[key + postfix])

        self.parent.ui_form.graphics_view_historikk.setMouseEnabled(x=False, y=False)
        self.parent.ui_form.graphics_view_historikk.getAxis('left').setStyle(showValues=False)
        self.parent.ui_form.graphics_view_historikk.getAxis('bottom').setStyle(showValues=False)

    @pyqtSlot()
    def clear_finn_history(self, postfix: str):
        """
        method for clearing finn ownership history from line_edit and graphics

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        for key in self._finn_history_keys:
            full_key = key + postfix
            if key == "historikk":
                self.clear_finn_data(full_key)
                BarChartWithLine.clear_graphics(self.parent.ui_form.graphics_view_historikk,
                                                self.parent.ui_form.table_view_historikk)
            else:
                self.clear_finn_data(full_key)
                getattr(self.parent.ui_form, "line_edit_" + key).clear()

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
