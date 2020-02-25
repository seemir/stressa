# -*- coding: utf-8 -*-

"""
Module of the Finn model based on the MVC principle

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from random import randint
import webbrowser

from PyQt5.QtCore import QObject, pyqtSlot, Qt

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
        self.finn_data = {}
        self.parent.ui.push_button_hent_finn_data_1.clicked.connect(
            lambda: self.add_finn_info("_1"))
        self.parent.ui.push_button_finn_1.clicked.connect(
            lambda: self.open_finn_url("_1"))
        self.parent.ui.push_button_eierskifte_historikk_1.clicked.connect(
            lambda: self.parent.history_view.add_finn_history("_1"))
        self.parent.ui.push_button_statistikk_1.clicked.connect(
            lambda: self.parent.statistics_view.add_statistics_info("_1"))

        self.parent.ui.push_button_hent_finn_data_2.clicked.connect(
            lambda: self.add_finn_info("_2"))
        self.parent.ui.push_button_finn_2.clicked.connect(
            lambda: self.open_finn_url("_2"))
        self.parent.ui.push_button_eierskifte_historikk_2.clicked.connect(
            lambda: self.parent.history_view.add_finn_history("_2"))
        self.parent.ui.push_button_statistikk_2.clicked.connect(
            lambda: self.parent.statistics_view.add_statistics_info("_2"))

        self.parent.ui.push_button_hent_finn_data_3.clicked.connect(
            lambda: self.add_finn_info("_3"))
        self.parent.ui.push_button_finn_3.clicked.connect(
            lambda: self.open_finn_url("_3"))
        self.parent.ui.push_button_eierskifte_historikk_3.clicked.connect(
            lambda: self.parent.history_view.add_finn_history("_3"))
        self.parent.ui.push_button_statistikk_3.clicked.connect(
            lambda: self.parent.statistics_view.add_statistics_info("_3"))

    @pyqtSlot()
    def finn_info(self):
        """
        Method for retrieving Finn ad information

        """
        self.parent.ui.line_edit_finnkode_1.editingFinished.connect(
            lambda: self.clear_finn_info("_1"))
        self.parent.ui.line_edit_finnkode_2.editingFinished.connect(
            lambda: self.clear_finn_info("_2"))
        self.parent.ui.line_edit_finnkode_3.editingFinished.connect(
            lambda: self.clear_finn_info("_3"))

    @pyqtSlot()
    def add_finn_info(self, postfix: str):
        """
        method for adding finn_info to line_edits

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        try:
            Assertor.assert_data_types([postfix], [str])
            finn_code = getattr(self.parent.ui, "line_edit_finnkode" + postfix).text().strip()
            if finn_code and finn_code not in self.data.values():
                getattr(self.parent.ui, "progress_bar" + postfix).setValue(randint(0, 30))
                getattr(self.parent.ui, "progress_bar" + postfix).setTextVisible(False)
                finn_processing = FinnAdvertProcessing(finn_code)
                finn_data = finn_processing.multiplex_info_2
                self.finn_data = {key + postfix: val for key, val in finn_data.items()}
                self.set_line_edits("finnkode", self._finn_keys, postfix=postfix, data=finn_data)
                self.parent.statistics_view.statistics_model.add_statistics_info(postfix)
                self.data.update(self.parent.statistics_view.statistics_model.data)
                self.parent.history_view.history_model.add_finn_history(postfix)
                self.data.update(self.parent.history_view.history_model.data)
                getattr(self.parent.ui, "progress_bar" + postfix).setValue(30)
                # finn_processing.print_pdf()
            elif finn_code and finn_code in self.data.values():
                if ("finnkode" + postfix) not in self.data.keys():
                    getattr(self.parent.ui, "progress_bar" + postfix).setValue(0)
                    getattr(self.parent.ui, "progress_bar" + postfix).setTextVisible(True)
                    getattr(self.parent.ui, "progress_bar" + postfix).setAlignment(
                        Qt.AlignCenter)
                    getattr(self.parent.ui, "progress_bar" + postfix).setFormat("Duplikat!")
            else:
                self.clear_finn_info(postfix)
        except Exception as finn_processing_error:
            self.parent.error_view.show_error(finn_processing_error, self.data)
            self.parent.error_view.exec_()
            self.clear_finn_info(postfix, force=True)
            getattr(self.parent.ui, "progress_bar" + postfix).setValue(0)
            getattr(self.parent.ui, "line_edit_finnkode" + postfix).setFocus()

    @pyqtSlot()
    def clear_finn_info(self, postfix, force=False):
        """
        method for clearing finn info

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits
        force       : bool
                      boolean to indicate if one wants to force a clear

        """
        Assertor.assert_data_types([postfix, force], [str, bool])
        finn_code = getattr(self.parent.ui, "line_edit_finnkode" + postfix).text().strip()
        if not finn_code or force:
            self.clear_line_edits(["finnkode" + postfix])
            self.clear_line_edits(self._finn_keys, postfix)
            self.parent.history_view.history_model.clear_finn_history(postfix)
            self.parent.statistics_view.statistics_model.clear_statistics_info(postfix)
            getattr(self.parent.ui, "progress_bar" + postfix).setTextVisible(False)
            getattr(self.parent.ui, "progress_bar" + postfix).setValue(0)

    @pyqtSlot()
    def open_finn_url(self, postfix: str):
        """
        method for opening Finn link

        Parameters
        ----------
        postfix     : str
                      index if used in naming of line_edits

        """
        Assertor.assert_data_types([postfix], [str])
        finn_code = getattr(self.parent.ui, "line_edit_finnkode" + postfix).text()
        if finn_code:
            webbrowser.open(FINN_URL[:FINN_URL.rfind("/")] + "/homes/ad.html?finnkode=" + finn_code)
        else:
            webbrowser.open(FINN_URL)

    @pyqtSlot()
    def clear_all(self):
        """
        method for clearing all line_edits and combo_boxes in model

        """
        self.parent.ui.tab_widget_finn.setCurrentIndex(0)
        self.clear_finn_info("_1", True)
        self.parent.history_view.history_model.clear_finn_history("_1")
        self.parent.statistics_view.statistics_model.clear_statistics_info("_1")

        self.clear_finn_info("_2", True)
        self.parent.history_view.history_model.clear_finn_history("_2")
        self.parent.statistics_view.statistics_model.clear_statistics_info("_2")

        self.clear_finn_info("_3", True)
        self.parent.history_view.history_model.clear_finn_history("_3")
        self.parent.statistics_view.statistics_model.clear_statistics_info("_3")
