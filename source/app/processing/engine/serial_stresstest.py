# -*- coding: utf-8 -*-
"""
Module with operation for stress testing with serial rate

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking
from source.domain import Serial

from .operation import Operation


class SerialStressTest(Operation):
    """
    Operation for stress testing with serial rate

    """

    @Tracking
    def __init__(self, mortgage_data: dict):
        """

        Parameters
        ----------
        mortgage_data        : dict
                               mortgage data

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([mortgage_data], [dict])
        super().__init__(name=self.name, desc="id: Serial Stress Test")
        self.mortgage_data = mortgage_data

    @Tracking
    def run(self):
        """
        method for running the operation

        """
        serial = Serial(self.mortgage_data)
        return {"stresstest_serie": serial.calculate_stress_rate()}
