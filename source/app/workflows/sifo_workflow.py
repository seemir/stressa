# -*- coding: utf-8 -*-

"""
Workflow for analysing app

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import time

from source.domain import Family, Expenses
from source.util import Assertor, LOGGER

from .engine import WorkFlow, Signal, ValidateFamily, ScrapeSifoBaseExpenses, Extract, Divide, \
    OutputOperation, OutputSignal, InputOperation


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

        self._data = self.input_operation({"data": data})
        self._family = self.validate_family(self.data["data"])
        self._base_expenses = None
        self._expenses_shares = None

        self.output_operation()
        LOGGER.success(
            "ending '{}' - elapsed: {}".format(self.__class__.__name__, str(time.time() - start)))

    @property
    def data(self):
        """
        data object getter

        Returns
        -------
        out     : dict
                  active _data property

        """
        return self._data

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
        out     : dict
                  active _sifo_base_expenses object

        """
        return self._base_expenses

    @base_expenses.setter
    def base_expenses(self, new_base_expenses: dict):
        """
        base expenses setter

        Parameters
        ----------
        new_base_expenses   : dict
                              new base expense to set

        """
        Assertor.assert_data_types([new_base_expenses], [dict])
        self._base_expenses = new_base_expenses

    @property
    def expenses_shares(self):
        """
        shares of expenses getter

        Returns
        -------
        out     : dict
                  active _expenses_shares

        """
        return self._expenses_shares

    @expenses_shares.setter
    def expenses_shares(self, new_expenses_shares: dict):
        """
        expenses shares setter

        Parameters
        ----------
        new_expenses_shares : dict
                              new expenses shares to set

        """
        Assertor.assert_data_types([new_expenses_shares], [dict])
        self._expenses_shares = new_expenses_shares

    def input_operation(self, data: dict):
        """
        method for retrieving information from SIFO form and saving it to sifo workflow

        Parameters
        ----------
        data        : dict
                      data sent in to workflow

        Returns
        -------
        out         : dict
                      data saved to object

        """
        input_operation = InputOperation("SIFO Form Data")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="SIFO Form Data")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

        return data

    def validate_family(self, data: dict):
        """
        method for validating family information

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
        populate_operation = ValidateFamily(data)
        self.add_node(populate_operation)
        self.add_transition(self.get_signal("input_signal"), populate_operation)

        family = populate_operation.run()
        populate_signal = Signal(family, "Validated Family Information")
        self.add_signal(populate_signal, "validated_family")

        self.add_transition(populate_operation, populate_signal)
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
        sifo_scraper_operation = ScrapeSifoBaseExpenses(data)
        self.add_node(sifo_scraper_operation)

        self.add_transition(self.get_signal("validated_family"), sifo_scraper_operation)

        sifo_base_expenses = Expenses(sifo_scraper_operation.run())
        sifo_base_expenses_signal = Signal(sifo_base_expenses.verdi, "SIFO Base Expenses")
        self.add_signal(sifo_base_expenses_signal, "sifo_base_expenses")

        self.add_transition(sifo_scraper_operation, sifo_base_expenses_signal)
        return sifo_base_expenses.verdi

    def extract(self, data: dict):
        """
        method for extracting the total monthly expenses from SIFO dict

        Parameters
        ----------
        data     : dict
                   dictionary with SIFO base expenses

        Returns
        -------
        out     : dict
                  dictionary with total monthly expenses

        """
        Assertor.assert_data_types([data], [dict])
        extract_total_operation = Extract(data, "totalt")
        self.add_node(extract_total_operation)

        self.add_transition(self.get_signal("sifo_base_expenses"), extract_total_operation)

        total_expenses = extract_total_operation.run()
        total_expenses_signal = Signal(total_expenses, "Total Monthly Expenses")
        self.add_signal(total_expenses_signal, "total_monthly_expenses")

        self.add_transition(extract_total_operation, total_expenses_signal)
        return total_expenses

    def divide(self, data: dict):
        """
        method for calculating shares of total expenses

        Parameters
        ----------
        data     : dict
                   dictionary with SIFO base expenses

        Returns
        -------
        out     : dict
                  dictionary with shares of total monthly expenses

        """
        Assertor.assert_data_types([data], [dict])
        total_expenses = self.extract(data)
        total_shares = Divide(data, total_expenses,
                              "id: Calculate Shares of Total Monthly Expenses")
        self.add_node(total_shares)

        self.add_transition(self.get_signal("total_monthly_expenses"), total_shares,
                            label="divisor")
        self.add_transition(self.get_signal("sifo_base_expenses"), total_shares, label="quantity")

        expenses_shares = total_shares.run()
        expenses_shares_signal = Signal(expenses_shares, "Shares of Total Monthly Expenses")
        self.add_signal(expenses_shares_signal, "share_of_total")

        self.add_transition(total_shares, expenses_shares_signal)
        return expenses_shares

    def output_operation(self):
        """
        final method call in workflow

        """
        base_expenses = self.scrape_sifo_base_expenses(self.family)
        self.base_expenses = base_expenses

        expenses_shares = self.divide(self.base_expenses)
        self.expenses_shares = expenses_shares

        output_operation = OutputOperation(
            decs="id: SIFO Base Expenses and Shares of Total Monthly Expenses")
        self.add_node(output_operation)

        self.add_transition(self.get_signal("share_of_total"), output_operation)
        self.add_transition(self.get_signal("sifo_base_expenses"), output_operation)

        self.add_signal(OutputSignal(base_expenses, "SIFO Base Expenses"), "output_base_expenses")
        self.add_signal(OutputSignal(expenses_shares, "Shares of Total Monthly Expenses"),
                        "output_shares")

        self.add_transition(output_operation, self.get_signal("output_base_expenses"))
        self.add_transition(output_operation, self.get_signal("output_shares"))
