# -*- coding: utf-8 -*-

"""
Module with logic for the Expenses entity

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from source.util import Assertor, LOGGER

from .share import Share
from .entity import Entity
from .money import Money


class Expenses(Entity):
    """
    Implementation of the Expenses entity

    """

    @staticmethod
    def extract_expenses_data_and_shares(data: dict):
        """
        method for extracting expenses (nok) and shares (%) of expenses in sifo data

        Parameters
        ----------
        data    : dict
                  dictionary of sifo expenses

        Returns
        -------
        out     : dict
                  dictionary of sifo expenses as percentage of total and nok

        """
        LOGGER.info(
            "'{}' for '{}'".format(Expenses.extract_expenses_data_and_shares.__name__,
                                   Expenses.__name__))
        LOGGER.disable("source.domain")
        keys = list(data.keys())
        values = [Money(val) if val != "0" else Money("0") for val in list(data.values())]
        shares = [Share(val, values[-1]).value if val != Money("0") else Share(Decimal(1)).value for
                  val in values]
        LOGGER.enable("source.domain")
        return dict(zip(keys, [val.value() for val in values])), dict(zip(keys, shares))

    def __init__(self, data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        data    : dict
                  dictionary of sifo expenses data

        """
        try:
            super(Expenses, self).__init__()
            Assertor.assert_data_types([data], [dict])
            self._expenses = self.extract_expenses_data_and_shares(data)
            self._expenses_values = self.expenses[0]
            self._expenses_shares = self.expenses[1]
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id))
        except Exception as sifo_expenses_error:
            LOGGER.exception(sifo_expenses_error)
            raise sifo_expenses_error

    @property
    def expenses(self):
        """
        expenses getter

        Returns
        -------
        out     : dict
                  dictionary of expenses as nok and percent

        """
        return self._expenses

    @property
    def expenses_values(self):
        """
        expenses as nok getter

        Returns
        -------
        out     : dict
                  dictionary of expenses as nok

        """
        return self._expenses_values

    @property
    def expenses_shares(self):
        """
        expenses as percent getter

        Returns
        -------
        out     : dict
                  dictionary of expenses as percent of total

        """
        return self._expenses_shares
