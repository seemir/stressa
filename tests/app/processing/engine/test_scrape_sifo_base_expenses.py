# -*- coding: utf-8 -*-

"""
Test module for the scrape base expenses operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import ScrapeSifoBaseExpenses, Operation
from source.domain import Male, Female, Family


class TestScrapeSifoBaseExpenses:
    """
    Test cases for ScrapeSifoBaseExpenses operation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.family = Family([Male(30), Female(29)], income=850000, cars=1)

    def test_scrape_sifo_base_expenses_is_instance_of_operation(self):
        """
        Test that scrape_sifo_base_expenses is instance and subclass of Operation

        """
        scraper = ScrapeSifoBaseExpenses(self.family)
        for parent in [ScrapeSifoBaseExpenses, Operation]:
            assert isinstance(scraper, parent)
            assert issubclass(scraper.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_data', [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_invalid_args_raises_typeerror(invalid_data):
        """
        Test that ScrapeSifoBaseExpenses object raises TypeError if data is invalid

        """
        with pt.raises(TypeError):
            ScrapeSifoBaseExpenses(invalid_data)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the ScrapeSifoBaseExpenses object

        """
        scraper = ScrapeSifoBaseExpenses(self.family)
        assert scraper.name == ScrapeSifoBaseExpenses.__name__
        assert scraper.data == self.family

    def test_scrape_sifo_base_expenses_run_method(self):
        """
        Test the run method in ScrapeSifoBaseExpenses operation

        """
        scraper = ScrapeSifoBaseExpenses(self.family)
        assert scraper.run() == {'mat': '5290', 'klar': '1590', 'helse': '1320', 'fritid': '2480',
                                 'kollektivt': '1500', 'spedbarn': '0', 'stordriftsfordel': '1',
                                 'sumindivid': '12180', 'dagligvarer': '340', 'husholdsart': '400',
                                 'mobler': '400', 'medier': '2240', 'biler': '2420',
                                 'barnehage': '0', 'sfo': '0', 'sumhusholdning': '5800',
                                 'totalt': '17980'}
