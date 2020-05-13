# -*- coding: utf-8 -*-
"""
Test module for the RateOfChange operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, RateOfChange
from source.util import TrackingError


class TestRateOfChange:
    """
    Test cases for the RateOfChange operation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.dataframe = {'Tinglyst': {0: 'Prisantydning', 1: '23.01.2019', 2: '23.10.2017'},
                         'Boligtype': {0: '-', 1: 'Blokkleilighet', 2: 'Blokkleilighet'},
                         'Seksjonsnummer': {0: '-', 1: '4', 2: '4'},
                         'Pris': {0: '3 325 000 kr', 1: '3\xa0490\xa0000 kr',
                                  2: '2\xa0570\xa0000 kr'}}
        cls.desc = "Ownership History with List Price"
        cls.rate_of_change = RateOfChange(cls.dataframe, cls.desc)

    def test_rate_of_change_is_instance_of_operation(self):
        """
        Test that RateOfChange is instance and subclass of Operation

        """
        for parent in [RateOfChange, Operation]:
            assert isinstance(self.rate_of_change, parent)
            assert issubclass(self.rate_of_change.__class__, parent)

    @pt.mark.parametrize('invalid_dataframe', [True, 'test', 90210, 90210.0, ('test', 'test')])
    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(self, invalid_dataframe, invalid_desc):
        """
        Test that RateOfChange object raises TrackingError if dataframe or desc
        argument are invalid

        """
        with pt.raises(TrackingError):
            RateOfChange(invalid_dataframe, self.desc)
        with pt.raises(TrackingError):
            RateOfChange(self.dataframe, invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the RateOfChange object

        """
        rate_of_change = RateOfChange(self.dataframe, self.desc)
        assert rate_of_change.dataframe == self.dataframe
        assert rate_of_change.desc == "id: " + self.desc

    def test_rate_of_change_run_method(self):
        """
        Test the run method in RateOfChange operation

        """
        rate_of_change = RateOfChange(self.dataframe, self.desc)
        assert rate_of_change.run() == self.rate_of_change.run()
        assert rate_of_change.run() == {
            'Tinglyst': {0: 'Prisantydning', 1: '23.01.2019', 2: '23.10.2017'},
            'Boligtype': {0: '-', 1: 'Blokkleilighet', 2: 'Blokkleilighet'},
            'Seksjonsnummer': {0: '-', 1: '4', 2: '4'},
            'Pris': {0: '3 325 000 kr', 1: '3\xa0490\xa0000 kr', 2: '2\xa0570\xa0000 kr'},
            'Endring': {0: '-4.73 %', 1: '35.8 %', 2: ''}}

    def test_rate_of_change_run_method_without_dataframe(self):
        """
        Test the run method in RateOfChange operation

        """
        with pt.raises(TrackingError):
            rate_of_change = RateOfChange(None, self.desc)
            rate_of_change.run()
