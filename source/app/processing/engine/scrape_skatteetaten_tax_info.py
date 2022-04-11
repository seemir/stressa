# -*- coding: utf-8 -*-
"""
Module with logic for Scraping Skatteetaten Tax Info

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking
from source.domain import TaxForm

from ...scrapers import Skatteetaten, SKATTEETATEN_URL

from .operation import Operation


class ScrapeSkatteetatenTaxinfo(Operation):
    """
    Operation that scrapes Skatteetaten Tax info

    """

    @Tracking
    def __init__(self, tax_form: TaxForm):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        tax_form       : TaxForm
                         object with all tax input

        """
        Assertor.assert_data_types([tax_form], [TaxForm])
        super().__init__(name=self.__class__.__name__,
                         desc="from: '{}\\{}' \n id: Scrape Skatteetaten Tax Info".format(
                             SKATTEETATEN_URL, tax_form.tax_year))
        self.tax_form = tax_form

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : dict
                      dictionary with tax calculation

        """
        tax_info = Skatteetaten(age=self.tax_form.age,
                                income=self.tax_form.income,
                                tax_year=self.tax_form.tax_year,
                                interest_income=self.tax_form.interest_income,
                                interest_cost=self.tax_form.interest_cost,
                                value_of_real_estate=self.tax_form.value_of_real_estate,
                                bank_deposit=self.tax_form.bank_deposit,
                                debt=self.tax_form.debt)
        return dict(sorted(tax_info.tax_information().items()))
