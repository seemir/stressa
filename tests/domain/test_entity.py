# -*- coding: utf-8 -*-

"""
Tests for the entity abstract base class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC
import pytest as pt

from source.domain import Entity


class TestEntity:
    """
    Test cases for abstract base class Entity

    """

    @staticmethod
    def test_entity_instance_of_abc():
        """
        Test that entity class is instance of abstract base class (abc)

        """
        assert isinstance(Entity, ABC.__class__)

    @staticmethod
    def test_entity_cannot_be_instantiated():
        """
        Test that Entity class cannot be instantiated because its an abstract base class

        """
        with pt.raises(TypeError):
            Entity() # pylint: disable=abstract-class-instantiated
