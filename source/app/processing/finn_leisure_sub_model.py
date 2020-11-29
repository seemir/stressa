# -*- coding: utf-8 -*-
"""
Module with logic for sub-model for Leisure Statistics in relation to an advert

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Debugger

from .finn_leisure_processing import FinnLeisureProcessing
from .engine import SubModel


class FinnLeisureSubModel(SubModel):
    """
    Sum-model that handles the Leisure statistics in relation to a real-estate on Finn

    """

    @Tracking
    def __init__(self, leisure_data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        leisure_data        : dict
                              dictionary with leisure statistics

        """
        Assertor.assert_data_types([leisure_data], [dict])
        self.name = FinnLeisureProcessing.__name__
        super().__init__(name=self.name, desc="Processing Finn Leisure Statistics")
        self.leisure_data = leisure_data

    @Debugger
    def run(self):
        """
        method for running the sub model

        """
        finn_leisure_processing = FinnLeisureProcessing(self.leisure_data)
        return finn_leisure_processing.leisure_statistics
