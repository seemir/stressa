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
        self._parent = parent
        self._error = error
        self._data = {"fornavn": "", "etternavn": "", "kjonn": "",
                      "fodselsdato": "", "adresse": "", "postnr": "",
                      "poststed": "", "kommune": "", "fylke": "",
                      "epost": "", "mobil_tlf": "", "privat_tlf": "",
                      "jobb_tlf": "", "fax": ""}

    @property
    def data(self):
        return self._data

    def contact_info(self):
        self._parent.ui.line_edit_fornavn.editingFinished.connect(
            lambda: self.set_content("fornavn", Name, "format_name"))
        self._parent.ui.line_edit_etternavn.editingFinished.connect(
            lambda: self.set_content("etternavn", Name, "format_name"))
        self._parent.ui.combo_box_kjonn.addItems(self._kjonn)
        self.data.update({"kjonn": self._parent.ui.combo_box_kjonn.currentText()})
        self.data.update({"fodselsdato": self._parent.ui.date_edit_fodselsdato.date()})
        self._parent.ui.line_edit_adresse.editingFinished.connect(
            lambda: self.set_content("adresse", Address, "format_address"))
        self._parent.ui.line_edit_postnr.editingFinished.connect(
            lambda: self.update_line_edits("postnr", self._post_code, Posten, "zip_code_info"))
        self._parent.ui.line_edit_epost.editingFinished.connect(
            lambda: self.set_content("epost", Email, "format_email"))
        self._parent.ui.line_edit_mobil_tlf.editingFinished.connect(
            lambda: self.set_content("mobil_tlf", Mobile, "format_number"))
        self._parent.ui.line_edit_privat_tlf.editingFinished.connect(
            lambda: self.set_content("privat_tlf", Phone, "format_number"))
        self._parent.ui.line_edit_jobb_tlf.editingFinished.connect(
            lambda: self.set_content("jobb_tlf", Phone, "format_number"))
        self._parent.ui.line_edit_fax.editingFinished.connect(
            lambda: self.set_content("fax", Phone, "format_number"))
