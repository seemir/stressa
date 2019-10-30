# -*- coding: utf-8 -*-

"""
Phone entity class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.log import LOGGER
from source.util import Assertor
from .entity import Entity


class Phone(Entity):
    """
    Logic to validate a phone number

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

    def formatted_number(self):
        """
        formatting of phone number

        Returns
        -------
        out     : str
                  formatted phone number

        """
        number = self.number
        return "+47 " + ' '.join([number[i:i + 2] for i in range(0, len(number), 2)])
