# -*- coding: utf-8 -*-
"""
Module with the logic for the Community sub-process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.util import Assertor, Tracking, Debugger

from .engine import SubModel
from .finn_community_process import FinnCommunityProcess


class FinnCommunitySubModel(SubModel):
    """
    Sub model that handles the FinnCommunityProcess

    """

    @Tracking
    def __init__(self, community_json: Union[dict, type(None)]):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        community_json      : dict
                              JSON object as dict with community statistics

        """
        Assertor.assert_data_types([community_json], [(dict, type(None))])
        self.name = FinnCommunityProcess.__name__
        super().__init__(name=self.name, desc="Processing Finn Community Statistics")
        self.community_json = community_json

    @Debugger
    def run(self):
        """
        method for running the sub model

        """
        community_data = None
        if self.community_json:
            community_data = FinnCommunityProcess(self.community_json).finn_community_statistics
        return community_data
