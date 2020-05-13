# -*- coding: utf-8 -*-

"""
Module with logic for currency value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import InvalidCurrencyError, Assertor, Tracking

from .value import Value


class Currency(Value):
    """
    Implementation of currency value object

    """

    @Tracking
    def validate_currency(self, currency: str):
        """
        method for validating currency string

        Parameters
        ----------
        currency    : str
                      string to be validated

        """
        if currency not in ["kr"]:
            raise InvalidCurrencyError(
                "'{}' is an unsupported currency".format(currency))

    def __init__(self, currency: str = "kr"):
        """
        constructor / instantiating of class

        Parameters
        ----------
        currency    : str
                      currency string

        """
        try:
            super().__init__()
            Assertor.assert_data_types([currency], [str])
            self.validate_currency(currency)
            self._currency = currency.lower()
        except Exception as currency_exception:
            raise currency_exception

    @property
    def currency(self):
        """
        currency getter

        Returns
        -------
        out     : str
                  active currency

        """
        return self._currency

    @currency.setter
    def currency(self, new_currency: str):
        """
        currency setter

        Parameters
        ----------
        new_currency    : str
                          new currency to be set

        """
        Assertor.assert_data_types([new_currency], [str])
        self.validate_currency(new_currency)
        self._currency = new_currency.lower()
