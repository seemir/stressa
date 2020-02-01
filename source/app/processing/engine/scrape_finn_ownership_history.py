# -*- coding: utf-8 -*-
"""
Module with logic for the Scrape Finn Ownership history information

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.app.scrapers import FinnOwnership, FINN_OWNER_URL
from source.util import Assertor

from .operation import Operation


class ScrapeFinnOwnershipHistory(Operation):
    """
    Operation that scrapes Finn Ownership history information

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
                         desc="from: '{}\\<[finn_code]\\>' \\n id: Scrape FINN Ownership "
                              "History".format(FINN_OWNER_URL))
        self.finn_coe = finn_code

    def run(self):
        """
        method for running the operation

        Returns
        -------
        dict        : dict
                      dictionary with all finn ownership information

        """
        finn_owner_history = FinnOwnership(self.finn_coe)
        return finn_owner_history.housing_ownership_information()
