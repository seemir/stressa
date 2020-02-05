# -*- coding: utf-8 -*-

"""
Module of the Finn model based on the MVC principle

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import webbrowser
from PyQt5.QtCore import QObject, pyqtSlot

from source.app import FinnAdvertProcessing
from source.util import Assertor

from .settings import FINN_URL
from .model import Model


class FinnModel(Model):
    """
    Implementation of the Finn model for which all the Finn based logic is stored

    """
    _finn_keys = ["finnkode", "status", "sistendret", "referanse", "finn_adresse",
                  "prisantydning", "formuesverdi", "fellesgjeld", "felleskostmnd",
                  "omkostninger", "kommunaleavg", "totalpris", "fellesformue",
                  "boligtype", "eieform", "etasje", "bygger", "soverom", "rom",
                  "renovertr", "primrrom", "bruttoareal", "energimerking",
                  "tomteareal", "sqm_price", "views", "email_sent", "favorite_click",
                  "prospect_viewed", "prospect_ordered", "add_to_calendar"]

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
            lambda: self.clear_finn_info("_1"))

    @pyqtSlot()
    def add_finn_info(self, postfix):
        """
        method for adding finn_info to line_edits

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        try:
            finn_code = getattr(self.parent.ui, "line_edit_finnkode" + postfix).text().strip()
            if finn_code and finn_code not in self.data.values():
                finn_processing = FinnAdvertProcessing(finn_code)
                self.set_line_edits("finnkode", self._finn_keys, postfix=postfix,
                                    data=finn_processing.multiplex_info)
                # finn_processing.print_pdf()
            elif finn_code and finn_code in self.data.values():
                pass
            else:
                self.clear_line_edits(["finnkode" + postfix])
                self.clear_line_edits(self._finn_keys, postfix)
        except Exception as finn_processing_error:
            self.clear_line_edits(["finnkode" + postfix])
            self.clear_line_edits(self._finn_keys, postfix)
            self.parent.error.show_error(finn_processing_error, self.data)
            self.parent.error.exec_()
            getattr(self.parent.ui, "line_edit_finnkode" + postfix).setFocus()

    @pyqtSlot()
    def clear_finn_info(self, postfix):
        """
        method for clearing finn info

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        finn_code = getattr(self.parent.ui, "line_edit_finnkode" + postfix).text().strip()
        if not finn_code:
            self.clear_line_edits(["finnkode" + postfix])
            self.clear_line_edits(self._finn_keys, postfix)

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
        self.clear_line_edits(["finnkode_1"])
        self.clear_line_edits(self._finn_keys, "_1")
