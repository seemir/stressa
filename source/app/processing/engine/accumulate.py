# -*- coding: utf-8 -*-
"""
Module containing the Accumulate operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from pandas import DataFrame

from source.util import Assertor, Tracking

from .operation import Operation


class Accumulate(Operation):
    """
    Implementation of the accumulate operation, which calculated the
    cumulative sum of a list of numeric values

    """

    @Tracking
    def __init__(self, data: dict, desc: str):
        """
        Constructor / instantiating the class

        Parameters
        ----------
        data        : dict
                      data dictionary, i.e. to be accumalated
        desc        : str
                      description of operation

        """
        Assertor.assert_data_types([data, desc], [dict, str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc=f"id: {desc}")
        self.data = data

    @Tracking
    def run(self):
        """
        method for running the operation

        """
        accumulated = DataFrame.from_dict(self.data).cumsum().to_dict()
        return {"accumulated": dict(*accumulated.values())}
