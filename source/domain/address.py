# -*- coding: utf-8 -*-

"""
Module for Address Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

from source.util import InvalidAddressError, LOGGER, Assertor

from .value import Value


class Address(Value):
    """
    Value object Address implementation

    """

    @staticmethod
    def validate_address(address: str):
        """
        Method for validating a address according to regrex

        Parameters
        ----------
        address    : str
                     string to be validated

        """
        valid_address = re.compile("[-a-zA-Z0-9]$").search(address)
        if not valid_address:
            raise InvalidAddressError("'{}' is an invalid address".format(address))

    def __init__(self, address: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        address   : str
                    address

        """
        super().__init__()
        try:
            Assertor.assert_data_types([address], [str])
            self.validate_address(address)
            self._address = address
            LOGGER.success(
                "created '{}'".format(self.__class__.__name__))
        except Exception as address_error:
            LOGGER.exception(address_error)
            raise address_error

    @property
    def address(self):
        """
        address getter

        Returns
        -------
        out     : str
                  active name
        """
        return self._address

    @address.setter
    def address(self, address_):
        """
        address setter

        Parameters
        ----------
        address_  : str
                    new address to be set

        """
        Assertor.assert_data_types([address_], [str])
        self.validate_address(address_)
        self._address = address_

    def format_address(self):
        """
        method that returns formatted address

        Returns
        -------
        out     : str
                  formatted name

        """
        address = self.address
        formatted = address.capitalize()
        LOGGER.info("format name '{}' to -> '{}'".format(address, formatted))
        return formatted