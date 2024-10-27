# -*- coding: utf-8 -*-

"""
Test module for the Addess Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.util import TrackingError
from source.domain import Address, Value


class TestAddress:
    """
    Test cases for Address Value Object

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.address = Address("Slottsplassen 1, 0010 Oslo")

    def test_address_is_instance_of_value_and_address(self):
        """
        Test that all address objects are instances and subclasses of Address and Value

        """
        for parent in [Value, Address]:
            assert isinstance(self.address, parent)
            assert issubclass(self.address.__class__, parent)

    @pt.mark.parametrize("invalid_address_type", [True, 90210, 90210.0, [], (), {}])
    def test_address_throws_type_error_for_invalid_argument_types(self, invalid_address_type):
        """
        Test that TypeError is thrown if invalid type, i.e. not str is passed to Address object

        """
        with pt.raises(TypeError):
            Address(invalid_address_type)
        with pt.raises(TypeError):
            self.address.address = invalid_address_type

    @pt.mark.parametrize("valid_address", ["Akersgata 59, 0180 Oslo", "Akersgata 40, 0180 Oslo"])
    def test_address_gets_set_in_object(self, valid_address):
        """
        Test that address string get set in Address object

        """
        self.address.address = valid_address
        assert self.address.address == valid_address

    @pt.mark.parametrize("invalid_address", ["///", "+++", "---", "___"])
    def test_validate_address_method(self, invalid_address):
        """
        Test the method validate_address method

        """
        with pt.raises(TrackingError):
            Address(invalid_address)
        with pt.raises(TrackingError):
            self.address.address = invalid_address
        with pt.raises(TrackingError):
            self.address.validate_address(invalid_address)

    @staticmethod
    @pt.mark.parametrize("valid_address", ["akersgata 59, 0180 Oslo", "akersgata 40, 0180 Oslo"])
    def test_format_address_method(valid_address):
        """
        Test that the format_address method returns capitalized address str

        """
        address = Address(valid_address)
        assert address.format_address() == valid_address.capitalize()

    def test_address_value_object_equal(self):
        """
        Testing that two Address Value objects are equal when all properties are equal

        """
        assert self.address == Address("Slottsplassen 1, 0010 Oslo")

    def test_address_value_object_not_equal(self):
        """
        Testing that two Address Value objects are not equal when some properties are not equal

        """
        assert self.address != Address("Slottsplassen 2, 0010 Oslo")
