# -*- coding: utf-8 -*-
"""
Module with logic for the output operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from .operation import Operation


class InputOperation(Operation):
    """
    A input operation is typically the first operation in a
    workflow documenting the output from the workflow

    """

    def __init__(self, decs: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        decs        : str
                      description

        """
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc=decs)

    def run(self):
        """
        method for running the operation

        """
