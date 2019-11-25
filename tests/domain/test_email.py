# -*- coding: utf-8 -*-

"""
Test module for the Email Value object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.util import InvalidEmailError
from source.domain import Email, Value


class TestEmail:
    """
    Test cases for Email Value Object

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.email = Email("ola.nordmann@gmail.com")

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
        with pt.raises(InvalidEmailError):
            Email(invalid_email)
        with pt.raises(InvalidEmailError):
            self.email.email = invalid_email
        with pt.raises(InvalidEmailError):
            self.email.validate_email(invalid_email)

    @staticmethod
    @pt.mark.parametrize("valid_email", ["kari.nordmann@gmail.com", "john.doe@gmail.com"])
    def test_format_email_method(valid_email):
        """
        Test that the format_email method returns capitalized Email str

        """
        email = Email(valid_email)
        assert email.format_email() == valid_email
