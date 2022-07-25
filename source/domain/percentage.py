# -*- coding: utf-8 -*-

"""
Module for the Percentage Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from source.util import Assertor, Tracking

from .value import Value


class Percentage(Value):
    """
    Implementation of the Percent Value object

    """

    @Tracking
    def validate_percentage(self):
        """
        method for validate percentage value

        """
        value = self._percentage.replace(",", ".").replace("%", "").replace(" ", "")
        try:
            Decimal(value)
        except Exception as percentage_error:
            raise ValueError("'{}' is an invalid percentage, exited with "
                             "'{}'".format(value, percentage_error))
        else:
            return value + " %"

    def __init__(self, percentage: str):
        """
        Constructor / instantiating class

        Parameters
        ----------
        percentage  : Decimal, str

        """
        try:
            super().__init__()
            Assertor.assert_data_types([percentage], [str])
            self._percentage = percentage
        except Exception as percent_error:
            raise percent_error

    def percentage_value(self):
        """
        method for percentage value

        """
        return self.validate_percentage()
