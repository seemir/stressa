# -*- coding: utf-8 -*-

"""
Test module for the Email Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.util import TrackingError
from source.domain import Email, Value


class TestEmail:
    """
    Test cases for Email Value Object

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.email = Email("ola.nordmann@gmail.com")

    def test_email_is_instance_of_value_and_address(self):
        """
        Test that all email objects are instances and subclasses of Email and Value

        """
        for parent in [Value, Email]:
            assert isinstance(self.email, parent)
            assert issubclass(self.email.__class__, parent)

    @pt.mark.parametrize("invalid_email_type", [True, 90210, 90210.0, [], (), {}])
    def test_email_throws_type_error_for_invalid_argument_types(self, invalid_email_type):
        """
        Test that TypeError is thrown if invalid type, i.e. not str is passed to Email object

        """
        with pt.raises(TypeError):
            Email(invalid_email_type)
        with pt.raises(TypeError):
            self.email.email = invalid_email_type

    @pt.mark.parametrize("valid_email", ["kari.nordmann@gmail.com", "john.doe@gmail.com"])
    def test_email_gets_set_in_object(self, valid_email):
        """
        Test that email string get set in Email object

        """
        self.email.email = valid_email
        assert self.email.email == valid_email

    @pt.mark.parametrize("invalid_email", ["ola.nordmann@", "kari_normanngmai.com"])
    def test_validate_email_method(self, invalid_email):
        """
        Test the static method validate_email method

        """
        with pt.raises(TrackingError):
            Email(invalid_email)
        with pt.raises(TrackingError):
            self.email.email = invalid_email
        with pt.raises(TrackingError):
            self.email.validate_email(invalid_email)

    @staticmethod
    @pt.mark.parametrize("valid_email", ["kari.nordmann@gmail.com", "john.doe@gmail.com"])
    def test_format_email_method(valid_email):
        """
        Test that the format_email method returns capitalized Email str

        """
        email = Email(valid_email)
        assert email.format_email() == valid_email

    def test_email_value_object_equal(self):
        """
        Testing that two Email Value objects are equal when all properties are equal

        """
        assert self.email == Email("ola.nordmann@gmail.com")

    def test_email_value_object_not_equal(self):
        """
        Testing that two Email Value objects are not equal when some properties are not equal

        """
        assert self.email != Email("kari.nordmann@gmail.com")
