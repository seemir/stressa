# -*- coding: utf-8 -*-
"""
Test module for the scrape_finn_advert_info operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, ScrapeFinnAdvertInfo, FINN_AD_URL


class TestScrapeFinnAdvertInfo:
    """
    Test cases for the ScrapeFinnAdvertInfo

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_code = "144857770"
        cls.scrape_finn_advert_info = ScrapeFinnAdvertInfo(cls.finn_code)

    def test_scrape_finn_advert_info_is_instance_of_operation(self):
        """
        Test that ScrapeFinnAdvertInfo is instance and subclass of Operation

        """
        for parent in [ScrapeFinnAdvertInfo, Operation]:
            assert isinstance(self.scrape_finn_advert_info, parent)
            assert issubclass(self.scrape_finn_advert_info.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_finn_code', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_typeerror(invalid_finn_code):
        """
        Test that ScrapeFinnAdvertInfo object raises TypeError if finn_code argument are invalid

        """
        with pt.raises(TypeError):
            ScrapeFinnAdvertInfo(invalid_finn_code)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the ScrapeFinnAdvertInfo object

        """
        assert self.scrape_finn_advert_info.name == self.scrape_finn_advert_info.__class__.__name__
        assert self.scrape_finn_advert_info.finn_code == self.finn_code
        assert self.scrape_finn_advert_info.desc == "from: '{}\\<[finn_code]\\>' " \
                                                    "\\n id: Scrape FINN Advert " \
                                                    "Info".format(FINN_AD_URL)

    def test_scrape_finn_advert_info_run_method(self):
        """
        Test the run method in Output operation

        """
        assert self.scrape_finn_advert_info.run() == {'finn_adresse': 'Sigyns gate 3, 0260 Oslo',
                                                      'prisantydning': '70 000 000 kr',
                                                      'status': 'Ikke solgt',
                                                      'omkostninger': '1 765 642 kr',
                                                      'totalpris': '71 765 642 kr',
                                                      'kommunaleavg': '12 716 kr per år',
                                                      'boligtype': 'Enebolig',
                                                      'eieform': 'Eier (Selveier)', 'soverom': '7',
                                                      'primrrom': '656 m²', 'bruksareal': '831 m²',
                                                      'bygger': '1918',
                                                      'energimerking': 'G - mørkegrønn',
                                                      'tomteareal': '1135 m² (eiet)',
                                                      'bruttoareal': '947 m²',
                                                      'formuesverdi': '9 283 581 kr',
                                                      'finnkode': '144857770',
                                                      'sistendret': '14. feb 2020 02:20',
                                                      'referanse': '3180364'}
