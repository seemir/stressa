# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Money

from .model import Model


class SifoModel(Model):

    def __init__(self, parent, error):
        super(SifoModel, self).__init__(parent, error)

    def sifo_info(self):
        self.parent.ui.line_edit_brutto_arsinntekt.setText(self.calculate_yearly_income(
            self.parent.parent.ui.line_edit_brutto_inntekt.text()))
        self.parent.ui.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_arsinntekt", Money, "value"))
        self.parent.exec_()

    @staticmethod
    def calculate_yearly_income(monthly_income):
        return Money(monthly_income) * Money("12") if monthly_income else ""
