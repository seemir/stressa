# -*- coding: utf-8 -*-

"""
Module for the Percent Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union
from decimal import Decimal

from source.util import Assertor

from .value import Value


class Percent(Value):
    """
    Implementation of the Percent Value object

    """

    def __init__(self, percentage: Union[Decimal, str]):
        """
        Constructor / instantiating class

        Parameters
        ----------
        percentage  : Decimal, str

        """
        try:
            super().__init__()
            Assertor.assert_data_types([percentage], [(Decimal, str)])
            self._percentage = Decimal(percentage)
            self._value = str(Decimal(self.percentage * 100).quantize(Decimal("0.01"))) + " %"
        except Exception as percent_error:
            raise percent_error

    @property
    def value(self):
        """
        value getter

        Returns
        -------
        out     : str
                  active _value

        """
        return self._value

    @property
    def percentage(self):
        """
        percentage getter

        Returns
        -------
        out     : Decimal
                  active _percentage

        """
        return self._percentage
