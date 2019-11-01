# -*- coding: utf-8 -*-

"""
Abstract base class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import uuid4

from abc import ABC, abstractmethod

from source.cross_cutting import LOGGER


class Entity(ABC):
    """
    abstract base entity class

    """

    @abstractmethod
    def __init__(self):
        """
        Constructor / Instantiate the class. Only one property, i.e. id given by uuid4

        """
        LOGGER.info(
            "trying to create '{}'".format(self.__class__.__name__))
        self._id_str = str(uuid4())

    @property
    def id_str(self):
        """
        Id getter

        """
        return self._id_str
