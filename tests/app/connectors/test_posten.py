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

    def setup_method(self):
        """
        setup that is run before every tests

        """
        self.posten = Posten("0010")

    def test_posten_is_instance_of_connector(self):
        """
        Test that Posten connector is instance and subclass of connector

        """
        assert isinstance(self.posten, Posten)
        assert isinstance(self.posten, Connector)
        assert issubclass(self.posten.__class__, Connector)

    @staticmethod
    @pt.mark.parametrize("invalid_postal_code_type", [90210, 90210.0, True, [], (), {}])
    def test_posten_raises_type_error_if_invalid_postal_code_passed(invalid_postal_code_type):
        """
        TypeError thrown if Posten does not get passed a valid postal code type

        """
        with pt.raises(TypeError):
            Posten(invalid_postal_code_type)

    def test_posten_has_uuid4_compatible_id(self):
        """
        Test Posten connector has uuid4 compatible ids

        """
        assert UUID(str(self.posten.id_))

    @pt.mark.parametrize("postal_code", ["0010", "0018", "0021", "0026", "0027"])
    def test_postal_code_gets_set(self, postal_code):
        """
        Test that postal code gets set in Posten connector object

        """
        self.posten.postal_code = postal_code
        assert self.posten.postal_code == postal_code

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

    def test_posten_response_method(self):
        """
        Test that response method returns HTTP code 200: OK

        """
        response = self.posten.response()
        assert response.status_code == 200

    def test_postal_code_info_method(self):
        """
        Test that postal_code_info method return correct content

        """
        correct_content = {'postnr': '0010', 'poststed': 'OSLO',
                           'kommune': 'OSLO', 'fylke': 'OSLO'}
        assert self.posten.postal_code_info() == correct_content

    @mock.patch("requests.get", mock.MagicMock(side_effect=ConnectTimeout))
    def test_response_throws_tracking_error_for_read_timeout(self):
        """
        Test that response method throws TrackingError if ConnectTimeout

        """
        with pt.raises(TrackingError):
            self.posten.response()

    @mock.patch("requests.get", mock.MagicMock(side_effect=ConnectError))
    def test_response_throws_tracking_error_for_no_connection_error(self):
        """
        Test that response method throws TrackingError if ConnectError

        """
        with pt.raises(TrackingError):
            self.posten.response()

    @mock.patch("source.app.connectors.posten.Posten.response", mock.MagicMock(return_value=""))
    def test_postal_code_info_throws_not_found_error(self):
        """
        Patch that mocks Posten.response() method to return '' and accordingly
        throws TrackingError if NotFoundError when calling postal_code_info() method

        """
        with pt.raises(TrackingError):
            self.posten.postal_code_info()

    @mock.patch("source.app.connectors.posten.Posten.postal_code_info",
                mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.posten.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1]), encoding='utf-8') as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)
