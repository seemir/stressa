# -*- coding: utf-8 -*-
"""
Module with logic for the Transportation sub-model

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Debugger

from .finn_transportation_process import FinnTransportationProcess
from .engine import SubModel


class FinnTransportationSubModel(SubModel):
    """
    Sub model that handles the Transportation statistics from Finn ads

    """

    @Tracking
    def __init__(self, transportation_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        transportation_data     : dict
                                  dict with transportation statistics

        """
        Assertor.assert_data_types([transportation_data], [dict])
        self.name = FinnTransportationProcess.__name__
        super().__init__(name=self.name, desc="Processing Finn Transportation Statistics")
        self.transportation_data = transportation_data

    @Debugger
    def run(self):
        """
        method for running the transportation sub model

        """
        finn_transportation_processing = FinnTransportationProcess(self.transportation_data)
        return finn_transportation_processing.transportation_statistics
