# -*- coding: utf-8 -*-

"""
Module for operation for validating restructure information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking
from source.domain import Mortgage

from .operation import Operation


class ValidateRestructure(Operation):
    """
    Implementation of Validate Restructure operation

    """

    @Tracking
    def __init__(self, restructure_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        restructure_data       : dict
                              mortgage data to be validated

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([restructure_data], [dict])
        super().__init__(name=self.name,
                         desc="rules: {} \\n id: Validate Restructure Information".format(
                             Mortgage.rules(restructure=True)))
        self.mortgage_data = restructure_data

    @Tracking
    def run(self):
        """
        method for running validate restructure operation

        Returns
        -------
        out                 : dict
                              Mortgage object with validated restructure information

        """
        mortgage = Mortgage(self.mortgage_data, restructure=True)
        return mortgage.restructure_data
