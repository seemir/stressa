# -*- coding: utf-8 -*-
"""
Module with logic for the output operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from .operation import Operation


class InputOperation(Operation):
    """
    A input operation is typically the first operation in a
    workflow documenting the output from the workflow

    """

    @Tracking
    def __init__(self, desc: str):
        """
        Constructor / Instantiate of the InputOperation class

        Parameters
        ----------
        desc        : str
                      description

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([desc], [str])
        super().__init__(name=self.name, desc=f"id: {desc}")

    @Tracking
    def run(self):
        """
        method for running the InputOperation class returns None

        """
        return
