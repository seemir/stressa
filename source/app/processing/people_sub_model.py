# -*- coding: utf-8 -*-
"""
Module with the logic for the People sub-model

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking, Debugger

from .people_data_processing import PeopleDataProcessing
from .engine import SubModel


class PeopleSubModel(SubModel):
    """
    Sub model that handles the PeopleDataProcess

    """

    @Tracking
    def __init__(self, people_data: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        people_data      : dict
                           dict with people statistics

        """
        Assertor.assert_data_types([people_data], [dict])
        self.name = PeopleDataProcessing.__name__
        super().__init__(name=self.name, desc="Processing Finn People Statistics")
        self.people_data = people_data

    @Debugger
    def run(self):
        """
        method for running the sub model

        """
        return PeopleDataProcessing(self.people_data).people_statistics
