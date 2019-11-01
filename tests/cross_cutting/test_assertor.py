# -*- coding: utf-8 -*-

"""
Test module for the Assertor class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.cross_cutting import Assertor


class TestAssertor:
    """
    Test case for Assertor class

    """

    @staticmethod
    def test_base_class_cannot_be_instantiated():
        """
        Test that the base-class Assertor cannot be instantiated

        """
        with pt.raises(TypeError):
            Assertor()

    @staticmethod
    @pt.mark.parametrize('correct_data_types', [str, float, bool, tuple, list, dict, (list, dict)])
    def test_assert_data_types(correct_data_types):
        """
        Test that assert_data_types() method raises TypeError if first
        argument is not of correct data_type.

        """
        invalid_arg = 90210
        with pt.raises(TypeError):
            Assertor.assert_data_types([invalid_arg], [correct_data_types])

    @staticmethod
    @pt.mark.parametrize('correct_argument', ['0', '1', ['0', '1']])
    def test_assert_arguments(correct_argument):
        """
        Test the assert_arguments() method, i.e. the object in dictionary of
        {object: [name, possible]} to see if 'object' is in 'possible' list. Raises
        ValueError if not match.

        """
        invalid_argument = '2'
        with pt.raises(ValueError):
            Assertor.assert_arguments({invalid_argument: ['invalid_argument', correct_argument]})

    @staticmethod
    @pt.mark.parametrize('negative_values', [-90210, -90210.0, [90210, -90210]])
    def test_non_negative(negative_values):
        """
        Test that assert_non_negative() method raises ValueError if value passed to method
        negative, i.e. less than zero.

        """
        with pt.raises(ValueError):
            Assertor.assert_non_negative(negative_values)
