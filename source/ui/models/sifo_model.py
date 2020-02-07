# -*- coding: utf-8 -*-

"""
Module with the logic for SIFO calculation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from PyQt5.QtCore import pyqtSlot, QObject

from source.app import CalculateSifoExpenses
from source.util import Assertor
from source.domain import Money

from .model import Model


class SifoModel(Model):
    """
    Implementation of the Sifo Model with logic for all SIFO calculations

    """
    _kjonn = ["", "Mann", "Kvinne"]
    _alder = ["", "0-5 mnd", "6-11 mnd", "1", "2", "3", "4-5",
              "6-9", "10-13", "14-17", "18-19", "20-50", "51-60",
              "61-66", "eldre enn 66"]
    _barnehage = ["", "Nei", "Ja"]
    _sfo = ["", "Nei", "Halvdag", "Heldag"]
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
        super(SifoModel, self).__init__(parent)
        for num in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(num)).addItems(
                self._kjonn)
            getattr(self.parent.ui, "combo_box_alder_" + str(num)).addItems(
                self._alder)
        self.parent.ui.combo_box_antall_biler.addItems(self._antall_biler)
        self._sifo_process = None
        self._extra_info = None

    @property
    def sifo_process(self):
        """
        Sifo process getter

        Returns
        -------
        out     : CalculateSifoExpenses
                  active SifoProcessing in SifoModel
        """
        return self._sifo_process

    @sifo_process.setter
    def sifo_process(self, new_sifo_process):
        """
        Sifo process setter

        Parameters
        ----------
        new_sifo_process       : CalculateSifoExpenses
                                 new SifoProcessing to be set in object
        """
        self._sifo_process = new_sifo_process

    @pyqtSlot()
    def set_income(self):
        """
        method for setting / formatting gross income

        """
        self.parent.ui.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_arsinntekt", Money, "value",
                                       clearing=self.clear_results))

    @pyqtSlot()
    def set_gender(self):
        """
        method for setting / formatting gender

        """
        self.parent.ui.combo_box_kjonn_1.activated.connect(
            lambda: self.set_age_and_gender("_1"))
        self.parent.ui.combo_box_kjonn_2.activated.connect(
            lambda: self.set_age_and_gender("_2"))
        self.parent.ui.combo_box_kjonn_3.activated.connect(
            lambda: self.set_age_and_gender("_3"))
        self.parent.ui.combo_box_kjonn_4.activated.connect(
            lambda: self.set_age_and_gender("_4"))
        self.parent.ui.combo_box_kjonn_5.activated.connect(
            lambda: self.set_age_and_gender("_5"))
        self.parent.ui.combo_box_kjonn_6.activated.connect(
            lambda: self.set_age_and_gender("_6"))
        self.parent.ui.combo_box_kjonn_7.activated.connect(
            lambda: self.set_age_and_gender("_7"))

    @pyqtSlot()
    def set_age(self):
        """
        method for setting / formatting age

        """
        self.parent.ui.combo_box_alder_1.activated.connect(
            lambda: self.set_age_and_gender("_1"))
        self.parent.ui.combo_box_alder_2.activated.connect(
            lambda: self.set_age_and_gender("_2"))
        self.parent.ui.combo_box_alder_3.activated.connect(
            lambda: self.set_age_and_gender("_3"))
        self.parent.ui.combo_box_alder_4.activated.connect(
            lambda: self.set_age_and_gender("_4"))
        self.parent.ui.combo_box_alder_5.activated.connect(
            lambda: self.set_age_and_gender("_5"))
        self.parent.ui.combo_box_alder_6.activated.connect(
            lambda: self.set_age_and_gender("_6"))
        self.parent.ui.combo_box_alder_7.activated.connect(
            lambda: self.set_age_and_gender("_7"))

    @pyqtSlot()
    def set_extra_info(self):
        """
        method for setting extra info, i.e. kindergarten, sfo or pregnant

        """
        self.parent.ui.combo_box_tillegg_1.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_1"))
        self.parent.ui.combo_box_tillegg_2.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_2"))
        self.parent.ui.combo_box_tillegg_3.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_3"))
        self.parent.ui.combo_box_tillegg_4.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_4"))
        self.parent.ui.combo_box_tillegg_5.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_5"))
        self.parent.ui.combo_box_tillegg_6.activated.connect(
            lambda: self.get_extra_info("tillegg", "person", "_6"))
        self.parent.ui.combo_box_tillegg_7.activated.connect(
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
        ui = self.parent.ui
        self.clear_extra_data(postfix)

        alder = getattr(ui, "combo_box_alder" + postfix).currentText()
        kvinne = getattr(ui, "combo_box_kjonn" + postfix).currentText() == "Kvinne"

        barnehage = (alder in ["1", "2", "3", "4-5"])
        sfo = (alder in ["6-9", "10-13"])
        gravid = (kvinne and (alder in ["14-17", "18-19", "20-50"]))

        if barnehage:
            self._extra_info = "barnehage" + postfix
            self.show_extra_info("barnehage", postfix, self._barnehage) if show_info else ""
        elif sfo:
            self._extra_info = "sfo" + postfix
            self.show_extra_info("sfo", postfix, self._sfo) if show_info else ""
        elif gravid:
            self._extra_info = "gravid" + postfix
            self.show_extra_info("gravid", postfix, self._barnehage) if show_info else ""
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
        ui = self.parent.ui
        getattr(ui, "label_tillegg" + postfix).setText(name.capitalize() + "?")
        getattr(ui, "combo_box_tillegg" + postfix).show()
        getattr(ui, "combo_box_tillegg" + postfix).setEnabled(True)
        getattr(ui, "combo_box_tillegg" + postfix).clear()
        getattr(ui, "combo_box_tillegg" + postfix).addItems(values)

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
        ui = self.parent.ui
        self._extra_info = None
        getattr(ui, "label_tillegg" + postfix).setText("")
        getattr(ui, "combo_box_tillegg" + postfix).setCurrentIndex(0)
        getattr(ui, "combo_box_tillegg" + postfix).setEnabled(False)
        getattr(ui, "combo_box_tillegg" + postfix).hide()
        self.clear_extra_data(postfix)

    @pyqtSlot()
    def hide_unused_combo_box(self):
        """
        method for hiding unused combo boxes

        """
        ui = self.parent.ui
        for i in range(1, 8):
            postfix = "_" + str(i)
            if not getattr(ui, "combo_box_tillegg" + postfix).isEnabled():
                getattr(ui, "label_tillegg" + postfix).setText("")
                getattr(ui, "combo_box_tillegg" + postfix).setCurrentIndex(0)
                getattr(ui, "combo_box_tillegg" + postfix).setEnabled(False)
                getattr(ui, "combo_box_tillegg" + postfix).hide()
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

    @pyqtSlot()
    def set_cars(self):
        """
        method for setting / formatting number of cars in family

        """
        self.parent.ui.combo_box_antall_biler.activated.connect(
            lambda: self.set_combo_box("antall_biler"))

    @pyqtSlot()
    def set_yearly_income(self):
        """
        method for setting / formatting yearly gross income

        """
        self.parent.ui.line_edit_brutto_arsinntekt.setText(self.calculate_yearly_income(
            self.parent.parent.ui.line_edit_brutto_inntekt.text()))

    @pyqtSlot()
    def calculate_yearly_income(self, monthly_income: str):
        """
        method for calculating / setting / formatting yearly gross income

        Parameters
        ----------
        monthly_income  : str

        """
        Assertor.assert_data_types([monthly_income], [str])
        yearly_income = self.parent.ui.line_edit_brutto_arsinntekt.text()
        if monthly_income and not yearly_income:
            yearly_income_from_monthly = Money(
                str(Decimal(monthly_income.replace(" kr", "").replace(" ", "")) * 12))
            self.data.update({"brutto_arsinntekt": yearly_income_from_monthly.value()})
            return yearly_income_from_monthly.value()
        else:
            return yearly_income

    def calculate_sifo_expenses(self):
        """
        method for calculating the SIFO expenses

        """
        try:
            self.clear_results()
            if self.data and all(len(val) > 1 for key, val in self.data.items() if "person" in key):
                self.parent.ui.tab_widget_sifo.setCurrentIndex(1)
                self.sifo_process = CalculateSifoExpenses(self.data)
                # self.sifo_process.print_pdf()
                self.set_line_edits(line_edit_text="", line_edits=self._sifo_expenses, postfix="_1",
                                    data=self.sifo_process.base_expenses)
                self.set_line_edits(line_edit_text="", line_edits=self._sifo_expenses, postfix="_2",
                                    data=self.sifo_process.expenses_shares)
        except Exception as sifo_expenses_error:
            self.clear_results()
            self.parent.error.show_error(sifo_expenses_error, self.data)
            self.parent.error.exec_()

    def sifo_info(self):
        """
        method for running all SIFO logic

        """
        self.hide_unused_combo_box()
        self.parent.ui.tab_widget_sifo.setCurrentIndex(0)
        self.parent.ui.combo_box_kjonn_1.setFocus()
        self.set_income()
        self.set_yearly_income()
        self.set_gender()
        self.set_age()
        self.set_extra_info()
        self.set_cars()

    @pyqtSlot()
    def clear_results(self):
        """
        method for clearing results from SIFO dialog

        """
        self.clear_line_edits(self._sifo_expenses, "_1")
        self.clear_line_edits(self._sifo_expenses, "_2")
        self.parent.ui.tab_widget_sifo.setCurrentIndex(0)

    def clear_all(self):
        """
        method for clearing all information from SIFO dialog

        """
        self.parent.ui.combo_box_kjonn_1.setFocus()
        for combo_box in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(combo_box)).setCurrentIndex(0)
            getattr(self.parent.ui, "combo_box_alder_" + str(combo_box)).setCurrentIndex(0)
            self.clear_extra_info("_" + str(combo_box))
        self.parent.ui.line_edit_brutto_arsinntekt.clear()
        self.parent.ui.combo_box_antall_biler.setCurrentIndex(0)
        self.clear_results()
        self.data = {}

    def export(self):
        """
        method for exporting SIFO expenses to HomeView

        """
        sifo_expenses = self.parent.ui.line_edit_totalt_1.text()
        grandparent = self.parent.parent
        grandparent.mortgage_model.set_line_edit("sifo_utgifter", data=sifo_expenses)
        self.close()

    def back(self):
        """
        method for returning for results page to input page

        """
        self.parent.ui.tab_widget_sifo.setCurrentIndex(0)

    def close(self):
        """
        method for canceling / closing SIFO dialog

        """
        self.parent.close()
