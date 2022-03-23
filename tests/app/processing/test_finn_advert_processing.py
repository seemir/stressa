# -*- coding: utf-8 -*-
"""
Test module for the FinnAdvertProcessing process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt
import mock

from prettytable import PrettyTable

from source.app import FinnAdvertProcessing, Process, Signal
from source.util import TrackingError


class TestFinnAdvertProcessing:
    """
    Test cases for the FinnAdvertProcessing Process

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.finn_code = "144857770"

    def test_finn_advert_processing_is_instance_of_process(self):
        """
        Test that FinnAdvertProcessing is instance and subclass of SifoProcessing

        """
        finn_advert_processing = FinnAdvertProcessing(self.finn_code)
        for parent in [FinnAdvertProcessing, Process]:
            assert isinstance(finn_advert_processing, parent)
            assert issubclass(finn_advert_processing.__class__, parent)

    @staticmethod
    def test_class_variables():
        """
        Test that all the class variables are correct in the object

        """
        assert isinstance(FinnAdvertProcessing.start, float)
        assert isinstance(FinnAdvertProcessing.profiling.__class__, PrettyTable.__class__)

    @staticmethod
    @pt.mark.parametrize('invalid_finn_code', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(invalid_finn_code):
        """
        Test that FinnAdvertProcessing object raises TrackingError if finn_code is invalid

        """
        with pt.raises(TrackingError):
            FinnAdvertProcessing(invalid_finn_code)

    def test_set_signal_method(self):
        """
        Test the set_signal method

        """
        new_finn_code = "164102753"
        signal = Signal(new_finn_code, "new_finn_code")
        finn_advert_processing = FinnAdvertProcessing(self.finn_code)
        finn_advert_processing.signal = {"new_finn_code": signal}
        assert finn_advert_processing.signal == {"new_finn_code": signal}

    @pt.mark.parametrize('invalid_signal', [True, "test", 90210, 90210.0, ('test', 'test')])
    def test_invalid_signals_raises_typeerror(self, invalid_signal):
        """
        Test that FinnAdvertProcessing object raises TypeError if signal is invalid

        """
        finn_advert_processing = FinnAdvertProcessing(self.finn_code)
        with pt.raises(TypeError):
            finn_advert_processing.signal = invalid_signal

    def test_get_signal_method(self):
        """
        Test that the get_signal() method returns correct signal

        """
        new_finn_code = "164102753"
        signal = Signal(new_finn_code, "new_finn_code")
        finn_advert_processing = FinnAdvertProcessing(self.finn_code)
        finn_advert_processing.signal = {"new_finn_code": signal}
        assert finn_advert_processing.get_signal("new_finn_code") == signal

    @mock.patch("source.app.processing.engine.scrape_finn_advert_info.ScrapeFinnAdvertInfo.run",
                mock.MagicMock(side_effect=ValueError("this is a test")))
    @mock.patch("source.app.processing.engine.scrape_finn_ownership_history."
                "ScrapeFinnOwnershipHistory.run",
                mock.MagicMock(side_effect=ValueError("this is a test")))
    @mock.patch("source.app.processing.engine.scrape_finn_statistics_info."
                "ScrapeFinnStatisticsInfo.run",
                mock.MagicMock(side_effect=ValueError("this is a test")))
    def test_threading_exception_method(self):
        """
        Test the threading_exception method in the Process super class

        """
        with pt.raises(TrackingError):
            finn_advert_processing = FinnAdvertProcessing(self.finn_code)
            finn_advert_processing.threading_exception()

    @mock.patch("pydot.Dot.write", mock.MagicMock(return_value=None))
    def test_print_pdf_method(self):
        """
        Test the print pdf method

        """
        finn_advert_processing = FinnAdvertProcessing(self.finn_code)
        assert not finn_advert_processing.print_pdf()

    def test_multiplex_info_2(self):
        """
        Test the multiplex_info_2

        """
        results = {'finn_adresse': 'Sigyns gate 3, 0260 Oslo', 'prisantydning': '70 000 000 kr',
                   'status': 'Ikke solgt', 'omkostninger': '1 765 642 kr',
                   'totalpris': '71 765 642 kr', 'kommunaleavg': '12 716 kr per år',
                   'boligtype': 'Enebolig', 'eieform': 'Eier (Selveier)', 'soverom': '7',
                   'primrrom': '656 m²', 'bruksareal': '831 m²', 'bygger': '1918',
                   'energimerking': 'G - mørkegrønn', 'tomteareal': '1135 m² (eiet)',
                   'bruttoareal': '947 m²', 'formuesverdi': '9 283 581 kr', 'finnkode': '144857770',
                   'sistendret': '6. apr. 2020 02:07', 'referanse': '3180364', 'kommunenr': '301',
                   'gardsnr': '212', 'bruksnr': '522',
                   'historikk': {
                       'Boligtype': {0: '-', 1: '-', 2: 'Frittliggende enebolig',
                                     3: 'Frittliggende enebolig'},
                       'Endring': {0: '-4.29 %', 1: '4.48 %', 2: '1596.2 %', 3: ''},
                       'Pris': {0: '67\xa0000\xa0000 kr', 1: '70 000 000 kr',
                                2: '67\xa0000\xa0000 kr', 3: '3\xa0950\xa0000 kr'},
                       'Tinglyst': {0: 'Salgspris (08.02.2022)', 1: 'Prisantydning',
                                    2: '08.02.2022', 3: '30.06.1994'}},
                   'published': '12.04.2019 16:03', 'location': 'Uranienborg - Majorstuen',
                   'price_range': 'større eller lik 70\xa0000\xa0000 kr',
                   'size_range': 'større eller lik 650 m²', 'property_type': 'Enebolig',
                   'city_area': 'Uranienborg - Majorstuen', 'municipality': 'Oslo'}

        finn_advert_processing = FinnAdvertProcessing(self.finn_code)

        for key, val in finn_advert_processing.multiplex_info_2.items():
            if key in results.keys():
                if key in ("sistendret", "published"):
                    continue
                assert results[key] == val
