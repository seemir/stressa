# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Money

from .model import Model


class BudgetModel(Model):

    def __init__(self, parent):
        super(BudgetModel, self).__init__(parent)

    def budget_info(self):
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
