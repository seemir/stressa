# -*- coding: utf-8 -*-
"""
Test module for Signal class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import ABC

from pydot import Node
import pytest as pt

from source.app import Signal


class TestSignal:
    """
    Test cases for Signal Node

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.data = {"klar": "500 kr", "sko": "500 kr", "mat": "500 kr"}
        cls.desc = "Expenses"
        cls.style = "dotted"
        cls.signal = Signal(cls.data, cls.desc)

    def test_signal_is_instance_of_node_and_abc(self):
        """
        Test that Signal is instance and subclass of Operation

        """
        for parent in [Signal, Node, ABC]:
            assert isinstance(self.signal, parent)
            assert issubclass(self.signal.__class__, parent)

    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_typeerror(self, invalid_desc):
        """
        Test that Signal object raises TypeError if desc or style arguments are invalid

        """
        with pt.raises(TypeError):
            Signal(self.data, invalid_desc, self.style)
        with pt.raises(TypeError):
            Signal(self.data, self.desc, invalid_desc)

    def test_arguments_gets_set_in_signal(self):
        """
        Test that arguments gets get in Signal object

        """
        assert self.signal.data == self.data
        assert self.signal.desc == self.desc
        assert self.signal.keys == Signal.remove_quotation(list(self.data.keys()))

        signal1 = Signal(self.signal, self.desc)
        signal2 = Signal(self.desc, self.desc)

        assert signal1.keys == Signal.remove_quotation(list(self.signal.__dict__.keys()))
        assert not signal2.keys
