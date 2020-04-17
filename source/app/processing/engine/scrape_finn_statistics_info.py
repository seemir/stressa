# -*- coding: utf-8 -*-
"""
Module with logic for the Scrape Finn Statistics information

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from ...scrapers import FinnStat, FINN_STAT_URL

from .operation import Operation


class ScrapeFinnStatisticsInfo(Operation):
    """
    Operation that scrapes Finn Statistics history information

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        finn_code       : str
                          finn_code for ad to scrape information from

        """
        Assertor.assert_data_types([finn_code], [str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name,
                         desc="from: '{}\\<[finn_code]\\>' \\n id: Scrape FINN Statistics "
                              "Info".format(FINN_STAT_URL))
        self.finn_code = finn_code

    def run(self):
        """
        method for running the operation

        Returns
        -------
        dict        : dict
                      dictionary with all finn statitics information

        """
        finn_stat_info = FinnStat(self.finn_code)
        return finn_stat_info.housing_stat_information()
