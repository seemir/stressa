# -*- coding: utf-8 -*-
"""
Test module for the input operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, InputOperation


class TestInputOperation:
    """
    Test cases for the InputOperation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.desc = "Share of Total Expenses"
        cls.input = InputOperation(cls.desc)

    def test_input_is_instance_of_operation(self):
        """
        Test that InputOperation is instance and subclass of Operation

        """
        for parent in [InputOperation, Operation]:
            assert isinstance(self.input, parent)
            assert issubclass(self.input.__class__, parent)

    @staticmethod
    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_typeerror(invalid_desc):
        """
        Test that InputOperation object raises TypeError if desc argument are invalid

        """
        with pt.raises(TypeError):
            InputOperation(invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the InputOperation object

        """
        assert self.input.name == self.input.__class__.__name__
        assert self.input.desc == self.desc

    def test_input_run_method(self):
        """
        Test the run method in input operation

        """
        assert not self.input.run()
