# -*- coding: utf-8 -*-

"""
Test module for the Percent Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

import pytest as pt

from source.domain import Value, Percent


class TestPercent:
    """
    Test cases for the Percent Value Object

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.percent = Percent(Decimal(0.10))

    def test_percent_is_instance_of_value(self):
        """
        Test that the Percent Value object is instance and subclass of Value and Percent

        """
        for parent in [Value, Percent]:
            assert isinstance(self.percent, parent)
            assert issubclass(self.percent.__class__, parent)

    @staticmethod
    @pt.mark.parametrize("invalid_types", [True, 90210, 90210.0, (), [], {}])
    def test_percent_throws_typeerror(invalid_types):
        """
        Test that TypeError is thrown when invalid type is passed through constructor

        """
        with pt.raises(TypeError):
            Percent(invalid_types)
