# -*- coding: utf-8 -*-

"""
Test module for the Connector against FinnAd.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json
import shutil

from uuid import UUID
import mock as mocker
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

import pytest as pt

from source.app import FinnAd, Connector
from source.util import TrackingError


class TestFinnAd:
    """
    Test cases for the FinnAd connector

    """

    def setup_method(self):
        """
        setup that is run before every tests

        """
        self.finn_ad = FinnAd("144857770")

    def test_finn_ad_is_instance_of_connector(self):
        """
        Test that FinnAd object is instance and subclass of Connector

        """
        for parent in [FinnAd, Connector]:
            assert isinstance(self.finn_ad, parent)
            assert issubclass(self.finn_ad.__class__, parent)

    @staticmethod
    @pt.mark.parametrize("invalid_finn_ad_code_types", [144857770, 144857770.0, True, [], (), {}])
    def test_invalid_finn_ad_code_raises_not_found_error(invalid_finn_ad_code_types):
        """
        Test that FinnAd raises TypeError for invalid finn_ad_code types

        """
        with pt.raises(TypeError):
            FinnAd(invalid_finn_ad_code_types)

    @pt.mark.parametrize("invalid_finn_ad_code", ["1448577", "2448577701", "24485777a"])
    def test_validate_finn_ad_code_method(self, invalid_finn_ad_code):
        """
        Test that invalid finn_ad_code raises TrackingError

        """
        with pt.raises(TrackingError):
            FinnAd(invalid_finn_ad_code)
        with pt.raises(TrackingError):
            self.finn_ad.validate_finn_code(invalid_finn_ad_code)

    def test_finn_ad_has_uuid4_compatible_id(self):
        """
        Test FinnAd connector has uuid4 compatible ids

        """
        assert UUID(str(self.finn_ad.id_))

    def test_ad_response_method(self):
        """
        Test the FinnAd response method

        """
        assert self.finn_ad.ad_response().status_code == 200

    @staticmethod
    @mocker.patch("requests.get", mocker.MagicMock(side_effect=ConnectTimeout))
    def test_response_throws_tracking_error_for_time_out():
        """
        Test that response method throws TrackingError if requests.get throws ConnectTimeOut

        """
        with pt.raises(TrackingError):
            finn_ad = FinnAd("144857770")
            finn_ad.ad_response()

    @staticmethod
    @mocker.patch("requests.get", mocker.MagicMock(side_effect=ConnectError))
    def test_response_throws_tracking_error_for_no_connection():
        """
        Test that response method throws TrackingError if requests.get throws ConnectError

        """
        with pt.raises(TrackingError):
            finn_ad = FinnAd("144857770")
            finn_ad.ad_response()

    @staticmethod
    @mocker.patch("source.app.connectors.finn_ad.FinnAd.ad_response",
                  mocker.MagicMock(return_value=None))
    def test_housing_ad_information_throws_not_found_error_if_none_response():
        """
        Test that housing_ad_information method throws TrackingError if ad_response is None

        """
        with pt.raises(TrackingError):
            finn_ad = FinnAd("144857770")
            finn_ad.housing_ad_information()

    @mocker.patch("source.app.connectors.finn_ad.FinnAd.housing_ad_information",
                  mocker.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.finn_ad.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)

    def test_finn_ad_has_no_browser_object(self):
        """
        Test that FinnAd has no _browser object

        """
        assert not self.finn_ad.browser
