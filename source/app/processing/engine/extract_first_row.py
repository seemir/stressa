# -*- coding: utf-8 -*-

"""
Module containing the Extract First Row Operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

import pandas as pd

from source.util import Assertor, Tracking

from .operation import Operation


class ExtractFirstRow(Operation):
    """
    Operation for extracting the first row from a pandas df dict

    """

    @Tracking
    def __init__(self, data: Union[dict, None], desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data    : dict
                  Dictionary to extract key, value
        desc    : str
                  Description of operation

        """
        Assertor.assert_data_types([data, desc], [(dict, type(None)), str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc=f"id: {desc}")
        self.data = data

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out     : dict
                  value of first fow as dictionary

        """
        data_frame = None
        if self.data:
            data_frame = pd.DataFrame.from_dict(list(self.data.values())[0]).iloc[0].to_dict()
        return data_frame
