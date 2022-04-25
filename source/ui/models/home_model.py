# -*- coding: utf-8 -*-

"""
Module with the logic of the Home model

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.domain import Money
from source.util import Assertor

from .model import Model


class HomeModel(Model):
    """
    Implementation of the Home model logic

    """

    def __init__(self, parent):
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])
        self.data = self.parent.meta_view.get_all_meta_data()

    def clear_all(self):
        """
        method for clearing all content in HomeView

        Returns
        -------

        """
        self.parent.mortgage_model.clear_all()
        self.parent.budget_view.clear_all()
        self.parent.tax_view.clear_all()
        self.parent.sifo_view.clear_all()
        self.parent.finn_model.clear_all()

        self.parent.ui.line_edit_fornavn_2.setFocus()
        self.parent.ui.tab_widget_lanesokere.setCurrentIndex(0)
        self.parent.ui.line_edit_fornavn_1.setFocus()

    def liquidity_info(self):
        self.parent.ui.line_edit_beregnet_skatt_per_mnd_beloep.textChanged.connect(
            self.calculate_net_income)
        self.parent.ui.line_edit_sifo_utgifter.textChanged.connect(
            self.calculate_total_costs)

    def calculate_net_income(self):
        person_income = self.parent.ui.line_edit_personinntekt_total.text()
        tax_value = self.parent.ui.line_edit_beregnet_skatt_per_mnd_beloep.text()

        gross_income = Money(person_income if person_income else "0")
        tax_cost = Money(tax_value if tax_value else "0")
        total_net = gross_income - tax_cost
        self.set_line_edit("total_netto", data=total_net)

    def calculate_total_costs(self):
        cost_value = self.parent.ui.line_edit_sum_utgifter_total.text()
        sifo_value = self.parent.ui.line_edit_sifo_utgifter.text()

        sum_cost = Money(cost_value if cost_value else "0")
        sifo_cost = Money(sifo_value if sifo_value else "0")
        total_cost = sum_cost + sifo_cost
        self.set_line_edit("totale_utgifter", data=total_cost)
