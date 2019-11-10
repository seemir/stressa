# -*- coding: utf-8 -*-

"""
Phone entity class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

from source.util import Assertor, LOGGER, NotPossibleError

from .entity import Entity


class Phone(Entity):
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
        only_numeric = "[^0-9]"
        for prefix in prefixes:
            if number.startswith(prefix):
                return re.sub(only_numeric, "", number.replace(prefix, ""))
        return re.sub(only_numeric, "", number)

    @staticmethod
    def validate_number(number: str):
        """
        method for validating a phone number

        Parameters
        ----------
        number      : str
                      number to be validated

        """
        number = Phone.remove_prefix(number)
        valid_number = re.compile("^\\+?[0-9]{8,20}$").search(number)
        if not valid_number:
            raise NotPossibleError("'{}' is an invalid phone number".format(number))

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
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
        except Exception as phone_exception:
            LOGGER.exception(phone_exception)
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
    def number(self, num):
        """
        number setter

        Parameters
        ----------
        num     : str
                  number to be set

        """
        Assertor.assert_data_types([num], [str])
        self.validate_number(num)
        self._number = num

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
        LOGGER.info("format number '{}' to -> '{}'".format(number, phone_number))
        return phone_number
