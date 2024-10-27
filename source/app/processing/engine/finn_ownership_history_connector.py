# -*- coding: utf-8 -*-
"""
Module with logic for the Finn Ownership history information connector

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from ...connectors import FinnOwnership, FINN_OWNER_URL

from .operation import Operation


class FinnOwnershipHistoryConnector(Operation):
    """
    Operation that retrieve Finn Ownership history information

    """

    @Tracking
    def __init__(self, finn_code: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        finn_code       : str
                          finn_code for ad to retrieve information from

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(name=self.__class__.__name__,
                         desc=f"from: '{FINN_OWNER_URL}\\<[finn_code]\\>' \\n id: FINN Ownership "
                              "History Connector")
        self.finn_code = finn_code

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        dict        : dict
                      dictionary with all finn ownership information

        """
        finn_owner_history = FinnOwnership(self.finn_code)
        return finn_owner_history.housing_ownership_information()
