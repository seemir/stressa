# -*- coding: utf-8 -*-

"""
Module with logic of Flatten operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from .operation import Operation


class Flatten(Operation):
    """
    Operation that flattens a dictionary

    """

    @Tracking
    def __init__(self, data: dict, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data        : dict
                      data to flatten
        desc        : str
                      description of operation

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([data, desc], [dict, str])
        super().__init__(name=self.name, desc=f"id: {desc}")
        self.data = data

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with flatten data

        """
        flatten_dict = {}

        for keys, values in self.data.items():
            if isinstance(values, dict):
                for key, value in values.items():
                    flatten_dict.update({keys + '_' + key: value})
            else:
                flatten_dict.update({keys: values})
        return flatten_dict
