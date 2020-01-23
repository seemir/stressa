# -*- coding: utf-8 -*-

"""
Abstract base class implementation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import uuid4

from abc import ABC, abstractmethod


class Entity(ABC):
    """
    abstract base entity class

    """

    @abstractmethod
    def __init__(self):
        """
        Constructor / Instantiate the class. Only one property, i.e. id given by uuid4

        """
        self._id = str(uuid4())

    @property
    def id(self):
        """
        Id getter

        """
        return self._id
