# -*- coding: utf-8 -*-

"""
Module with the logic for SIFO calculation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from PyQt5.QtCore import pyqtSlot, QObject

from source.app import SifoWorkFlow
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
        self._sifo_workflow = None

    @pyqtSlot()
    def sifo_info(self):
        """
        method for running all SIFO logic

        """
        self.set_yearly_income()
        self.set_age()
        self.set_gender()
        self.set_cars()
        self.set_income()
        self.parent.ui.push_button_vis_resultatet.clicked.connect(self.calculate_sifo_expenses)
        self.parent.ui.push_button_tom_skjema_1.clicked.connect(self.clear_all)
        self.parent.ui.push_button_avbryt_1.clicked.connect(self.close)
        self.parent.ui.push_button_tom_skjema_2.clicked.connect(self.clear_all)
        self.parent.ui.push_button_avbryt_2.clicked.connect(self.close)
        self.parent.ui.push_button_tilbake.clicked.connect(self.back)
        self.parent.ui.push_button_eksporter.clicked.connect(self.export)

    @pyqtSlot()
    def set_income(self):
        """
        method for setting / formatting gross income

        """
        self.parent.ui.line_edit_brutto_arsinntekt.editingFinished.connect(
            lambda: self.set_line_edit("brutto_arsinntekt", Money, "value",
                                       clearing=self.clear_results))

    @pyqtSlot()
    def set_age(self):
        """
        method for setting / formatting age

        """
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

    @pyqtSlot()
    def set_gender(self):
        """
        method for setting / formatting gender

        """
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
            if all(len(val) == 1 for val in self.data.values() if isinstance(val, dict)):
                self.clear_results()
            self.parent.ui.tabwidget_sifo.setCurrentIndex(1)
            self._sifo_workflow = SifoWorkFlow(self.data)
            self.set_line_edits(line_edit_text="", line_edits=self._sifo_expenses, postfix="_1",
                                data=self._sifo_workflow.expenses_value)
            self.set_line_edits(line_edit_text="", line_edits=self._sifo_expenses, postfix="_2",
                                data=self._sifo_workflow.expenses_share)
        except Exception as sifo_expenses_error:
            self.clear_results()
            self.parent.error.show_error(sifo_expenses_error, self.data)
            self.parent.error.exec_()

    def show(self):
        """
        method for showing SIFO calculator

        """
        self.parent.ui.tabwidget_sifo.setCurrentIndex(0)
        self.parent.ui.combo_box_kjonn_1.setFocus()
        self.sifo_info()
        self.parent.ui.show()

    def clear_results(self):
        """
        method for clearing results from SIFO dialog

        """
        self.clear_line_edits(self._sifo_expenses, "_1")
        self.clear_line_edits(self._sifo_expenses, "_2")
        self.parent.ui.tabwidget_sifo.setCurrentIndex(0)

    def clear_all(self):
        """
        method for clearing all information from SIFO dialog

        """
        self.parent.ui.combo_box_kjonn_1.setFocus()
        for combo_box in range(1, 8):
            getattr(self.parent.ui, "combo_box_kjonn_" + str(combo_box)).setCurrentIndex(0)
            getattr(self.parent.ui, "combo_box_alder_" + str(combo_box)).setCurrentIndex(0)
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
        self.parent.ui.tabwidget_sifo.setCurrentIndex(0)

    def close(self):
        """
        method for canceling / closing SIFO dialog

        """
        self.parent.close()
