# -*- coding: utf-8 -*-
"""
Test module for the division operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, Division
from source.util import TrackingError


class TestDivision:
    """
    Test cases for the division operation

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.numerator = {"klar": "500 kr", "sko": "500 kr", "mat": "500 kr"}
        self.denominator = {"total": "1 500 kr"}
        self.desc = "Share of Total Expenses"
        self.division = Division(self.numerator, self.denominator, self.desc)

    def test_division_is_instance_of_operation(self):
        """
        Test that division is instance and subclass of Operation

        """
        for parent in [Division, Operation]:
            assert isinstance(self.division, parent)
            assert issubclass(self.division.__class__, parent)

    @pt.mark.parametrize('invalid_num', [True, 'test', 90210, 90210.0, ('test', 'test')])
    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(self, invalid_num, invalid_desc):
        """
        Test that division object raises TrackingError if numerator, denominator or desc
        argument are invalid

        """
        with pt.raises(TrackingError):
            Division(invalid_num, self.denominator, self.desc)
        with pt.raises(TrackingError):
            Division(self.numerator, invalid_num, self.desc)
        with pt.raises(TrackingError):
            Division(self.numerator, self.denominator, invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the division object

        """
        division = Division(self.numerator, self.denominator, self.desc)
        assert division.numerator == self.numerator
        assert division.denominator == self.denominator
        assert division.desc == "id: " + self.desc

    def test_division_run_method(self):
        """
        Test the run method in division operation

        """
        division = Division(self.numerator, self.denominator, self.desc)
        assert division.run() == self.division.run()
        assert division.run() == {'klar': '33.33 %', 'sko': '33.33 %', 'mat': '33.33 %'}
