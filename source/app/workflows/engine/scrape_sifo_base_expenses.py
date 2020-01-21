# -*- coding: utf-8 -*-

"""
Module for operation of Scraping SIFO base expenses

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.app.scrapers import SIFO_URL, Sifo
from source.domain import Family
from source.util import Assertor

from .operation import Operation


class ScrapeSifoBaseExpenses(Operation):
    """
    Implementation of operation

    """

    def __init__(self, data: Family):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data     : Family
                   Sifo compatible Family object with all necessary family information

        """
        Assertor.assert_data_types([data], [Family])
        self.name = self.__class__.__name__
        super().__init__(name=self.name,
                         desc="Scrape SIFO Base Expenses \\n from: '{}'".format(SIFO_URL))
        self.data = data

    def run(self):
        """
        method for running operation

        Returns
        -------
        out     : dict
                  SIFO compatible dictionary with all necessary family information

        """
        sifo = Sifo(self.data)
        return sifo.sifo_base_expenses()
