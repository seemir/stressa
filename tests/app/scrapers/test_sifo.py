# -*- coding: utf-8 -*-

"""
Test module for Sifo scraper class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import shutil
import os
import json

from uuid import UUID
from urllib.error import URLError

import mock
import pytest as pt
from mechanize import Browser
from mechanize._response import response_seek_wrapper

from source.domain import Female, Family, Male
from source.util import NoConnectionError, TimeOutError
from source.app import Scraper, Sifo


class TestSifo:
    """
    Test cases for Sifo scraper

    """

    @classmethod
    def setup(cls):
        """
        Executed before every test

        """
        family_members = [Male(age=45), Female(age=40)]
        cls.family = Family(family_members, income=850000, cars=1)
        cls.sifo = Sifo(cls.family)

    def test_sifo_is_instance_of_scraper(self):
        """
        Test that Sifo scraper is instance and subclass of Scraper

        """
        assert isinstance(self.sifo, Sifo)
        assert isinstance(self.sifo, Scraper)
        assert issubclass(self.sifo.__class__, Scraper)

    def test_sifo_has_browser_object_as_attribute(self):
        """
        Test that Sifo scraper has Browser object

        """
        assert isinstance(self.sifo.browser, Browser)

    @staticmethod
    @pt.mark.parametrize("invalid_family", [90210, 90210.0, True, [], (), {}])
    def test_sifo_raises_type_error_if_family_instance_not_passed(invalid_family):
        """
        TypeError thrown if Sifo does not get passed a Family instance
        through constructor

        """
        with pt.raises(TypeError):
            Sifo(invalid_family)

    def test_sifo_has_uuid4_compatible_id(self):
        """
        Test sifo scraper has uuid4 compatible ids

        """
        assert UUID(str(self.sifo.id_))

    def test_that_family_gets_set(self):
        """
        Test that Family object gets set if passed through constructor or setter

        """
        assert self.sifo.family == self.family
        new_family = Family([Female(age=40), Female(age=13, sfo='1'), Male(age=10, sfo='1')])
        self.sifo.family = new_family
        assert self.sifo.family == new_family

    @mock.patch("mechanize.Browser.open", mock.MagicMock(side_effect=URLError("timed out")))
    def test_response_throws_time_out_error_for_read_timeout(self):
        """
        Test that response method throws TimeOutError

        """
        with pt.raises(TimeOutError):
            self.sifo.response()

    @mock.patch("mechanize.Browser.open", mock.MagicMock(side_effect=URLError("")))
    def test_response_throws_no_connection_error(self):
        """
        Test that response method throws NoConnectionError

        """
        with pt.raises(NoConnectionError):
            self.sifo.response()

    def test_sifo_response_received(self):
        """
        Test HTTP response 200 is received and of correct type, i.e. response_seek_wrapper

        """
        response = self.sifo.response()
        assert response.code == 200
        assert isinstance(response, response_seek_wrapper)

    def test_sifo_expenses_method(self):
        """
        Test that sifo_expenses method returns correct content

        """
        correct_content = {'mat': '5290', 'klar': '1590', 'helse': '1320', 'fritid': '2480',
                           'kollektivt': '1500', 'spedbarn': '0', 'stordriftsfordel': '1',
                           'sumindivid': '12180', 'dagligvarer': '340', 'husholdsart': '400',
                           'mobler': '400', 'medier': '2240', 'biler': '2420', 'barnehage': '0',
                           'sfo': '0', 'sumhusholdning': '5800', 'totalt': '17980'}
        sifo_expenses = self.sifo.sifo_base_expenses()
        assert sifo_expenses == correct_content
        assert "_id" not in sifo_expenses.keys()

    @mock.patch("source.app.scrapers.sifo.Sifo.sifo_base_expenses", mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.sifo.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)

    @mock.patch("source.app.scrapers.sifo.Sifo.response", mock.MagicMock(return_value=""))
    def test_sifo_expenses_raises_exception(self):
        """
        Test that sifo_base_expenses() method raises exception if no response received
        from response() method.

        """
        with pt.raises(Exception):
            self.sifo.sifo_base_expenses()

    @mock.patch("xml.etree.ElementTree", mock.MagicMock(return_value={}))
    def test_include_id_in_sifo_expenses_method(self):
        """
        Test that '_id' is included in output from sifo_expenses() method

        """
        assert "_id" in self.sifo.sifo_base_expenses(include_id=True).keys()

    def test_sifo_scraper_id_is_uuid4(self):
        """
        Test that sifo id is uuid4 compatible

        """
        assert UUID(str(self.sifo.id_))
