# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception import BaseClassCannotBeInstantiated
from source.log import logger
from uuid import uuid4
from abc import ABC


class Entity(ABC):
    """
    Base entity class

    """

    def __init__(self):
        """
        Constructor / Instantiate the class.
        Only one property, i.e. id given by uuid4

        """
        if type(self) == Entity:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))
        self._id = str(uuid4())
        logger.info(
            "Created Entity, '{}', with id: '{}'".format(self.__class__.__name__, self.id))

    @property
    def id(self):
        """
        Id getter

        """
        return self._id
