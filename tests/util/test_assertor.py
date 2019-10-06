# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.util.assertor import Assertor
import pytest as pt


class TestAssertor:
    def test_base_class_cannot_be_instantiated(self):
        """
        Test that the base-class Assertor cannot be instantiated

        """
        with pt.raises(BaseClassCannotBeInstantiated):
            Assertor()

    @pt.mark.parametrize('corrent_argument', ['0', '1', ['0', '1']])
    def test_assert_arguments_method(self, corrent_argument):
        """
        Test the assert_arguments() method, i.e. the object in dictionary of
        {object: [name, possible]} to see if object is in possibility. Raises
        ValueError if not match.

        """
        invalid_argument = '2'
        with pt.raises(ValueError):
            Assertor.assert_arguments({invalid_argument: ['invalid_argument', corrent_argument]})
