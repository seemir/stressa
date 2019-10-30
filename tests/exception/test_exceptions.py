# -*- coding: utf-8 -*-

"""
All tests against exceptions are to be stored here

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception import DomainError


class TestExceptions:
    """
    Test for exceptions

    """

    @staticmethod
    def test_that_all_application_exceptions_are_exceptions():
        """
        Test that all exceptions in the application, e.g. BaseClassCannotBeInstantiated,
        InvalidZipCode etc. are all instances and subclasses of python Exception. Keeping
        in-line with recommendation from PEP 352 -- Required Superclass for Exceptions.

        """
        assert isinstance(DomainError('test'), Exception)
        assert issubclass(DomainError, Exception)
