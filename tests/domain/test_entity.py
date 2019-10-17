# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception import InstantiationError
from source.domain import Entity
import pytest as pt


class TestEntity:

    def test_entity_cannot_be_instantiated(self):
        """
        Test that Entity class cannot be instantiated because its an abstract base class

        """
        with pt.raises(InstantiationError):
            Entity()
