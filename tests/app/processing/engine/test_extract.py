# -*- coding: utf-8 -*-
"""
Test module for the extract operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, Extract
from source.util import TrackingError


class TestExtract:
    """
    Test cases for the Extract operation

    """

    def setup_method(self):
        """
        Executed before all tests

        """
        self.data = {"klar": "500 kr", "sko": "500 kr", "mat": "500 kr", "totalt": "1500"}

    def test_extract_is_instance_of_operation(self):
        """
        Test that Extract is instance and subclass of Operation

        """
        extract = Extract(self.data, "totalt")
        for parent in [Extract, Operation]:
            assert isinstance(extract, parent)
            assert issubclass(extract.__class__, parent)

    @pt.mark.parametrize('invalid_data', [True, 'test', 90210, 90210.0, ('test', 'test')])
    @pt.mark.parametrize('invalid_key', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(self, invalid_data, invalid_key):
        """
        Test that Extract object raises TrackingError if data or desc argument are invalid

        """
        with pt.raises(TrackingError):
            Extract(invalid_data, "totalt")
        with pt.raises(TrackingError):
            Extract(self.data, invalid_key)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the Extract object

        """
        extract = Extract(self.data, "totalt")
        assert extract.data == self.data
        assert extract.key == "totalt"

    def test_extract_run_method(self):
        """
        Test the run method in the Extract operation

        """
        extract = Extract(self.data, "totalt")
        assert extract.run() == {'totalt': '1500'}

    def test_extract_run_method_with_non_existing_key(self):
        """
        Test the run method in the Extract operation with a non existing key

        """
        extract = Extract(self.data, "sub_total")
        assert not extract.run()
