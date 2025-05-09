# -*- coding: utf-8 -*-
"""
Module containing model with budget logic and calculation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from PyQt5.QtCore import QObject  # pylint: disable=no-name-in-module

from source.util import Assertor
from source.domain import Money

from .model import Model


class BudgetModel(Model):
    """
    Model implementation of all budget logic

    """

    _interval = {"": "", "Årlig": "1", "Halvårlig": "2", "Kvartalsvis": "4", "Annenhver måned": "6",
                 "Månedlig": "12", "Semi-månedlig": "24", "Annenhver uke": "26", "Ukentlig": "52"}

    _primary_posts = ["brutto_inntekt_1", "trygde_inntekt_1", "leieinntekt_1", "renteinntekter_1",
                      "andre_inntekter_1", "personinntekt_1", "student_lan_1", "kreditt_gjeld_1",
                      "husleie_1", "strom_1", "rentekostnader_1", "andre_utgifter_1",
                      "variable_utgifter_1"]

    _secondary_posts = ["brutto_inntekt_2", "trygde_inntekt_2", "leieinntekt_2", "renteinntekter_2",
                        "andre_inntekter_2", "personinntekt_2", "student_lan_2", "kreditt_gjeld_2",
                        "husleie_2", "strom_2", "rentekostnader_2", "andre_utgifter_2",
                        "variable_utgifter_2"]

    _total_posts = ["brutto_inntekt_total", "trygde_inntekt_total", "leieinntekt_total",
                    "renteinntekter_total", "andre_inntekter_total", "personinntekt_total",
                    "student_lan_total", "kreditt_gjeld_total", "husleie_total",
                    "strom_total", "rentekostnader_total", "andre_utgifter_total",
                    "variable_utgifter_total"]

    def __init__(self, parent: QObject):
        """
        Constructor / instantiating class

        Parameters
        ----------
        parent      : QObject
                      parent object of model

        """
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])
        for num in range(1, 23):
            getattr(self.parent.ui_form,
                    "combo_box_interval_" + str(num)).addItems(
                self.interval.keys())

    @property
    def interval(self):
        """
        interval getter

        """
        return self._interval

    @property
    def primary_posts(self):
        """
        primary_posts getter

        """
        return self._primary_posts

    @property
    def secondary_posts(self):
        """
        secondary_posts getter

        """
        return self._secondary_posts

    @property
    def total_posts(self):
        """
        total_posts getter

        """
        return self._total_posts

    def budget_info(self):
        """
        method for setting all info in budget model

        """
        self.parent.ui_form.combo_box_interval_1.setFocus()
        self.parent.ui_form.combo_box_interval_1.activated.connect(
            lambda: self.set_combo_box_value("brutto_inntekt", "_1", "_1"))
        self.parent.ui_form.line_edit_brutto_inntekt_1.textEdited.connect(
            lambda: self.set_value("brutto_inntekt", "_1", "_1"))
        self.parent.ui_form.combo_box_interval_2.activated.connect(
            lambda: self.set_combo_box_value("trygde_inntekt", "_1", "_2"))
        self.parent.ui_form.line_edit_trygde_inntekt_1.textEdited.connect(
            lambda: self.set_value("trygde_inntekt", "_1", "_2"))
        self.parent.ui_form.combo_box_interval_3.activated.connect(
            lambda: self.set_combo_box_value("leieinntekt", "_1", "_3"))
        self.parent.ui_form.line_edit_leieinntekt_1.textEdited.connect(
            lambda: self.set_value("leieinntekt", "_1", "_3"))
        self.parent.ui_form.combo_box_interval_4.activated.connect(
            lambda: self.set_combo_box_value("renteinntekter", "_1", "_4"))
        self.parent.ui_form.line_edit_renteinntekter_1.textEdited.connect(
            lambda: self.set_value("renteinntekter", "_1", "_4"))
        self.parent.ui_form.combo_box_interval_5.activated.connect(
            lambda: self.set_combo_box_value("andre_inntekter", "_1", "_5"))
        self.parent.ui_form.line_edit_andre_inntekter_1.textEdited.connect(
            lambda: self.set_value("andre_inntekter", "_1", "_5"))

        self.parent.ui_form.combo_box_interval_6.activated.connect(
            lambda: self.set_combo_box_value("student_lan", "_1", "_6"))
        self.parent.ui_form.line_edit_student_lan_1.textEdited.connect(
            lambda: self.set_value("student_lan", "_1", "_6"))
        self.parent.ui_form.combo_box_interval_7.activated.connect(
            lambda: self.set_combo_box_value("kreditt_gjeld", "_1", "_7"))
        self.parent.ui_form.line_edit_kreditt_gjeld_1.textEdited.connect(
            lambda: self.set_value("kreditt_gjeld", "_1", "_7"))
        self.parent.ui_form.combo_box_interval_8.activated.connect(
            lambda: self.set_combo_box_value("husleie", "_1", "_8"))
        self.parent.ui_form.line_edit_husleie_1.textEdited.connect(
            lambda: self.set_value("husleie", "_1", "_8"))
        self.parent.ui_form.combo_box_interval_9.activated.connect(
            lambda: self.set_combo_box_value("strom", "_1", "_9"))
        self.parent.ui_form.line_edit_strom_1.textEdited.connect(
            lambda: self.set_value("strom", "_1", "_9"))
        self.parent.ui_form.combo_box_interval_10.activated.connect(
            lambda: self.set_combo_box_value("rentekostnader", "_1", "_10"))
        self.parent.ui_form.line_edit_rentekostnader_1.textEdited.connect(
            lambda: self.set_value("rentekostnader", "_1", "_10"))
        self.parent.ui_form.combo_box_interval_11.activated.connect(
            lambda: self.set_combo_box_value("andre_utgifter", "_1", "_11"))
        self.parent.ui_form.line_edit_andre_utgifter_1.textEdited.connect(
            lambda: self.set_value("andre_utgifter", "_1", "_11"))

        self.parent.ui_form.combo_box_interval_12.activated.connect(
            lambda: self.set_combo_box_value("brutto_inntekt", "_2", "_12"))
        self.parent.ui_form.line_edit_brutto_inntekt_2.textEdited.connect(
            lambda: self.set_value("brutto_inntekt", "_2", "_12"))
        self.parent.ui_form.combo_box_interval_13.activated.connect(
            lambda: self.set_combo_box_value("trygde_inntekt", "_2", "_13"))
        self.parent.ui_form.line_edit_trygde_inntekt_2.textEdited.connect(
            lambda: self.set_value("trygde_inntekt", "_2", "_13"))
        self.parent.ui_form.combo_box_interval_14.activated.connect(
            lambda: self.set_combo_box_value("leieinntekt", "_2", "_14"))
        self.parent.ui_form.line_edit_leieinntekt_2.textEdited.connect(
            lambda: self.set_value("leieinntekt", "_2", "_14"))
        self.parent.ui_form.combo_box_interval_15.activated.connect(
            lambda: self.set_combo_box_value("renteinntekter", "_2", "_15"))
        self.parent.ui_form.line_edit_renteinntekter_2.textEdited.connect(
            lambda: self.set_value("renteinntekter", "_2", "_15"))
        self.parent.ui_form.combo_box_interval_16.activated.connect(
            lambda: self.set_combo_box_value("andre_inntekter", "_2", "_16"))
        self.parent.ui_form.line_edit_andre_inntekter_2.textEdited.connect(
            lambda: self.set_value("andre_inntekter", "_2", "_16"))

        self.parent.ui_form.combo_box_interval_17.activated.connect(
            lambda: self.set_combo_box_value("student_lan", "_2", "_17"))
        self.parent.ui_form.line_edit_student_lan_2.textEdited.connect(
            lambda: self.set_value("student_lan", "_2", "_17"))
        self.parent.ui_form.combo_box_interval_18.activated.connect(
            lambda: self.set_combo_box_value("kreditt_gjeld", "_2", "_18"))
        self.parent.ui_form.line_edit_kreditt_gjeld_2.textEdited.connect(
            lambda: self.set_value("kreditt_gjeld", "_2", "_18"))
        self.parent.ui_form.combo_box_interval_19.activated.connect(
            lambda: self.set_combo_box_value("husleie", "_2", "_19"))
        self.parent.ui_form.line_edit_husleie_2.textEdited.connect(
            lambda: self.set_value("husleie", "_2", "_19"))
        self.parent.ui_form.combo_box_interval_20.activated.connect(
            lambda: self.set_combo_box_value("strom", "_2", "_20"))
        self.parent.ui_form.line_edit_strom_2.textEdited.connect(
            lambda: self.set_value("strom", "_2", "_20"))
        self.parent.ui_form.combo_box_interval_21.activated.connect(
            lambda: self.set_combo_box_value("rentekostnader", "_2", "_21"))
        self.parent.ui_form.line_edit_rentekostnader_2.textEdited.connect(
            lambda: self.set_value("rentekostnader", "_2", "_21"))
        self.parent.ui_form.combo_box_interval_22.activated.connect(
            lambda: self.set_combo_box_value("andre_utgifter", "_2", "_22"))
        self.parent.ui_form.line_edit_andre_utgifter_2.textEdited.connect(
            lambda: self.set_value("andre_utgifter", "_2", "_22"))

        self.parent.ui_form.radio_button_skattefrie_inntekt_1.toggled.connect(
            lambda: self.set_radio_button("skattefrie_inntekt_1"))
        self.parent.ui_form.radio_button_skattefrie_inntekt_2.toggled.connect(
            lambda: self.set_radio_button("skattefrie_inntekt_2"))

    def set_value(self, line_edit, postfix, combofix):
        """
        method for setting value in model

        """
        if getattr(self.parent.ui_form,
                   "line_edit_" + line_edit + postfix).text():
            self.set_line_edit(line_edit + postfix, Money, "value")
        else:
            self.clear_line_edit(line_edit + postfix)
            getattr(self.parent.ui_form,
                    "combo_box_interval" + combofix).setCurrentIndex(0)
        self.monthly_value()
        self.yearly_value()

    def set_combo_box_value(self, line_edit, postfix, combofix):
        """
        method for setting value in combo_box

        """
        if getattr(self.parent.ui_form,
                   "combo_box_interval" + combofix).currentText():
            pass
        else:
            self.clear_line_edit(line_edit + postfix)
        self.monthly_value()
        self.yearly_value()

    def monthly_value(self):
        """
        method for calculating monthly values

        """
        parent = self.parent.ui_form
        brutto_income_1 = self.calculate_monthly_values(
            "brutto_inntekt_1", parent.line_edit_brutto_inntekt_1.text(),
            self._interval[parent.combo_box_interval_1.currentText()])
        trygd_income_1 = self.calculate_monthly_values(
            "trygde_inntekt_1", parent.line_edit_trygde_inntekt_1.text(),
            self._interval[parent.combo_box_interval_2.currentText()])
        if "skattefrie_inntekt_1" in self.data:
            leie_income_1 = self.calculate_monthly_values(
                "leieinntekt_1", "0 kr",
                self._interval[parent.combo_box_interval_3.currentText()])
        else:
            leie_income_1 = self.calculate_monthly_values(
                "leieinntekt_1", parent.line_edit_leieinntekt_1.text(),
                self._interval[parent.combo_box_interval_3.currentText()])

        interest_income_1 = self.calculate_monthly_values(
            "renteinntekter_1", parent.line_edit_renteinntekter_1.text(),
            self._interval[parent.combo_box_interval_4.currentText()])
        other_income_1 = self.calculate_monthly_values(
            "andre_inntekter_1", parent.line_edit_andre_inntekter_1.text(),
            self._interval[parent.combo_box_interval_5.currentText()])

        sum_income_1 = sum(
            [brutto_income_1, trygd_income_1, leie_income_1, interest_income_1,
             other_income_1])
        person_income_1 = Money(
            str(sum_income_1)).value() if sum_income_1 != 0 else ""
        parent.line_edit_personinntekt_1.setText(person_income_1)
        self.set_line_edit("personinntekt_1", data=person_income_1)

        brutto_income_2 = self.calculate_monthly_values(
            "brutto_inntekt_2", parent.line_edit_brutto_inntekt_2.text(),
            self._interval[parent.combo_box_interval_12.currentText()])
        trygd_income_2 = self.calculate_monthly_values(
            "trygde_inntekt_2", parent.line_edit_trygde_inntekt_2.text(),
            self._interval[parent.combo_box_interval_13.currentText()])
        if "skattefrie_inntekt_2" in self.data:
            leie_income_2 = self.calculate_monthly_values(
                "leieinntekt_2", "0 kr",
                self._interval[parent.combo_box_interval_14.currentText()])
        else:
            leie_income_2 = self.calculate_monthly_values(
                "leieinntekt_2", parent.line_edit_leieinntekt_2.text(),
                self._interval[parent.combo_box_interval_14.currentText()])

        interest_income_2 = self.calculate_monthly_values(
            "renteinntekter_2", parent.line_edit_renteinntekter_2.text(),
            self._interval[parent.combo_box_interval_15.currentText()])
        other_income_2 = self.calculate_monthly_values(
            "andre_inntekter_2", parent.line_edit_andre_inntekter_2.text(),
            self._interval[parent.combo_box_interval_16.currentText()])

        sum_income_2 = sum(
            [brutto_income_2, trygd_income_2, leie_income_2, interest_income_2,
             other_income_2])
        person_income_2 = Money(
            str(sum_income_2)).value() if sum_income_2 != 0 else ""
        parent.line_edit_personinntekt_2.setText(person_income_2)
        self.set_line_edit("personinntekt_2", data=person_income_2)

        student_loan_1 = self.calculate_monthly_values(
            "student_lan_1", parent.line_edit_student_lan_1.text(),
            self._interval[parent.combo_box_interval_6.currentText()])
        credit_debt_1 = self.calculate_monthly_values(
            "kreditt_gjeld_1", parent.line_edit_kreditt_gjeld_1.text(),
            self._interval[parent.combo_box_interval_7.currentText()])
        housing_rent_1 = self.calculate_monthly_values(
            "husleie_1", parent.line_edit_husleie_1.text(),
            self._interval[parent.combo_box_interval_8.currentText()])
        power_1 = self.calculate_monthly_values(
            "strom_1", parent.line_edit_strom_1.text(),
            self._interval[parent.combo_box_interval_9.currentText()])
        interest_cost_1 = self.calculate_monthly_values(
            "rentekostnader_1", parent.line_edit_rentekostnader_1.text(),
            self._interval[parent.combo_box_interval_10.currentText()])
        other_1 = self.calculate_monthly_values(
            "andre_utgifter_1", parent.line_edit_andre_utgifter_1.text(),
            self._interval[parent.combo_box_interval_11.currentText()])

        sum_expenses_1 = sum(
            [student_loan_1, credit_debt_1, housing_rent_1, power_1,
             interest_cost_1, other_1])
        person_expenses_1 = Money(
            str(sum_expenses_1)).value() if sum_expenses_1 != 0 else ""
        parent.line_edit_variable_utgifter_1.setText(person_expenses_1)
        self.set_line_edit("variable_utgifter_1", data=person_expenses_1)

        student_loan_2 = self.calculate_monthly_values(
            "student_lan_2", parent.line_edit_student_lan_2.text(),
            self._interval[parent.combo_box_interval_17.currentText()])
        credit_debt_2 = self.calculate_monthly_values(
            "kreditt_gjeld_2", parent.line_edit_kreditt_gjeld_2.text(),
            self._interval[parent.combo_box_interval_18.currentText()])
        housing_rent_2 = self.calculate_monthly_values(
            "husleie_2", parent.line_edit_husleie_2.text(),
            self._interval[parent.combo_box_interval_19.currentText()])
        power_2 = self.calculate_monthly_values(
            "strom_2", parent.line_edit_strom_2.text(),
            self._interval[parent.combo_box_interval_20.currentText()])
        interest_cost_2 = self.calculate_monthly_values(
            "rentekostnader_2", parent.line_edit_rentekostnader_2.text(),
            self._interval[parent.combo_box_interval_21.currentText()])
        other_2 = self.calculate_monthly_values(
            "andre_utgifter_2", parent.line_edit_andre_utgifter_2.text(),
            self._interval[parent.combo_box_interval_22.currentText()])

        sum_expenses_2 = sum(
            [student_loan_2, credit_debt_2, housing_rent_2, power_2,
             interest_cost_2, other_2])
        person_expenses_2 = Money(
            str(sum_expenses_2)).value() if sum_expenses_2 != 0 else ""
        parent.line_edit_variable_utgifter_2.setText(person_expenses_2)
        self.set_line_edit("variable_utgifter_2", data=person_expenses_2)

        self.set_total_value(brutto_income_1, brutto_income_2,
                             "brutto_inntekt_1",
                             "brutto_inntekt_2", "brutto_inntekt_total")
        self.set_total_value(trygd_income_1, trygd_income_2, "trygde_inntekt_1",
                             "trygde_inntekt_2", "trygde_inntekt_total")
        self.set_total_value(leie_income_1, leie_income_2, "leieinntekt_1",
                             "leieinntekt_2", "leieinntekt_total")
        self.set_total_value(interest_income_1, interest_income_2,
                             "renteinntekter_1",
                             "renteinntekter_2", "renteinntekter_total")
        self.set_total_value(other_income_1, other_income_2,
                             "andre_inntekter_1",
                             "andre_inntekter_2", "andre_inntekter_total")
        self.set_total_value(person_income_1, person_income_2,
                             "personinntekt_1",
                             "personinntekt_2", "personinntekt_total")

        self.set_total_value(student_loan_1, student_loan_2, "student_lan_1",
                             "student_lan_2",
                             "student_lan_total")
        self.set_total_value(credit_debt_1, credit_debt_2, "kreditt_gjeld_1",
                             "kreditt_gjeld_2",
                             "kreditt_gjeld_total")
        self.set_total_value(housing_rent_1, housing_rent_2, "husleie_1",
                             "husleie_2",
                             "husleie_total")
        self.set_total_value(power_1, power_2, "strom_1", "strom_2",
                             "strom_total")
        self.set_total_value(interest_cost_1, interest_cost_2,
                             "rentekostnader_1",
                             "rentekostnader_2", "rentekostnader_total")
        self.set_total_value(other_1, other_2, "andre_utgifter_1",
                             "andre_utgifter_2",
                             "andre_utgifter_total")
        self.set_total_value(sum_expenses_1, sum_expenses_2, "variable_utgifter_1",
                             "variable_utgifter_2",
                             "variable_utgifter_total")

    def yearly_value(self):
        """
        method for calculating yearly values

        """
        parent = self.parent.ui_form
        brutto_income_1 = self.calculate_yearly_values(
            "brutto_inntekt_aar_1", parent.line_edit_brutto_inntekt_1.text(),
            self._interval[parent.combo_box_interval_1.currentText()])
        trygd_income_1 = self.calculate_yearly_values(
            "trygde_inntekt_aar_1", parent.line_edit_trygde_inntekt_1.text(),
            self._interval[parent.combo_box_interval_2.currentText()])
        if "skattefrie_inntekt_aar_1" in self.data:
            leie_income_1 = self.calculate_yearly_values(
                "leieinntekt_aar_1", "0 kr",
                self._interval[parent.combo_box_interval_3.currentText()])
        else:
            leie_income_1 = self.calculate_yearly_values(
                "leieinntekt_aar_1", parent.line_edit_leieinntekt_1.text(),
                self._interval[parent.combo_box_interval_3.currentText()])

        interest_income_1 = self.calculate_yearly_values(
            "renteinntekter_aar_1", parent.line_edit_renteinntekter_1.text(),
            self._interval[parent.combo_box_interval_4.currentText()])
        other_income_1 = self.calculate_yearly_values(
            "andre_inntekter_aar_1", parent.line_edit_andre_inntekter_1.text(),
            self._interval[parent.combo_box_interval_5.currentText()])

        sum_income_1 = sum(
            [brutto_income_1, trygd_income_1, leie_income_1, interest_income_1,
             other_income_1])
        person_income_1 = Money(
            str(sum_income_1)).value() if sum_income_1 != 0 else ""
        self.data.update({"personinntekt_aar_1": person_income_1})

        brutto_income_2 = self.calculate_yearly_values(
            "brutto_inntekt_aar_2", parent.line_edit_brutto_inntekt_2.text(),
            self._interval[parent.combo_box_interval_12.currentText()])
        trygd_income_2 = self.calculate_yearly_values(
            "trygde_inntekt_aar_2", parent.line_edit_trygde_inntekt_2.text(),
            self._interval[parent.combo_box_interval_13.currentText()])
        if "skattefrie_inntekt_aar_2" in self.data:
            leie_income_2 = self.calculate_yearly_values(
                "leieinntekt_aar_2", "0 kr",
                self._interval[parent.combo_box_interval_14.currentText()])
        else:
            leie_income_2 = self.calculate_yearly_values(
                "leieinntekt_aar_2", parent.line_edit_leieinntekt_2.text(),
                self._interval[parent.combo_box_interval_14.currentText()])

        interest_income_2 = self.calculate_yearly_values(
            "renteinntekter_aar_2", parent.line_edit_renteinntekter_2.text(),
            self._interval[parent.combo_box_interval_15.currentText()])
        other_income_2 = self.calculate_yearly_values(
            "andre_inntekter_aar_2", parent.line_edit_andre_inntekter_2.text(),
            self._interval[parent.combo_box_interval_16.currentText()])

        sum_income_2 = sum(
            [brutto_income_2, trygd_income_2, leie_income_2, interest_income_2,
             other_income_2])
        person_income_2 = Money(
            str(sum_income_2)).value() if sum_income_2 != 0 else ""
        self.data.update({"personinntekt_aar_2": person_income_2})

        student_loan_1 = self.calculate_yearly_values(
            "student_lan_aar_1", parent.line_edit_student_lan_1.text(),
            self._interval[parent.combo_box_interval_6.currentText()])
        credit_debt_1 = self.calculate_yearly_values(
            "kreditt_gjeld_aar_1", parent.line_edit_kreditt_gjeld_1.text(),
            self._interval[parent.combo_box_interval_7.currentText()])
        housing_rent_1 = self.calculate_yearly_values(
            "husleie_aar_1", parent.line_edit_husleie_1.text(),
            self._interval[parent.combo_box_interval_8.currentText()])
        power_1 = self.calculate_yearly_values(
            "strom_aar_1", parent.line_edit_strom_1.text(),
            self._interval[parent.combo_box_interval_9.currentText()])
        interest_cost_1 = self.calculate_yearly_values(
            "rentekostnader_aar_1", parent.line_edit_rentekostnader_1.text(),
            self._interval[parent.combo_box_interval_10.currentText()])
        other_1 = self.calculate_yearly_values(
            "andre_utgifter_aar_1", parent.line_edit_andre_utgifter_1.text(),
            self._interval[parent.combo_box_interval_11.currentText()])

        sum_expenses_1 = sum(
            [student_loan_1, credit_debt_1, housing_rent_1, power_1,
             interest_cost_1, other_1])
        person_expenses_1 = Money(
            str(sum_expenses_1)).value() if sum_expenses_1 != 0 else ""
        self.data.update({"variable_utgifter_1": person_expenses_1})

        student_loan_2 = self.calculate_yearly_values(
            "student_lan_aar_2", parent.line_edit_student_lan_2.text(),
            self._interval[parent.combo_box_interval_17.currentText()])
        credit_debt_2 = self.calculate_yearly_values(
            "kreditt_gjeld_aar_2", parent.line_edit_kreditt_gjeld_2.text(),
            self._interval[parent.combo_box_interval_18.currentText()])
        housing_rent_2 = self.calculate_yearly_values(
            "husleie_aar_2", parent.line_edit_husleie_2.text(),
            self._interval[parent.combo_box_interval_19.currentText()])
        power_2 = self.calculate_yearly_values(
            "strom_aar_2", parent.line_edit_strom_2.text(),
            self._interval[parent.combo_box_interval_20.currentText()])
        interest_cost_2 = self.calculate_yearly_values(
            "rentekostnader_aar_2", parent.line_edit_rentekostnader_2.text(),
            self._interval[parent.combo_box_interval_21.currentText()])
        other_2 = self.calculate_yearly_values(
            "andre_utgifter_aar_2", parent.line_edit_andre_utgifter_2.text(),
            self._interval[parent.combo_box_interval_22.currentText()])

        sum_expenses_2 = sum(
            [student_loan_2, credit_debt_2, housing_rent_2, power_2,
             interest_cost_2, other_2])
        person_expenses_2 = Money(
            str(sum_expenses_2)).value() if sum_expenses_2 != 0 else ""
        self.data.update({"variable_utgifter_aar_2": person_expenses_2})

        self.set_total_value(brutto_income_1, brutto_income_2,
                             "brutto_inntekt_1",
                             "brutto_inntekt_2", "brutto_inntekt_total_aar")
        self.set_total_value(trygd_income_1, trygd_income_2, "trygde_inntekt_1",
                             "trygde_inntekt_2", "trygde_inntekt_total_aar")
        self.set_total_value(leie_income_1, leie_income_2, "leieinntekt_1",
                             "leieinntekt_2",
                             "leieinntekt_total_aar")
        self.set_total_value(interest_income_1, interest_income_2,
                             "renteinntekter_1",
                             "renteinntekter_2", "renteinntekter_total_aar")
        self.set_total_value(other_income_1, other_income_2,
                             "andre_inntekter_1",
                             "andre_inntekter_2", "andre_inntekter_total_aar")
        self.set_total_value(person_income_1, person_income_2,
                             "personinntekt_1", "personinntekt_2",
                             "personinntekt_total_aar")
        self.set_total_value(student_loan_1, student_loan_2, "student_lan_1",
                             "student_lan_2",
                             "student_lan_total_aar")
        self.set_total_value(credit_debt_1, credit_debt_2, "kreditt_gjeld_1",
                             "kreditt_gjeld_2",
                             "kreditt_gjeld_total_aar")
        self.set_total_value(housing_rent_1, housing_rent_2, "husleie_1",
                             "husleie_2",
                             "husleie_total_aar")
        self.set_total_value(power_1, power_2, "strom_1", "strom_2",
                             "strom_total_aar")
        self.set_total_value(interest_cost_1, interest_cost_2,
                             "rentekostnader_1",
                             "rentekostnader_2", "rentekostnader_total_aar")
        self.set_total_value(other_1, other_2, "andre_utgifter_1",
                             "andre_utgifter_2",
                             "andre_utgifter_total_aar")
        self.set_total_value(sum_expenses_1, sum_expenses_2, "variable_utgifter_1",
                             "variable_utgifter_2",
                             "varibale_utgifter_total_aar")

    def set_radio_button(self, radio_button):
        """
        method for setting value in radio button

        """
        if getattr(self.parent.ui_form,
                   "radio_button_" + radio_button).isChecked():
            self.data.update(
                {radio_button: True})
            self.monthly_value()
            self.yearly_value()
        elif radio_button in self.data:
            del self.data[radio_button]
            self.monthly_value()
            self.yearly_value()

    def set_total_value(self, val_1, val_2, line_edit_1, line_edit_2,
                        total_name):
        """
        method for setting total value

        """
        if getattr(self.parent.ui_form, "line_edit_" + line_edit_1).text() or \
                getattr(self.parent.ui_form, "line_edit_" + line_edit_2).text():
            val_1 = int(
                (str(val_1) if val_1 else "0").replace(" ", "").replace("kr",
                                                                        ""))
            val_2 = int(
                (str(val_2) if val_2 else "0").replace(" ", "").replace("kr",
                                                                        ""))
            self.data.update({total_name: Money(
                str(Decimal(val_1) + Decimal(val_2))).value()})
        elif total_name in self.data:
            del self.data[total_name]

    def clear_total_data(self):
        """
        method for clearing all data in model

        """
        self.data = {}

    def calculate_monthly_values(self, line_edit: str, value: str, factor: str):
        """
        method for calculating monthly values

        """
        Assertor.assert_data_types([value, factor], [str, str])
        if value and factor:
            quantity = Decimal(
                value.replace(" ", "").replace("kr", "")) * Decimal(
                factor.replace(" ", "").replace("kr", ""))
            divisor = Decimal("12")
            monthly_values = round(Decimal(quantity / divisor))
            self.data.update({line_edit: Money(str(monthly_values)).value()})
        elif value:
            monthly_values = round(
                Decimal(value.replace(" ", "").replace("kr", "")))
        else:
            monthly_values = round(Decimal("0"))
        return monthly_values

    def calculate_yearly_values(self, line_edit: str, value: str, factor: str):
        """
        method for calculating yearly values

        """
        Assertor.assert_data_types([value, factor], [str, str])
        if value and factor:
            quantity = Decimal(
                value.replace(" ", "").replace("kr", "")) * Decimal(
                factor.replace(" ", "").replace("kr", ""))
            yearly_values = round(Decimal(quantity))
            self.data.update({line_edit: Money(str(yearly_values)).value()})
        elif value:
            yearly_values = round(
                Decimal(value.replace(" ", "").replace("kr", "")))
        else:
            yearly_values = round(Decimal("0"))
        return yearly_values
