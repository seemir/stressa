# -*- coding: utf-8 -*-

"""
Module for operation for validating mortgage information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking
from source.domain import Mortgage

from .operation import Operation


class ValidateMortgage(Operation):
    """
    Implementation of Validate Mortgage operation

    """

    @Tracking
    def __init__(self, mortgage_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        mortgage_data       : dict
                              mortgage data to be validated

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([mortgage_data], [dict])
        super().__init__(name=self.name,
                         desc="rules: {} \\n id: Validate Mortgage Information".format(
                             Mortgage.rules()))
        self.mortgage_data = mortgage_data

    @Tracking
    def run(self):
        """
        method for running validate mortgage operation

        Returns
        -------
        out                 : dict
                              Mortgage object with validated mortgage information

        """
        mortgage = Mortgage(self.mortgage_data)
        return mortgage.mortgage_data
