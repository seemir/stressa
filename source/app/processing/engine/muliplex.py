# -*- coding: utf-8 -*-
"""
Implementation module for the Multiplex operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from .operation import Operation


class Multiplex(Operation):
    """
    This operation combines / merges multiple signals into one

    """

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
        Assertor.assert_data_types([signals, desc], [list, str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc=desc)
        self.signals = signals

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
            signals.update(**signal)
        return signals
