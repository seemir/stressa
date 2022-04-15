# -*- coding: utf-8 -*-
"""
Module with logic for the connector Finn advert information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from ...connectors import FinnAd, FINN_AD_URL

from .operation import Operation


class FinnAdvertInfoConnector(Operation):
    """
    Operation that retrieves Finn advert information

    """

    @Tracking
    def __init__(self, finn_code: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        finn_code       : str
                          finn_code for advert to connector

        """
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(name=self.__class__.__name__,
                         desc="from: '{}\\<[finn_code]\\>' \\n id: "
                              "FINN Advert Info Connector".format(FINN_AD_URL))
        self.finn_code = finn_code

    @Tracking
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
