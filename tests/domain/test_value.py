# -*- coding: utf-8 -*-

"""
Test module for Value object

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.domain import Value


class TestValue:
    """
    Test cases for the Value object

    """

    @staticmethod
    def test_value_object_cannot_be_created():
        """
        Test that Value() object cannot be instantiated

        """
        with pt.raises(TypeError):
            Value() # pylint: disable=abstract-class-instantiated
