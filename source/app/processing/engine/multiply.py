# -*- coding: utf-8 -*-
"""
Module with the Divide operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from source.domain import Amount, Money
from source.util import Assertor, Tracking

from .operation import Operation


class Multiply(Operation):
    """
    Operation for multiply two signals (assuming one is a factor)

    """

    @Tracking
    def __init__(self, factor_1: dict, factor_2: dict, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        factor_1     : dict
                       quantity
        factor_2     : dict
                       divisor assumed to be of length one
        desc         : str
                       description

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([factor_1, factor_2, desc], [dict, dict, str])
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.factor_1 = factor_1
        self.factor_2 = factor_2

    @Tracking
    def run(self, money=False, rnd=2):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with multiple

        """
        multiple = {}
        factor_2 = Decimal(
            str(list(self.factor_2.values())[0]).replace(" ", "").replace("kr", ""))
        for key, val in self.factor_1.items():
            num = Decimal(val.replace(" ", "").replace("kr", ""))

            base = round(float(str(Amount(str(num)) * Amount(str(factor_2))).replace(" ", "")), rnd)
            multiply = str(base) if not money else Money(str(int(base))).value()
            multiple.update({key: multiply})

        return multiple
