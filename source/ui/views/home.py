# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from source.app import Posten, Finn
from source.domain import Phone

from .error import Error
from . import resources

LINE_EDITS = {"zip_code": ["postnr",
                           "poststed",
                           "kommune",
                           "fylke"],
              "finn_code": ["sistendret",
                            "referanse",
                            "finn_adresse",
                            "prisantydning",
                            "formuesverdi",
                            "fellesgjeld",
                            "felleskostmnd",
                            "omkostninger",
                            "kommunaleavg",
                            "totalpris",
                            "fellesformue",
                            "boligtype",
                            "eieform",
                            "etasje",
                            "bygger",
                            "soverom",
                            "rom",
                            "primrrom",
                            "bruttoareal",
                            "energimerking",
                            "tomteareal"]}

FIELDS = {"kjønn": ["", "Mann", "Kvinne"],
          "lånetype": ["", "Sammenligning", "Annuitetslån", "Serielån"],
          "låneperiode": [""] + [str(yr) + " år" for yr in range(1, 31)],
          "betalingsinterval": ["", "Ukentlig", "Annenhver uke",
                                "Månedlig", "Annenhver måned", "Kvartalsvis", "Årlig"]}


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/home.ui"), self)
        self.ui.combo_box_kjonn.addItems(FIELDS["kjønn"])

        self.ui.line_edit_postnr.editingFinished.connect(self.update_post_code_info)

        self.ui.line_edit_finn_kode_1.editingFinished.connect(lambda: self.update_finn_info("1"))
        self.ui.line_edit_finn_kode_2.editingFinished.connect(lambda: self.update_finn_info("2"))
        self.ui.line_edit_finn_kode_3.editingFinished.connect(lambda: self.update_finn_info("3"))

        self.ui.line_edit_mobil_tlf.editingFinished.connect(
            lambda: self.format_phone_number("mobil_tlf"))
        self.ui.line_edit_privat_tlf.editingFinished.connect(
            lambda: self.format_phone_number("privat_tlf"))
        self.ui.line_edit_jobb_tlf.editingFinished.connect(
            lambda: self.format_phone_number("jobb_tlf"))

        self.ui.combo_box_lanetype.addItems(FIELDS["lånetype"])
        self.ui.combo_box_laneperiode.addItems(FIELDS["låneperiode"])
        self.ui.combo_box_betalingsinterval.addItems(FIELDS["betalingsinterval"])

    def update_post_code_info(self):
        line_edits = LINE_EDITS["zip_code"]
        zip_code = self.ui.line_edit_postnr.text().strip()
        try:
            if zip_code:
                posten = Posten(zip_code)
                zip_code_info = posten.zip_code_info()
                for line_edit in line_edits:
                    getattr(self.ui, "line_edit_" + line_edit).setText(zip_code_info[line_edit])
            else:
                for line_edit in line_edits:
                    getattr(self.ui, "line_edit_" + line_edit).setText("")
        except Exception as post_error:
            pop_up = Error(self, post_error)
            for line_edit in line_edits:
                getattr(self.ui, "line_edit_" + line_edit).setText("")
            pop_up.exec_()

    def update_finn_info(self, index):
        line_edits = LINE_EDITS["finn_code"]
        finn_code = getattr(self.ui, "line_edit_finn_kode_" + index).text().strip()
        try:
            if finn_code:
                finn = Finn(finn_code)
                finn_info = finn.housing_information()
                for line_edit in line_edits:
                    getattr(self.ui, "line_edit_" + line_edit + "_" + index).setText(
                        finn_info[line_edit] if line_edit in finn_info.keys() else "")
            else:
                for line_edit in line_edits:
                    getattr(self.ui, "line_edit_" + line_edit + "_" + index).setText("")
        except Exception as finn_error:
            pop_up = Error(self, finn_error)
            for line_edit in line_edits:
                getattr(self.ui, "line_edit_" + line_edit + "_" + index).setText("")
            pop_up.exec_()

    def format_phone_number(self, name: str):
        line_edit = getattr(self.ui, "line_edit_" + name)
        line_edit_str = line_edit.text().strip()
        try:
            if line_edit_str:
                phone = Phone(line_edit_str)
                line_edit.setText(phone.format_number())
            else:
                line_edit.clear()
        except Exception as phone_error:
            pop_up = Error(self, phone_error)
            line_edit.clear()
            pop_up.exec_()
