# -*- coding: utf-8 -*-

"""
Test module for the Ssb scraper object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from uuid import UUID
import json
import shutil

from requests.models import Response
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

import pytest as pt
import mock

from source.app import Ssb, SsbPayload, Scraper
from source.util import TrackingError


class TestSsb:
    """
    Test cases for the Ssb scraper object

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.payload = SsbPayload(tid=["2019M08"])
        cls.ssb = Ssb(cls.payload)

    def test_ssb_is_instance_of_scraper(self):
        """
        Test that Ssb objects are instances of Ssb class and subclass of Scraper

        """
        assert isinstance(self.ssb, Ssb)
        assert isinstance(self.ssb, Scraper)
        assert issubclass(self.ssb.__class__, Scraper)

    @staticmethod
    @pt.mark.parametrize("invalid_payload_type", [90210, 90210.0, True, [], (), {}])
    def test_ssb_raises_type_error_if_invalid_payload(invalid_payload_type):
        """
        TypeError thrown if Ssb gets passed an invalid payload type

        """
        with pt.raises(TypeError):
            Ssb(invalid_payload_type)

    def test_ssb_has_uuid4_compatible_id(self):
        """
        Test Ssb scraper has uuid4 compatible ids

        """
        assert UUID(str(self.ssb.id_))

    @pt.mark.parametrize("payload", [SsbPayload(rentebinding=["08"])])
    def test_payload_gets_set(self, payload):
        """
        Test that payload gets set in Ssb scraper object

        """
        self.ssb.payload = payload
        assert self.ssb.payload == payload

    @mock.patch("requests.post", mock.MagicMock(side_effect=ConnectError))
    def test_response_throws_tracking_error_for_connect_error(self):
        """
        Test that response method throws TrackingError if requests.post throws ConnectError

        """
        with pt.raises(TrackingError):
            self.ssb.response()

    @mock.patch("requests.post", mock.MagicMock(side_effect=ConnectTimeout))
    def test_response_throws_tracking_error_for_readtimeout(self):
        """
        Test that response method throws TrackingError if requests.post throws ConnectTimeout

        """
        with pt.raises(TrackingError):
            self.ssb.response()

    def test_ssb_response_method(self):
        """
        Test that response method returns HTTP code 200: OK

        """
        response = self.ssb.response()
        assert response.status_code == 200
        assert isinstance(response, Response)

    def test_ssb_interest_rates_method(self):
        """
        Test that ssb_interest_rates method return correct content

        """
        correct_content = {'inntil 3 måneder (flytende rente)': '2.85',
                           'over 3 måneder (fast rente)': '2.8', '1 år - 3 år': '2.7',
                           '3 år - 5 år': '2.8', 'over 5 år': '2.9'}
        assert self.ssb.ssb_interest_rates() == correct_content

    @mock.patch("source.app.scrapers.ssb.Ssb.response", mock.MagicMock(return_value=""))
    def test_ssb_interest_rates_throws_exception(self):
        """
        Patch that mocks Ssb.response() method to return '' and accordingly
        throws TrackingError

        """
        with pt.raises(TrackingError):
            self.ssb.ssb_interest_rates()

    @mock.patch("source.app.scrapers.ssb.Ssb.ssb_interest_rates", mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.ssb.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
