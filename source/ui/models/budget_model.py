# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Money

from .model import Model


class BudgetModel(Model):

    def __init__(self, parent, error):
        super(BudgetModel, self).__init__(parent, error)
        self._parent = parent
        self._error = error
        self._data = {"brutto_inntekt": "", "trygde_inntekt": "", "leieinntekt": "",
                      "total_skatt": "", "total_netto": "", "netto_likviditet": "",
                      "student_lan": "", "kreditt_gjeld": "", "strom": "",
                      "andre_utgifter": ""}

    @property
    def data(self):
        return self._data

    def budget_info(self):
        self._parent.ui.line_edit_brutto_inntekt.editingFinished.connect(
            lambda: self.set_content("brutto_inntekt", Money, "value"))
        self._parent.ui.line_edit_trygde_inntekt.editingFinished.connect(
            lambda: self.set_content("trygde_inntekt", Money, "value"))
        self._parent.ui.line_edit_leieinntekt.editingFinished.connect(
            lambda: self.set_content("leieinntekt", Money, "value"))
        self._parent.ui.line_edit_total_skatt.editingFinished.connect(
            lambda: self.set_content("total_skatt", Money, "value"))
        self._parent.ui.line_edit_total_netto.editingFinished.connect(
            lambda: self.set_content("total_netto", Money, "value"))
        self._parent.ui.line_edit_netto_likviditet.editingFinished.connect(
            lambda: self.set_content("netto_likviditet", Money, "value"))
        self._parent.ui.line_edit_student_lan.editingFinished.connect(
            lambda: self.set_content("student_lan", Money, "value"))
        self._parent.ui.line_edit_kreditt_gjeld.editingFinished.connect(
            lambda: self.set_content("kreditt_gjeld", Money, "value"))
        self._parent.ui.line_edit_strom.editingFinished.connect(
            lambda: self.set_content("strom", Money, "value"))
        self._parent.ui.line_edit_andre_utgifter.editingFinished.connect(
            lambda: self.set_content("andre_utgifter", Money, "value"))
        self._parent.ui.line_edit_sifo_utgifter.editingFinished.connect(
            lambda: self.set_content("sifo_utgifter", Money, "value"))
        self._parent.ui.line_edit_totale_utgifter.editingFinished.connect(
            lambda: self.set_content("totale_utgifter", Money, "value"))
        self._parent.ui.line_edit_likviditetsgrad.editingFinished.connect(
            lambda: self.set_content("likviditetsgrad", Money, "value"))
