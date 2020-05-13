# -*- coding: utf-8 -*-
"""
Test module for the AddRowToDataFrame operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame

import pytest as pt

from source.app import AddRowToDataFrame, Operation
from source.util import TrackingError


class TestAddRowToDataFrame:
    """
    Test cases for the AddRowToDataFrame operation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.row = {'prisantydning': '3 325 000 kr'}
        cls.dataframe = {"historikk": DataFrame({'Tinglyst': {0: '23.01.2019', 1: '23.10.2017'},
                                                 'Boligtype': {0: 'Blokkleilighet',
                                                               1: 'Blokkleilighet'},
                                                 'Seksjonsnummer': {0: '4', 1: '4'},
                                                 'Pris': {0: '3\xa0490\xa0000 kr',
                                                          1: '2\xa0570\xa0000 kr'}})}
        cls.desc = "Add List Price to Ownership History"
        cls.add_row_to_dataframe = AddRowToDataFrame(cls.row, cls.dataframe, cls.desc)

    def test_add_row_to_dataframe_is_instance_of_operation(self):
        """
        Test that AddRowToDataFrame is instance and subclass of Operation

        """
        for parent in [AddRowToDataFrame, Operation]:
            assert isinstance(self.add_row_to_dataframe, parent)
            assert issubclass(self.add_row_to_dataframe.__class__, parent)

    @pt.mark.parametrize('invalid_row', ['test', 90210])
    @pt.mark.parametrize('invalid_dataframe', [True, 90210.0, ('test', 'test')])
    @pt.mark.parametrize('invalid_desc', [['test'], {'test': 'test'}])
    def test_invalid_args_raises_tracking_error(self, invalid_row, invalid_dataframe, invalid_desc):
        """
        Test that AddRowToDataFrame object raises TrackingError if row, dataframe or desc
        argument are invalid

        """
        with pt.raises(TrackingError):
            AddRowToDataFrame(invalid_row, self.dataframe, self.desc)
        with pt.raises(TrackingError):
            AddRowToDataFrame(self.row, invalid_dataframe, self.desc)
        with pt.raises(TrackingError):
            AddRowToDataFrame(self.row, self.dataframe, invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the AddRowToDataFrame object

        """
        assert self.add_row_to_dataframe.row == self.row
        assert self.add_row_to_dataframe.dataframe == self.dataframe
        assert self.add_row_to_dataframe.desc == "id: " + self.desc

    def test_add_row_to_dataframe_run_method(self):
        """
        Test the run method in AddRowToDataFrame operation

        """
        add_row_to_dataframe = AddRowToDataFrame(self.row, self.dataframe, self.desc)
        assert add_row_to_dataframe.run() == self.add_row_to_dataframe.run()
        assert add_row_to_dataframe.run() == {
            'Tinglyst': {0: 'Prisantydning', 1: '23.01.2019', 2: '23.10.2017'},
            'Boligtype': {0: '-', 1: 'Blokkleilighet', 2: 'Blokkleilighet'},
            'Seksjonsnummer': {0: '-', 1: '4', 2: '4'},
            'Pris': {0: '3 325 000 kr', 1: '3\xa0490\xa0000 kr', 2: '2\xa0570\xa0000 kr'}}

    def test_add_row_to_dataframe_run_method_without_dataframe(self):
        """
        Test the run method in AddRowToDataFrame operation without passed DataFrame

        """
        add_row_to_dataframe = AddRowToDataFrame(self.row, None, self.desc)
        assert add_row_to_dataframe.run() == {'Tinglyst': {0: 'Prisantydning'},
                                              'Boligtype': {0: '-'},
                                              'Bolig identifikasjon': {0: '-'},
                                              'Pris': {0: '3 325 000 kr'}}
