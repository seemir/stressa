# -*- coding: utf-8 -*-

"""
Workflow for analysing app

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import time

from source.domain import Family, Expenses
from source.util import Assertor, LOGGER

from .engine import WorkFlow, Signal, PopulateFamily, ScrapeSifoBaseExpenses


class SifoWorkFlow(WorkFlow):
    """
    Workflow for the calculation of the SIFO expenses with shares of total expenses

    """

    def __init__(self, data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data    : dict
                  information about the family, i.e. arguments to be passed to Family object

        """
        super().__init__(name=self.__class__.__name__)
        start = time.time()
        LOGGER.info("starting '{}'".format(self.__class__.__name__))
        Assertor.assert_data_types([data], [dict])
        self._family = self.populate_family(data)
        self._base_expenses = Expenses(
            self.scrape_sifo_base_expenses(self.family)) if self.family else None
        self._expenses_value = self.base_expenses.expenses_values if \
            self.base_expenses else None
        self._expenses_share = self.base_expenses.expenses_shares if \
            self.base_expenses else None

        self._signal = None

        LOGGER.success(
            "ending '{}' - elapsed: {}".format(self.__class__.__name__, str(time.time() - start)))

    @property
    def signal(self):
        """
        signal getter

        Returns
        -------
        out      : Signal
                   active _signal property

        """
        return self._signal

    @signal.setter
    def signal(self, new_signal):
        """
        signal setter

        Parameters
        ----------
        new_signal  : Signal
                      new signal to set in workflow

        """
        Assertor.assert_data_types([new_signal], [Signal])
        self._signal = new_signal

    @property
    def family(self):
        """
        family object getter

        Returns
        -------
        out     : Family
                  active _family property

        """
        return self._family

    @property
    def base_expenses(self):
        """
        base expenses getter, i.e. expenses as returned from Sifo.sifo_base_expenses() method

        Returns
        -------
        out     : Expenses
                  active _sifo_base_expenses object

        """
        return self._base_expenses

    @property
    def expenses_value(self):
        """
        gets the sifo expenses values in NOK

        Returns
        -------
        out     : dict
                  active _expenses_values

        """
        return self._expenses_value

    @property
    def expenses_share(self):
        """
        gets the sifo expenses values as a percent of total

        Returns
        -------
        out     : dict
                  active _expenses_shares

        """
        return self._expenses_share

    def populate_family(self, data: dict):
        """
        method for populating family information into Family object

        Parameters
        ----------
        data    : dict
                  Sifo compatible dictionary with input

        Returns
        -------
        out     : Family
                  Sifo compatible Family object with all necessary family information

        """
        Assertor.assert_data_types([data], [dict])
        populate_family = PopulateFamily(data)
        family = populate_family.run()
        self.add_node(populate_family)
        self.signal = Signal(family, "Family")
        self.add_node(self.signal)
        self.add_transition(populate_family, self.signal)
        return family

    def scrape_sifo_base_expenses(self, data: Family):
        """
        method for scraping SIFO base expenses

        Parameters
        ----------
        data    : Family
                  family object

        Returns
        -------
        out     : dict
                  dictionary with SIFO base expenses

        """
        Assertor.assert_data_types([data], [Family])
        sifo_scraper = ScrapeSifoBaseExpenses(data)
        self.add_node(sifo_scraper)
        self.add_transition(self.signal, sifo_scraper)

        sifo_base_expenses = sifo_scraper.run()
        self.signal = Signal(sifo_base_expenses, "SIFO Base Expenses")
        self.add_node(self.signal)
        self.add_transition(sifo_scraper, self.signal)
        return sifo_base_expenses
