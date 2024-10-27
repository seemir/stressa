# -*- coding: utf-8 -*-

"""
Test module for Mobile Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.domain import Mobile, Phone, Value
from source.util import TrackingError


class TestMobile:
    """
    Test cases for the Mobile Value object

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.mobile = Mobile("98989898")

    def test_mobile_instance_of_mobile_phone_and_value(self):
        """
        Test that Mobile object is instance and subclass of Phone and Value

        """
        for parent in [Mobile, Phone, Value]:
            assert isinstance(self.mobile, parent)
            assert issubclass(self.mobile.__class__, parent)

    @pt.mark.parametrize("invalid_mobile_type", [True, 90210, 90210.0, [], (), {}])
    def test_type_error_thrown_for_invalid_arguments(self, invalid_mobile_type):
        """
        Test that TypeError is thrown for invalid argument types

        """
        with pt.raises(TypeError):
            Mobile(invalid_mobile_type)
        with pt.raises(TypeError):
            self.mobile.number = invalid_mobile_type

    @pt.mark.parametrize("valid_mobile_number", ["91919191", "92929292", "41414141"])
    def test_argument_gets_get_in_mobile_object(self, valid_mobile_number):
        """
        Test that arguments get set in object

        """
        self.mobile.number = valid_mobile_number
        assert self.mobile.number == valid_mobile_number

    @pt.mark.parametrize("invalid_mobile_number", ["71717171", "61616161"])
    def test_validate_mobile_number_method(self, invalid_mobile_number):
        """
        Test the validate_mobile_number method

        """
        with pt.raises(TrackingError):
            self.mobile.number = invalid_mobile_number
        with pt.raises(TrackingError):
            self.mobile.validate_mobile_number(invalid_mobile_number)

    def test_mobile_value_object_equal(self):
        """
        Testing that two Mobile Value objects are equal when all properties are equal

        """
        assert self.mobile == Mobile("98989898")

    def test_mobile_value_object_not_equal(self):
        """
        Testing that two Mobile Value objects are not equal when some properties are equal

        """
        assert self.mobile != Mobile("98989897")
