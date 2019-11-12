# -*- coding: utf-8 -*-

"""
Test module for Posten scraper

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json
from uuid import UUID
import shutil

import mock
import pytest as pt
from mechanize._response import response_seek_wrapper

from source.app import Posten, Scraper
from source.util import NotFoundError


class TestPosten:
    """
    Test cases for Posten scraper

    """

    @classmethod
    def setup(cls):
        """
        Executed before every test

        """
        cls.posten = Posten("0010")

    def test_posten_is_instance_of_scraper(self):
        """
        Test that Posten scraper is instance and subclass of Scraper

        """
        assert isinstance(self.posten, Posten)
        assert isinstance(self.posten, Scraper)
        assert issubclass(self.posten.__class__, Scraper)

    @staticmethod
    @pt.mark.parametrize("invalid_zip_code_type", [90210, 90210.0, True, [], (), {}])
    def test_posten_raises_type_error_if_invalid_zip_code_passed(invalid_zip_code_type):
        """
        TypeError thrown if Posten does not get passed a valid zip code type

        """
        with pt.raises(TypeError):
            Posten(invalid_zip_code_type)

    def test_posten_has_uuid4_compatible_id(self):
        """
        Test Posten scraper has uuid4 compatible ids

        """
        assert UUID(str(self.posten.id_str))

    @pt.mark.parametrize("zip_code", ["0010", "0018", "0021", "0026", "0027"])
    def test_zip_code_gets_set(self, zip_code):
        """
        Test that zip code gets set in Posten scraper object

        """
        self.posten.zip_code = zip_code
        assert self.posten.zip_code == zip_code

    @pt.mark.parametrize("invalid_zip_code", ["0", "00", "000", "+0", "0+", "-1"])
    def test_validate_zip_code_method(self, invalid_zip_code):
        """
        Test that NotFoundError is thrown for invalid zip_codes

        """
        with pt.raises(NotFoundError):
            Posten(invalid_zip_code)
        with pt.raises(NotFoundError):
            self.posten.validate_zip_code(invalid_zip_code)

    @mock.patch("source.app.scrapers.posten.POSTEN_URL", mock.MagicMock(return_value=None))
    def test_posten_exception_for_invalid_url(self):
        """
        Test that posten raises TypeError if POSTEN_URL if None

        """
        with pt.raises(TypeError):
            self.posten.response()

    def test_posten_response_method(self):
        """
        Test that response method returns HTTP code 200: OK

        """
        assert self.posten.response().code == 200
        assert isinstance(self.posten.response(), response_seek_wrapper)

    def test_zip_code_info_method(self):
        """
        Test that zip_code_info method return correct content

        """
        correct_content = {'postnr': '0010', 'poststed': 'OSLO',
                           'kommune': 'OSLO', 'fylke': 'OSLO'}
        assert self.posten.zip_code_info() == correct_content

    @mock.patch("source.app.scrapers.posten.Posten.response", mock.MagicMock(return_value=""))
    def test_zip_code_info_throws_not_found_error(self):
        """
        Patch that mocks Posten.response() method to return '' and accordingly
        throws NotFoundError

        """
        with pt.raises(NotFoundError):
            self.posten.zip_code_info()

    @mock.patch("source.app.scrapers.posten.Posten.zip_code_info", mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.posten.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
        assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
