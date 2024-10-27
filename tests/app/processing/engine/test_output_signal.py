# -*- coding: utf-8 -*-
"""
Test module for the output signal

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Signal, OutputSignal
from source.util import TrackingError


class TestOutsignal:
    """
    Test cases for the Divide operation

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.data = {"totalt": "12 500 kr"}
        self.desc = "Total Expenses"
        self.output = OutputSignal(self.data, self.desc)

    def test_output_signal_is_instance_of_signal(self):
        """
        Test that OutputOperation is instance and subclass of Operation

        """
        for parent in [OutputSignal, Signal]:
            assert isinstance(self.output, parent)
            assert issubclass(self.output.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_data', [True, 'test', 90210, 90210.0, ('test', 'test')])
    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_data, invalid_desc):
        """
        Test that OutputOperation object raises TrackingError if desc argument are invalid

        """
        with pt.raises(TrackingError):
            OutputSignal(invalid_data, invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the OutputSignal object

        """
        assert self.output.data == self.data
        assert self.output.desc == self.desc
