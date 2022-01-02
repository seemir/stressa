# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from PyQt5.QtCore import QObject

from source.util import Assertor
from source.domain import Money

from .model import Model


class BudgetModel(Model):
    _intervall = {"": "", "Årlig": "1", "Halvårlig": "2", "Kvartalsvis": "4",
                  "Annenhver måned": "6", "Månedlig": "12", "Semi-månedlig": "24",
                  "Annenhver uke": "26", "Ukentlig": "52"}
    _budget_posts = ["brutto_inntekt_1", "trygde_inntekt_1", "leieinntekt_1", "andre_inntekter_1",
                     "personinntekt_1", "student_lan_1", "kreditt_gjeld_1", "husleie_1", "strom_1",
                     "andre_utgifter_1", "sum_utgifter_1"]

    def __init__(self, parent: QObject):
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])
        for num in range(1, 19):
            getattr(self.parent.ui, "combo_box_interval_" + str(num)).addItems(
                self._intervall.keys())

    @property
    def budget_posts(self):
        return self._budget_posts

    def budget_info(self):
        self.parent.ui.combo_box_interval_1.setFocus()
        self.parent.ui.combo_box_interval_1.activated.connect(
            lambda: self.set_combo_box_value("brutto_inntekt", "_1"))
        self.parent.ui.line_edit_brutto_inntekt_1.textEdited.connect(
            lambda: self.set_value("brutto_inntekt", "_1"))
        self.parent.ui.combo_box_interval_2.activated.connect(
            lambda: self.set_combo_box_value("trygde_inntekt", "_1"))
        self.parent.ui.line_edit_trygde_inntekt_1.textEdited.connect(
            lambda: self.set_value("trygde_inntekt", "_1"))
        self.parent.ui.combo_box_interval_3.activated.connect(
            lambda: self.set_combo_box_value("leieinntekt", "_1"))
        self.parent.ui.line_edit_leieinntekt_1.textEdited.connect(
            lambda: self.set_value("leieinntekt", "_1"))
        self.parent.ui.combo_box_interval_4.activated.connect(
            lambda: self.set_combo_box_value("andre_inntekter", "_1"))
        self.parent.ui.line_edit_andre_inntekter_1.textEdited.connect(
            lambda: self.set_value("andre_inntekter", "_1"))

        self.parent.ui.combo_box_interval_5.activated.connect(
            lambda: self.set_combo_box_value("student_lan", "_1"))
        self.parent.ui.line_edit_student_lan_1.textEdited.connect(
            lambda: self.set_value("student_lan", "_1"))
        self.parent.ui.combo_box_interval_6.activated.connect(
            lambda: self.set_combo_box_value("kreditt_gjeld", "_1"))
        self.parent.ui.line_edit_kreditt_gjeld_1.textEdited.connect(
            lambda: self.set_value("kreditt_gjeld", "_1"))
        self.parent.ui.combo_box_interval_7.activated.connect(
            lambda: self.set_combo_box_value("husleie", "_1"))
        self.parent.ui.line_edit_husleie_1.textEdited.connect(
            lambda: self.set_value("husleie", "_1"))
        self.parent.ui.combo_box_interval_8.activated.connect(
            lambda: self.set_combo_box_value("strom", "_8"))
        self.parent.ui.line_edit_strom_1.textEdited.connect(
            lambda: self.set_value("strom", "_1"))
        self.parent.ui.combo_box_interval_9.activated.connect(
            lambda: self.set_combo_box_value("andre_utgifter", "_1"))
        self.parent.ui.line_edit_andre_utgifter_1.textEdited.connect(
            lambda: self.set_value("andre_utgifter", "_1"))

    def set_value(self, line_edit, postfix):
        if getattr(self.parent.ui, "line_edit_" + line_edit + postfix).text():
            self.set_line_edit(line_edit + postfix, Money, "value")
        else:
            self.clear_line_edit(line_edit + postfix)
            getattr(self.parent.ui, "combo_box_interval" + postfix).setCurrentIndex(0)
        self.monthly_value()

    def set_combo_box_value(self, line_edit, postfix):
        if getattr(self.parent.ui, "combo_box_interval" + postfix).currentText():
            pass
        else:
            self.clear_line_edit(line_edit)
        self.monthly_value()

    def monthly_value(self):
        parent = self.parent.ui
        brutto_income = self.calculate_monthly_values(
            "brutto_inntekt_1", parent.line_edit_brutto_inntekt_1.text(),
            self._intervall[parent.combo_box_interval_1.currentText()])
        trygd_income = self.calculate_monthly_values(
            "trygde_inntekt_1", parent.line_edit_trygde_inntekt_1.text(),
            self._intervall[parent.combo_box_interval_2.currentText()])
        leie_income = self.calculate_monthly_values(
            "leieinntekt_1", parent.line_edit_leieinntekt_1.text(),
            self._intervall[parent.combo_box_interval_3.currentText()])
        other_income = self.calculate_monthly_values(
            "andre_inntekter_1", parent.line_edit_andre_inntekter_1.text(),
            self._intervall[parent.combo_box_interval_4.currentText()])

        sum_income = brutto_income + trygd_income + leie_income + other_income
        person_income = Money(str(sum_income)).value() if sum_income != 0 else ""
        parent.line_edit_personinntekt_1.setText(person_income)
        self.set_line_edit("personinntekt_1", data=person_income)

        student_loan = self.calculate_monthly_values(
            "student_lan_1", parent.line_edit_student_lan_1.text(),
            self._intervall[parent.combo_box_interval_5.currentText()])
        credit_debt = self.calculate_monthly_values(
            "kreditt_gjeld_1", parent.line_edit_kreditt_gjeld_1.text(),
            self._intervall[parent.combo_box_interval_6.currentText()])
        housing_rent = self.calculate_monthly_values(
            "husleie_1", parent.line_edit_husleie_1.text(),
            self._intervall[parent.combo_box_interval_7.currentText()])
        power = self.calculate_monthly_values(
            "strom_1", parent.line_edit_strom_1.text(),
            self._intervall[parent.combo_box_interval_8.currentText()])
        other = self.calculate_monthly_values(
            "andre_utgifter_1", parent.line_edit_andre_utgifter_1.text(),
            self._intervall[parent.combo_box_interval_9.currentText()])

        sum_expenses = student_loan + credit_debt + housing_rent + power + other
        person_expenses = Money(str(sum_expenses)).value() if sum_expenses != 0 else ""
        parent.line_edit_sum_utgifter_1.setText(person_expenses)
        self.set_line_edit("sum_utgifter_1", data=person_expenses)

    def calculate_monthly_values(self, line_edit: str, value: str, factor: str):
        Assertor.assert_data_types([value, factor], [str, str])
        if value and factor:
            quantity = Decimal(value.replace(" ", "").replace("kr", "")) * Decimal(
                factor.replace(" ", "").replace("kr", ""))
            divisor = Decimal("12")
            monthly_values = round(Decimal(quantity / divisor))
            self.data.update({line_edit: Money(str(monthly_values)).value()})
        elif value:
            monthly_values = round(Decimal(value.replace(" ", "").replace("kr", "")))
        else:
            monthly_values = round(Decimal("0"))
        return monthly_values
