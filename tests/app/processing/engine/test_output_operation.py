# -*- coding: utf-8 -*-
"""
Test module for the output operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, OutputOperation
from source.util import TrackingError


class TestOutputOperation:
    """
    Test cases for the OutputOperation

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.desc = "Share of Total Expenses"
        self.output = OutputOperation(self.desc)

    def test_output_is_instance_of_operation(self):
        """
        Test that OutputOperation is instance and subclass of Operation

        """
        for parent in [OutputOperation, Operation]:
            assert isinstance(self.output, parent)
            assert issubclass(self.output.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_desc):
        """
        Test that OutputOperation object raises TrackingError if desc argument are invalid

        """
        with pt.raises(TrackingError):
            OutputOperation(invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the OutputOperation object

        """
        assert self.output.name == self.output.__class__.__name__
        assert self.output.desc == "id: " + self.desc

    def test_output_run_method(self):
        """
        Test the run method in Output operation

        """
        assert not self.output.run()
