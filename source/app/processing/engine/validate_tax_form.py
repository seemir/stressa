# -*- coding: utf-8 -*-

"""
Module for operation for validating tax information in tax form

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking
from source.domain import TaxForm

from .operation import Operation


class ValidateTaxForm(Operation):
    """
    Implementation of Validate tax form operation

    """

    @Tracking
    def __init__(self, tax_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        tax_data    : dict
                      Skatteetaten compatible dictionary with tax information

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([tax_data], [dict])
        super().__init__(name=self.name,
                         desc="rules: {} \\n id: Validate Tax Form Information".format(
                             TaxForm.rules()))
        self.tax_data = tax_data

    @Tracking
    def run(self):
        """
        method for running validate tax operation

        Returns
        -------
        out         : TaxForm
                      Skatteetaten compatible TaxForm object with all necessary tax information

        """
        if "age" in self.tax_data.keys():
            age = self.tax_data["age"]
        else:
            age = 0
        if "income" in self.tax_data.keys():
            income = self.tax_data["income"]
        else:
            income = 0
        if "tax_year" in self.tax_data.keys():
            tax_year = self.tax_data["tax_year"]
        else:
            tax_year = 0
        if "interst_income" in self.tax_data.keys():
            interest_income = self.tax_data["interest_income"]
        else:
            interest_income = 0
        if "interst_cost" in self.tax_data.keys():
            interest_cost = self.tax_data["interest_cost"]
        else:
            interest_cost = 0
        if "value_of_real_estate" in self.tax_data.keys():
            value_of_real_estate = self.tax_data["value_of_real_estate"]
        else:
            value_of_real_estate = 0
        if "bank_deposit" in self.tax_data.keys():
            bank_deposit = self.tax_data["bank_deposit"]
        else:
            bank_deposit = 0
        if "debt" in self.tax_data.keys():
            debt = self.tax_data["debt"]
        else:
            debt = 0

        tax_form = TaxForm(age=age, income=income, tax_year=tax_year,
                           interest_income=interest_income, interest_cost=interest_cost,
                           value_of_real_estate=value_of_real_estate, bank_deposit=bank_deposit,
                           debt=debt)
        return tax_form
