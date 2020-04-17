# -*- coding: utf-8 -*-
"""
Module with logic for the Scrape Finn advert information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from ...scrapers import FinnAd, FINN_AD_URL

from .operation import Operation


class ScrapeFinnAdvertInfo(Operation):
    """
    Operation that scrapes Finn advert information

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        finn_code       : str
                          finn_code for advert to scrape information from

        """
        Assertor.assert_data_types([finn_code], [str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name,
                         desc="from: '{}\\<[finn_code]\\>' \\n id: Scrape FINN Advert Info".format(
                             FINN_AD_URL))
        self.finn_code = finn_code

    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : dict
                      dictionary with all finn advert information

        """
        finn_ad_info = FinnAd(self.finn_code)
        return finn_ad_info.housing_ad_information()
