# -*- coding: utf-8 -*-
"""
Module with logic for the Finn Statistics information connector

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from ...connectors import FinnStat, FINN_STAT_URL

from .operation import Operation


class FinnStatisticsInfoConnector(Operation):
    """
    Operation that retrieves Finn Statistics history information

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
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(name=self.__class__.__name__,
                         desc=f"from: '{FINN_STAT_URL}\\<[finn_code]\\>' \\n id: FINN Statistics "
                              "Info Connector")
        self.finn_code = finn_code

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        dict        : dict
                      dictionary with all finn statistics information

        """
        finn_stat_info = FinnStat(self.finn_code)
        return finn_stat_info.housing_stat_information()
