# -*- coding: utf-8 -*-
"""
Module with the Converter operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from source.domain import Money
from source.util import Assertor, Tracking

from .operation import Operation


class Converter(Operation):
    """
    Operation for converter amount to various periodic amounts

    """
    interval_mapping = {"Årlig": 1, "Halvårlig": 2, "Kvartalsvis": 4, "Annenhver måned": 6,
                        "Månedlig": 12, "Semi-månedlig": 24, "Annenhver uke": 26, "Ukentlig": 52}

    @Tracking
    def __init__(self, amount: dict, convert_from: str, convert_to: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        amount          : dict
                          amount to be converted
        convert_from    : str
                          period to convert from
        convert_to      : str
                          period to convert to

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([amount, convert_from, convert_to], [dict, str, str])
        super().__init__(name=self.name,
                         desc=f"id: Convert amount \n from '{convert_from}' to '{convert_to}'")
        self.amount = amount
        self.convert_from = self.interval_mapping[convert_from]
        self.convert_to = self.interval_mapping[convert_to]

    @Tracking
    def run(self, rnd=0):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with shares

        """
        results = {}
        for key, val in self.amount.items():
            converted_value = (Decimal(val.replace(" ", "").replace("kr", "")) * Decimal(
                self.convert_from)) / Decimal(self.convert_to)
            results.update({key: Money(str(int(round(float(converted_value), rnd)))).value()})
        return results
