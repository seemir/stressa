# -*- coding: utf-8 -*-

"""
Test module for Posten connector

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json
from uuid import UUID
import shutil

import mock
import pytest as pt
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from source.util import TrackingError
from source.app import Posten, Connector


class TestPosten:
    """
    Test cases for Posten connector

    """

    @staticmethod
    def test_posten_is_instance_of_connector():
        """
        Test that Posten connector is instance and subclass of connector

        """
        posten = Posten("0010")
        assert isinstance(posten, Posten)
        assert isinstance(posten, Connector)
        assert issubclass(posten.__class__, Connector)

    @staticmethod
    @pt.mark.parametrize("invalid_postal_code_type", [90210, 90210.0, True, [], (), {}])
    def test_posten_raises_type_error_if_invalid_postal_code_passed(invalid_postal_code_type):
        """
        TypeError thrown if Posten does not get passed a valid postal code type

        """
        with pt.raises(TypeError):
            Posten(invalid_postal_code_type)

    @staticmethod
    def test_posten_has_uuid4_compatible_id():
        """
        Test Posten connector has uuid4 compatible ids

        """
        posten = Posten("0010")
        assert UUID(str(posten.id_))

    @staticmethod
    @pt.mark.parametrize("postal_code", ["0010", "0018", "0021", "0026", "0027"])
    def test_postal_code_gets_set(postal_code):
        """
        Test that postal code gets set in Posten connector object

        """
        posten = Posten("0010")
        posten.postal_code = postal_code
        assert posten.postal_code == postal_code

    @staticmethod
    @pt.mark.parametrize("invalid_postal_code", ["0", "00", "000", "+0", "0+", "-1"])
    def test_validate_postal_code_method(invalid_postal_code):
        """
        Test that TrackingError is thrown for invalid zip_codes

        """
        with pt.raises(TrackingError):
            Posten(invalid_postal_code)
        with pt.raises(TrackingError):
            Posten.validate_postal_code(invalid_postal_code)

    @staticmethod
    def test_posten_response_method():
        """
        Test that response method returns HTTP code 200: OK

        """
        posten = Posten("0010")
        response = posten.response()
        assert response.status_code == 200

    @staticmethod
    def test_postal_code_info_method():
        """
        Test that postal_code_info method return correct content

        """
        posten = Posten("0010")
        correct_content = {'postnr': '0010', 'poststed': 'OSLO',
                           'kommune': 'OSLO', 'fylke': 'OSLO'}
        assert posten.postal_code_info() == correct_content

    @staticmethod
    @mock.patch("requests.get", mock.MagicMock(side_effect=ConnectTimeout))
    def test_response_throws_tracking_error_for_read_timeout():
        """
        Test that response method throws TrackingError if ConnectTimeout

        """
        posten = Posten("0010")
        with pt.raises(TrackingError):
            posten.response()

    @staticmethod
    @mock.patch("requests.get", mock.MagicMock(side_effect=ConnectError))
    def test_response_throws_tracking_error_for_no_connection_error():
        """
        Test that response method throws TrackingError if ConnectError

        """
        posten = Posten("0010")
        with pt.raises(TrackingError):
            posten.response()

    @staticmethod
    @mock.patch("source.app.connectors.posten.Posten.response", mock.MagicMock(return_value=""))
    def test_postal_code_info_throws_not_found_error():
        """
        Patch that mocks Posten.response() method to return '' and accordingly
        throws TrackingError if NotFoundError when calling postal_code_info() method

        """
        posten = Posten("0010")
        with pt.raises(TrackingError):
            posten.postal_code_info()

    @staticmethod
    @mock.patch("source.app.connectors.posten.Posten.postal_code_info",
                mock.MagicMock(return_value=""))
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
