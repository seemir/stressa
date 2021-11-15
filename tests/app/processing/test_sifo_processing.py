# -*- coding: utf-8 -*-
"""
Test module for the CalculateSifoExpenses process

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from prettytable import PrettyTable

from source.app import SifoExpensesProcess, Process, Signal
from source.util import TrackingError


class TestCalculateSifoExpenses:
    """
    Test cases for the CalculateSifoExpenses Process

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.data = {"person_1": {"alder_1": "20-30 år", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-30 år", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "select_year": "2021"}

    def test_calculate_sifo_expenses_is_instance_of_process(self):
        """
        Test that CalculateSifoExpenses is instance and subclass of SifoProcessing

        """
        calculate_sifo_expenses = SifoExpensesProcess(self.data)
        for parent in [SifoExpensesProcess, Process]:
            assert isinstance(calculate_sifo_expenses, parent)
            assert issubclass(calculate_sifo_expenses.__class__, parent)

    @staticmethod
    def test_class_variables():
        """
        Test that all the class variables are correct in the object

        """
        assert isinstance(SifoExpensesProcess.start, float)
        assert isinstance(SifoExpensesProcess.profiling.__class__, PrettyTable.__class__)

    @staticmethod
    @pt.mark.parametrize('invalid_data', [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_invalid_args_raises_tracking_error(invalid_data):
        """
        Test that CalculateSifoExpenses object raises TrackingError if data is invalid

        """
        with pt.raises(TrackingError):
            SifoExpensesProcess(invalid_data)

    def test_set_signal_method(self):
        """
        Test the set_signal method

        """
        new_data = {"person_1": {"alder_1": "20-50", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-50", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "person_3": {"alder_3": "6-9", "kjonn_3": "Kvinne", "sfo_3": "Heldag"},
                    "person_4": {"alder_4": "3", "barnehage_4": "Ja", "kjonn_4": "Mann"}}
        signal = Signal(new_data, "new_data")
        calculate_sifo_expenses = SifoExpensesProcess(self.data)
        calculate_sifo_expenses.signal = {"new_data": signal}
        assert calculate_sifo_expenses.signal == {"new_data": signal}

    @pt.mark.parametrize('invalid_signal', [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_invalid_signals_raises_typeerror(self, invalid_signal):
        """
        Test that CalculateSifoExpenses object raises TypeError if signal is invalid

        """
        calculate_sifo_expenses = SifoExpensesProcess(self.data)
        with pt.raises(TypeError):
            calculate_sifo_expenses.signal = invalid_signal

    def test_get_signal_method(self):
        """
        Test that the get_signal() method returns correct signal

        """
        new_data = {"person_1": {"alder_1": "20-50", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-50", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "person_3": {"alder_3": "6-9", "kjonn_3": "Kvinne", "sfo_3": "Heldag"},
                    "person_4": {"alder_4": "3", "barnehage_4": "Ja", "kjonn_4": "Mann"}}
        signal = Signal(new_data, "new_data")
        calculate_sifo_expenses = SifoExpensesProcess(self.data)
        calculate_sifo_expenses.signal = {"new_data": signal}
        assert calculate_sifo_expenses.get_signal("new_data") == signal
        assert calculate_sifo_expenses.get_signal("new_data").keys == signal.remove_quotation(
            list(new_data.keys()))

    @staticmethod
    def test_get_signal_method_with_none():
        """
        Test that the get_signal() method returns None if no signal is present in process object

        """
        new_data = {"person_1": {"alder_1": "20-30 år", "kjonn_1": "Mann"},
                    "person_2": {"alder_2": "20-30 år", "gravid_2": "Ja", "kjonn_2": "Kvinne"},
                    "person_3": {"alder_3": "6-9 år", "kjonn_3": "Kvinne", "sfo_3": "Heldag"},
                    "person_4": {"alder_4": "3 år", "barnehage_4": "Ja", "kjonn_4": "Mann"},
                    "select_year": "2021"}
        calculate_sifo_expenses = SifoExpensesProcess(new_data)
        assert not calculate_sifo_expenses.get_signal("new_data")

    @staticmethod
    def test_base_expenses_shares_getter():
        """
        Test that the expenses_shares getter

        """
        data = {"person_1": {"alder_1": "20-30 år", "kjonn_1": "Mann"}, "select_year": "2021"}
        base_expenses_shares = {'barnehage': '0.00 %', 'biler': '0.00 %', 'dagligvarer': '2.84 %',
                                'fritid': '13.83 %', 'helse': '6.41 %', 'husholdsart': '3.66 %',
                                'klar': '8.15 %', 'kollektivt': '7.28 %', 'mat': '35.64 %',
                                'medier': '18.05 %', 'mobler': '4.12 %', 'sfo': '0.00 %',
                                'spedbarn': '0.00 %', 'sumhusholdning': '28.68 %',
                                'sumindivid': '71.32 %', 'totalt': '100.00 %'}
        calculate_sifo_expenses = SifoExpensesProcess(data)
        print(calculate_sifo_expenses.expenses_shares)
        assert calculate_sifo_expenses.expenses_shares == base_expenses_shares
