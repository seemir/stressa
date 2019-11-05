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
            self.number = number
            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_str))
        except Exception as phone_exception:
            LOGGER.exception(phone_exception)
            raise phone_exception

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
        try:
            prefix, number = "+47", self.remove_prefix(self.number)
            valid_number = re.compile("^\\+?[- 0-9]{8,20}$").search(number)
            if valid_number:
                phone_number = prefix + " " + " ".join(
                    [number[i:i + 2] for i in range(0, len(number), 2)])
                LOGGER.info("format number '{}' to -> '{}'".format(number, phone_number))
                return phone_number
            raise NotPossibleError("'{}' is an invalid phone number".format(number))
        except Exception as format_number_error:
            LOGGER.exception(format_number_error)
            raise format_number_error

    @staticmethod
    def remove_prefix(number):
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
