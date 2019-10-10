# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.exception.invalid_zip_code import InvalidZipCode


class TestExceptions:

    def test_that_all_application_exceptions_are_exceptions(self):
        """
        Test that all exceptions in the application, e.g. BaseClassCannotBeInstantiated,
        InvalidZipCode etc. are all instances and subclasses of python Exception. Keeping
        in-line with recommendation from PEP 352 -- Required Superclass for Exceptions.

        """
        for exception in [BaseClassCannotBeInstantiated, InvalidZipCode]:
            assert isinstance(exception('test'), Exception)
            assert issubclass(exception, Exception)
