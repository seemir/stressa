# -*- coding: utf-8 -*-
"""
Module with Separate operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from .operation import Operation


class Separate(Operation):
    """
    The separate operation splits a list of dictionaries into a dict of dicts

    """

    def __init__(self, data: list, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data        : list
                      data to separate
        desc        : str
                      description of operation

        """
        Assertor.assert_data_types([data, desc], [list, str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.data = data

    def run(self):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with data

        """
        output = {}
        for dictionary in self.data:
            if "type" in dictionary.keys():
                output.update({dictionary["type"].lower(): dictionary})
            else:
                output.update(dictionary)
        return output
