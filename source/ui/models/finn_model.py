# -*- coding: utf-8 -*-

"""
Module of the Finn model based on the MVC principle

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import webbrowser
from PyQt5.QtCore import QObject, pyqtSlot

from source.app import Finn
from source.util import Assertor

from .settings import FINN_URL
from .model import Model


class FinnModel(Model):
    """
    Implementation of the Finn model for which all the Finn based logic is stored

    """
    _finn_kode = ["finnkode", "status", "sistendret", "referanse", "finn_adresse",
                  "prisantydning", "formuesverdi", "fellesgjeld", "felleskostmnd",
                  "omkostninger", "kommunaleavg", "totalpris", "fellesformue",
                  "boligtype", "eieform", "etasje", "bygger", "soverom", "rom",
                  "primrrom", "bruttoareal", "energimerking", "tomteareal", "sq_price",
                  "views", "email_sent", "favorite_click", "prospect_viewed",
                  "prospect_ordered", "add_to_calendar"]

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

    @pyqtSlot()
    def finn_info(self):
        """
        Method for retrieving Finn ad information

        """
        self.parent.ui.line_edit_finnkode_1.editingFinished.connect(
            lambda: self.update_line_edits("finnkode", self._finn_kode, Finn,
                                           "housing_information", "_1"))
        self.parent.ui.line_edit_finnkode_2.editingFinished.connect(
            lambda: self.update_line_edits("finnkode", self._finn_kode, Finn,
                                           "housing_information", "_2"))
        self.parent.ui.line_edit_finnkode_3.editingFinished.connect(
            lambda: self.update_line_edits("finnkode", self._finn_kode, Finn,
                                           "housing_information", "_3"))

    @pyqtSlot()
    def open_finn_url(self, line_edit: str):
        """
        method for opening Finn link

        Parameters
        ----------
        line_edit   : str
                      name of the line_edit for which the Finn code is inputted

        """
        Assertor.assert_data_types([line_edit], [str])
        finn_code = getattr(self.parent.ui, "line_edit_" + line_edit).text()
        if finn_code:
            webbrowser.open(FINN_URL[:FINN_URL.rfind("/")] + "/homes/ad.html?finnkode=" + finn_code)
        else:
            webbrowser.open(FINN_URL)

    @pyqtSlot()
    def clear_all(self):
        """
        method for clearing all line_edits and combo_boxes in model

        """
        self.clear_line_edits(["finnkode_1", "finnkode_2", "finnkode_3"])
        self.clear_line_edits(self._finn_kode, "_1")
        self.clear_line_edits(self._finn_kode, "_2")
        self.clear_line_edits(self._finn_kode, "_3")
