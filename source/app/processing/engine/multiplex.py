# -*- coding: utf-8 -*-
"""
Implementation module for the Multiplex operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from .operation import Operation
from .signal import Signal


class Multiplex(Operation):
    """
    This operation combines / merges multiple signals into one

    """

    @Tracking
    def __init__(self, signals: list, desc: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        signals     : list
                      list of Signal objects
        desc        : str
                      description of operation

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([signals, desc], [list, str])
        super().__init__(name=self.name, desc=f"id: {desc}")
        self.signals = signals

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        dict        : dict
                      dictionary with all signal information in one dict

        """
        signals = {}
        for signal in self.signals:
            if isinstance(signal, Signal) and hasattr(signal, "data"):
                if signal.data:
                    signals.update(signal.data)
            elif signal:
                signals.update(signal)
        return dict(sorted(signals.items()))
