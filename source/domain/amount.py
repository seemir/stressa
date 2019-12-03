# -*- coding: utf-8 -*-

"""
Module for the Amount Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re
from decimal import Decimal, InvalidOperation

from source.util import Assertor, InvalidAmountError, LOGGER

from .value import Value


class Amount(Value):
    """
    Amount value object implementation

    """

    @staticmethod
    def validate_amount(amount: str):
        """
        method for validating an amount

        Parameters
        ----------
        amount      : str
                      amount to be validated

        """
        valid_amount = re.compile(r"[0-9]").search(amount.lower())
        if not valid_amount:
            raise InvalidAmountError("'{}' is an invalid amount".format(amount))

    @staticmethod
    def format_amount(amount: str):
        """
        method for formatting an amount with thousand spacing

        Parameters
        ----------
        amount

        Returns
        -------
        out         : str
                      formatted amount with thousand separator

        """
        try:
            amount = Decimal(amount)
            return '{:,}'.format(amount).replace(',', ' ')
        except InvalidOperation as format_error:
            raise InvalidAmountError(
                "'{}' is an invalid amount, exited with '{}'".format(amount, format_error))

    def __init__(self, amount: str):
        """
        Constructor / instantiating class

        Parameters
        ----------
        amount  : str
                  amount in str representation

        """
        try:
            super().__init__()
            Assertor.assert_data_types([amount], [str])
            self.validate_amount(amount)
            self._amount = self.format_amount(amount)
            LOGGER.success(
                "created '{}'".format(self.__class__.__name__))
        except Exception as amount_exception:
            LOGGER.exception(amount_exception)
            raise amount_exception

    @property
    def amount(self):
        """
        amount getter

        Returns
        -------
        out         : str
                      active amount in object

        """
        return self._amount

    @amount.setter
    def amount(self, new_amount):
        """
        amount setter

        Parameters
        ----------
        new_amount  : str
                      new string to be set

        """
        Assertor.assert_data_types([new_amount], [str])
        self.validate_amount(new_amount)
        self._amount = self.format_amount(new_amount)

    def __add__(self, other):
        """
        addition helper method

        Parameters
        ----------
        other       : Amount
                      other Amount object

        Returns
        -------
        out         : str
                      sum of amount in object and amount in other object

        """
        Assertor.assert_data_types([other], [type(self)])
        return self.format_amount(
            str(Decimal(self.amount.replace(" ", "")) + Decimal(other.amount.replace(" ", ""))))

    def __sub__(self, other):
        """
        subtraction helper method

        Parameters
        ----------
        other   : Amount
                  other Amount object

        Returns
        -------
        out     : str
                  amount in object subtracted from amount in other object

        """
        Assertor.assert_data_types([other], [type(self)])
        return self.format_amount(
            str(Decimal(self.amount.replace(" ", "")) - Decimal(other.amount.replace(" ", ""))))

    def __mul__(self, other):
        """
        multiplication helper method

        Parameters
        ----------
        other   : Amount
                  other Amount object

        Returns
        -------
        out     : str
                  amount in object multiplication with amount in other object

        """
        Assertor.assert_data_types([other], [type(self)])
        return self.format_amount(
            str(Decimal(self.amount.replace(" ", "")) * Decimal(other.amount.replace(" ", ""))))

    def __truediv__(self, other):
        """
        division helper method

        Parameters
        ----------
        other   : Amount
                  other Amount object

        Returns
        -------
        out     : str
                  amount in object divided with amount in other object

        """
        Assertor.assert_data_types([other], [type(self)])
        return self.format_amount(
            str(Decimal(self.amount.replace(" ", "")) / Decimal(other.amount.replace(" ", ""))))
