# -*- coding: utf-8 -*-
"""
Test module for the divide operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, Divide
from source.util import TrackingError


class TestDivide:
    """
    Test cases for the Divide operation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.numerator = {"klar": "500 kr", "sko": "500 kr", "mat": "500 kr"}
        cls.denominator = {"total": "1 500 kr"}
        cls.desc = "Share of Total Expenses"
        cls.divide = Divide(cls.numerator, cls.denominator, cls.desc)

    def test_divide_is_instance_of_operation(self):
        """
        Test that Divide is instance and subclass of Operation

        """
        for parent in [Divide, Operation]:
            assert isinstance(self.divide, parent)
            assert issubclass(self.divide.__class__, parent)

    @pt.mark.parametrize('invalid_num', [True, 'test', 90210, 90210.0, ('test', 'test')])
    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(self, invalid_num, invalid_desc):
        """
        Test that Divide object raises TrackingError if numerator, denominator or desc
        argument are invalid

        """
        with pt.raises(TrackingError):
            Divide(invalid_num, self.denominator, self.desc)
        with pt.raises(TrackingError):
            Divide(self.numerator, invalid_num, self.desc)
        with pt.raises(TrackingError):
            Divide(self.numerator, self.denominator, invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the Divide object

        """
        divide = Divide(self.numerator, self.denominator, self.desc)
        assert divide.numerator == self.numerator
        assert divide.denominator == self.denominator
        assert divide.desc == "id: " + self.desc

    def test_divide_run_method(self):
        """
        Test the run method in Divide operation

        """
        divide = Divide(self.numerator, self.denominator, self.desc)
        assert divide.run() == self.divide.run()
        assert divide.run() == {'klar': '33.33 %', 'sko': '33.33 %', 'mat': '33.33 %'}
