# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Name, Address, Email, Mobile, Phone, Money
from source.app import Posten

from .model import Model


class LaneModel(Model):
    _kjonn = ["", "Mann", "Kvinne"]
    _post_code = ["postnr", "poststed", "kommune", "fylke"]
    _lanetype = ["", "Sammenligning", "Annuitetslån", "Serielån"]
    _laneperiode = [""] + [str(yr) + " år" for yr in range(1, 31)]
    _intervall = ["", "Ukentlig", "Annenhver uke", "Månedlig", "Annenhver måned",
                  "Kvartalsvis", "Årlig"]

    def __init__(self, parent):
        super(LaneModel, self).__init__(parent)
        self.parent.ui.combo_box_kjonn.addItems(self._kjonn)
        self.parent.ui.combo_box_lanetype.addItems(self._lanetype)
        self.parent.ui.combo_box_laneperiode.addItems(self._laneperiode)
        self.parent.ui.combo_box_intervall.addItems(self._intervall)

    def lane_info(self):
        self.parent.ui.line_edit_fornavn.editingFinished.connect(
            lambda: self.set_line_edit("fornavn", Name, "format_name"))
        self.parent.ui.line_edit_etternavn.editingFinished.connect(
            lambda: self.set_line_edit("etternavn", Name, "format_name"))
        self.parent.ui.combo_box_kjonn.activated.connect(
            lambda: self.set_combo_box("kjonn"))
        self.parent.ui.date_edit_fodselsdato.editingFinished.connect(
            lambda: self.set_date_edit("fodselsdato"))
        self.parent.ui.line_edit_adresse.editingFinished.connect(
            lambda: self.set_line_edit("adresse", Address, "format_address"))
        self.parent.ui.line_edit_postnr.editingFinished.connect(
            lambda: self.update_line_edits("postnr", self._post_code, Posten, "zip_code_info"))
        self.parent.ui.line_edit_epost.editingFinished.connect(
            lambda: self.set_line_edit("epost", Email, "format_email"))
        self.parent.ui.line_edit_mobil_tlf.editingFinished.connect(
            lambda: self.set_line_edit("mobil_tlf", Mobile, "format_number"))
        self.parent.ui.line_edit_privat_tlf.editingFinished.connect(
            lambda: self.set_line_edit("privat_tlf", Phone, "format_number"))
        self.parent.ui.line_edit_jobb_tlf.editingFinished.connect(
            lambda: self.set_line_edit("jobb_tlf", Phone, "format_number"))
        self.parent.ui.line_edit_fax.editingFinished.connect(
            lambda: self.set_line_edit("fax", Phone, "format_number"))

        self.parent.ui.line_edit_brutto_inntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_inntekt", Money, "value"))
        self.parent.ui.line_edit_trygde_inntekt.editingFinished.connect(
            lambda: self.set_line_edit("trygde_inntekt", Money, "value"))
        self.parent.ui.line_edit_leieinntekt.editingFinished.connect(
            lambda: self.set_line_edit("leieinntekt", Money, "value"))
        self.parent.ui.line_edit_total_skatt.editingFinished.connect(
            lambda: self.set_line_edit("total_skatt", Money, "value"))
        self.parent.ui.line_edit_total_netto.editingFinished.connect(
            lambda: self.set_line_edit("total_netto", Money, "value"))
        self.parent.ui.line_edit_netto_likviditet.editingFinished.connect(
            lambda: self.set_line_edit("netto_likviditet", Money, "value"))
        self.parent.ui.line_edit_student_lan.editingFinished.connect(
            lambda: self.set_line_edit("student_lan", Money, "value"))
        self.parent.ui.line_edit_kreditt_gjeld.editingFinished.connect(
            lambda: self.set_line_edit("kreditt_gjeld", Money, "value"))
        self.parent.ui.line_edit_strom.editingFinished.connect(
            lambda: self.set_line_edit("strom", Money, "value"))
        self.parent.ui.line_edit_andre_utgifter.editingFinished.connect(
            lambda: self.set_line_edit("andre_utgifter", Money, "value"))
        self.parent.ui.line_edit_sifo_utgifter.editingFinished.connect(
            lambda: self.set_line_edit("sifo_utgifter", Money, "value"))
        self.parent.ui.line_edit_totale_utgifter.editingFinished.connect(
            lambda: self.set_line_edit("totale_utgifter", Money, "value"))
        self.parent.ui.line_edit_likviditetsgrad.editingFinished.connect(
            lambda: self.set_line_edit("likviditetsgrad", Money, "value"))


        self.parent.ui.combo_box_lanetype.activated.connect(
            lambda: self.set_combo_box("lanetype"))
        self.parent.ui.combo_box_intervall.activated.connect(
            lambda: self.set_combo_box("intervall"))
        self.parent.ui.combo_box_laneperiode.activated.connect(
            lambda: self.set_combo_box("laneperiode"))
        self.parent.ui.date_edit_startdato.editingFinished.connect(
            lambda: self.set_date_edit("startdato"))
        self.parent.ui.line_edit_egenkapital.editingFinished.connect(
            lambda: self.set_line_edit("egenkapital", Money, "value"))
