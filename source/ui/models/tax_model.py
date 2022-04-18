# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.util import Assertor
from source.domain import Money

from .model import Model


class TaxModel(Model):
    _tax_year = ["", "2022", "2021", "2020", "2019", "2018"]
    _total_posts = ["brutto_inntekt_total", "trygde_inntekt_total", "leieinntekt_total",
                    "renteinntekter_total", "andre_inntekter_total", "personinntekt_total",
                    "rentekostnader_total"]

    def __init__(self, parent: QObject):
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])

        self.parent.ui.combo_box_tax_year.addItems(self.tax_year)

    @property
    def tax_year(self):
        return self._tax_year

    @property
    def total_posts(self):
        return self._total_posts

    def tax_info(self):
        self.parent.ui.combo_box_tax_year.setFocus()
        self.parent.ui.combo_box_tax_year.activated.connect(
            lambda: self.set_combo_box("tax_year", key_name="skatte_aar"))
        self.parent.ui.line_edit_alder.textEdited.connect(
            lambda: self.set_line_edit("alder"))
        self.parent.ui.line_edit_verdi_primarbolig.textEdited.connect(
            lambda: self.set_value('verdi_primarbolig'))
        self.parent.ui.line_edit_bankinnskudd.textEdited.connect(
            lambda: self.set_value('bankinnskudd'))
        self.parent.ui.line_edit_gjeld.textEdited.connect(
            lambda: self.set_value('gjeld'))
        self.set_line_edits("", line_edits=self.total_posts,
                            data=self.parent.parent.budget_view.budget_model.data)

    def set_value(self, line_edit):
        if getattr(self.parent.ui, "line_edit_" + line_edit).text():
            self.set_line_edit(line_edit, Money, "value")
        else:
            self.clear_line_edit(line_edit)
