# -*- coding: utf-8 -*-

"""
Implementation of connector against Finn.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

from source.util import Assertor, LOGGER, InvalidDataError, Tracking

from .connector import Connector


class Finn(Connector):
    """
    Connector that extracts housing information from Finn.no given a Finn-code

    """

    @Tracking
    def validate_finn_code(self):
        """
        static method for validating Finn.no code

        """
        valid_finn_code = re.compile("^[1-9][0-9]{7,8}$").search(self.finn_code)
        if not valid_finn_code:
            raise InvalidDataError(
                f"'{self.finn_code}' is an invalid Finn code")

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
            self._finn_code = finn_code
            self.validate_finn_code()
            self._browser = None
            LOGGER.success(
                f"created '{self.__class__.__name__}', with id: [{self.id_}]")
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
        list of all rules in this connector

        Returns
        -------
        out         : list
                      all rules in connector
        """
        return ", ".join(
            ["only_numeric_values", "starts_with_one_or_two",
             "max_len_eight_or_nine"]).replace("'", "")
