# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import webbrowser

from PyQt5.QtCore import QObject, pyqtSlot

from source.domain import Name, Address, Email, Mobile, Phone, Money
from source.app import Posten, Finn

from .settings import LINE_EDITS, FIELDS, FINN_URL


class Formatting(QObject):

    def __init__(self, parent, error=None):
        super().__init__()
        self._parent = parent
        self._error = error

    def format_contact_info(self):
        self._parent.ui.line_edit_fornavn.editingFinished.connect(
            lambda: self.format_line_edit("fornavn", Name, "format_name"))
        self._parent.ui.line_edit_etternavn.editingFinished.connect(
            lambda: self.format_line_edit("etternavn", Name, "format_name"))
        self._parent.ui.line_edit_adresse.editingFinished.connect(
            lambda: self.format_line_edit("adresse", Address, "format_address"))
        self._parent.ui.combo_box_kjonn.addItems(FIELDS["kjønn"])
        self._parent.ui.line_edit_postnr.editingFinished.connect(
            lambda: self.update_line_edits("postnr", Posten, "zip_code_info"))
        self._parent.ui.line_edit_epost.editingFinished.connect(
            lambda: self.format_line_edit("epost", Email, "format_email"))
        self._parent.ui.line_edit_mobil_tlf.editingFinished.connect(
            lambda: self.format_line_edit("mobil_tlf", Mobile, "format_number"))
        self._parent.ui.line_edit_privat_tlf.editingFinished.connect(
            lambda: self.format_line_edit("privat_tlf", Phone, "format_number"))
        self._parent.ui.line_edit_jobb_tlf.editingFinished.connect(
            lambda: self.format_line_edit("jobb_tlf", Phone, "format_number"))
        self._parent.ui.line_edit_fax.editingFinished.connect(
            lambda: self.format_line_edit("fax", Phone, "format_number"))

        self._parent.ui.line_edit_brutto_inntekt.editingFinished.connect(
            lambda: self.format_line_edit("brutto_inntekt", Money, "value"))
        self._parent.ui.line_edit_trygde_inntekt.editingFinished.connect(
            lambda: self.format_line_edit("trygde_inntekt", Money, "value"))
        self._parent.ui.line_edit_leieinntekt.editingFinished.connect(
            lambda: self.format_line_edit("leieinntekt", Money, "value"))
        self._parent.ui.line_edit_total_skatt.editingFinished.connect(
            lambda: self.format_line_edit("total_skatt", Money, "value"))
        self._parent.ui.line_edit_total_netto.editingFinished.connect(
            lambda: self.format_line_edit("total_netto", Money, "value"))
        self._parent.ui.line_edit_netto_likviditet.editingFinished.connect(
            lambda: self.format_line_edit("netto_likviditet", Money, "value"))

        self._parent.ui.line_edit_student_lan.editingFinished.connect(
            lambda: self.format_line_edit("student_lan", Money, "value"))
        self._parent.ui.line_edit_kreditt_gjeld.editingFinished.connect(
            lambda: self.format_line_edit("kreditt_gjeld", Money, "value"))
        self._parent.ui.line_edit_strom.editingFinished.connect(
            lambda: self.format_line_edit("strom", Money, "value"))
        self._parent.ui.line_edit_andre_utgifter.editingFinished.connect(
            lambda: self.format_line_edit("andre_utgifter", Money, "value"))
        self._parent.ui.push_button_sifo_utgifter.clicked.connect(self._parent.open_sifo_calculator)
        self._parent.ui.line_edit_sifo_utgifter.editingFinished.connect(
            lambda: self.format_line_edit("sifo_utgifter", Money, "value"))
        self._parent.ui.line_edit_totale_utgifter.editingFinished.connect(
            lambda: self.format_line_edit("totale_utgifter", Money, "value"))
        self._parent.ui.line_edit_likviditetsgrad.editingFinished.connect(
            lambda: self.format_line_edit("likviditetsgrad", Money, "value"))

        self._parent.ui.push_button_finn_1.clicked.connect(self.open_finn_url)
        self._parent.ui.line_edit_finn_kode_1.editingFinished.connect(
            lambda: self.update_line_edits("finn_kode", Finn, "housing_information", 1))

        self._parent.ui.push_button_finn_2.clicked.connect(self.open_finn_url)
        self._parent.ui.line_edit_finn_kode_2.editingFinished.connect(
            lambda: self.update_line_edits("finn_kode", Finn, "housing_information", 2))

        self._parent.ui.push_button_finn_3.clicked.connect(self.open_finn_url)
        self._parent.ui.line_edit_finn_kode_3.editingFinished.connect(
            lambda: self.update_line_edits("finn_kode", Finn, "housing_information", 3))

        self._parent.ui.combo_box_lanetype.addItems(FIELDS["lånetype"])
        self._parent.ui.combo_box_laneperiode.addItems(FIELDS["låneperiode"])
        self._parent.ui.combo_box_interval.addItems(FIELDS["interval"])

        self._parent.ui.line_edit_egenkapital.editingFinished.connect(
            lambda: self.format_line_edit("egenkapital", Money, "value"))

    def format_sifo_info(self, parent):
        self._parent.ui.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.format_line_edit("brutto_arsinntekt", Money, "value"))
        self._parent.ui.line_edit_brutto_arsinntekt.setText(
            parent.ui.line_edit_brutto_inntekt.text())

    @pyqtSlot()
    def format_line_edit(self, line_edit_name: str, model, method: str):
        line_edit = getattr(self._parent.ui, "line_edit_" + line_edit_name)
        line_edit_str = line_edit.text().strip()
        try:
            if line_edit_str:
                line_edit.setText(getattr(model(line_edit_str), method)())
            else:
                line_edit.clear()
        except Exception as formatting_error:
            error = self._error(self._parent, formatting_error)
            line_edit.clear()
            error.exec_()

    @pyqtSlot()
    def update_line_edits(self, line_edit_name: str, model, method, index=None):
        line_edits = LINE_EDITS[line_edit_name]
        postfix = "_" + str(index) if index else ""
        line_edit_text = getattr(self._parent.ui, "line_edit_" + line_edit_name + postfix).text()
        try:
            if line_edit_text:
                model_info = getattr(model(line_edit_text), method)()
                for line_edit in line_edits:
                    getattr(self._parent.ui, "line_edit_" + line_edit + postfix).setText(
                        model_info[line_edit] if line_edit in model_info.keys() else "")
            else:
                self.clear_line_edits(line_edit_name, index)
        except Exception as update_error:
            error = self._error(self._parent, update_error)
            self.clear_line_edits(line_edit_name, index)
            error.exec_()

    @pyqtSlot()
    def clear_line_edits(self, line_edit_name: str, index=None):
        line_edits = LINE_EDITS[line_edit_name]
        postfix = "_" + str(index) if index else ""
        for line_edit in line_edits:
            getattr(self._parent.ui, "line_edit_" + line_edit + postfix).clear()

    @pyqtSlot()
    def open_finn_url(self):
        webbrowser.open(FINN_URL)
