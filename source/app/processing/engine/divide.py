# -*- coding: utf-8 -*-
"""
Module with the Divide operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from source.domain import Share
from source.util import Assertor

from .operation import Operation


class Divide(Operation):
    """
    Operation for dividing two signals (assuming one is a factor)

    """

    def __init__(self, numerator: dict, denominator: dict, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        numerator       : dict
                          quantity
        denominator     : dict
                          divisor assumed to be of length one
        desc            : str
                          description

        """
        Assertor.assert_data_types([numerator, denominator, desc], [dict, dict, str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.numerator = numerator
        self.denominator = denominator

    def run(self):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with shares

        """
        shares = {}
        den = Decimal(str(list(self.denominator.values())[0]).replace(" ", "").replace("kr", ""))
        for key, val in self.numerator.items():
            num = Decimal(val.replace(" ", "").replace("kr", ""))
            shares.update({key: Share(num, den).value})
        return shares
