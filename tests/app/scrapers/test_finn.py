# -*- coding: utf-8 -*-

"""
Test module for the Scraper against Finn.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import UUID

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

    @pt.mark.parametrize("invalid_finn_code", ["1448577", "2448577701", "24485777a"])
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
        assert UUID(str(self.finn.id_))
