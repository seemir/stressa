# -*- coding: utf-8 -*-
"""
Test module for the connectorFinnOwnershipHistory operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, FinnOwnershipHistoryConnector, FINN_OWNER_URL
from source.util import TrackingError


class TestFinnOwnershipHistoryConnector:
    """
    Test cases for the FinnOwnershipHistoryConnector

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_code = "144857770"
        cls.connector_finn_ownership_history = FinnOwnershipHistoryConnector(cls.finn_code)

    def test_connector_finn_ownership_history_is_instance_of_operation(self):
        """
        Test that FinnOwnershipHistoryConnector is instance and subclass of Operation

        """
        for parent in [FinnOwnershipHistoryConnector, Operation]:
            assert isinstance(self.connector_finn_ownership_history, parent)
            assert issubclass(self.connector_finn_ownership_history.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_finn_code', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_finn_code):
        """
        Test that FinnOwnershipHistoryConnector object raises TrackingError if finn_code
        argument are invalid

        """
        with pt.raises(TrackingError):
            FinnOwnershipHistoryConnector(invalid_finn_code)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the FinnOwnershipHistoryConnector object

        """
        name = self.connector_finn_ownership_history.__class__.__name__
        assert self.connector_finn_ownership_history.name == name
        assert self.connector_finn_ownership_history.finn_code == self.finn_code
        assert self.connector_finn_ownership_history.desc == "from: '{}\\<[finn_code]\\>' " \
                                                             "\\n id: FINN Ownership " \
                                                             "History Connector".format(
            FINN_OWNER_URL)

    def test_connector_finn_ownership_history_run_method(self):
        """
        Test the run method in FinnOwnershipHistoryConnector operation

        """
        ownership_history = self.connector_finn_ownership_history.run()
        assert ownership_history["historikk"] == {
            'Boligtype': {0: 'Frittliggende enebolig', 1: 'Frittliggende enebolig'},
            'Pris': {0: '67\xa0000\xa0000 kr', 1: '3\xa0950\xa0000 kr'},
            'Tinglyst': {0: '08.02.2022', 1: '30.06.1994'}}
