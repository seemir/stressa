# -*- coding: utf-8 -*-
"""
Test module for the ScrapeFinnOwnershipHistory operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, ScrapeFinnOwnershipHistory, FINN_OWNER_URL
from source.util import TrackingError


class TestScrapeFinnOwnershipHistory:
    """
    Test cases for the ScrapeFinnOwnershipHistory

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_code = "144857770"
        cls.scrape_finn_ownership_history = ScrapeFinnOwnershipHistory(cls.finn_code)

    def test_scrape_finn_ownership_history_is_instance_of_operation(self):
        """
        Test that ScrapeFinnOwnershipHistory is instance and subclass of Operation

        """
        for parent in [ScrapeFinnOwnershipHistory, Operation]:
            assert isinstance(self.scrape_finn_ownership_history, parent)
            assert issubclass(self.scrape_finn_ownership_history.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_finn_code', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_finn_code):
        """
        Test that ScrapeFinnOwnershipHistory object raises TrackingError if finn_code
        argument are invalid

        """
        with pt.raises(TrackingError):
            ScrapeFinnOwnershipHistory(invalid_finn_code)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the ScrapeFinnOwnershipHistory object

        """
        name = self.scrape_finn_ownership_history.__class__.__name__
        assert self.scrape_finn_ownership_history.name == name
        assert self.scrape_finn_ownership_history.finn_code == self.finn_code
        assert self.scrape_finn_ownership_history.desc == "from: '{}\\<[finn_code]\\>' " \
                                                          "\\n id: Scrape FINN Ownership " \
                                                          "History".format(FINN_OWNER_URL)

    def test_scrape_finn_ownership_history_run_method(self):
        """
        Test the run method in ScrapeFinnOwnershipHistory operation

        """
        ownership_history = self.scrape_finn_ownership_history.run()
        assert ownership_history["historikk"] == {'Tinglyst': {0: '30.06.1994'},
                                                  'Boligtype': {0: 'Frittliggende enebolig'},
                                                  'Pris': {0: '3\xa0950\xa0000 kr'}}
