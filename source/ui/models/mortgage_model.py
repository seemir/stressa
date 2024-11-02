# -*- coding: utf-8 -*-

"""
Module for main mortgage model for the HomeView

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject, pyqtSlot  # pylint: disable=no-name-in-module

from source.domain import Name, Address, Email, Mobile, Phone, Money
from source.app import PostalCodeProcess
from source.util import Assertor

from .model import Model


class MortgageModel(Model):
    """
    Implementation of the MortgageModel in the HomeView, i.e. contains logic / mortgage
    related data inputted in the HomeView

    """
    _kjonn = ["", "Mann", "Kvinne"]
    _post_code = ["postnr", "poststed", "kommune", "fylke"]
    _lanetype = ["", "Sammenligning", "Annuitetslån", "Serielån"]
    _laneperiode = [""] + [str(yr) + " år" for yr in range(1, 31)]
    _intervall = ["", "Årlig", "Halvårlig", "Kvartalsvis", "Annenhver måned",
                  "Månedlig",
                  "Semi-månedlig", "Annenhver uke", "Ukentlig"]

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation of class

        Parameters
        ----------
        parent  : QObject
                  parent view for which the model resides

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent)
        self.parent.ui_form.combo_box_kjonn_1.addItems(self._kjonn)
        self.parent.ui_form.combo_box_kjonn_2.addItems(self._kjonn)
        self.parent.ui_form.combo_box_lanetype.addItems(self._lanetype)
        self.parent.ui_form.combo_box_laneperiode.addItems(self._laneperiode)
        self.parent.ui_form.combo_box_intervall.addItems(self._intervall)

    @pyqtSlot()
    def mortgage_info(self):
        """
        Method for retrieving and formatting all inputted mortgage information

        """
        # contact information
        self.parent.ui_form.line_edit_fornavn_1.editingFinished.connect(
            lambda: self.set_line_edit("fornavn_1", Name, "format_name"))
        self.parent.ui_form.line_edit_etternavn_1.editingFinished.connect(
            lambda: self.set_line_edit("etternavn_1", Name, "format_name"))
        self.parent.ui_form.combo_box_kjonn_1.activated.connect(
            lambda: self.set_combo_box("kjonn_1"))
        self.parent.ui_form.date_edit_fodselsdato_1.editingFinished.connect(
            lambda: self.set_date_edit("fodselsdato_1"))
        self.parent.ui_form.line_edit_adresse_1.editingFinished.connect(
            lambda: self.set_line_edit("adresse_1", Address, "format_address"))

        self.parent.ui_form.line_edit_postnr_1.editingFinished.connect(
            lambda: self.update_line_edits("postnr", self._post_code,
                                           PostalCodeProcess,
                                           "postal_code_info", postfix="_1"))

        self.parent.ui_form.line_edit_postnr_1.textEdited.connect(
            lambda: self.clear_empty_line_edits("postnr", self._post_code,
                                                postfix="_1"))

        self.parent.ui_form.line_edit_epost_1.editingFinished.connect(
            lambda: self.set_line_edit("epost_1", Email, "format_email"))
        self.parent.ui_form.line_edit_mobil_tlf_1.editingFinished.connect(
            lambda: self.set_line_edit("mobil_tlf_1", Mobile, "format_number"))
        self.parent.ui_form.line_edit_privat_tlf_1.editingFinished.connect(
            lambda: self.set_line_edit("privat_tlf_1", Phone, "format_number"))
        self.parent.ui_form.line_edit_jobb_tlf_1.editingFinished.connect(
            lambda: self.set_line_edit("jobb_tlf_1", Phone, "format_number"))
        self.parent.ui_form.line_edit_fax_1.editingFinished.connect(
            lambda: self.set_line_edit("fax_1", Phone, "format_number"))

        self.parent.ui_form.line_edit_fornavn_2.editingFinished.connect(
            lambda: self.set_line_edit("fornavn_2", Name, "format_name"))
        self.parent.ui_form.line_edit_etternavn_2.editingFinished.connect(
            lambda: self.set_line_edit("etternavn_2", Name, "format_name"))
        self.parent.ui_form.combo_box_kjonn_2.activated.connect(
            lambda: self.set_combo_box("kjonn_2"))
        self.parent.ui_form.date_edit_fodselsdato_2.editingFinished.connect(
            lambda: self.set_date_edit("fodselsdato_2"))
        self.parent.ui_form.line_edit_adresse_2.editingFinished.connect(
            lambda: self.set_line_edit("adresse_2", Address, "format_address"))

        self.parent.ui_form.line_edit_postnr_2.editingFinished.connect(
            lambda: self.update_line_edits("postnr", self._post_code,
                                           PostalCodeProcess,
                                           "output_operation", postfix="_2"))

        self.parent.ui_form.line_edit_postnr_2.textEdited.connect(
            lambda: self.clear_empty_line_edits("postnr", self._post_code,
                                                postfix="_2"))

        self.parent.ui_form.line_edit_epost_2.editingFinished.connect(
            lambda: self.set_line_edit("epost_2", Email, "format_email"))
        self.parent.ui_form.line_edit_mobil_tlf_2.editingFinished.connect(
            lambda: self.set_line_edit("mobil_tlf_2", Mobile, "format_number"))
        self.parent.ui_form.line_edit_privat_tlf_2.editingFinished.connect(
            lambda: self.set_line_edit("privat_tlf_2", Phone, "format_number"))
        self.parent.ui_form.line_edit_jobb_tlf_2.editingFinished.connect(
            lambda: self.set_line_edit("jobb_tlf_2", Phone, "format_number"))
        self.parent.ui_form.line_edit_fax_2.editingFinished.connect(
            lambda: self.set_line_edit("fax_2", Phone, "format_number"))

        # budget information
        self.parent.ui_form.line_edit_brutto_inntekt_total.editingFinished.connect(
            lambda: self.set_line_edit("brutto_inntekt_total", Money, "value"))
        self.parent.ui_form.line_edit_trygde_inntekt_total.editingFinished.connect(
            lambda: self.set_line_edit("trygde_inntekt_total", Money, "value"))
        self.parent.ui_form.line_edit_leieinntekt_total.editingFinished.connect(
            lambda: self.set_line_edit("leieinntekt_total", Money, "value"))
        self.parent.ui_form.line_edit_beregnet_skatt_per_mnd_beloep.editingFinished.connect(
            lambda: self.set_line_edit("beregnet_skatt_per_mnd_beloep", Money,
                                       "value"))
        self.parent.ui_form.line_edit_total_netto.editingFinished.connect(
            lambda: self.set_line_edit("total_netto", Money, "value"))
        self.parent.ui_form.line_edit_netto_likviditet.editingFinished.connect(
            lambda: self.set_line_edit("netto_likviditet", Money, "value"))
        self.parent.ui_form.line_edit_student_lan_total.editingFinished.connect(
            lambda: self.set_line_edit("student_lan_total", Money, "value"))
        self.parent.ui_form.line_edit_kreditt_gjeld_total.editingFinished.connect(
            lambda: self.set_line_edit("kreditt_gjeld_total", Money, "value"))
        self.parent.ui_form.line_edit_husleie_total.editingFinished.connect(
            lambda: self.set_line_edit("husleie_total", Money, "value"))
        self.parent.ui_form.line_edit_strom_total.editingFinished.connect(
            lambda: self.set_line_edit("strom_total", Money, "value"))
        self.parent.ui_form.line_edit_andre_utgifter_total.editingFinished.connect(
            lambda: self.set_line_edit("andre_utgifter_total", Money, "value"))
        self.parent.ui_form.line_edit_sifo_utgifter.editingFinished.connect(
            lambda: self.set_line_edit("sifo_utgifter", Money, "value"))
        self.parent.ui_form.line_edit_totale_utgifter.editingFinished.connect(
            lambda: self.set_line_edit("totale_utgifter", Money, "value"))
        self.parent.ui_form.line_edit_likviditetsgrad.editingFinished.connect(
            lambda: self.set_line_edit("likviditetsgrad", Money, "value"))

        # mortgage structure information
        self.parent.ui_form.combo_box_lanetype.activated.connect(
            lambda: self.set_combo_box("lanetype"))
        self.parent.ui_form.combo_box_intervall.activated.connect(
            lambda: self.set_combo_box("intervall"))
        self.parent.ui_form.combo_box_laneperiode.activated.connect(
            lambda: self.set_combo_box("laneperiode"))
        self.parent.ui_form.date_edit_startdato.editingFinished.connect(
            lambda: self.set_date_edit("startdato"))
        self.parent.ui_form.line_edit_egenkapital.textEdited.connect(
            lambda: self.set_line_edit("egenkapital", Money, "value"))

    @pyqtSlot()
    def clear_all(self):
        """
        method for clearing all line_edits and combo_boxes in model

        """
        self.clear_line_edits(["fornavn", "etternavn", "adresse", "postnr",
                               "poststed", "kommune", "fylke", "epost",
                               "mobil_tlf",
                               "privat_tlf", "jobb_tlf", "fax"], postfix="_1")
        self.clear_line_edits(["fornavn", "etternavn", "adresse", "postnr",
                               "poststed", "kommune", "fylke", "epost",
                               "mobil_tlf",
                               "privat_tlf", "jobb_tlf", "fax"], postfix="_2")
        self.clear_line_edits(
            ["brutto_inntekt", "trygde_inntekt", "leieinntekt",
             "personinntekt", "student_lan", "kreditt_gjeld",
             "husleie", "strom", "andre_utgifter", "variable_utgifter"],
            postfix="_total")
        self.clear_line_edits(
            ["beregnet_skatt_per_mnd_beloep", "sifo_utgifter", "total_netto",
             "totale_utgifter", "netto_likviditet", "likviditetsgrad",
             "egenkapital"])
        self.clear_combo_boxes(
            ["kjonn_1", "kjonn_2", "lanetype", "intervall", "laneperiode"])
        self.clear_date_edits(["fodselsdato_1", "fodselsdato_2", "startdato"])
        self.parent.budget_view.clear_all()

    def print_pdf(self):
        """
        test method for printing pdf of procedure graph

        """
        postal_code = PostalCodeProcess(
            self.parent.ui_form.line_edit_postnr_1.text())
        postal_code.print_pdf()
