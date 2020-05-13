# -*- coding: utf-8 -*-
"""
Test module for the ValidateFinnCode operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, ValidateFinnCode, Finn
from source.util import TrackingError


class TestValidateFinnCode:
    """
    Test cases for the ValidateFinnCode

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_code = "144857770"
        cls.validate_finn_code = ValidateFinnCode(cls.finn_code)

    def test_validate_finn_code_is_instance_of_operation(self):
        """
        Test that ValidateFinnCode is instance and subclass of Operation

        """
        for parent in [ValidateFinnCode, Operation]:
            assert isinstance(self.validate_finn_code, parent)
            assert issubclass(self.validate_finn_code.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_finn_code', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_finn_code):
        """
        Test that ValidateFinnCode object raises TrackingError if finn_code
        argument are invalid

        """
        with pt.raises(TrackingError):
            ValidateFinnCode(invalid_finn_code)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the ValidateFinnCode object

        """
        name = self.validate_finn_code.__class__.__name__
        assert self.validate_finn_code.name == name
        assert self.validate_finn_code.finn_code == self.finn_code
        assert self.validate_finn_code.desc == "rules: {} \\n id: Validate Finn Code".format(
            Finn.rules())

    @pt.mark.parametrize('invalid_finn_code', ["1945623", "1965426351", "29536542"])
    def test_validate_finn_code_run_method(self, invalid_finn_code):
        """
        Test the run method in ValidateFinnCode operation

        """
        with pt.raises(TrackingError):
            validate_finn_code = ValidateFinnCode(invalid_finn_code)
            validate_finn_code.run()

        assert self.validate_finn_code.run() == self.finn_code
