# -*- coding: utf-8 -*-
"""
Module with logic for the Environment sub-process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Debugger

from .finn_environment_process import FinnEnvironmentProcess
from .engine import SubModel


class FinnEnvironmentSubModel(SubModel):
    """
    Implementation of Handler for Environmental statistics

    """

    @Tracking
    def __init__(self, environmental_data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        environmental_data      : dict
                                  dict with family statistics

        """
        Assertor.assert_data_types([environmental_data], [dict])
        self.name = FinnEnvironmentSubModel.__name__
        super().__init__(name=self.name, desc="Processing Finn Environmental Statistics")
        self.environmental_data = environmental_data

    @Debugger
    def run(self):
        """
        method for running the environmental data sub model

        """
        return FinnEnvironmentProcess(self.environmental_data).environment_statistics
