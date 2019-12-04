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

    def contact_info(self):
        self._parent.ui.line_edit_fornavn.editingFinished.connect(
            lambda: self.set_line_edit("fornavn", Name, "format_name"))
        self._parent.ui.line_edit_etternavn.editingFinished.connect(
            lambda: self.set_line_edit("etternavn", Name, "format_name"))
        self._parent.ui.combo_box_kjonn.addItems(self._kjonn)
        self._parent.ui.combo_box_kjonn.activated.connect(self.set_kjonn)
        self._parent.ui.date_edit_fodselsdato.editingFinished.connect(self.set_fodselsdato)
        self._parent.ui.line_edit_adresse.editingFinished.connect(
            lambda: self.set_line_edit("adresse", Address, "format_address"))
        self._parent.ui.line_edit_postnr.editingFinished.connect(
            lambda: self.update_line_edits("postnr", self._post_code, Posten, "zip_code_info"))
        self._parent.ui.line_edit_epost.editingFinished.connect(
            lambda: self.set_line_edit("epost", Email, "format_email"))
        self._parent.ui.line_edit_mobil_tlf.editingFinished.connect(
            lambda: self.set_line_edit("mobil_tlf", Mobile, "format_number"))
        self._parent.ui.line_edit_privat_tlf.editingFinished.connect(
            lambda: self.set_line_edit("privat_tlf", Phone, "format_number"))
        self._parent.ui.line_edit_jobb_tlf.editingFinished.connect(
            lambda: self.set_line_edit("jobb_tlf", Phone, "format_number"))
        self._parent.ui.line_edit_fax.editingFinished.connect(
            lambda: self.set_line_edit("fax", Phone, "format_number"))

    def set_kjonn(self):
        kjonn = str(self._parent.ui.combo_box_kjonn.currentText())
        if kjonn and kjonn not in self.data.values():
            self.data.update({"kjonn": kjonn})
        else:
            self.data.pop("kjonn") if "kjonn" in self.data.keys() else ""

    def set_fodselsdato(self):
        fodselsdato = self._parent.ui.date_edit_fodselsdato.date()
        if fodselsdato.year() != 0000:
            self.data.update({"fodselsdato": fodselsdato})
        else:
            self.data.pop("fodselsdato") if "fodselsdato" in self.data.keys() else ""
