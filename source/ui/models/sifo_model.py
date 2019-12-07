# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from source.domain import Money

from .model import Model


class SifoModel(Model):
    _kjonn = ["", "Mann", "Kvinne"]
    _alder = ["", "0-5 mnd", "6-11 mnd", "1", "2", "3", "4-5",
              "6-9", "10-13", "14-17", "18-19", "20-50", "51-60",
              "61-66", "eldre enn 66"]
    _antall_biler = ["", "0", "1", "2", "3", "4"]

    def __init__(self, parent, error):
        super(SifoModel, self).__init__(parent, error)

        for combo_box in range(1, 8):
            getattr(self.parent.ui, "combobox_kjonn_person_" + str(combo_box)).addItems(self._kjonn)
            getattr(self.parent.ui, "combobox_alder_person_" + str(combo_box)).addItems(self._alder)
        self.parent.ui.combobox_antall_biler.addItems(self._antall_biler)

    def sifo_info(self):
        self.parent.ui.line_edit_brutto_arsinntekt.setText(self.calculate_yearly_income(
            self.parent.parent.ui.line_edit_brutto_inntekt.text()))
        self.parent.ui.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_arsinntekt", Money, "value"))
        self.parent.ui.pushbutton_tom_skjema.clicked.connect(self.clear_content)
        self.parent.exec_()

    def calculate_yearly_income(self, monthly_income):
        yearly_income = self.parent.ui.line_edit_brutto_arsinntekt.text()
        if monthly_income and not yearly_income:
            yearly_income_from_monthly = Money(
                str(Decimal(monthly_income.replace(" kr", "").replace(" ", "")) * 12))
            return yearly_income_from_monthly.value()
        else:
            return yearly_income

    def clear_content(self):
        for combo_box in range(1, 8):
            getattr(self.parent.ui, "combobox_kjonn_person_" + str(combo_box)).setCurrentIndex(0)
            getattr(self.parent.ui, "combobox_alder_person_" + str(combo_box)).setCurrentIndex(0)
        self.parent.ui.line_edit_brutto_arsinntekt.clear()
        self.parent.ui.combobox_antall_biler.setCurrentIndex(0)
