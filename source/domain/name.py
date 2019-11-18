# -*- coding: utf-8 -*-

"""
Module for the Name value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

from source.util import NotPossibleError, LOGGER, Assertor

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
            raise NotPossibleError("'{}' is an invalid name".format(name))

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
    def name(self, name_):
        """
        name setter

        Parameters
        ----------
        name_  : str
                 new name to be set

        """
        Assertor.assert_data_types([name_], [str])
        self.validate_name(name_)
        self._name = name_

    def format_name(self):
        """
        method that returns formatted name

        Returns
        -------
        out     : str
                  formatted name

        """
        name = self._name
        form = name.capitalize()
        LOGGER.info("format name '{}' to -> '{}'".format(name, form))
        return form
