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

    def __init__(self, parent, error):
        super(FinnModel, self).__init__(parent, error)

    def finn_info(self):
        self.parent.ui.line_edit_finnkode_1.editingFinished.connect(
            lambda: self.update_line_edits("finnkode_1", self._finn_kode, Finn,
                                           "housing_information", "1"))
        self.parent.ui.push_button_finn_1.clicked.connect(self.open_finn_url)

        self.parent.ui.line_edit_finnkode_2.editingFinished.connect(
            lambda: self.update_line_edits("finnkode_2", self._finn_kode, Finn,
                                           "housing_information", "2"))
        self.parent.ui.push_button_finn_2.clicked.connect(self.open_finn_url)

        self.parent.ui.line_edit_finnkode_3.editingFinished.connect(
            lambda: self.update_line_edits("finnkode_3", self._finn_kode, Finn,
                                           "housing_information", "3"))
        self.parent.ui.push_button_finn_3.clicked.connect(self.open_finn_url)

    @staticmethod
    def open_finn_url():
        webbrowser.open(FINN_URL)
