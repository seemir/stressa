# -*- coding: utf-8 -*-

"""
Test module for the Scraper against FinnStat.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json
import shutil
import os

from uuid import UUID
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError
import mock

import pytest as pt

from source.app import FinnStat, Scraper
from source.util import TrackingError


class TestFinnStat:
    """
    Test cases for the FinnStat scraper

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_stat = FinnStat("144857770")

    def test_finn_stat_is_instance_of_scraper(self):
        """
        Test that FinnStat object is instance and subclass of Scraper

        """
        for parent in [FinnStat, Scraper]:
            assert isinstance(self.finn_stat, parent)
            assert issubclass(self.finn_stat.__class__, parent)

    @staticmethod
    @pt.mark.parametrize("invalid_finn_stat_code_types",
                         [144857770, 144857770.0, True, [], (), {}])
    def test_invalid_finn_stat_code_raises_not_found_error(invalid_finn_stat_code_types):
        """
        Test that FinnStat raises TypeError for invalid finn_stat_code types

        """
        with pt.raises(TypeError):
            FinnStat(invalid_finn_stat_code_types)

    @pt.mark.parametrize("invalid_finn_stat_code", ["1448577", "2448577701", "24485777a"])
    def test_validate_finn_stat_code_method(self, invalid_finn_stat_code):
        """
        Test that invalid finn_stat_code raises TrackingError

        """
        with pt.raises(TrackingError):
            FinnStat(invalid_finn_stat_code)
        with pt.raises(TrackingError):
            self.finn_stat.validate_finn_code(invalid_finn_stat_code)

    def test_finn_stat_has_uuid4_compatible_id(self):
        """
        Test FinnStat scraper has uuid4 compatible ids

        """
        assert UUID(str(self.finn_stat.id_))

    def test_stat_response_method(self):
        """
        Test the FinnStat response method

        """
        assert self.finn_stat.stat_response().status_code == 200

    @staticmethod
    @mock.patch("requests.get", mock.MagicMock(side_effect=ConnectTimeout))
    def test_response_throws_tracking_error_for_time_out_error():
        """
        Test that response method throws TrackingError if requests.get throws ConnectTimeout

        """
        with pt.raises(TrackingError):
            finn_stat = FinnStat("144857770")
            finn_stat.stat_response()

    @staticmethod
    @mock.patch("requests.get", mock.MagicMock(side_effect=ConnectError))
    def test_response_throws_tracking_error_for_no_connection_error():
        """
        Test that response method throws TrackingError if requests.get throws ConnectError

        """
        with pt.raises(TrackingError):
            finn_stat = FinnStat("144857770")
            finn_stat.stat_response()

    @staticmethod
    @mock.patch("source.app.scrapers.finn_stat.FinnStat.stat_response",
                mock.MagicMock(return_value=None))
    def test_housing_stat_information_throws_not_found_error_if_none_response():
        """
        Test that housing_stat_information method does not throws AttributeError
        if stat_response is None

        """
        finn_stat = FinnStat("144857770")
        finn_stat.housing_stat_information()

    @mock.patch("source.app.scrapers.finn_stat.FinnStat.stat_response",
                mock.MagicMock(side_effect=ValueError("this is a test")))
    def test_housing_stat_information_throws_exception(self):
        """
        Test that housing_stat_information captures and raises exception

        """
        with pt.raises(TrackingError):
            self.finn_stat.housing_stat_information()

    @mock.patch("source.app.scrapers.finn_stat.FinnStat.housing_stat_information",
                mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.finn_stat.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
