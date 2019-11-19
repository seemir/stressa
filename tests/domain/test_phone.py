# -*- coding: utf-8 -*-

"""
Test module for Phone entity

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.domain import Phone, Value
from source.util import InvalidPhoneNumberError


class TestPhone:
    """
    Test cases for logic in Phone entity

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.phone = Phone("91515915")

    @classmethod
    def teardown(cls):
        """
        Executed after all tests

        """
        cls.phone = None

    def test_phone_instance_of_value(self):
        """
        Test that all phone objects are instances of Phone and Value class

        """
        for parent in [Phone, Value]:
            isinstance(self.phone, parent)
            issubclass(self.phone.__class__, parent)

    @pt.mark.parametrize("invalid_types", [True, 90210, 90210.0, [], (), {}])
    def test_type_error_gets_thrown_for_invalid_types(self, invalid_types):
        """
        Test that typeerror is raised if anything other that 'str' is passed to Phone obkect

        """
        with pt.raises(TypeError):
            self.phone.number = invalid_types
        with pt.raises(TypeError):
            Phone(invalid_types)

    @pt.mark.parametrize("valid_numbers", ["97575975", "93535935", "95151951"])
    def test_number_gets_set_in_constructor(self, valid_numbers):
        """
        Test that only valid numbers gets set in object

        """
        self.phone.number = valid_numbers
        assert self.phone.number == valid_numbers

    @staticmethod
    @pt.mark.parametrize("numbers", ["+4791515915", "91515915"])
    def test_format_number_method(numbers):
        """
        Test that format_number() method produces number with correct format

        """
        correct_number_format = "+47 91 51 59 15"
        phone = Phone(numbers)
        assert phone.format_number() == correct_number_format

    @pt.mark.parametrize("invalid_numbers", ["1121121", "+471121121", "00471121121"])
    def test_validate_number_method(self, invalid_numbers):
        """
        Test validate number method, i.e. NotPossibleError thrown for invalid numbers

        """
        with pt.raises(InvalidPhoneNumberError):
            self.phone.validate_number(invalid_numbers)

    @pt.mark.parametrize("numbers", ["+4791515915", "004791515915", "+47 91 51 59 15",
                                     "0047 91 51 59 15", "91515915"])
    def test_remove_prefix_method(self, numbers):
        """
        Test remove_prefix() method

        """
        assert self.phone.remove_prefix(numbers) == "91515915"
