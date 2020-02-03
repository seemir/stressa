# -*- coding: utf-8 -*-

"""
Test module for Posten scraper

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json
from uuid import UUID
from urllib.error import URLError
import shutil

import mock
import pytest as pt
from mechanize._response import response_seek_wrapper

from source.util import NotFoundError, NoConnectionError, TimeOutError
from source.app import Posten, Scraper


class TestPosten:
    """
    Test cases for Posten scraper

    """

    @staticmethod
    def test_posten_is_instance_of_scraper():
        """
        Test that Posten scraper is instance and subclass of Scraper

        """
        posten = Posten("0010")
        assert isinstance(posten, Posten)
        assert isinstance(posten, Scraper)
        assert issubclass(posten.__class__, Scraper)

    @staticmethod
    @pt.mark.parametrize("invalid_zip_code_type", [90210, 90210.0, True, [], (), {}])
    def test_posten_raises_type_error_if_invalid_zip_code_passed(invalid_zip_code_type):
        """
        TypeError thrown if Posten does not get passed a valid zip code type

        """
        with pt.raises(TypeError):
            Posten(invalid_zip_code_type)

    @staticmethod
    def test_posten_has_uuid4_compatible_id():
        """
        Test Posten scraper has uuid4 compatible ids

        """
        posten = Posten("0010")
        assert UUID(str(posten.id_))

    @staticmethod
    @pt.mark.parametrize("zip_code", ["0010", "0018", "0021", "0026", "0027"])
    def test_zip_code_gets_set(zip_code):
        """
        Test that zip code gets set in Posten scraper object

        """
        posten = Posten("0010")
        posten.zip_code = zip_code
        assert posten.zip_code == zip_code

    @staticmethod
    @pt.mark.parametrize("invalid_zip_code", ["0", "00", "000", "+0", "0+", "-1"])
    def test_validate_zip_code_method(invalid_zip_code):
        """
        Test that NotFoundError is thrown for invalid zip_codes

        """
        with pt.raises(NotFoundError):
            Posten(invalid_zip_code)
        with pt.raises(NotFoundError):
            Posten.validate_zip_code(invalid_zip_code)

    @staticmethod
    def test_posten_response_method():
        """
        Test that response method returns HTTP code 200: OK

        """
        posten = Posten("0010")
        response = posten.response()
        assert response.code == 200
        assert isinstance(response, response_seek_wrapper)

    @staticmethod
    def test_zip_code_info_method():
        """
        Test that zip_code_info method return correct content

        """
        posten = Posten("0010")
        correct_content = {'postnr': '0010', 'poststed': 'OSLO',
                           'kommune': 'OSLO', 'fylke': 'OSLO'}
        assert posten.zip_code_info() == correct_content

    @staticmethod
    @mock.patch("mechanize.Browser.open", mock.MagicMock(side_effect=URLError("timed out")))
    def test_response_throws_time_out_error_for_read_timeout():
        """
        Test that response method throws TimeOutError

        """
        posten = Posten("0010")
        with pt.raises(TimeOutError):
            posten.response()

    @staticmethod
    @mock.patch("mechanize.Browser.open", mock.MagicMock(side_effect=URLError("")))
    def test_response_throws_no_connection_error():
        """
        Test that response method throws NoConnectionError

        """
        posten = Posten("0010")
        with pt.raises(NoConnectionError):
            posten.response()

    @staticmethod
    @mock.patch("source.app.scrapers.posten.Posten.response", mock.MagicMock(return_value=""))
    def test_zip_code_info_throws_not_found_error():
        """
        Patch that mocks Posten.response() method to return '' and accordingly
        throws NotFoundError when calling zip_code_info() method

        """
        posten = Posten("0010")
        with pt.raises(NotFoundError):
            posten.zip_code_info()

    @staticmethod
    @mock.patch("source.app.scrapers.posten.Posten.zip_code_info", mock.MagicMock(return_value=""))
    def test_to_json():
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        posten = Posten("0010")
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        posten.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1])) as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
