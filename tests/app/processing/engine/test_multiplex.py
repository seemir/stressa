# -*- coding: utf-8 -*-
"""
Test module for the multiplex operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import Operation, Multiplex
from source.util import TrackingError


class TestMultiplex:
    """
    Test cases for the multiplex operation

    """

    @classmethod
    def setup(cls):
        """
        Executed before all tests

        """
        cls.signals = [{"klar": "500 kr", "sko": "500 kr", "mat": "500 kr"},
                       {"mobler": "360 kr", "bil": "2 420 kr", "sfo": "2 081 kr"}]
        cls.desc = "Monthly Expenses"
        cls.multiplex = Multiplex(cls.signals, cls.desc)

    def test_multiplex_is_instance_of_operation(self):
        """
        Test that multiplex is instance and subclass of Operation

        """
        for parent in [Multiplex, Operation]:
            assert isinstance(self.multiplex, parent)
            assert issubclass(self.multiplex.__class__, parent)

    @pt.mark.parametrize('invalid_signals', [True, 'test', 90210, 90210.0, ('test', 'test')])
    @pt.mark.parametrize('invalid_desc', [True, 90210, 90210.0, ('test', 'test'), {}])
    def test_invalid_args_raises_tracking_error(self, invalid_signals, invalid_desc):
        """
        Test that multiplex object raises TrackingError if numerator, denominator or desc
        argument are invalid

        """
        with pt.raises(TrackingError):
            Multiplex(invalid_signals, self.desc)
        with pt.raises(TrackingError):
            Multiplex(self.signals, invalid_desc)

    def test_arguments_gets_set_in_object(self):
        """
        Test that arguments gets set in the multiplex object

        """
        multiplex = Multiplex(self.signals, self.desc)
        assert multiplex.signals == self.signals
        assert multiplex.desc == "id: " + self.desc

    def test_multiplex_run_method(self):
        """
        Test the run method in multiplex operation

        """
        multiplex = Multiplex(self.signals, self.desc)
        assert multiplex.run() == self.multiplex.run()
        assert multiplex.run() == {"klar": "500 kr", "sko": "500 kr", "mat": "500 kr",
                                   "mobler": "360 kr", "bil": "2 420 kr", "sfo": "2 081 kr"}
