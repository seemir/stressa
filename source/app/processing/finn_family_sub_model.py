# -*- coding: utf-8 -*-
"""
Module with the logic for the Family sub-model

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Debugger

from .finn_family_data_processing import FinnFamilyDataProcessing
from .engine import SubModel


class FinnFamilySubModel(SubModel):
    """
    Sub model that handles the FamilyDataProcess

    """

    @Tracking
    def __init__(self, family_data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        family_data      : dict
                           dict with family statistics

        """
        Assertor.assert_data_types([family_data], [dict])
        self.name = FinnFamilyDataProcessing.__name__
        super().__init__(name=self.name, desc="Processing Finn Family Statistics")
        self.family_data = family_data

    @Debugger
    def run(self):
        """
        method for running the family data sub model

        """
        return FinnFamilyDataProcessing(self.family_data).family_statistics
