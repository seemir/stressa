# -*- coding: utf-8 -*-
"""
Test module for the SifoProcessing process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from prettytable import PrettyTable

from source.app import SifoProcessing, Process, Signal


class TestSifoProcessing:
    """
    Test cases for the SifoProcessing Process

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.data = {"person_1": {"alder_1": "20-50", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-50", "gravid_2": "Ja", "kjonn_2": "Kvinne"}}

    def test_sifo_processing_is_instance_of_process(self):
        """
        Test that SifoProcessing is instance and subclass of SifoProcessing

        """
        sifo_processing = SifoProcessing(self.data)
        for parent in [SifoProcessing, Process]:
            assert isinstance(sifo_processing, parent)
            assert issubclass(sifo_processing.__class__, parent)

    @staticmethod
    def test_class_variables():
        """
        Test that all the class variables are correct in the object

        """
        assert isinstance(SifoProcessing.start, float)
        assert isinstance(SifoProcessing.profiling.__class__, PrettyTable.__class__)

    @staticmethod
    @pt.mark.parametrize('invalid_data', [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_invalid_args_raises_typeerror(invalid_data):
        """
        Test that SifoProcessing object raises TypeError if data is invalid

        """
        with pt.raises(TypeError):
            SifoProcessing(invalid_data)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the SifoProcessing object

        """
        sifo_processing = SifoProcessing(self.data)
        assert sifo_processing.data == {"data": self.data}

    def test_set_signal_method(self):
        """
        Test the set_signal method

        """
        new_data = {"person_1": {"alder_1": "20-50", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-50", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "person_3": {"alder_3": "6-9", "kjonn_3": "Kvinne", "sfo_3": "Heldag"},
                    "person_4": {"alder_4": "3", "barnehage_4": "Ja", "kjonn_4": "Mann"}}
        signal = Signal(new_data, "new_data")
        sifo_processing = SifoProcessing(self.data)
        sifo_processing.signal = {"new_data": signal}
        assert sifo_processing.signal == {"new_data": signal}

    @pt.mark.parametrize('invalid_signal', [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_invalid_signals_raises_typeerror(self, invalid_signal):
        """
        Test that SifoProcessing object raises TypeError if signal is invalid

        """
        sifo_processing = SifoProcessing(self.data)
        with pt.raises(TypeError):
            sifo_processing.signal = invalid_signal

    def test_get_signal_method(self):
        """
        Test that the get_signal() method returns correct signal

        """
        new_data = {"person_1": {"alder_1": "20-50", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-50", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "person_3": {"alder_3": "6-9", "kjonn_3": "Kvinne", "sfo_3": "Heldag"},
                    "person_4": {"alder_4": "3", "barnehage_4": "Ja", "kjonn_4": "Mann"}}
        signal = Signal(new_data, "new_data")
        sifo_processing = SifoProcessing(self.data)
        sifo_processing.signal = {"new_data": signal}
        assert sifo_processing.get_signal("new_data") == signal
        assert sifo_processing.get_signal("new_data").keys == new_data.keys()

    @pt.mark.parametrize('invalid_base_expenses', [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_invalid_base_expenses_raises_typeerror(self, invalid_base_expenses):
        """
        Test that SifoProcessing object raises TypeError if base_expenses is invalid

        """
        sifo_processing = SifoProcessing(self.data)
        with pt.raises(TypeError):
            sifo_processing.base_expenses = invalid_base_expenses

    @staticmethod
    def test_get_signal_method_with_none():
        """
        Test that the get_signal() method returns None if no signal is present in process object

        """
        new_data = {"person_1": {"alder_1": "20-50", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-50", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "person_3": {"alder_3": "6-9", "kjonn_3": "Kvinne", "sfo_3": "Heldag"},
                    "person_4": {"alder_4": "3", "barnehage_4": "Ja", "kjonn_4": "Mann"}}
        sifo_processing = SifoProcessing(new_data)
        assert not sifo_processing.get_signal("new_data")

    def test_base_expenses_setter(self):
        """
        Test that the base_expenses gets set in object

        """
        base_expenses = {"mat_1": "2 930 kr", "klar_1": "770 kr", "helse_1": "580 kr",
                         "fritid_1": "1 240 kr", "kollektivt_1": "750 kr", "spedbarn_1": "0 kr",
                         "sumindivid_1": "6 270 kr", "dagligvarer_1": "270 kr",
                         "husholdsart_1": "370 kr", "mobler_1": "360 kr", "medier_1": "2 240 kr",
                         "biler_1": "0 kr", "barnehage_1": "0 kr", "sfo_1": "0 kr",
                         "sumhusholdning_1": "3 240 kr", "totalt_1": "9 510 kr", }
        sifo_processing = SifoProcessing(self.data)
        sifo_processing.base_expenses = base_expenses
        assert sifo_processing.base_expenses == base_expenses

    @staticmethod
    def test_base_expenses_shares_getter():
        """
        Test that the expenses_shares getter

        """
        data = {"person_1": {"alder_1": "20-50", "kjonn_1": "Mann"}}
        base_expenses_shares = {"mat": "30.81 %", "klar": "8.10 %", "helse": "6.10 %",
                                "fritid": "13.04 %", "kollektivt": "7.89 %",
                                "spedbarn": "0.00 %", 'stordriftsfordel': '0.01 %',
                                "sumindivid": "65.93 %", "dagligvarer": "2.84 %",
                                "husholdsart": "3.89 %", "mobler": "3.79 %", "medier": "23.55 %",
                                "biler": "0.00 %", "barnehage": "0.00 %", "sfo": "0.00 %",
                                "sumhusholdning": "34.07 %", "totalt": "100.00 %"}
        sifo_processing = SifoProcessing(data)
        assert sifo_processing.expenses_shares == base_expenses_shares
