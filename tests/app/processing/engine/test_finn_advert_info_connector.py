# -*- coding: utf-8 -*-
"""
Test module for the connector_finn_advert_info operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, FinnAdvertInfoConnector, FINN_AD_URL
from source.util import TrackingError


class TestFinnAdvertInfoConnector:
    """
    Test cases for the FinnAdvertInfoConnector

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_code = "144857770"
        cls.connector_finn_advert_info = FinnAdvertInfoConnector(cls.finn_code)

    def test_connector_finn_advert_info_is_instance_of_operation(self):
        """
        Test that FinnAdvertInfoConnector is instance and subclass of Operation

        """
        for parent in [FinnAdvertInfoConnector, Operation]:
            assert isinstance(self.connector_finn_advert_info, parent)
            assert issubclass(self.connector_finn_advert_info.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_finn_code', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_finn_code):
        """
        Test that FinnAdvertInfoConnector object raises TrackingError if finn_code argument
        are invalid

        """
        with pt.raises(TrackingError):
            FinnAdvertInfoConnector(invalid_finn_code)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the FinnAdvertInfoConnector object

        """
        assert self.connector_finn_advert_info.name == self.connector_finn_advert_info.__class__. \
            __name__
        assert self.connector_finn_advert_info.finn_code == self.finn_code
        assert self.connector_finn_advert_info.desc == "from: '{}\\<[finn_code]\\>' " \
                                                       "\\n id: FINN Advert Info " \
                                                       "Connector".format(FINN_AD_URL)

    def test_connector_finn_advert_info_run_method(self):
        """
        Test the run method in FinnAdvertInfoConnector operation

        """
        results = {'finn_adresse': 'Sigyns gate 3, 0260, Oslo',
                   'prisantydning': '70 000 000 kr',
                   'status': 'Ikke solgt',
                   'omkostninger': '1 765 642 kr',
                   'totalpris': '71 765 642 kr',
                   'kommunaleavg': '12 716 kr per år',
                   'boligtype': 'Enebolig',
                   'eieform': 'Eier (Selveier)', 'soverom': '7',
                   'primrrom': '656 m²', 'bruksareal': '831 m²',
                   'bygger': '1918',
                   'energimerking': 'G - Mørkegrønn',
                   'tomteareal': '1135 m² (eiet)',
                   'bruttoareal': '947 m²',
                   'formuesverdi': '9 283 581 kr',
                   'finnkode': '144857770',
                   'sistendret': '6. apr. 2020 02:07',
                   'referanse': '3180364'}
        for key, val in self.connector_finn_advert_info.run().items():
            if key in results.keys():
                if key == "sistendret":
                    continue
                assert val == results[key]
