# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from source.app import SifoWorkFlow
from source.domain import Money

from .model import Model


class SifoModel(Model):
    _kjonn = ["", "Mann", "Kvinne"]
    _alder = ["", "0-5 mnd", "6-11 mnd", "1", "2", "3", "4-5",
              "6-9", "10-13", "14-17", "18-19", "20-50", "51-60",
              "61-66", "eldre enn 66"]
    _antall_biler = ["", "1", "2", "3", "4"]

    def __init__(self, parent, error):
        super(SifoModel, self).__init__(parent, error)
        for num in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(num)).addItems(
                self._kjonn)
            getattr(self.parent.ui, "combo_box_alder_" + str(num)).addItems(
                self._alder)
        self.parent.ui.combo_box_antall_biler.addItems(self._antall_biler)
        self.sifo_info()

    def sifo_info(self):
        self.set_gender()
        self.set_age()
        self.set_cars()
        self.parent.ui.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_arsinntekt", Money, "value"))
        self.parent.ui.push_button_vis_resultatet.clicked.connect(self.calculate_sifo_expenses)
        self.parent.ui.push_button_tom_skjema.clicked.connect(self.clear_content)

    def set_cars(self):
        self.parent.ui.combo_box_antall_biler.activated.connect(
            lambda: self.set_combo_box("antall_biler"))

    def set_gender(self):
        self.parent.ui.combo_box_kjonn_1.activated.connect(
            lambda: self.set_buddy_combo_box("kjonn_1", "person_1"))
        self.parent.ui.combo_box_kjonn_2.activated.connect(
            lambda: self.set_buddy_combo_box("kjonn_2", "person_2"))
        self.parent.ui.combo_box_kjonn_3.activated.connect(
            lambda: self.set_buddy_combo_box("kjonn_3", "person_3"))
        self.parent.ui.combo_box_kjonn_4.activated.connect(
            lambda: self.set_buddy_combo_box("kjonn_4", "person_4"))
        self.parent.ui.combo_box_kjonn_5.activated.connect(
            lambda: self.set_buddy_combo_box("kjonn_5", "person_5"))
        self.parent.ui.combo_box_kjonn_6.activated.connect(
            lambda: self.set_buddy_combo_box("kjonn_6", "person_6"))
        self.parent.ui.combo_box_kjonn_7.activated.connect(
            lambda: self.set_buddy_combo_box("kjonn_7", "person_7"))

    def set_age(self):
        self.parent.ui.combo_box_alder_1.activated.connect(
            lambda: self.set_buddy_combo_box("alder_1", "person_1"))
        self.parent.ui.combo_box_alder_2.activated.connect(
            lambda: self.set_buddy_combo_box("alder_2", "person_2"))
        self.parent.ui.combo_box_alder_3.activated.connect(
            lambda: self.set_buddy_combo_box("alder_3", "person_3"))
        self.parent.ui.combo_box_alder_4.activated.connect(
            lambda: self.set_buddy_combo_box("alder_4", "person_4"))
        self.parent.ui.combo_box_alder_5.activated.connect(
            lambda: self.set_buddy_combo_box("alder_5", "person_5"))
        self.parent.ui.combo_box_alder_6.activated.connect(
            lambda: self.set_buddy_combo_box("alder_6", "person_6"))
        self.parent.ui.combo_box_alder_7.activated.connect(
            lambda: self.set_buddy_combo_box("alder_7", "person_7"))

    def set_yearly_income(self):
        self.parent.ui.line_edit_brutto_arsinntekt.setText(self.calculate_yearly_income(
            self.parent.parent.ui.line_edit_brutto_inntekt.text()))

    def calculate_yearly_income(self, monthly_income):
        yearly_income = self.parent.ui.line_edit_brutto_arsinntekt.text()
        if monthly_income and not yearly_income:
            yearly_income_from_monthly = Money(
                str(Decimal(monthly_income.replace(" kr", "").replace(" ", "")) * 12))
            self.data.update({"brutto_arsinntekt": yearly_income_from_monthly.value()})
            return yearly_income_from_monthly.value()
        else:
            return yearly_income

    def calculate_sifo_expenses(self):
        try:
            sifo_workflow = SifoWorkFlow(self.data)
            print(sifo_workflow.get_base_sifo_expenses())
        except Exception as sifo_expenses_error:
            self.error.show_error(sifo_expenses_error)
            self.error.exec_()

    def clear_content(self):
        for combo_box in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(combo_box)).setCurrentIndex(0)
            getattr(self.parent.ui, "combo_box_alder_" + str(combo_box)).setCurrentIndex(0)
        self.parent.ui.line_edit_brutto_arsinntekt.clear()
        self.parent.ui.combo_box_antall_biler.setCurrentIndex(0)
        self.data = {}

    def show_sifo_calculator(self):
        self.set_yearly_income()
        self.parent.ui.combo_box_kjonn_1.setFocus()
        self.parent.exec_()
