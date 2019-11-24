# -*- coding: utf-8 -*-

"""
Module with logic for Money value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, LOGGER

from .currency import Currency
from .amount import Amount
from .value import Value


class Money(Value):
    """
    Money value object implementation

    """

    def __init__(self, amount: str):
        """
        Constructor / instantiating class

        Parameters
        ----------
        amount  : str
                  amount string

        """
        try:
            super().__init__()
            Assertor.assert_data_types([amount], [str])
            self._amount = Amount(amount)
            self._currency = Currency()
            LOGGER.success(
                "created '{}' -> {}".format(self.__class__.__name__, self.value()))
        except Exception as amount_error:
            LOGGER.exception(amount_error)
            raise amount_error

    @property
    def amount(self):
        """
        amount getter

        Returns
        -------
        out     : str
                  active amount in object

        """
        return self._amount.amount

    @amount.setter
    def amount(self, new_amount: str):
        """
        amount setter

        Parameters
        ----------
        new_amount  : str
                      new amount to set

        """
        Assertor.assert_data_types([new_amount], [str])
        self._amount.amount = new_amount

    @property
    def currency(self):
        """
        currency getter

        Returns
        -------
        out         : str
                      active currency in object

        """
        return self._currency.currency

    def value(self):
        """
        money value is defined as the amount + currency

        Returns
        -------
        out         : str
                      amount str concatenated with currency str

        """
        return self.amount + " " + self.currency

    def __add__(self, other):
        """
        addition helper method

        Parameters
        ----------
        other       : Money
                      other money object

        Returns
        -------
        out         : str
                      sum of amount in object and amount in other object

        """
        Assertor.assert_data_types([other], [type(self)])
        return self._amount + other._amount + " " + self.currency

    def __sub__(self, other):
        """
        subtraction helper method

        Parameters
        ----------
        other   : Money
                  other Money object

        Returns
        -------
        out     : str
                  amount in object subtracted from amount in other object

        """
        Assertor.assert_data_types([other], [type(self)])
        return self._amount + other._amount + " " + self.currency
