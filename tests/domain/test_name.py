# -*- coding: utf-8 -*-
"""
Test module for the Name Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.util import TrackingError
from source.domain import Name, Value


class TestName:
    """
    Test cases for Name Value object

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.name = Name("Ola")

    def test_name_is_instance_of_value_and_address(self):
        """
        Test that all name objects are instances and subclasses of Name and Value

        """
        for parent in [Value, Name]:
            assert isinstance(self.name, parent)
            assert issubclass(self.name.__class__, parent)

    @pt.mark.parametrize("invalid_name_type", [True, 90210, 90210.0, [], (), {}])
    def test_name_throws_type_error_for_invalid_argument_types(self, invalid_name_type):
        """
        Test that TypeError is thrown if invalid type, i.e. not str is passed to Name object

        """
        with pt.raises(TypeError):
            Name(invalid_name_type)
        with pt.raises(TypeError):
            self.name.name = invalid_name_type

    @pt.mark.parametrize("valid_name", ["Jens", "Kari", "Christian", "Hanne"])
    def test_name_gets_set_in_object(self, valid_name):
        """
        Test that name string get set in Name object

        """
        self.name.name = valid_name
        assert self.name.name == valid_name

    @pt.mark.parametrize("invalid_name", ["Jens_", "Kari+", "Christian/", "Hanne."])
    def test_name_name_method(self, invalid_name):
        """
        Test the static method validate_name method

        """
        with pt.raises(TrackingError):
            Name(invalid_name)
        with pt.raises(TrackingError):
            self.name.name = invalid_name
        with pt.raises(TrackingError):
            self.name.validate_name(invalid_name)

    @staticmethod
    @pt.mark.parametrize("valid_name", ["jens", "Kari", "CHRISTIAN", "hANNE"])
    def test_format_name_method(valid_name):
        """
        Test that the format_name method returns capitalized address str

        """
        name = Name(valid_name)
        assert name.format_name() == valid_name.capitalize()

    def test_name_value_object_equal(self):
        """
        Testing that two Name Value objects are equal when all properties are equal

        """
        assert self.name == Name("Ola")

    def test_name_value_object_not_equal(self):
        """
        Testing that two Name Value objects are not equal when some properties are equal

        """
        assert self.name != Name("kari")
