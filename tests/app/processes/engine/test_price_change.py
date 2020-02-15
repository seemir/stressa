# -*- coding: utf-8 -*-
"""
Test module for the PriceChange operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame

import pytest as pt

from source.app import Operation, PriceChange


class TestPriceChange:
    """
    Test cases for the PriceChange operation

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
        cls.price_change = PriceChange(cls.dataframe, cls.desc)

    def test_price_change_is_instance_of_operation(self):
        """
        Test that PriceChange is instance and subclass of Operation

        """
        for parent in [PriceChange, Operation]:
            assert isinstance(self.price_change, parent)
            assert issubclass(self.price_change.__class__, parent)

    @pt.mark.parametrize('invalid_dataframe', [True, 'test', 90210, 90210.0, ('test', 'test')])
    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_typeerror(self, invalid_dataframe, invalid_desc):
        """
        Test that PriceChange object raises TypeError if dataframe or desc
        argument are invalid

        """
        with pt.raises(TypeError):
            PriceChange(invalid_dataframe, self.desc)
        with pt.raises(TypeError):
            PriceChange(self.dataframe, invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the PriceChange object

        """
        price_change = PriceChange(self.dataframe, self.desc)
        assert price_change.dataframe == self.dataframe
        assert price_change.desc == "id: " + self.desc

    def test_price_change_run_method(self):
        """
        Test the run method in PriceChange operation

        """
        price_change = PriceChange(self.dataframe, self.desc)
        assert price_change.run().equals(self.price_change.run())
        assert price_change.run().equals(DataFrame(
            {'Tinglyst': {0: 'Prisantydning', 1: '23.01.2019', 2: '23.10.2017'},
             'Boligtype': {0: '-', 1: 'Blokkleilighet', 2: 'Blokkleilighet'},
             'Seksjonsnummer': {0: '-', 1: '4', 2: '4'},
             'Pris': {0: '3 325 000 kr', 1: '3\xa0490\xa0000 kr', 2: '2\xa0570\xa0000 kr'},
             'Endring': {0: '-4.73 %', 1: '35.8 %', 2: ''}}))

    def test_price_change_run_method_without_dataframe(self):
        """
        Test the run method in PriceChange operation

        """
        price_change = PriceChange(None, self.desc)
        assert not price_change.run()
