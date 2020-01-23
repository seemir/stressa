# -*- coding: utf-8 -*-

"""
Module with logic for the Expenses entity

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from .entity import Entity
from .money import Money


class Expenses(Entity):
    """
    Implementation of the Expenses entity

    """

    @staticmethod
    def cast_expenses(data: dict):
        """
        method for making expenses (NOK)

        Parameters
        ----------
        data    : dict
                  dictionary of sifo expenses

        Returns
        -------
        out     : dict
                  dictionary of sifo expenses as nok

        """
        keys = list(data.keys())
        values = [Money(val) if val != "0" else Money("0") for val in list(data.values())]
        return dict(zip(keys, [val.value() for val in values]))

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
            self._verdi = self.cast_expenses(data)
        except Exception as sifo_expenses_error:
            raise sifo_expenses_error

    @property
    def verdi(self):
        """
        Value getter

        Returns
        -------
        out     : dict
                  active value dictionary in object

        """
        return self._verdi
