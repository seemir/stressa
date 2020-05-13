# -*- coding: utf-8 -*-
"""
Module with logic for the output operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from .operation import Operation


class OutputOperation(Operation):
    """
    A output operation is typically the last operation in a
    workflow documenting the output from the workflow

    """

    @Tracking
    def __init__(self, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        desc        : str
                      description

        """
        Assertor.assert_data_types([desc], [str])
        super().__init__(name=self.__class__.__name__, desc="id: {}".format(desc))

    @Tracking
    def run(self):
        """
        method for running the operation

        """
