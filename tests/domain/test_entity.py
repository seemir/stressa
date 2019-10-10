# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.domain.entity import Entity
from abc import ABC
import pytest as pt


class TestEntity:

    def test_entity_is_instances_of_abc_entity(self):
        """
        Test Entity class is an instance of python Abstract Base Class

        """
        assert isinstance(Entity, ABC.__class__)
        assert issubclass(Entity.__class__, ABC.__class__)

    def test_entity_cannot_be_instantiated(self):
        """
        Test that Entity class cannot be instantiated because its an abstract base class

        """
        with pt.raises(BaseClassCannotBeInstantiated):
            Entity()
