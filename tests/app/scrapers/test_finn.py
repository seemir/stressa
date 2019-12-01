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

import mock
import pytest as pt

from source.app import Finn
from source.util import NotFoundError


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
        assert UUID(str(self.finn.id_str))

    def test_finn_response_method(self):
        """
        Test that response method returns HTTP code 200: OK

        """
        response = self.finn.response()
        assert response.status_code == 200
        assert isinstance(response, Response)

    @mock.patch("source.app.scrapers.finn.FINN_URL", mock.MagicMock(return_value=None))
    def test_finn_exception_for_invalid_url(self):
        """
        Test that Finn raises exception if FINN_URL if None

        """
        with pt.raises(Exception):
            self.finn.response()

    def test_housing_information_method(self):
        """
        Test that the housing_information method returns correct content

        """
        correct_content = {'finn_adresse': 'Sigyns gate 3, 0260 Oslo',
                           'prisantydning': '70 000 000 kr', 'omkostninger': '1 765 122 kr',
                           'totalpris': '71 765 122 kr', 'kommunaleavg': '12 716 kr per år',
                           'boligtype': 'Enebolig', 'eieform': 'Eier (Selveier)', 'soverom': '7',
                           'primrrom': '656 m²', 'bruksareal': '831 m²', 'bygger': '1918',
                           'energimerking': 'G - mørkegrønn', 'tomteareal': '1135 m² (eiet)',
                           'bruttoareal': '947 m²', 'formuesverdi': '9 283 581 kr',
                           'finnkode': '144857770', 'sistendret': '29. nov 2019 08:21',
                           'referanse': '3180364'}
        assert self.finn.housing_information() == correct_content

    @staticmethod
    @mock.patch("source.app.scrapers.finn.Finn.response", mock.MagicMock(return_value=None))
    def test_housing_information_throws_attribute_error_for_none_response():
        """
        Test that housing_information method throws AttributeError if response is None

        """
        finn = Finn("144857770")
        with pt.raises(AttributeError):
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
