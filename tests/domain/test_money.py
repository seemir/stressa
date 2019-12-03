# -*- coding: utf-8 -*-

"""
Test module of Money Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

import pytest as pt

from source.domain import Money, Value


class TestMoney:
    """
    Test case of Money Value object

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.money = Money("90210")

    def test_money_is_instance_of_money_and_value(self):
        """
        Test that Money object is instance and subclass of Money and Value

        """
        for parent in [Money, Value]:
            assert isinstance(self.money, parent)
            assert issubclass(self.money.__class__, parent)

    @pt.mark.parametrize("invalid_money_type", [True, 90210, 90210.0, [], (), {}])
    def test_money_throws_type_error_for_invalid_argument_types(self, invalid_money_type):
        """
        Test that TypeError is thrown if invalid type, i.e. not str is passed to Money object

        """
        with pt.raises(TypeError):
            Money(invalid_money_type)
        with pt.raises(TypeError):
            self.money.amount = invalid_money_type

    @pt.mark.parametrize("valid_amount", ["1", "1.0", "100", "100.0", "1000", "1000.0"])
    def test_amount_gets_set_in_money_object(self, valid_amount):
        """
        Test that amount string get set in Money object

        """
        self.money.amount = valid_amount
        assert self.money.amount.replace(" ", "") == valid_amount

    def test_money_value_object_equal(self):
        """
        Testing that two Money Value objects are equal when all properties are equal

        """
        assert self.money == Money("90210")

    def test_money_value_object_not_equal(self):
        """
        Testing that two Money Value objects are not equal when all properties are not equal

        """
        assert self.money != Money("90211")

    @pt.mark.parametrize("amount", ["1", "1.5", "100", "1000.45"])
    def test_money_adding_method(self, amount):
        """
        Testing adding two amounts together in Money object

        """
        correct_sum = str(Decimal(self.money.amount.replace(" ", "")) + Decimal(amount)) + "kr"
        assert str(self.money + Money(amount)).replace(" ", "") == correct_sum

    @pt.mark.parametrize("amount", ["1", "1.5", "100", "1000.45"])
    def test_money_subtracting_method(self, amount):
        """
        Testing subtracting two amounts together

        """
        correct_sum = str(Decimal(self.money.amount.replace(" ", "")) - Decimal(amount)) + "kr"
        assert str(self.money - Money(amount)).replace(" ", "") == correct_sum

    @pt.mark.parametrize("amount", ["1", "1.5", "100", "1000.45"])
    def test_money_multiplication_method(self, amount):
        """
        Test the multiplication method of Money object

        """
        correct_mul = str(Decimal(self.money.amount.replace(" ", "")) * Decimal(amount)) + "kr"
        assert (self.money * Money(amount)).replace(" ", "") == correct_mul

    @pt.mark.parametrize("amount", ["1", "1.5", "100", "1000.45"])
    def test_money_true_division_method(self, amount):
        """
        Test the division method of Money object

        """
        correct_mul = str(Decimal(self.money.amount.replace(" ", "")) / Decimal(amount)) + "kr"
        assert (self.money / Money(amount)).replace(" ", "") == correct_mul

    def test_money_division_by_zero(self):
        """
        Test that dividing Money object by zero throws ZeroDivisionError exception

        """
        with pt.raises(ZeroDivisionError):
            assert self.money / Money("0")
