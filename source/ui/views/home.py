# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import webbrowser

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from source.app import Posten, Finn
from source.domain import Name, Address, Phone, Mobile, Email

from .settings import FINN_URL, FIELDS, LINE_EDITS
from .error import Error
from . import resources


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self._ui = loadUi(os.path.join(os.path.dirname(__file__), "forms/home.ui"), self)
        self._ui.combo_box_kjonn.addItems(FIELDS["kjønn"])

        self._ui.line_edit_fornavn.editingFinished.connect(
            lambda: self.format_line_edit("fornavn", Name, "format_name"))
        self._ui.line_edit_etternavn.editingFinished.connect(
            lambda: self.format_line_edit("etternavn", Name, "format_name"))
        self._ui.line_edit_adresse.editingFinished.connect(
            lambda: self.format_line_edit("adresse", Address, "format_address"))
        self._ui.line_edit_postnr.editingFinished.connect(
            lambda: self.update_line_edits("postnr", Posten, "zip_code_info"))
        self._ui.line_edit_epost.editingFinished.connect(
            lambda: self.format_line_edit("epost", Email, "format_email"))

        self._ui.line_edit_finn_kode_1.editingFinished.connect(
            lambda: self.update_line_edits("finn_kode", Finn, "housing_information", 1))
        self._ui.line_edit_finn_kode_2.editingFinished.connect(
            lambda: self.update_line_edits("finn_kode", Finn, "housing_information", 2))
        self._ui.line_edit_finn_kode_3.editingFinished.connect(
            lambda: self.update_line_edits("finn_kode", Finn, "housing_information", 3))

        self._ui.line_edit_mobil_tlf.editingFinished.connect(
            lambda: self.format_line_edit("mobil_tlf", Mobile, "format_number"))
        self._ui.line_edit_privat_tlf.editingFinished.connect(
            lambda: self.format_line_edit("privat_tlf", Phone, "format_number"))
        self._ui.line_edit_jobb_tlf.editingFinished.connect(
            lambda: self.format_line_edit("jobb_tlf", Phone, "format_number"))
        self._ui.line_edit_fax.editingFinished.connect(
            lambda: self.format_line_edit("fax", Phone, "format_number"))

        self._ui.combo_box_lanetype.addItems(FIELDS["lånetype"])
        self._ui.combo_box_laneperiode.addItems(FIELDS["låneperiode"])
        self._ui.combo_box_betalingsinterval.addItems(FIELDS["betalingsinterval"])

        self._ui.push_button_finn_1.clicked.connect(self.open_finn_url)
        self._ui.push_button_finn_2.clicked.connect(self.open_finn_url)
        self._ui.push_button_finn_3.clicked.connect(self.open_finn_url)

    @pyqtSlot()
    def format_line_edit(self, line_edit_name: str, obj, method: str):
        line_edit = getattr(self._ui, "line_edit_" + line_edit_name)
        line_edit_str = line_edit.text().strip()
        try:
            if line_edit_str:
                ob = obj(line_edit_str)
                line_edit.setText(getattr(ob, method)())
            else:
                line_edit.clear()
        except Exception as formatting_error:
            error = Error(self, formatting_error)
            line_edit.clear()
            error.exec_()

    @pyqtSlot()
    def update_line_edits(self, line_edit_name: str, obj, method, index=None):
        line_edits = LINE_EDITS[line_edit_name]
        postfix = "_" + str(index) if index else ""
        line_edit_str = getattr(self._ui, "line_edit_" + line_edit_name + postfix).text().strip()
        try:
            if line_edit_str:
                ob = obj(line_edit_str)
                ob_info = getattr(ob, method)()
                for line_edit in line_edits:
                    getattr(self._ui, "line_edit_" + line_edit + postfix).setText(
                        ob_info[line_edit] if line_edit in ob_info.keys() else "")
            else:
                for line_edit in line_edits:
                    getattr(self._ui, "line_edit_" + line_edit + postfix).clear()
        except Exception as update_error:
            error = Error(self, update_error)
            for line_edit in line_edits:
                getattr(self._ui,
                        "line_edit_" + line_edit + postfix).clear()
            error.exec_()

    @pyqtSlot()
    def open_finn_url(self):
        webbrowser.open(FINN_URL)
