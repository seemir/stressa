# -*- coding: utf-8 -*-
"""
Module for generating Fixed Payment Plan

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.util import Tracking, Assertor
from source.domain import PaymentPlan

from .operation import Operation


class GenerateFixedPaymentPlan(Operation):
    """
    Operation for generating Fixed Payment Plan

    """

    @Tracking
    def __init__(self, interest_rate: Union[str, float], period: Union[str, int],
                 interval: Union[str, int], amount: Union[str, float], start_date: str):
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
        start_date          : str
                              start_date for mortgage plan

        """
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc="id: Generate Fixed Mortgage\n Payment Plan")
        Assertor.assert_data_types([interest_rate, period, interval, amount, start_date],
                                   [(str, float), (str, int), (str, int), (str, float), str])
        self.interest_rate = interest_rate
        self.period = period
        self.interval = interval
        self.amount = amount
        self.start_date = start_date

    @Tracking
    def run(self):
        """
        method for running the operation

        """
        fixed_plan = PaymentPlan(self.interest_rate, self.interval, self.period, self.amount,
                                 self.start_date)
        return fixed_plan.fixed_mortgage_plan()
