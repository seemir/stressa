# -*- coding: utf-8 -*-
"""
Module with logic for the Scrape Posten Postal code information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from ...scrapers import POSTEN_URL, Posten

from .operation import Operation


class ScrapePostalCodeInfo(Operation):
    """
    Operation that scrapes Postal Code from Norwegian Postal Code Information from Postens
    public address search

    """

    def __init__(self, postal_code: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        postal_code       : str
                         postal_code for advert to scrape information from

        """
        Assertor.assert_data_types([postal_code], [str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name,
                         desc="from: '{}' \\n id: Scrape Postal Code Info".format(
                             POSTEN_URL))
        self.postal_code = postal_code

    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : dict
                      dictionary with postal_code information

        """
        postal_code_info = Posten(self.postal_code)
        return postal_code_info.postal_code_info()
