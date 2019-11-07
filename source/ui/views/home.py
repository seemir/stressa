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
              "finn_code": ["finn_kode",
                            "sistendret",
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


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = loadUi(os.path.join(os.path.dirname(__file__), "home.ui"), self)
        self.ui.combo_box_kjonn.addItems(["", "Mann", "Kvinne"])

        self.ui.line_edit_postnr.editingFinished.connect(self.update_post_code_info)
        self.ui.line_edit_finn_kode.editingFinished.connect(self.update_finn_info)

        self.ui.line_edit_mobil_tlf.editingFinished.connect(
            lambda: self.format_phone_number("mobil_tlf"))
        self.ui.line_edit_privat_tlf.editingFinished.connect(
            lambda: self.format_phone_number("privat_tlf"))
        self.ui.line_edit_jobb_tlf.editingFinished.connect(
            lambda: self.format_phone_number("jobb_tlf"))

    def update_post_code_info(self):
        line_edits = LINE_EDITS["zip_code"]
        zip_code = self.ui.line_edit_postnr.text().strip()
        try:
            if zip_code:
                posten = Posten(zip_code)
                zip_code_info = posten.zip_code_info()
                self.set_line_edit_content(line_edits[1:], zip_code_info)
            else:
                self.set_line_edit_content(line_edits)
        except Exception as post_error:
            pop_up = Error(self, post_error)
            self.set_line_edit_content(line_edits)
            pop_up.exec_()

    def update_finn_info(self):
        line_edits = LINE_EDITS["finn_code"]
        finn_code = self.ui.line_edit_finn_kode.text().strip()
        try:
            if finn_code:
                finn = Finn(finn_code)
                finn_info = finn.housing_information()
                self.set_line_edit_content(line_edits, finn_info)
            else:
                self.set_line_edit_content(line_edits)
        except Exception as finn_error:
            pop_up = Error(self, finn_error)
            self.set_line_edit_content(line_edits)
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

    def set_line_edit_content(self, line_edits, content=None):
        for line_edit in line_edits:
            try:
                getattr(self.ui, "line_edit_" + line_edit).setText(
                    content[line_edit] if content else "")
            except Exception:
                continue
