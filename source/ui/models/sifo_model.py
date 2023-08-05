# -*- coding: utf-8 -*-

"""
Module with the logic for SIFO calculation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from PyQt5.QtCore import pyqtSlot, QObject

from source.app import SifoExpensesProcess
from source.util import Assertor
from source.domain import Money

from .model import Model


class SifoModel(Model):
    """
    Implementation of the Sifo Model with logic for all SIFO calculations

    """
    _budsjett_aar = ["", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015",
                     "2014", "2013", "2012", "2011", "2010"]
    _kjonn = ["", "Mann", "Kvinne"]
    _alder = ["", "0-5 mnd", "6-11 mnd", "1 år", "2 år", "3 år", "4-5 år",
              "6-9 år", "10-13 år", "14-17 år", "18-19 år", "20-30 år", "31-50 år", "51-60 år",
              "61-66 år", "67-73 år", "eldre enn 74 år"]
    _barnehage = ["", "Nei", "Ja"]
    _sfo = ["", "Nei", "Halvdag", "Heldag"]
    _student = ["", "Nei", "Ja"]
    _antall_biler = ["", "1", "2", "3", "4"]
    _sifo_expenses = ['mat', 'klar', 'helse', 'fritid', 'kollektivt', 'spedbarn', 'sumindivid',
                      'dagligvarer', 'husholdsart', 'mobler', 'medier', 'biler', 'barnehage',
                      'sfo', 'sumhusholdning', 'totalt']

    def __init__(self, parent: QObject):
        """
        Constructor / Instantiation

        Parameters
        ----------
        parent  : QObject
                  parent view for which the SifoModel resides

        """
        Assertor.assert_data_types([parent], [QObject])
        super().__init__(parent=parent)
        self.parent.ui_form.combo_box_budsjett_aar.addItems(self._budsjett_aar)
        for num in range(1, 8):
            getattr(self.parent.ui_form, "combo_box_kjonn_" + str(num)).addItems(
                self._kjonn)
            getattr(self.parent.ui_form, "combo_box_alder_" + str(num)).addItems(
                self._alder)
        self.parent.ui_form.combo_box_antall_biler.addItems(self._antall_biler)
        self.parent.ui_form.combo_box_antall_elbiler.addItems(self._antall_biler)
        self._sifo_process = None
        self._extra_info = None

    @property
    def sifo_process(self):
        """
        Sifo process getter

        Returns
        -------
        out     : SifoExpensesProcess
                  active SifoProcessing in SifoModel
        """
        return self._sifo_process

    @sifo_process.setter
    def sifo_process(self, new_sifo_process):
        """
        Sifo process setter

        Parameters
        ----------
        new_sifo_process       : SifoExpensesProcess
                                 new SifoProcessing to be set in object
        """
        self._sifo_process = new_sifo_process

    @pyqtSlot()
    def set_income(self):
        """
        method for setting / formatting gross income

        """
        self.parent.ui_form.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_arsinntekt", Money, "value",
                                       clearing=self.clear_results))

    @pyqtSlot()
    def set_budsjett_aar(self):
        """
        method for setting the budget year

        """
        self.parent.ui_form.combo_box_budsjett_aar.activated.connect(
            lambda: self.set_combo_box("budsjett_aar"))

    @pyqtSlot()
    def set_gender(self):
        """
        method for setting / formatting gender

        """
        self.parent.ui_form.combo_box_kjonn_1.activated.connect(
            lambda: self.set_age_and_gender("_1"))
        self.parent.ui_form.combo_box_kjonn_2.activated.connect(
            lambda: self.set_age_and_gender("_2"))
        self.parent.ui_form.combo_box_kjonn_3.activated.connect(
            lambda: self.set_age_and_gender("_3"))
        self.parent.ui_form.combo_box_kjonn_4.activated.connect(
            lambda: self.set_age_and_gender("_4"))
        self.parent.ui_form.combo_box_kjonn_5.activated.connect(
            lambda: self.set_age_and_gender("_5"))
        self.parent.ui_form.combo_box_kjonn_6.activated.connect(
            lambda: self.set_age_and_gender("_6"))
        self.parent.ui_form.combo_box_kjonn_7.activated.connect(
            lambda: self.set_age_and_gender("_7"))

    @pyqtSlot()
    def set_age(self):
        """
        method for setting / formatting age

        """
        self.parent.ui_form.combo_box_alder_1.activated.connect(
            lambda: self.set_age_and_gender("_1"))
        self.parent.ui_form.combo_box_alder_2.activated.connect(
            lambda: self.set_age_and_gender("_2"))
        self.parent.ui_form.combo_box_alder_3.activated.connect(
            lambda: self.set_age_and_gender("_3"))
        self.parent.ui_form.combo_box_alder_4.activated.connect(
            lambda: self.set_age_and_gender("_4"))
        self.parent.ui_form.combo_box_alder_5.activated.connect(
            lambda: self.set_age_and_gender("_5"))
        self.parent.ui_form.combo_box_alder_6.activated.connect(
            lambda: self.set_age_and_gender("_6"))
        self.parent.ui_form.combo_box_alder_7.activated.connect(
            lambda: self.set_age_and_gender("_7"))

    @pyqtSlot()
    def set_extra_info(self):
        """
        method for setting extra info, i.e. kindergarten, sfo or pregnant

        """
        self.parent.ui_form.combo_box_tillegg_1.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_1"))
        self.parent.ui_form.combo_box_tillegg_2.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_2"))
        self.parent.ui_form.combo_box_tillegg_3.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_3"))
        self.parent.ui_form.combo_box_tillegg_4.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_4"))
        self.parent.ui_form.combo_box_tillegg_5.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_5"))
        self.parent.ui_form.combo_box_tillegg_6.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_6"))
        self.parent.ui_form.combo_box_tillegg_7.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_7"))

    @pyqtSlot()
    def set_age_and_gender(self, postfix: str):
        """
        method for setting / validating age and gender

        Parameters
        ----------
        postfix : str
                  postfix matching naming convention

        """
        Assertor.assert_data_types([postfix], [str])
        self.check_extra_info(postfix, show_info=True)
        self.set_combo_box("kjonn" + postfix, "person" + postfix)
        self.set_combo_box("alder" + postfix, "person" + postfix)

    @pyqtSlot()
    def get_extra_info(self, name: str, common_key: str, postfix: str):
        """
        method for getting the extra information if already supplied

        Parameters
        ----------
        name        : str
                      name of extra info, i.e. barnehage, sfo or gravid
        common_key  : str
                      common key data is stored under
        postfix     : str
                      postfix matching naming convention

        """
        Assertor.assert_data_types([name, common_key, postfix], [str, str, str])
        self.check_extra_info(postfix)
        self.set_combo_box(name + postfix, common_key + postfix, self._extra_info)

    @pyqtSlot()
    def check_extra_info(self, postfix: str, show_info: bool = False):
        """
        method for checking if conditions are meet inorder to display additional info

        Parameters
        ----------
        postfix     : str
                      postfix matching naming convention
        show_info   : bool
                      argument indicating if one wants to show the extra info in the gui

        """
        Assertor.assert_data_types([postfix, show_info], [str, bool])
        ui_form = self.parent.ui_form
        self.clear_extra_data(postfix)

        alder = getattr(ui_form, "combo_box_alder" + postfix).currentText()
        kvinne = getattr(ui_form, "combo_box_kjonn" + postfix).currentText() == "Kvinne"

        barnehage = (alder in ["1 år", "2 år", "3 år", "4-5 år"])
        sfo = (alder in ["6-9 år", "10-13 år"])
        gravid = (kvinne and (alder in ["14-17 år", "18-19 år", "20-30 år", "31-50 år"]))
        student = (alder == "20-30 år")

        if barnehage:
            self._extra_info = "barnehage" + postfix
            if show_info:
                self.show_extra_info("barnehage", postfix, self._barnehage)
        elif sfo:
            self._extra_info = "sfo" + postfix
            if show_info:
                self.show_extra_info("sfo", postfix, self._sfo)
        elif student:
            self._extra_info = "student" + postfix
            if show_info:
                self.show_extra_info("student", postfix, self._student)
        elif gravid:
            self._extra_info = "gravid" + postfix
            if show_info:
                self.show_extra_info("gravid", postfix, self._barnehage)
        else:
            self.clear_extra_info(postfix)

    @pyqtSlot()
    def show_extra_info(self, name: str, postfix: str, values: list):
        """
        method for showing the extra info if chosen to be displayed

        Parameters
        ----------
        name        : str
                      name of extra info, i.e. barnehage, sfo or gravid
        postfix     : str
                      postfix matching naming convention
        values      : list
                      values for combobox dropdown

        """
        Assertor.assert_data_types([name, postfix, values], [str, str, list])
        ui_form = self.parent.ui_form
        name = name.capitalize() if name != "sfo" else name.upper()
        getattr(ui_form, "label_tillegg" + postfix).setText(name + "?")
        getattr(ui_form, "combo_box_tillegg" + postfix).show()
        getattr(ui_form, "combo_box_tillegg" + postfix).setEnabled(True)
        getattr(ui_form, "combo_box_tillegg" + postfix).clear()
        getattr(ui_form, "combo_box_tillegg" + postfix).addItems(values)

    @pyqtSlot()
    def clear_extra_info(self, postfix: str):
        """
        method for clearing the combobox information

        Parameters
        ----------
        postfix     : str
                      postfix matching naming convention

        """
        Assertor.assert_data_types([postfix], [str])
        ui_form = self.parent.ui_form
        self._extra_info = None
        getattr(ui_form, "label_tillegg" + postfix).setText("")
        getattr(ui_form, "combo_box_tillegg" + postfix).setCurrentIndex(0)
        getattr(ui_form, "combo_box_tillegg" + postfix).setEnabled(False)
        getattr(ui_form, "combo_box_tillegg" + postfix).hide()
        self.clear_extra_data(postfix)

    @pyqtSlot()
    def hide_unused_combo_box(self):
        """
        method for hiding unused combo boxes

        """
        ui_form = self.parent.ui_form
        for i in range(1, 8):
            postfix = "_" + str(i)
            if not getattr(ui_form, "combo_box_tillegg" + postfix).isEnabled():
                getattr(ui_form, "label_tillegg" + postfix).setText("")
                getattr(ui_form, "combo_box_tillegg" + postfix).setCurrentIndex(0)
                getattr(ui_form, "combo_box_tillegg" + postfix).setEnabled(False)
                getattr(ui_form, "combo_box_tillegg" + postfix).hide()
                self.clear_extra_data(postfix)

    @pyqtSlot()
    def clear_extra_data(self, postfix: str):
        """
        method for clearing the combobox data

        Parameters
        ----------
        postfix     : str
                      postfix matching naming convention

        """
        Assertor.assert_data_types([postfix], [str])
        self.clear_data("barnehage" + postfix, "person" + postfix)
        self.clear_data("sfo" + postfix, "person" + postfix)
        self.clear_data("gravid" + postfix, "person" + postfix)
        self.clear_data("student" + postfix, "person" + postfix)

    @pyqtSlot()
    def set_cars(self):
        """
        method for setting / formatting number of cars in family

        """
        self.parent.ui_form.combo_box_antall_biler.activated.connect(
            lambda: self.set_combo_box("antall_biler"))

    @pyqtSlot()
    def set_electric_cars(self):
        """
        method for setting / formatting number of electric cars in family

        """
        self.parent.ui_form.combo_box_antall_elbiler.activated.connect(
            lambda: self.set_combo_box("antall_elbiler"))

    @pyqtSlot()
    def set_yearly_income(self):
        """
        method for setting / formatting yearly gross income

        """
        if "personinntekt_total_aar" in self.parent.parent.budget_view.budget_model.data:
            self.parent.ui_form.line_edit_brutto_arsinntekt.setText(
                self.parent.parent.budget_view.budget_model.data["personinntekt_total_aar"])

    @pyqtSlot()
    def calculate_yearly_income(self, monthly_income: str):
        """
        method for calculating / setting / formatting yearly gross income

        Parameters
        ----------
        monthly_income  : str

        """
        Assertor.assert_data_types([monthly_income], [str])
        yearly_income = self.parent.ui_form.line_edit_brutto_arsinntekt.text()
        final_income = None
        if monthly_income and not yearly_income:
            yearly_income_from_monthly = Money(
                str(Decimal(monthly_income.replace(" kr", "").replace(" ", "")) * 12))
            self.data.update({"brutto_arsinntekt": yearly_income_from_monthly.value()})
            final_income = yearly_income_from_monthly.value()
        else:
            final_income = yearly_income
        return final_income

    def calculate_sifo_expenses(self):
        """
        method for calculating the SIFO expenses

        """
        try:
            self.clear_results()
            if "budsjett_aar" in self.data.keys() and any("person" in key and len(val) > 1 for
                                                          key, val in self.data.items()):
                self.parent.ui_form.tab_widget_sifo.setCurrentIndex(1)
                self.sifo_process = SifoExpensesProcess(self.data)
                self.set_line_edits(line_edit_text="", line_edits=self._sifo_expenses, postfix="_1",
                                    data=self.sifo_process.base_expenses)
                self.set_line_edits(line_edit_text="", line_edits=self._sifo_expenses, postfix="_2",
                                    data=self.sifo_process.expenses_shares)
        except Exception as sifo_expenses_error:
            self.clear_results()
            self.parent.error_view.show_error(sifo_expenses_error, self.data)
            self.parent.error_view.exec_()

    def sifo_info(self):
        """
        method for running all SIFO logic

        """
        self.hide_unused_combo_box()
        self.parent.ui_form.combo_box_kjonn_1.setFocus()
        self.set_income()
        self.set_yearly_income()
        self.set_gender()
        self.set_age()
        self.set_extra_info()
        self.set_cars()
        self.set_electric_cars()
        self.set_budsjett_aar()

    @pyqtSlot()
    def clear_results(self):
        """
        method for clearing results from SIFO dialog

        """
        self.clear_line_edits(self._sifo_expenses, "_1")
        self.clear_line_edits(self._sifo_expenses, "_2")

    def clear_all(self):
        """
        method for clearing all information from SIFO dialog

        """
        self.parent.ui_form.combo_box_budsjett_aar.setCurrentIndex(0)
        for combo_box in range(1, 8):
            getattr(self.parent.ui_form, "combo_box_kjonn_" + str(combo_box)).setCurrentIndex(0)
            getattr(self.parent.ui_form, "combo_box_alder_" + str(combo_box)).setCurrentIndex(0)
            self.clear_extra_info("_" + str(combo_box))
        self.parent.ui_form.line_edit_brutto_arsinntekt.clear()
        self.parent.ui_form.combo_box_antall_biler.setCurrentIndex(0)
        self.parent.ui_form.combo_box_antall_elbiler.setCurrentIndex(0)
        self.clear_results()
        self.data = {}
        self.parent.ui_form.combo_box_kjonn_1.setFocus()
