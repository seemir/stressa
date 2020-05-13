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
from source.util import TrackingError


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
    def test_invalid_args_raises_tracking_error(self, invalid_desc):
        """
        Test that Signal object raises TrackingError if desc or style arguments are invalid

        """
        with pt.raises(TrackingError):
            Signal(self.data, invalid_desc, self.style)
        with pt.raises(TrackingError):
            Signal(self.data, self.desc, invalid_desc)

    def test_arguments_gets_set_in_signal(self):
        """
        Test that arguments gets get in Signal object

        """
        assert self.signal.data == self.data
        assert self.signal.desc == self.desc
        assert self.signal.keys == self.signal.remove_quotation(list(self.data.keys()))

        signal1 = Signal(self.signal, self.desc)
        signal2 = Signal(self.desc, self.desc)

        assert signal1.keys == self.signal.remove_quotation(list(self.signal.__dict__.keys()))
        assert signal2.keys == "None"

    def test_prettify_dict_keys_method(self):
        """
        Test the prettify_dict_keys method in the Signal class

        """
        test_dict_1 = {"test1": "test1", "test2": "test2"}
        test_dict_2 = dict(zip(["test" + str(i) for i in range(16)],
                               ["test" + str(i) for i in range(16)]))
        assert self.signal.prettify_dict_keys(test_dict_1) == self.signal.remove_quotation(
            list(test_dict_1.keys()))

        assert self.signal.prettify_dict_keys(test_dict_2) == "[test0, test1, test2, test3, " \
                                                              "test4, test5, test6, test7, " \
                                                              "test8, test9, test10, test11, " \
                                                              "test12, test13, test14, \\ntest15]"
