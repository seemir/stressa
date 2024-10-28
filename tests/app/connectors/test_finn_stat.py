# -*- coding: utf-8 -*-

"""
Test module for the connector against FinnStat.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json
import shutil
import os

from uuid import UUID

import asyncio
from asyncio import TimeoutError as TError
from aiohttp.client_exceptions import ClientConnectionError

import pytest as pt
import mock

from source.app import FinnStat, Connector
from source.util import TimeOutError, TrackingError, NoConnectionError


class TestFinnStat:
    """
    Test cases for the FinnStat connector

    """

    def setup_method(self):
        """
        setup that is run before every tests

        """
        self.finn_stat = FinnStat("144857770")

    def test_finn_stat_is_instance_of_connector(self):
        """
        Test that FinnStat object is instance and subclass of connector

        """
        for parent in [FinnStat, Connector]:
            assert isinstance(self.finn_stat, parent)
            assert issubclass(self.finn_stat.__class__, parent)

    @staticmethod
    @pt.mark.parametrize("invalid_finn_stat_code_types",
                         [144857770, 144857770.0, True, [], (), {}])
    def test_invalid_finn_stat_code_raises_not_found_error(
            invalid_finn_stat_code_types):
        """
        Test that FinnStat raises TypeError for invalid finn_stat_code types

        """
        with pt.raises(TypeError):
            FinnStat(invalid_finn_stat_code_types)

    @pt.mark.parametrize("invalid_finn_stat_code",
                         ["1448577", "2448577701", "24485777a"])
    def test_validate_finn_stat_code_method(self, invalid_finn_stat_code):
        """
        Test that invalid finn_stat_code raises TrackingError

        """
        with pt.raises(TrackingError):
            FinnStat(invalid_finn_stat_code)

    def test_finn_stat_has_uuid4_compatible_id(self):
        """
        Test FinnStat connector has uuid4 compatible ids

        """
        assert UUID(str(self.finn_stat.id_))

    def test_stat_response_method(self):
        """
        Test the FinnStat response method

        """
        assert asyncio.run(self.finn_stat.stat_response())

    @staticmethod
    @mock.patch("aiohttp.ClientSession.get", mock.MagicMock(side_effect=TError))
    def test_response_throws_time_out_error_for_time_out_error():
        """
        Test that response method throws TimeOutError if aiohttp.ClientSession.get
        throws TimeoutError

        """
        with pt.raises(TimeOutError):
            finn_stat = FinnStat("144857770")
            asyncio.run(finn_stat.stat_response())

    @staticmethod
    @mock.patch("aiohttp.ClientSession.get",
                mock.MagicMock(side_effect=ClientConnectionError))
    def test_response_throws_no_connection_error_for_client_connection_error():
        """
        Test that response method throws NoConnectionError if aiohttp.ClientSession.get
        throws ClientConnectionError

        """
        with pt.raises(NoConnectionError):
            finn_stat = FinnStat("144857770")
            asyncio.run(finn_stat.stat_response())

    @staticmethod
    @mock.patch("source.app.connectors.finn_stat.FinnStat.stat_response",
                mock.MagicMock(return_value=None))
    def test_housing_stat_information_throws_tracking_error_if_none_response():
        """
        Test that housing_stat_information method throws TrackingError if stat_response is None

        """
        with pt.raises(TrackingError):
            finn_stat = FinnStat("144857770")
            finn_stat.housing_stat_information()

    @mock.patch("source.app.connectors.finn_stat.FinnStat.stat_response",
                mock.MagicMock(side_effect=ValueError("this is a test")))
    def test_housing_stat_information_throws_exception(self):
        """
        Test that housing_stat_information captures and raises exception

        """
        with pt.raises(TrackingError):
            self.finn_stat.housing_stat_information()

    @mock.patch(
        "source.app.connectors.finn_stat.FinnStat.housing_stat_information",
        mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.finn_stat.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1]),
                  encoding='utf-8') as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
