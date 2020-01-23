# -*- coding: utf-8 -*-

"""
Phone value object class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

from source.util import Assertor, InvalidPhoneNumberError

from .value import Value


class Phone(Value):
    """
    logic to validate a phone number

    """

    @staticmethod
    def remove_prefix(number: str):
        """
        method for removing country code prefix, i.e. 0047 or +47 from phone number

        Parameters
        ----------
        number      : str
                      number to be evaluated

        Returns
        -------
        out         : str
                      number with prefix removed

        """
        prefixes = ["0047", "+47"]
        for prefix in prefixes:
            if number.startswith(prefix):
                return number.replace(prefix, "").replace(" ", "")
        return number.replace(" ", "")

    def __init__(self, number: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        number      : str
                      phone number to be validated
        """
        try:
            super().__init__()
            Assertor.assert_data_types([number], [str])
            self.validate_number(number)
            self._number = number
        except Exception as phone_exception:
            raise phone_exception

    @property
    def number(self):
        """
        number getter

        Returns
        -------
        out     : str
                  active number in object

        """
        return self._number

    @number.setter
    def number(self, new_number):
        """
        number setter

        Parameters
        ----------
        new_number     : str
                         number to be set

        """
        Assertor.assert_data_types([new_number], [str])
        self.validate_number(new_number)
        self._number = new_number

    def validate_number(self, number: str):
        """
        method for validating a phone number

        Parameters
        ----------
        number      : str
                      number to be validated

        """
        number = self.remove_prefix(number)
        valid_number = re.compile("^\\+?[0-9]{8,20}$").search(number)
        if not valid_number:
            raise InvalidPhoneNumberError("'{}' is an invalid phone number".format(number))

    def format_number(self):
        """
        formatting of phone number according to norwegian standard

        Returns
        -------
        out     : str
                  formatted phone number

        References
        -------
        https://begrep.difi.no/Felles/mobiltelefonnummer

        """
        prefix, number = "+47", self.remove_prefix(self.number)
        phone_number = prefix + " " + " ".join(
            [number[i:i + 2] for i in range(0, len(number), 2)])
        return phone_number
