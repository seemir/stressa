# -*- coding: utf-8 -*-

"""
Test module for the Scraper against Finn.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json
import shutil
import os
from uuid import UUID
from requests.models import Response
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

import mock
import pytest as pt

from source.app import Finn
from source.util import NotFoundError, NoConnectionError, TimeOutError


class TestFinn:
    """
    Test cases for the Finn scraper

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn = Finn("144857770")

    def test_finn_is_instance_of_scraper(self):
        """
        Test that Finn object is instance and subclass of Scraper

        """
        assert isinstance(self.finn, Finn)
        assert isinstance(self.finn, Finn)
        assert issubclass(self.finn.__class__, Finn)

    @staticmethod
    @pt.mark.parametrize("invalid_finn_code_types", [144857770, 144857770.0, True, [], (), {}])
    def test_invalid_finn_code_raises_not_found_error(invalid_finn_code_types):
        """
        Test that Finn raises TypeError for invalid finn_code types

        """
        with pt.raises(TypeError):
            Finn(invalid_finn_code_types)

    @pt.mark.parametrize("invalid_finn_code", ["14485777", "244857770", "24485777a"])
    def test_validate_finn_code_method(self, invalid_finn_code):
        """
        Test that invalid finn_code raises NotFoundError

        """
        with pt.raises(NotFoundError):
            Finn(invalid_finn_code)
        with pt.raises(NotFoundError):
            self.finn.validate_finn_code(invalid_finn_code)

    def test_finn_has_uuid4_compatible_id(self):
        """
        Test Finn scraper has uuid4 compatible ids

        """
        assert UUID(str(self.finn.id))

    def test_finn_response_method(self):
        """
        Test that response method returns HTTP code 200: OK

        """
        ad_response, stat_response = self.finn.response()
        assert ad_response.status_code == 200
        assert isinstance(ad_response, Response)

        assert stat_response.status_code == 200
        assert isinstance(stat_response, Response)

    def test_housing_information_method(self):
        """
        Test that the housing_information method returns correct information

        """
        assert len(self.finn.housing_information().keys()) == 26

    @staticmethod
    @mock.patch("requests.post", mock.MagicMock(side_effect=ConnectError))
    def test_response_throws_no_connection_error_for_connection_error():
        """
        Test that response method throws NotConnectionError if requests.post throws ConnectionError

        """
        finn = Finn("144857770")
        with pt.raises(NoConnectionError):
            finn.response()

    @staticmethod
    @mock.patch("requests.post", mock.MagicMock(side_effect=ConnectTimeout))
    def test_response_throws_time_out_error_for_readtimeout():
        """
        Test that response method throws TimeOutError if requests.post throws ReadTimeout

        """
        finn = Finn("144857770")
        with pt.raises(TimeOutError):
            finn.response()

    @staticmethod
    @mock.patch("source.app.scrapers.finn.Finn.response", mock.MagicMock(return_value=None))
    def test_housing_information_throws_not_found_error_for_none_response():
        """
        Test that housing_information method throws NotFoundError if response is None

        """
        finn = Finn("144857770")
        with pt.raises(NotFoundError):
            finn.housing_information()

    @staticmethod
    def test_housing_information_throws_not_found_error():
        """
        Test that housing_information method throws NotFoundError for invalid FINN-code

        """
        finn = Finn("144857771")
        with pt.raises(NotFoundError):
            finn.housing_information()

    @mock.patch("source.app.scrapers.finn.Finn.housing_information",
                mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.finn.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
