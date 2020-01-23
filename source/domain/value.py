# -*- coding: utf-8 -*-

"""
Value object module in accordance with DDD

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC, abstractmethod


class Value(ABC):
    """
    Value object implementation in the Domain model

    """

    @abstractmethod
    def __init__(self):
        """
        Constructor / Instantiate the class. Cannot be instantiated as its an @abstractmethod

        """

    def __eq__(self, other):
        """
        Method for asserting that value objects are equal

        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Method for asserting that value objects are not equal

        """
        return self.__dict__ != other.__dict__
