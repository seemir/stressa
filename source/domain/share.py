# -*- coding: utf-8 -*-

"""
Module for the Share Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal
from typing import Union

from source.util import LOGGER, Assertor

from .percent import Percent
from .value import Value
from .money import Money


class Share(Value):
    """
    Implementation of the Share Value object

    """

    def __init__(self, numerator: Union[Decimal, Money],
                 denominator: Union[Decimal, Money] = None):
        """
        Constructor / instantiation

        Parameters
        ----------
        numerator   : Decimal, Money
                      numerator of the share object
        denominator : Decimal, Money
                      denominator of the share object

        """
        try:
            Assertor.assert_data_types([numerator, denominator],
                                       [(Decimal, Money), (Decimal, Money, type(None))])
            super().__init__()
            self._numerator = numerator
            self._denominator = denominator
            self._percent = Percent(numerator / denominator) if self.denominator else Percent("0")
            self._value = self._percent.value
            LOGGER.success(
                "created '{}' -> {}".format(self.__class__.__name__, self.value))
        except Exception as share_error:
            LOGGER.exception(share_error)
            raise share_error

    @property
    def numerator(self):
        """
        numerator getter

        Returns
        -------
        out     : Decimal, Money
                  active numerator in object

        """
        return self._numerator

    @property
    def denominator(self):
        """
        denominator getter

        Returns
        -------
        out     : Decimal, Money
                  active denominator in object

        """
        return self._denominator

    @property
    def value(self):
        """
        percent value getter

        Returns
        -------
        out     : str
                  active percent getter

        """
        return self._value
