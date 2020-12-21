# -*- coding: utf-8 -*-
"""
Test module for the ScrapeFinnStatisticsInfo operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, ScrapeFinnStatisticsInfo, FINN_STAT_URL
from source.util import TrackingError


class TestScrapeFinnStatisticsInfo:
    """
    Test cases for the ScrapeFinnStatisticsInfo

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_code = "144857770"
        cls.scrape_finn_statistics_info = ScrapeFinnStatisticsInfo(cls.finn_code)

    def test_scrape_finn_statistics_info_is_instance_of_operation(self):
        """
        Test that ScrapeFinnStatisticsInfo is instance and subclass of Operation

        """
        for parent in [ScrapeFinnStatisticsInfo, Operation]:
            assert isinstance(self.scrape_finn_statistics_info, parent)
            assert issubclass(self.scrape_finn_statistics_info.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_finn_code', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_finn_code):
        """
        Test that ScrapeFinnStatisticsInfo object raises TrackingError if finn_code
        argument are invalid

        """
        with pt.raises(TrackingError):
            ScrapeFinnStatisticsInfo(invalid_finn_code)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the ScrapeFinnStatisticsInfo object

        """
        name = self.scrape_finn_statistics_info.__class__.__name__
        assert self.scrape_finn_statistics_info.name == name
        assert self.scrape_finn_statistics_info.finn_code == self.finn_code
        assert self.scrape_finn_statistics_info.desc == "from: '{}\\<[finn_code]\\>' " \
                                                        "\\n id: Scrape FINN Statistics " \
                                                        "Info".format(FINN_STAT_URL)
