# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Name, Address, Email, Mobile, Phone
from source.app import Posten

from .model import Model


class ContactModel(Model):
    _kjonn = ["", "Mann", "Kvinne"]
    _post_code = ["postnr", "poststed", "kommune", "fylke"]

    def __init__(self, parent, error):
        super(ContactModel, self).__init__(parent, error)
        self.parent.ui.combo_box_kjonn.addItems(self._kjonn)

    def contact_info(self):
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
