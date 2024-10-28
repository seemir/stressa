# -*- coding: utf-8 -*-
"""
Module with the Comparing operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from .operation import Operation


class Comparison(Operation):
    """
    Operation for comparing two signals

    """

    @Tracking
    def __init__(self, signal_1: dict, signal_2: dict, key: str, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        signal_1     : dict
                       quantity
        signal_2     : dict
                       divisor assumed to be of length one
        key          : str
                       name of output key
        desc         : str
                       description

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([signal_1, signal_2, desc],
                                   [dict, dict, str])
        super().__init__(name=self.name, desc=f"id: {desc}")
        self.signal_1 = signal_1
        self.signal_2 = signal_2
        self.key = key

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with shares

        """
        results = {}
        if len(self.signal_1) == 1 and len(self.signal_2) == 1:
            val_1 = float(
                list(self.signal_1.values())[0].replace(" kr", "")
                .replace(" ", ""))
            val_2 = float(
                list(self.signal_2.values())[0].replace(" kr", "")
                .replace(" ", ""))
            if val_1 < val_2:
                results = {self.key: list(self.signal_1.values())[0]}
            else:
                results = {self.key: list(self.signal_2.values())[0]}
        return results
