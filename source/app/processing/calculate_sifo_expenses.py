# -*- coding: utf-8 -*-

"""
Process for calculating Sifo expenses

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.domain import Expenses
from source.util import Assertor, Profiling, LOGGER

from .engine import Process, Signal, ValidateFamily, ScrapeSifoBaseExpenses, Extract, Divide, \
    OutputOperation, OutputSignal, InputOperation


class CalculateSifoExpenses(Process):
    """
    Process for the calculation of the SIFO expenses with shares of total expenses

    """

    def __init__(self, data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data    : dict
                  information about the family, i.e. arguments to be passed to Family object

        """
        try:
            self.start_process()
            super().__init__(name=self.__class__.__name__)
            Assertor.assert_data_types([data], [dict])
            self.input_operation({"data": data})
            self.validate_family()
            self._base_expenses = self.scrape_sifo_base_expenses()
            self.extract()
            self._expenses_shares = self.divide()
            self.output_operation()
            self.end_process()
        except Exception as sifo_processing_error:
            LOGGER.exception(sifo_processing_error)
            raise sifo_processing_error

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

    @Profiling
    def input_operation(self, data: dict):
        """
        method for retrieving information from SIFO form and saving it to sifo processing object

        Parameters
        ----------
        data        : dict
                      data sent in to process

        """
        Assertor.assert_data_types([data], [dict])
        input_operation = InputOperation("SIFO Form Data")
        self.add_node(input_operation)

        input_signal = Signal(data, desc="SIFO Form Data")
        self.add_signal(input_signal, "input_signal")

        self.add_transition(input_operation, input_signal)

    @Profiling
    def validate_family(self):
        """
        method for validating family information

        """
        input_signal = self.get_signal("input_signal")
        populate_operation = ValidateFamily(input_signal.data["data"])
        self.add_node(populate_operation)
        self.add_transition(input_signal, populate_operation)

        family = populate_operation.run()
        populate_signal = Signal(family, "Validated Family Information")
        self.add_signal(populate_signal, "validated_family")

        self.add_transition(populate_operation, populate_signal)

    @Profiling
    def scrape_sifo_base_expenses(self):
        """
        method for scraping SIFO base expenses

        Returns
        -------
        out     : dict
                  dictionary with SIFO base expenses

        """
        validated_family = self.get_signal("validated_family")
        sifo_scraper_operation = ScrapeSifoBaseExpenses(validated_family.data)
        self.add_node(sifo_scraper_operation)

        self.add_transition(validated_family, sifo_scraper_operation)

        sifo_base_expenses = Expenses(sifo_scraper_operation.run())
        sifo_base_expenses_signal = Signal(sifo_base_expenses.verdi, "SIFO Base Expenses",
                                           prettify_keys=True, length=10)
        self.add_signal(sifo_base_expenses_signal, "sifo_base_expenses")

        self.add_transition(sifo_scraper_operation, sifo_base_expenses_signal)
        return sifo_base_expenses.verdi

    @Profiling
    def extract(self):
        """
        method for extracting the total monthly expenses from SIFO dict

        """
        extract_total_operation = Extract(self.base_expenses, "totalt")
        self.add_node(extract_total_operation)

        self.add_transition(self.get_signal("sifo_base_expenses"), extract_total_operation)

        total_expenses = extract_total_operation.run()
        total_expenses_signal = Signal(total_expenses, "Total Monthly Expenses")
        self.add_signal(total_expenses_signal, "total_monthly_expenses")

        self.add_transition(extract_total_operation, total_expenses_signal)

    @Profiling
    def divide(self):
        """
        method for calculating shares of total expenses

        Returns
        -------
        out     : dict
                  dictionary with shares of total monthly expenses

        """

        total_shares = Divide(self.base_expenses, self.get_signal("total_monthly_expenses").data,
                              "Calculate Shares of Total Monthly Expenses")
        self.add_node(total_shares)

        self.add_transition(self.get_signal("total_monthly_expenses"), total_shares,
                            label="divisor")
        self.add_transition(self.get_signal("sifo_base_expenses"), total_shares, label="quantity")

        expenses_shares = total_shares.run()
        expenses_shares_signal = Signal(expenses_shares, "Shares of Total Monthly Expenses",
                                        prettify_keys=True, length=10)
        self.add_signal(expenses_shares_signal, "share_of_total")

        self.add_transition(total_shares, expenses_shares_signal)
        return expenses_shares

    @Profiling
    def output_operation(self):
        """
        final method call in process

        """
        output_operation = OutputOperation(
            desc="SIFO Base Expenses and Shares of Total Monthly Expenses")
        self.add_node(output_operation)

        self.add_transition(self.get_signal("share_of_total"), output_operation)
        self.add_transition(self.get_signal("sifo_base_expenses"), output_operation)

        self.add_signal(OutputSignal(self._base_expenses, "SIFO Base Expenses", prettify_keys=True,
                                     length=10), "output_base_expenses")
        self.add_signal(
            OutputSignal(self._expenses_shares, "Shares of Total Monthly Expenses",
                         prettify_keys=True, length=10), "output_shares")

        self.add_transition(output_operation, self.get_signal("output_base_expenses"))
        self.add_transition(output_operation, self.get_signal("output_shares"))
