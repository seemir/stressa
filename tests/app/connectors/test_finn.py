# -*- coding: utf-8 -*-

"""
Test module for the connectorr against Finn.no housing search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from uuid import UUID

import pytest as pt

from source.app import Finn
from source.util import TrackingError


class TestFinn:
    """
    Test cases for the Finn connectorr

    """

    def setup_method(self):
        """
        setup that is run before every tests

        """
        self.finn = Finn("144857770")

    def test_finn_is_instance_of_connectorr(self):
        """
        Test that Finn object is instance and subclass of connectorr

        """
        assert isinstance(self.finn, Finn)
        assert isinstance(self.finn, Finn)
        assert issubclass(self.finn.__class__, Finn)

    @staticmethod
    @pt.mark.parametrize("invalid_finn_code_types", [144857770, 144857770.0, True, [], (), {}])
    def test_invalid_finn_code_raises_type_error(invalid_finn_code_types):
        """
        Test that Finn raises TypeError for invalid finn_code types

        """
        with pt.raises(TypeError):
            Finn(invalid_finn_code_types)

    @pt.mark.parametrize("invalid_finn_code", ["1448577", "2448577701", "24485777a"])
    def test_validate_finn_code_method(self, invalid_finn_code):
        """
        Test that invalid finn_code raises TrackingError

        """
        with pt.raises(TrackingError):
            Finn(invalid_finn_code)

    def test_finn_has_uuid4_compatible_id(self):
        """
        Test Finn connectorr has uuid4 compatible ids

        """
        assert UUID(str(self.finn.id_))
