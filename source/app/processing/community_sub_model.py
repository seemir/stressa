# -*- coding: utf-8 -*-
"""
Module with the logic for the Community sub-process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.app.processing.engine.sub_model import SubModel
from .finn_community_process import FinnCommunityProcess


class CommunitySubModel(SubModel):
    """
    Sub model that handles the FinnCommunityProcess

    """

    def __init__(self, community_json: dict):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        community_json      : dict
                              JSON object as dict with community statistics

        """
        self.name = FinnCommunityProcess.__name__
        super().__init__(name=self.name, desc="Processing Community Data / Statistics")
        self.community_json = community_json

    def run(self):
        """
        method for running the sub model

        """
        finn_community_process = FinnCommunityProcess(self.community_json)
        finn_community_process.print_pdf()
