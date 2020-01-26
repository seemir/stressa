# -*- coding: utf-8 -*-

"""
Test module for the Expenses Entity

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.domain import Expenses, Entity


class TestExpenses:
    """
    Test cases for Expenses Entity

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.data = {'mat': '5290', 'klar': '1590', 'helse': '1320', 'fritid': '2480',
                    'kollektivt': '1500', 'spedbarn': '0', 'stordriftsfordel': '1',
                    'sumindivid': '12180', 'dagligvarer': '340', 'husholdsart': '400',
                    'mobler': '400', 'medier': '2240', 'biler': '2420', 'barnehage': '0',
                    'sfo': '0', 'sumhusholdning': '5800', 'totalt': '17980'}
        cls.expenses = Expenses(cls.data)

    def test_expenses_is_instance_if_entity(self):
        """
        Test that all Expenses objects are instances and subclasses of Expenses and Entity

        """
        for parent in [Expenses, Entity]:
            assert isinstance(self.expenses, parent)
            assert issubclass(self.expenses.__class__, parent)

    @staticmethod
    @pt.mark.parametrize("invalid_types", [True, 'test', 90210, 90210.0, ('test', 'test')])
    def test_expenses_throws_typeerror_for_invalid_input_type(invalid_types):
        """
        Test that Expenses throws TypeError if invalid type is passed to object

        """
        with pt.raises(TypeError):
            Expenses(invalid_types)

    def test_cast_expenses_method(self):
        """
        Test the make expenses method

        """
        expenses = self.expenses.cast_expenses(self.data)
        assert expenses == self.expenses.verdi
