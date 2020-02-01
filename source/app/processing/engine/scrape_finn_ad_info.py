# -*- coding: utf-8 -*-
"""
Module with logic for the Scrape Finn Ad information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.app.scrapers import FinnAd, FINN_AD_URL
from source.util import Assertor

from .operation import Operation


class ScrapeFinnAdInfo(Operation):
    """
    Operation that scrapes Finn Ad information

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
                         desc="from: '{}\\<[finn_code]\\>' \\n id: Scrape FINN Ad Info".format(
                             FINN_AD_URL))
        self.finn_code = finn_code

    def run(self):
        """
        method for running the operation

        Returns
        -------
        dict        : dict
                      dictionary with all finn ad information

        """
        finn_ad_info = FinnAd(self.finn_code)
        return finn_ad_info.housing_ad_information()
