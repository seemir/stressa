# -*- coding: utf-8 -*-
"""
Module with operation for stress testing with fixed rate

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking
from source.domain import FixedRate

from .operation import Operation


class FixedStressTest(Operation):
    """
    Operation for stress testing with fixed rate

    """

    @Tracking
    def __init__(self, mortgage_data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        mortgage_data        : dict
                               mortgage data

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([mortgage_data], [dict])
        super().__init__(name=self.name, desc="id: Fixed Stress Test")
        self.mortgage_data = mortgage_data

    @Tracking
    def run(self):
        """
        method for running the operation

        """
        fixed_rate = FixedRate(self.mortgage_data)
        return {"stresstest_annuitet": fixed_rate.calculate_stress_rate()}
