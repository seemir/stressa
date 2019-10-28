# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor
import pytest as pt


class TestAssertor:

    def test_base_class_cannot_be_instantiated(self):
        """
        Test that the base-class Assertor cannot be instantiated

        """
        with pt.raises(TypeError):
            Assertor()

    @pt.mark.parametrize('correct_data_types', [str, float, bool, tuple, list, dict, (list, dict)])
    def test_assert_data_types(self, correct_data_types):
        """
        Test that assert_data_types() method raises TypeError if first
        argument is not of correct data_type.

        """
        invalid_arg = 90210
        with pt.raises(TypeError):
            Assertor.assert_data_types([invalid_arg], [correct_data_types])

    @pt.mark.parametrize('correct_argument', ['0', '1', ['0', '1']])
    def test_assert_arguments(self, correct_argument):
        """
        Test the assert_arguments() method, i.e. the object in dictionary of
        {object: [name, possible]} to see if 'object' is in 'possible' list. Raises
        ValueError if not match.

        """
        invalid_argument = '2'
        with pt.raises(ValueError):
            Assertor.assert_arguments({invalid_argument: ['invalid_argument', correct_argument]})

    @pt.mark.parametrize('negative_values', [-90210, -90210.0, [90210, -90210]])
    def test_non_negative(self, negative_values):
        """
        Test that assert_non_negative() method raises ValueError if value passed to method
        negative, i.e. less than zero.

        """
        with pt.raises(ValueError):
            Assertor.assert_non_negative(negative_values)
