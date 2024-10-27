# -*- coding: utf-8 -*-

"""
Test module for the Currency Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.util import TrackingError
from source.domain import Currency, Value


class TestCurrency:
    """
    Test cases for the Currency Value object

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.currency = Currency()

    def test_currency_is_instance_of_value(self):
        """
        Test that currency is instance and subclass of Currency and Value

        """
        for parent in [Currency, Value]:
            assert isinstance(self.currency, parent)
            assert issubclass(self.currency.__class__, parent)

    @pt.mark.parametrize("invalid_currency_type", [True, 90210, 90210.0, [], (), {}])
    def test_currency_throws_type_error_for_invalid_argument_types(self, invalid_currency_type):
        """
        Test that TypeError is thrown if invalid type, i.e. not str is passed to Currency object

        """
        with pt.raises(TypeError):
            Currency(invalid_currency_type)
        with pt.raises(TypeError):
            self.currency.currency = invalid_currency_type

    @pt.mark.parametrize("valid_currency", ["kr"])
    def test_address_gets_set_in_object(self, valid_currency):
        """
        Test that currency string get set in Currency object

        """
        self.currency.currency = valid_currency
        assert self.currency.currency == valid_currency

    @pt.mark.parametrize("invalid_currency", ["euro", "usd", "gbp"])
    def test_validate_currency_method(self, invalid_currency):
        """
        Test the static method validate_currency method

        """
        with pt.raises(TrackingError):
            Currency(invalid_currency)
        with pt.raises(TrackingError):
            self.currency.currency = invalid_currency
        with pt.raises(TrackingError):
            self.currency.validate_currency(invalid_currency)

    def test_currency_value_object_equal(self):
        """
        Testing that two Currency Value objects are equal when some properties are equal

        """
        assert self.currency == Currency()
