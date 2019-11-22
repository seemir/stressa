# -*- coding: utf-8 -*-

"""
Value object module in accordance with DDD

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC, abstractmethod

from source.util import LOGGER


class Value(ABC):
    """
    Value object implementation in the Domain model

    """

    @abstractmethod
    def __init__(self):
        """
        Constructor / Instantiate the class. Cannot be instantiated as its an @abstractmethod

        """
        LOGGER.info(
            "trying to create '{}'".format(self.__class__.__name__))

    @property
    def hash(self):
        """
        Hash getter

        """
        return hash(repr(self))

    def __eq__(self, other):
        """
        Method for asserting that value objects are equal

        """
        if other is None:
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Method for asserting that value objects are not equal

        """
        return self.__dict__ != other.__dict__

    def __str__(self):
        """
        String representation

        """
        return repr(self)
