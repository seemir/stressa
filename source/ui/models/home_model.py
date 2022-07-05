# -*- coding: utf-8 -*-
"""
Module with the logic of the Home model

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.domain import Money, Share
from source.util import Assertor

from .model import Model


class HomeModel(Model):
    """
    Implementation of the Home model logic

    """

    def __init__(self, parent):
        """
        Constructor / instantiation of class

        Parameters
        ----------
        parent      : QMainWindow
                      class of parent class

        """
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])
        self.data = self.parent.meta_view.get_all_meta_data()

    def clear_all(self):
        """
        method for clearing all content in HomeView

        """
        self.parent.mortgage_model.clear_all()
        self.parent.budget_view.clear_all()
        self.parent.tax_view.clear_all()
        self.parent.sifo_view.clear_all()
        self.parent.finn_model.clear_all()
        self.parent.analysis_model.clear_all()
        self.parent.restructure_model.clear_all()
        self.parent.payment_model.clear_all()

        self.parent.ui_form.line_edit_fornavn_2.setFocus()
        self.parent.ui_form.tab_widget_lanesokere.setCurrentIndex(0)
        self.parent.ui_form.line_edit_fornavn_1.setFocus()

    def liquidity_info(self):
        """
        method for calculating liquidity information

        """
        self.parent.ui_form.line_edit_personinntekt_total.textChanged.connect(
            self.calculate_net_income)
        self.parent.ui_form.line_edit_beregnet_skatt_per_mnd_beloep.textChanged.connect(
            self.calculate_net_income)

        self.parent.ui_form.line_edit_sum_utgifter_total.textChanged.connect(
            self.calculate_total_costs)
        self.parent.ui_form.line_edit_sifo_utgifter.textChanged.connect(
            self.calculate_total_costs)

        self.parent.ui_form.line_edit_total_netto.textChanged.connect(
            self.calculate_net_liquidity)
        self.parent.ui_form.line_edit_totale_utgifter.textChanged.connect(
            self.calculate_net_liquidity)

        self.parent.ui_form.line_edit_personinntekt_total.textChanged.connect(
            self.calculate_liquidity_share)
        self.parent.ui_form.line_edit_netto_likviditet.textChanged.connect(
            self.calculate_liquidity_share)

    def calculate_net_income(self):
        """
        method for calculating net income

        """
        person_income = self.parent.ui_form.line_edit_personinntekt_total.text()
        tax_value = self.parent.ui_form.line_edit_beregnet_skatt_per_mnd_beloep.text()

        gross_income = Money(person_income if person_income else "0")
        tax_cost = Money(tax_value if tax_value else "0")
        total_net = gross_income - tax_cost
        if total_net != "0 kr":
            self.set_line_edit("total_netto", data=total_net)
        else:
            self.clear_line_edit("total_netto")

    def calculate_total_costs(self):
        """
        method for calculating total cost

        """
        cost_value = self.parent.ui_form.line_edit_sum_utgifter_total.text()
        sifo_value = self.parent.ui_form.line_edit_sifo_utgifter.text()

        sum_cost = Money(cost_value if cost_value else "0")
        sifo_cost = Money(sifo_value if sifo_value else "0")
        total_cost = sum_cost + sifo_cost
        if total_cost != "0 kr":
            self.set_line_edit("totale_utgifter", data=total_cost)
        else:
            self.clear_line_edit("totale_utgifter")

    def calculate_net_liquidity(self):
        """
        method for calculating net liquidity

        """
        total_net_value = self.parent.ui_form.line_edit_total_netto.text()
        total_cost_value = self.parent.ui_form.line_edit_totale_utgifter.text()

        total_net = Money(total_net_value if total_net_value else "0")
        total_cost = Money(total_cost_value if total_cost_value else "0")
        net_liquidity = total_net - total_cost

        if net_liquidity != "0 kr":
            self.set_line_edit("netto_likviditet", data=net_liquidity)
        else:
            self.clear_line_edit("netto_likviditet")

    def calculate_liquidity_share(self):
        """
        method for calculating share net liquidity

        """
        gross_income = self.parent.ui_form.line_edit_personinntekt_total.text()
        net_liquidity = self.parent.ui_form.line_edit_netto_likviditet.text()

        gross_value = Money(gross_income if gross_income else "0")
        net_value = Money(net_liquidity if net_liquidity else "0")
        if gross_value.value() == "0 kr":
            self.clear_line_edit("likviditetsgrad")
        else:
            liquidity_share = Share(numerator=net_value, denominator=gross_value)

            if liquidity_share.value != "0 %":
                self.set_line_edit("likviditetsgrad", data=liquidity_share.value)
            else:
                self.clear_line_edit("likviditetsgrad")
