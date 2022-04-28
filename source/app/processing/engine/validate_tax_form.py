# -*- coding: utf-8 -*-

"""
Module for operation for validating tax information in tax form

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from datetime import date

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
        if "alder" in self.tax_data.keys():
            age = self.tax_data["alder"]
        else:
            age = 0
        if "brutto_inntekt_total" in self.tax_data.keys():
            income = self.tax_data["brutto_inntekt_total"]
        else:
            income = 0
        if "skatte_aar" in self.tax_data.keys():
            tax_year = self.tax_data["skatte_aar"]
        else:
            tax_year = date.today().year
        if "renteinntekter_total" in self.tax_data.keys():
            interest_income = self.tax_data["renteinntekter_total"]
        else:
            interest_income = 0
        if "rentekostnader_total" in self.tax_data.keys():
            interest_cost = self.tax_data["rentekostnader_total"]
        else:
            interest_cost = 0
        if "verdi_primarbolig" in self.tax_data.keys():
            value_of_real_estate = self.tax_data["verdi_primarbolig"]
        else:
            value_of_real_estate = 0
        if "bankinnskudd" in self.tax_data.keys():
            bank_deposit = self.tax_data["bankinnskudd"]
        else:
            bank_deposit = 0
        if "gjeld" in self.tax_data.keys():
            debt = self.tax_data["gjeld"]
        else:
            debt = 0
        if "fagforeningskontigent" in self.tax_data.keys():
            union_fee = self.tax_data["fagforeningskontigent"]
        else:
            union_fee = 0
        if "bsu" in self.tax_data.keys():
            bsu = self.tax_data["bsu"]
        else:
            bsu = 0
        if "andre_inntekter_total" in self.tax_data.keys():
            other_income = self.tax_data["andre_inntekter_total"]
        else:
            other_income = 0
        if "leieinntekt_total" in self.tax_data.keys():
            rental_income = self.tax_data["leieinntekt_total"]
        else:
            rental_income = 0

        tax_form = TaxForm(age=age, income=income, tax_year=tax_year,
                           interest_income=interest_income, interest_cost=interest_cost,
                           value_of_real_estate=value_of_real_estate, bank_deposit=bank_deposit,
                           debt=debt, union_fee=union_fee, bsu=bsu, other_income=other_income,
                           rental_income=rental_income)
        return tax_form
