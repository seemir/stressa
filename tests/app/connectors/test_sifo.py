# -*- coding: utf-8 -*-

"""
Test module for Sifo connector class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import shutil
import os
import json

from uuid import UUID
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError
from requests import Response

import mock
import pytest as pt
from mechanize import Browser

from source.domain import Female, Family, Male
from source.util import TrackingError
from source.app import Connector, Sifo


class TestSifo:
    """
    Test cases for Sifo connector

    """

    def setup_method(self):
        """
        setup that is run before every tests

        """
        self.family_members = [Male(age=45), Female(age=40)]
        self.family = Family(self.family_members, income=850000, fossil_cars=1, select_year=2021)
        self.sifo = Sifo(self.family)

    def test_sifo_is_instance_of_connector(self):
        """
        Test that Sifo connector is instance and subclass of Connector

        """
        assert isinstance(self.sifo, Sifo)
        assert isinstance(self.sifo, Connector)
        assert issubclass(self.sifo.__class__, Connector)

    def test_sifo_has_browser_object_as_attribute(self):
        """
        Test that Sifo connector has Browser object

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
        Test sifo connector has uuid4 compatible ids

        """
        assert UUID(str(self.sifo.id_))

    def test_that_family_gets_set(self):
        """
        Test that Family object gets set if passed through constructor or setter

        """
        assert self.sifo.family == self.family
        new_family = Family([Female(age=40), Female(age=13, sfo='1'), Male(age=10, sfo='1')],
                            select_year=2021)
        self.sifo.family = new_family
        assert self.sifo.family == new_family

    @mock.patch("requests.post", mock.MagicMock(side_effect=ConnectTimeout("timed out")))
    def test_response_throws_time_out_error_for_read_timeout(self):
        """
        Test that response method throws TrackingError if URLError("timed out")

        """
        with pt.raises(TrackingError):
            self.sifo.response()

    @mock.patch("requests.post", mock.MagicMock(side_effect=ConnectError))
    def test_response_throws_no_connection_error(self):
        """
        Test that response method throws TrackingError if URLError("")

        """
        with pt.raises(TrackingError):
            self.sifo.response()

    def test_sifo_response_received(self):
        """
        Test HTTP response 200 is received and of correct type, i.e. response_seek_wrapper

        """
        response = self.sifo.response()
        assert response.status_code == 200
        assert isinstance(response, Response)

    def test_sifo_expenses_method(self):
        """
        Test that sifo_expenses method returns correct content

        """
        correct_content = {'barnehage': '0', 'biler': '2608', 'dagligvarer': '390',
                           'fritid': '3020', 'helse': '1580', 'husholdsart': '430', 'klar': '1850',
                           'kollektivt': '1590', 'mat': '6760', 'medier': '1970', 'mobler': '490',
                           'sfo': '0', 'spedbarn': '0', 'sumhusholdning': '5888',
                           'sumindivid': '14800', 'totalt': '20688'}
        sifo_expenses = self.sifo.sifo_base_expenses()

        assert sifo_expenses == correct_content
        assert "_id" not in sifo_expenses.keys()

    @mock.patch("source.app.connectors.sifo.Sifo.sifo_base_expenses",
                mock.MagicMock(return_value=""))
    def test_to_json(self):
        """
        Test that staticmethod to_json() produces json file with correct content

        """
        current_dir = os.path.dirname(__file__)
        file_dir = os.path.join(current_dir, "report", "json")
        self.sifo.to_json(file_dir=file_dir)
        with open(os.path.join(file_dir, os.listdir(file_dir)[-1]), encoding='utf-8') as json_file:
            data = json.load(json_file)
            assert data == ""
        shutil.rmtree(os.path.join(current_dir, "report"), ignore_errors=True)

    @mock.patch("source.app.connectors.sifo.Sifo.response", mock.MagicMock(return_value=""))
    def test_sifo_expenses_raises_exception(self):
        """
        Test that sifo_base_expenses() method raises exception if no response received
        from response() method.

        """
        with pt.raises(Exception):
            self.sifo.sifo_base_expenses()

    def test_include_id_in_sifo_expenses_method(self):
        """
        Test that '_id' is included in output from sifo_expenses() method

        """
        assert "_id" in self.sifo.sifo_base_expenses(include_id=True).keys()

    def test_sifo_connector_id_is_uuid4(self):
        """
        Test that sifo id is uuid4 compatible

        """
        assert UUID(str(self.sifo.id_))
