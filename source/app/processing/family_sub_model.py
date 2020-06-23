# -*- coding: utf-8 -*-
"""
Module with the logic for the Family sub-model

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Debugger

from .family_data_processing import FamilyDataProcessing
from .engine import SubModel


class FamilySubModel(SubModel):
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
        self.name = FamilyDataProcessing.__name__
        super().__init__(name=self.name, desc="Processing Finn Family Statistics")
        self.family_data = family_data

    @Debugger
    def run(self):
        """
        method for running the sub model

        """
        return FamilyDataProcessing(self.family_data).family_statistics
