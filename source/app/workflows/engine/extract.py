# -*- coding: utf-8 -*-

"""
Module containing the Extract Operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from .operation import Operation


class Extract(Operation):
    """
    Operation for extracting a key from a signal dict

    """

    def __init__(self, data: dict, key: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data    : dict
                  Dictionary to extract key, value
        key     : str
                  name of key to extract

        """
        Assertor.assert_data_types([data, key], [dict, str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name,
                         desc="id: Extract \\<key '{}'\\>".format(key))
        self.data = data
        self.key = key

    def run(self):
        """
        method for running operation

        Returns
        -------
        out     :
                  value in dictionary key

        """
        if self.key in self.data.keys():
            extracted_data = {self.key: self.data[self.key]}
        else:
            extracted_data = None
        return extracted_data
