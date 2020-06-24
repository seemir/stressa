# -*- coding: utf-8 -*-
"""
Module containing operation for calculating change in price of a pandas dataframe

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame as DataFrame_

from source.util import Assertor, Tracking, Debugger

from .operation import Operation


class RateOfChange(Operation):
    """
    Implementation of Operation for calculating rate of change in vector

    """

    @Tracking
    def __init__(self, dataframe: dict, desc: str):
        """
        Constructor / instantiating the class

        Parameters
        ----------
        dataframe   : dict
                      dataframe as a dictionary to calculate changes in vector
        desc        : str
                      description of operation

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([dataframe, desc], [dict, str])
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.dataframe = dataframe

    @Debugger
    def run(self):
        """
        method for running the operation

        """
        change = DataFrame_(self.dataframe).iloc[:, -1].astype(str).str.replace(
            u"\xa0", "").str.replace(" kr", "").str.replace(" ", "")
        final_change = DataFrame_.from_dict(self.dataframe).assign(
            Endring=(change.astype(float).pct_change(-1).mul(100).round(2).astype(
                str) + " %").replace("nan %", "").replace("inf %", "0.0 %"))
        return final_change.to_dict()
