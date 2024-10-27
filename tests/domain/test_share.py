# -*- coding: utf-8 -*-

"""
Test module of the Share Value Object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

import pytest as pt

from source.domain import Share, Value, Percent


class TestShare:
    """
    Test cases for the Share Value Object

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.share = Share(Decimal(1))

    def test_share_is_instance_of_value(self):
        """
        Test that the Share Value Object is instance and subclass of Value

        """
        for parent in [Share, Value]:
            assert isinstance(self.share, parent)
            assert issubclass(self.share.__class__, parent)

    @staticmethod
    @pt.mark.parametrize("invalid_types", [1, 1.0, True, "1", [], (), {}])
    def test_invalid_type_throws_typeerror(invalid_types):
        """
        test that TypeError is thrown for invalid types passed to Share

        """
        with pt.raises(TypeError):
            Share(numerator=invalid_types)
        with pt.raises(TypeError):
            Share(numerator=Decimal(1), denominator=invalid_types)

    @staticmethod
    @pt.mark.parametrize("num", [Decimal(1), Decimal(2)])
    @pt.mark.parametrize("den", [Decimal(1), Decimal(2)])
    def test_arguments_get_set(num, den):
        """
        That arguments in the Share object

        """
        share = Share(num, den)
        assert share.numerator == num
        assert share.denominator == den
        assert share.value == Percent(num / den).value
