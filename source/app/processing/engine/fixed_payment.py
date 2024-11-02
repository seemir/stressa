# -*- coding: utf-8 -*-
"""
Module with operation for calculating amount with fixed rate

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.util import Assertor, Tracking
from source.domain import FixedRate, Money

from .operation import Operation


class FixedPayment(Operation):
    """
    Operation for calculating amount with fixed rate

    """

    @Tracking
    def __init__(self, interest_rate: Union[str, float], period: Union[str, int],
                 interval: Union[str, int], amount: Union[str, float]):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        interest_rate       : str, float
                              interest rate
        period              : str, int
                              period of mortgage
        interval            : str, int
                              interval for the mortgage
        amount              : str, float
                              amount to borrow

        """
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc="id: Calculation of Fixed Amount")
        Assertor.assert_data_types([interest_rate, period, interval, amount],
                                   [(str, float), (str, int), (str, int), (str, float)])
        self.interest_rate = interest_rate
        self.period = period
        self.interval = interval
        self.amount = amount

    @Tracking
    def run(self):
        """
        method for running the operation

        """
        fixed_amount = FixedRate.periodical_payments(self.interest_rate, self.interval, self.period,
                                                     self.amount)
        return {"krav_betjeningsevne": Money(str(fixed_amount)).value()}
