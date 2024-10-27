# -*- coding: utf-8 -*-
"""
Test module for the FinnStatisticsInfoConnector operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, FinnStatisticsInfoConnector, FINN_STAT_URL
from source.util import TrackingError


class TestFinnStatisticsInfoConnector:
    """
    Test cases for the FinnStatisticsInfoConnector

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.finn_code = "144857770"
        self.connector_finn_statistics_info = FinnStatisticsInfoConnector(self.finn_code)

    def test_connector_finn_statistics_info_is_instance_of_operation(self):
        """
        Test that FinnStatisticsInfoConnector is instance and subclass of Operation

        """
        for parent in [FinnStatisticsInfoConnector, Operation]:
            assert isinstance(self.connector_finn_statistics_info, parent)
            assert issubclass(self.connector_finn_statistics_info.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_finn_code', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_finn_code):
        """
        Test that FinnStatisticsInfoConnector object raises TrackingError if finn_code
        argument are invalid

        """
        with pt.raises(TrackingError):
            FinnStatisticsInfoConnector(invalid_finn_code)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the FinnStatisticsInfoConnector object

        """
        name = self.connector_finn_statistics_info.__class__.__name__
        assert self.connector_finn_statistics_info.name == name
        assert self.connector_finn_statistics_info.finn_code == self.finn_code
        assert self.connector_finn_statistics_info.desc == "from: '{}\\<[finn_code]\\>' " \
                                                           "\\n id: FINN Statistics " \
                                                           "Info Connector".format(FINN_STAT_URL)
