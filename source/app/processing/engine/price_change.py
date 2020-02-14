# -*- coding: utf-8 -*-
"""
Module containing operation for calculating change in price of a pandas dataframe

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame as DataFrame_

from source.util import Assertor

from .operation import Operation


class PriceChange(Operation):
    """
    Implementation of Operation for calculating changes in price

    """

    def __init__(self, dataframe: dict, desc: str):
        """

        Parameters
        ----------
        dataframe   : dict
                      dataframe as a dictionary to calculate changes in price
        desc        : str
                      description of operation

        """
        Assertor.assert_data_types([dataframe, desc], [(dict, type(None)), str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.dataframe = dataframe

    def run(self):
        """
        method for running the operation

        """
        final_change = None
        if self.dataframe:
            change = DataFrame_(self.dataframe).iloc[:, -1].str.replace(
                u"\xa0", "").str.replace(" kr", "").str.replace(" ", "")
            final_change = DataFrame_(self.dataframe).assign(
                Endring=(change.astype(float).pct_change(-1).mul(100).round(2).astype(
                    str) + " %").replace("nan %", ""))
        return final_change
