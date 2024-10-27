# -*- coding: utf-8 -*-
"""
Module with the Divide operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from source.domain import Share, Amount, Money
from source.util import Assertor, Tracking

from .operation import Operation


class Division(Operation):
    """
    Operation for dividing two signals (assuming one is a factor)

    """

    @Tracking
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
        self.name = self.__class__.__name__
        Assertor.assert_data_types([numerator, denominator, desc], [dict, dict, str])
        super().__init__(name=self.name, desc=f"id: {desc}")
        self.numerator = numerator
        self.denominator = denominator

    @Tracking
    def run(self, percent=True, money=False, rnd=2):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with shares

        """
        shares = {}
        den = Decimal(
            str(list(self.denominator.values())
                [0]).replace(" ", "").replace("kr", "").replace("%", ""))
        den = den if den != 0 else Decimal("1")

        for key, val in self.numerator.items():
            num = Decimal(val.replace(" ", "").replace("kr", "").replace("%", ""))

            base = round(float(str(Amount(str(num)) / Amount(str(den))).replace(" ", "")), rnd)
            ration = str(base) if not money else Money(str(int(base))).value()
            shares.update(
                {key: Share(num, den).value if percent else ration})

        return shares
