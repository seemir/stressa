# -*- coding: utf-8 -*-

"""
Implementation of scarper against Finn.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

import requests

from source.util import cache, Assertor, LOGGER, NotFoundError

from .scraper import Scraper

cache(__file__, "cache")


class Finn(Scraper):
    """
    Scraper that scrapes housing information from Finn.no given a Finn-code

    """

    @staticmethod
    def validate_finn_code(finn_code: str):
        """
        static method for validating Finn.no code

        Parameters
        ----------
        finn_code    : str
                       Finn-code to be validated

        """
        valid_finn_code = re.compile("^1[0-9]{7,8}$").search(finn_code)
        if not valid_finn_code:
            raise NotFoundError("'{}' is an invalid Finn code".format(finn_code))

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to be searched for

        """
        try:
            super().__init__()
            Assertor.assert_data_types([finn_code], [str])
            self.validate_finn_code(finn_code)
            self._finn_code = finn_code
            self._browser = requests.session()
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_))
        except Exception as finn_exception:
            LOGGER.exception(finn_exception)
            raise finn_exception

    @property
    def finn_code(self):
        """
        Finn-code getter

        Returns
        -------
        out     : str
                  active finn-kode in object

        """
        return self._finn_code

    @staticmethod
    def rules():
        """
        list of all rules in this scraper

        Returns
        -------
        out         : list
                      all rules in scraper
        """
        return ["starts_with_one", "numeric_values", "max_len_seven_or_eight (zero_based_indexing)"]
