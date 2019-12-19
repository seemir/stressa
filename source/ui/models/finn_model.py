# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import webbrowser

from source.app import Finn

from .settings import FINN_URL
from .model import Model


class FinnModel(Model):
    _finn_kode = ["finnkode", "sistendret", "referanse", "finn_adresse", "prisantydning",
                  "formuesverdi", "fellesgjeld", "felleskostmnd", "omkostninger",
                  "kommunaleavg", "totalpris", "fellesformue", "boligtype", "eieform",
                  "etasje", "bygger", "soverom", "rom", "primrrom", "bruttoareal",
                  "energimerking", "tomteareal"]

    def __init__(self, parent):
        super(FinnModel, self).__init__(parent)

    def finn_info(self):
        self.parent.ui.line_edit_finnkode_1.editingFinished.connect(
            lambda: self.update_line_edits("finnkode_1", self._finn_kode, Finn,
                                           "housing_information", "1"))
        self.parent.ui.push_button_finn_1.clicked.connect(lambda: self.open_finn_url("finnkode_1"))

        self.parent.ui.line_edit_finnkode_2.editingFinished.connect(
            lambda: self.update_line_edits("finnkode_2", self._finn_kode, Finn,
                                           "housing_information", "2"))
        self.parent.ui.push_button_finn_2.clicked.connect(lambda: self.open_finn_url("finnkode_2"))

        self.parent.ui.line_edit_finnkode_3.editingFinished.connect(
            lambda: self.update_line_edits("finnkode_3", self._finn_kode, Finn,
                                           "housing_information", "3"))
        self.parent.ui.push_button_finn_3.clicked.connect(lambda: self.open_finn_url("finnkode_3"))

    def open_finn_url(self, line_edit):
        finn_code = getattr(self.parent.ui, "line_edit_" + line_edit).text()
        if finn_code:
            webbrowser.open(FINN_URL[:FINN_URL.rfind("/")] + "/homes/ad.html?finnkode=" + finn_code)
        else:
            webbrowser.open(FINN_URL)
