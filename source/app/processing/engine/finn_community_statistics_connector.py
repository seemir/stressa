# -*- coding: utf-8 -*-
"""
Module with logic for the Finn Community Statistics connector

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from .operation import Operation

from ...connectors import FinnCommunity, FINN_COMMUNITY_URL


class FinnCommunityStatisticsConnector(Operation):
    """
    Operation that retrieves Finn Community Statistics

    """

    @Tracking
    def __init__(self, finn_code: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        finn_code       : str
                          finn_code of ad to retrieve Statistics from

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(name=self.name,
                         desc="from: '{}\\<[finn_code]\\>' \\n id: FINN Community"
                              "Statistics Connector".format(FINN_COMMUNITY_URL))
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
        finn_community_statistics = FinnCommunity(self.finn_code)
        return finn_community_statistics.community_stat_information()
