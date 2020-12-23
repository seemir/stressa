# -*- coding: utf-8 -*-

"""
Module containing the Check Newest Date Operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from datetime import datetime

from source.util import Assertor, Tracking

from .operation import Operation


class CheckNewestDate(Operation):
    """
    Operation for extracting a key from a signal dict

    """

    @Tracking
    def __init__(self, date_1: Union[dict, None], date_2: Union[dict, None], desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        date_1    : dict
                    dictionary with first date
        date_2    : dict
                    dictionary with second date
        desc      : str
                    Description of operation

        """
        Assertor.assert_data_types([date_1, date_2], [(dict, type(None)), (dict, type(None))])
        self.name = self.__class__.__name__
        super().__init__(name=self.name,
                         desc="id: {}".format(desc))
        self.date_1 = list(date_1.values())[0] if date_1 else None
        self.date_2 = list(date_2.values())[0] if date_2 else None

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out     :
                  dict

        """
        newest = False
        if self.date_1 and self.date_2:
            newest = datetime.strptime(self.date_1, "%d.%m.%Y %H:%M") < datetime.strptime(
                self.date_2, "%d.%m.%Y")
        return newest
