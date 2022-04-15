# -*- coding: utf-8 -*-

"""
Test module for the connectorr against FinnOwnership.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import shutil
import json

from uuid import UUID
import mock
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

import pytest as pt

from source.app import FinnOwnership, Connector
from source.util import TrackingError


class TestFinnOwnership:
    """
    Test cases for the FinnOwnership connectorr

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_ownership = FinnOwnership("144857770")

    def test_finn_ownership_is_instance_of_connectorr(self):
        """
        Test that FinnOwnership object is instance and subclass of connectorr

        """
        for parent in [FinnOwnership, Connector]:
            assert isinstance(self.finn_ownership, parent)
            assert issubclass(self.finn_ownership.__class__, parent)

    @staticmethod
    @pt.mark.parametrize("invalid_finn_ownership_code_types",
                         [144857770, 144857770.0, True, [], (), {}])
    def test_invalid_finn_ownership_code_raises_not_found_error(invalid_finn_ownership_code_types):
        """
        Test that FinnOwnership raises TypeError for invalid finn_ownership_code types

        """
        with pt.raises(TypeError):
            FinnOwnership(invalid_finn_ownership_code_types)

    @pt.mark.parametrize("invalid_finn_ownership_code", ["1448577", "2448577701", "24485777a"])
    def test_validate_finn_ownership_code_method(self, invalid_finn_ownership_code):
        """
        Test that invalid finn_ownership_code raises TrackingError

        """
        with pt.raises(TrackingError):
            FinnOwnership(invalid_finn_ownership_code)
        with pt.raises(TrackingError):
            self.finn_ownership.validate_finn_code(invalid_finn_ownership_code)

    def test_finn_ownership_has_uuid4_compatible_id(self):
        """
        Test FinnOwnership connectorr has uuid4 compatible ids

        """
        assert UUID(str(self.finn_ownership.id_))

    def test_ownership_response_method(self):
        """
        Test the FinnOwnership response method

        """
        assert self.finn_ownership.ownership_response().status_code == 200

    @staticmethod
    @mock.patch("requests.get", mock.MagicMock(side_effect=ConnectTimeout))
    def test_response_throws_tracking_error_for_time_out():
        """
        Test that response method throws TrackingError if requests.get throws ConnectTimeout

        """
        with pt.raises(TrackingError):
            finn_ownership = FinnOwnership("144857770")
            finn_ownership.ownership_response()

    @staticmethod
    @mock.patch("requests.get", mock.MagicMock(side_effect=ConnectError))
    def test_response_throws_tracking_error_no_connection():
        """
        Test that response method throws TrackingError if requests.get throws ConnectError

        """
        with pt.raises(TrackingError):
            finn_ownership = FinnOwnership("144857770")
            finn_ownership.ownership_response()

    @staticmethod
    @mock.patch("source.app.connectors.finn_ownership.FinnOwnership.ownership_response",
                mock.MagicMock(return_value=None))
    def test_housing_ownership_information_throws_not_found_error_if_none_response():
        """
        Test that housing_ownership_information method does not throws AttributeError
        if ownership_response is None

        """
        finn_ownership = FinnOwnership("144857770")
        finn_ownership.housing_ownership_information()

    @mock.patch("source.app.connectors.finn_ownership.FinnOwnership.ownership_response",
                mock.MagicMock(side_effect=ValueError("this is a test")))
    def test_housing_ownership_information_throws_exception(self):
        """
        Test that housing_ad_information captures and raises exception

        """
        with pt.raises(TrackingError):
            self.finn_ownership.housing_ownership_information()

    @mock.patch("source.app.connectors.finn_ownership.FinnOwnership.housing_ownership_information",
                mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.finn_ownership.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
