# -*- coding: utf-8 -*-

"""
Test module for Amount Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

import pytest as pt

from source.util import TrackingError
from source.domain import Value, Amount


class TestAmount:
    """
    Test cases for the Amount Value object

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.amount = Amount("90210")

    def test_amount_is_instance_of_value_and_amount(self):
        """
        Test that all amount objects are instances and subclasses of Amount and Value

        """
        for parent in [Value, Amount]:
            assert isinstance(self.amount, parent)
            assert issubclass(self.amount.__class__, parent)

    @pt.mark.parametrize("invalid_amount_type", [True, 90210, 90210.0, [], (), {}])
    def test_amount_throws_type_error_for_invalid_argument_types(self, invalid_amount_type):
        """
        Test that TypeError is thrown if invalid type, i.e. not str is passed to Amount object

        """
        with pt.raises(TypeError):
            Amount(invalid_amount_type)
        with pt.raises(TypeError):
            self.amount.amount = invalid_amount_type

    @pt.mark.parametrize("valid_amount", ["1", "1.0", "100", "100.0", "1000", "1000.0"])
    def test_amount_gets_set_in_object(self, valid_amount):
        """
        Test that amount string get set in Amount object

        """
        self.amount.amount = valid_amount
        assert self.amount.amount.replace(" ", "") == valid_amount

    @pt.mark.parametrize("invalid_amount", ["one", "ten_", "one_thousand", "ten_thousands"])
    def test_validate_amount_method(self, invalid_amount):
        """
        Test the static method validate_amount method

        """
        with pt.raises(TrackingError):
            Amount(invalid_amount)
        with pt.raises(TrackingError):
            self.amount.amount = invalid_amount
        with pt.raises(TrackingError):
            self.amount.validate_amount(invalid_amount)

    @pt.mark.parametrize("invalid_amount", ["one", "ten_", "one_thousand", "ten-thousand"])
    def test_format_amount_method_thrown_exception(self, invalid_amount):
        """
        Test that the format_amount method throws InvalidAmountError for invalid amounts

        """
        with pt.raises(TrackingError):
            self.amount.format_amount(invalid_amount)

    def test_amount_value_object_equal(self):
        """
        Testing that two Amount Value objects are equal when all properties are equal

        """
        assert self.amount == Amount("90210")

    def test_amount_value_object_not_equal(self):
        """
        Testing that two Amount Value objects are equal when some properties are not equal

        """
        assert self.amount != Amount("90211")

    @pt.mark.parametrize("amount", ["1", "1.5", "100", "1000.45"])
    def test_adding_method(self, amount):
        """
        Testing adding two amounts together

        """
        correct_sum = str(Decimal(self.amount.amount.replace(" ", "")) + Decimal(amount))
        assert (self.amount + Amount(amount)).replace(" ", "") == correct_sum

    @pt.mark.parametrize("amount", ["1", "1.5", "100", "1000.45"])
    def test_subtracting_method(self, amount):
        """
        Testing subtracting two amounts together

        """
        correct_sub = str(Decimal(self.amount.amount.replace(" ", "")) - Decimal(amount))
        assert (self.amount - Amount(amount)).replace(" ", "") == correct_sub

    @pt.mark.parametrize("amount", ["1", "1.5", "100", "1000.45"])
    def test_multiplication_method(self, amount):
        """
        Test the multiplication method of Amount object

        """
        correct_mul = str(Decimal(self.amount.amount.replace(" ", "")) * Decimal(amount))
        assert (self.amount * Amount(amount)).replace(" ", "") == correct_mul

    @pt.mark.parametrize("amount", ["1", "1.5", "100", "1000.45"])
    def test_true_division_method(self, amount):
        """
        Test the division method of Amount object

        """
        correct_mul = str(Decimal(self.amount.amount.replace(" ", "")) / Decimal(amount))
        assert (self.amount / Amount(amount)).replace(" ", "") == correct_mul

    def test_division_by_zero(self):
        """
        Test that dividing Amount object by zero throws ZeroDivisionError exception

        """
        with pt.raises(ZeroDivisionError):
            assert self.amount / Amount("0")
