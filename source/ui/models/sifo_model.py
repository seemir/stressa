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
    _sifo_expenses = ['mat', 'klar', 'helse', 'fritid', 'kollektivt', 'spedbarn', 'sumindivid',
                      'dagligvarer', 'husholdsart', 'mobler', 'medier', 'biler', 'barnehage',
                      'sfo', 'sumhusholdning', 'totalt']

    def __init__(self, parent):
        super(SifoModel, self).__init__(parent)
        for num in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(num)).addItems(
                self._kjonn)
            getattr(self.parent.ui, "combo_box_alder_" + str(num)).addItems(
                self._alder)
        self.parent.ui.combo_box_antall_biler.addItems(self._antall_biler)
        self._sifo_workflow = None

    @property
    def sifo_workflow(self):
        return self._sifo_workflow

    @sifo_workflow.setter
    def sifo_workflow(self, new_sifo_workflow):
        self._sifo_workflow = new_sifo_workflow

    def sifo_info(self):
        self.set_yearly_income()
        self.set_age()
        self.set_gender()
        self.set_cars()
        self.parent.ui.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_arsinntekt", Money, "value"))
        self.parent.ui.push_button_vis_resultatet.clicked.connect(self.calculate_sifo_expenses)
        self.parent.ui.push_button_tom_skjema_1.clicked.connect(self.clear_all)
        self.parent.ui.push_button_cancel_1.clicked.connect(self.cancel)

        self.parent.ui.push_button_tom_skjema_2.clicked.connect(self.clear_all)
        self.parent.ui.push_button_cancel_2.clicked.connect(self.cancel)
        self.parent.ui.push_button_back.clicked.connect(self.back)

    def set_age(self):
        self.parent.ui.combo_box_alder_1.activated.connect(
            lambda: self.set_combo_box("alder_1", "person_1"))
        self.parent.ui.combo_box_alder_2.activated.connect(
            lambda: self.set_combo_box("alder_2", "person_2"))
        self.parent.ui.combo_box_alder_3.activated.connect(
            lambda: self.set_combo_box("alder_3", "person_3"))
        self.parent.ui.combo_box_alder_4.activated.connect(
            lambda: self.set_combo_box("alder_4", "person_4"))
        self.parent.ui.combo_box_alder_5.activated.connect(
            lambda: self.set_combo_box("alder_5", "person_5"))
        self.parent.ui.combo_box_alder_6.activated.connect(
            lambda: self.set_combo_box("alder_6", "person_6"))
        self.parent.ui.combo_box_alder_7.activated.connect(
            lambda: self.set_combo_box("alder_7", "person_7"))

    def set_gender(self):
        self.parent.ui.combo_box_kjonn_1.activated.connect(
            lambda: self.set_combo_box("kjonn_1", "person_1"))
        self.parent.ui.combo_box_kjonn_2.activated.connect(
            lambda: self.set_combo_box("kjonn_2", "person_2"))
        self.parent.ui.combo_box_kjonn_3.activated.connect(
            lambda: self.set_combo_box("kjonn_3", "person_3"))
        self.parent.ui.combo_box_kjonn_4.activated.connect(
            lambda: self.set_combo_box("kjonn_4", "person_4"))
        self.parent.ui.combo_box_kjonn_5.activated.connect(
            lambda: self.set_combo_box("kjonn_5", "person_5"))
        self.parent.ui.combo_box_kjonn_6.activated.connect(
            lambda: self.set_combo_box("kjonn_6", "person_6"))
        self.parent.ui.combo_box_kjonn_7.activated.connect(
            lambda: self.set_combo_box("kjonn_7", "person_7"))

    def set_cars(self):
        self.parent.ui.combo_box_antall_biler.activated.connect(
            lambda: self.set_combo_box("antall_biler"))

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
            self.parent.ui.tabwidget_sifo.setCurrentIndex(1)
            self.sifo_workflow = SifoWorkFlow(self.data)
            self.set_line_edits(line_edit_text="", line_edits=self._sifo_expenses, postfix="_1",
                                data=self.sifo_workflow.expenses_value)
            self.set_line_edits(line_edit_text="", line_edits=self._sifo_expenses, postfix="_2",
                                data=self.sifo_workflow.expenses_share)
        except Exception as sifo_expenses_error:
            self.clear_results()
            self.parent.error.show_error(sifo_expenses_error, self.data)
            self.parent.error.exec_()

    def show(self):
        self.parent.ui.tabwidget_sifo.setCurrentIndex(0)
        self.parent.ui.combo_box_kjonn_1.setFocus()
        self.sifo_info()
        self.parent.ui.show()

    def clear_results(self):
        self.clear_line_edits(self._sifo_expenses, "1")
        self.clear_line_edits(self._sifo_expenses, "2")
        self.parent.ui.tabwidget_sifo.setCurrentIndex(0)

    def clear_all(self):
        self.parent.ui.combo_box_kjonn_1.setFocus()
        for combo_box in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(combo_box)).setCurrentIndex(0)
            getattr(self.parent.ui, "combo_box_alder_" + str(combo_box)).setCurrentIndex(0)
        self.parent.ui.line_edit_brutto_arsinntekt.clear()
        self.parent.ui.combo_box_antall_biler.setCurrentIndex(0)
        self.clear_results()
        self.data = {}

    def back(self):
        self.parent.ui.tabwidget_sifo.setCurrentIndex(0)

    def cancel(self):
        self.parent.close()
