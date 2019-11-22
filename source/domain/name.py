# -*- coding: utf-8 -*-

"""
Module for the Name value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

from source.util import InvalidNameError, LOGGER, Assertor

from .value import Value


class Name(Value):
    """
    Value object name implementation

    """

    @staticmethod
    def validate_name(name: str):
        """
        Method for validating a name according to regrex

        Parameters
        ----------
        name    : str
                  string to be validated

        """
        valid_name = re.compile("[-a-zA-Z]$").search(name)
        if not valid_name:
            raise InvalidNameError("'{}' is an invalid name".format(name))

    def __init__(self, name: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        name   : str
                 name

        """
        super().__init__()
        try:
            Assertor.assert_data_types([name], [str])
            self.validate_name(name)
            self._name = name
            LOGGER.success(
                "created '{}'".format(self.__class__.__name__))
        except Exception as name_error:
            LOGGER.exception(name_error)
            raise name_error

    @property
    def name(self):
        """
        name getter

        Returns
        -------
        out     : str
                  active name
        """
        return self._name

    @name.setter
    def name(self, new_name):
        """
        name setter

        Parameters
        ----------
        new_name  : str
                    new name to be set

        """
        Assertor.assert_data_types([new_name], [str])
        self.validate_name(new_name)
        self._name = new_name

    def format_name(self):
        """
        method that returns formatted name

        Returns
        -------
        out     : str
                  formatted name

        """
        name = self.name
        formatted = name.capitalize()
        LOGGER.info("format name '{}' to -> '{}'".format(name, formatted))
        return formatted
