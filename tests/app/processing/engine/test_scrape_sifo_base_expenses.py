# -*- coding: utf-8 -*-

"""
Test module for the scrape base expenses operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import ScrapeSifoBaseExpenses, Operation
from source.domain import Male, Female, Family
from source.util import TrackingError


class TestScrapeSifoBaseExpenses:
    """
    Test cases for ScrapeSifoBaseExpenses operation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.family = Family([Male(30), Female(29)], income=850000, cars=1, select_year=2021)

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
    def test_invalid_args_raises_tracking_error(invalid_data):
        """
        Test that ScrapeSifoBaseExpenses object raises TrackingError if data is invalid

        """
        with pt.raises(TrackingError):
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
        assert scraper.run() == {'barnehage': '0', 'biler': '2608', 'dagligvarer': '390',
                                 'fritid': '3020', 'helse': '1580', 'husholdsart': '430',
                                 'klar': '1850', 'kollektivt': '1590', 'mat': '7170',
                                 'medier': '1970', 'mobler': '490', 'sfo': '0', 'spedbarn': '0',
                                 'sumhusholdning': '5888', 'sumindivid': '15210', 'totalt': '21098'}
