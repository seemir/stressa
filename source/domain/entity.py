# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from uuid import uuid4
from abc import ABC


class Entity(ABC):
    """
    Base entity class

    """

    def __init__(self):
        if type(self) == Entity:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))
        self.id = str(uuid4())
