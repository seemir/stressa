# -*- coding: utf-8 -*-

"""
Mobile phone number value object module

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

from source.util import InvalidMobilePhoneNumberError, LOGGER

from .phone import Phone


class Mobile(Phone):
    """
    Implementation of Mobile phone number value object

    """

    def __init__(self, number: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        number      : str
                      mobile phone number to be validated

        """
        try:
            super(Mobile, self).__init__(number)
            self.validate_mobile_number(number)
            self._number = number
            LOGGER.success(
                "created '{}'".format(self.__class__.__name__))
        except Exception as mobile_phone_error:
            LOGGER.exception(mobile_phone_error)
            raise mobile_phone_error

    def validate_mobile_number(self, number: str):
        """
        method for validating a mobile phone number

        Parameters
        ----------
        number      : str
                      number to be validated

        """
        number = self.remove_prefix(number)
        valid_mobile_number = re.compile(r"^([49])").search(number)
        if not valid_mobile_number:
            raise InvalidMobilePhoneNumberError(
                "'{}' is an invalid mobile phone number".format(number))
