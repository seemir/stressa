# -*- coding: utf-8 -*-

"""
Test module for Portalen scraper against Finansportalen.no grunndata for boliglån

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import UUID
import json
import os
import shutil
from requests.models import Response
from requests.exceptions import ReadTimeout, ConnectionError as ConnectError

import mock
import pytest as pt

from source.util import NoConnectionError, NotFoundError, TimeOutError
from source.app import Portalen, Scraper


class TestPortalen:
    """
    Test cases for the Portalen scraper

    """

    @classmethod
    def setup(cls):
        """
        Runs before every test

        """
        cls.portalen = Portalen()

    def test_portalen_is_instance_of_scraper(self):
        """
        Test that Portalen scraper is instance and subclass of Scraper

        """
        assert isinstance(self.portalen, Portalen)
        assert isinstance(self.portalen, Scraper)
        assert issubclass(self.portalen.__class__, Scraper)

    def test_portalen_has_uuid4_compatible_id(self):
        """
        Test Portalen scraper has uuid4 compatible ids

        """
        assert UUID(str(self.portalen.id))

    def test_portalen_response_method(self):
        """
        Test that response method returns HTTP code 200: OK

        """
        response = self.portalen.response()
        assert response.status_code == 200
        assert isinstance(response, Response)

    def test_portalen_mortgage_offers_method(self):
        """
        Test the mortgage_offers in the Portalen scraper by confirming that the
        number of PORTALEN_ENTRIES are greater than 700

        """
        assert self.portalen.mortgage_offers().keys().__len__() >= 700

    @staticmethod
    @mock.patch("requests.post", mock.MagicMock(side_effect=ConnectError))
    def test_response_throws_no_connection_error_for_connection_error():
        """
        Test that response method throws NotConnectionError if requests.post throws ConnectionError

        """
        portalen = Portalen()
        with pt.raises(NoConnectionError):
            portalen.response()

    @staticmethod
    @mock.patch("requests.post", mock.MagicMock(side_effect=ReadTimeout))
    def test_response_throws_time_out_error_for_read_timeout():
        """
        Test that response method throws TimeOutError if requests.post throws ReadTimeout

        """
        portalen = Portalen()
        with pt.raises(TimeOutError):
            portalen.response()

    @staticmethod
    @mock.patch("source.app.scrapers.portalen.Portalen.response", mock.MagicMock(return_value=None))
    def test_mortgage_offers_throws_not_found_error_for_none_response():
        """
        Test that mortgage offers method throws NotFoundError if response is None

        """
        portalen = Portalen()
        with pt.raises(NotFoundError):
            portalen.mortgage_offers()

    @mock.patch("source.app.scrapers.portalen.Portalen.mortgage_offers",
                mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.portalen.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
