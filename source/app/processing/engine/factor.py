# -*- coding: utf-8 -*-

"""
Operation to generating a factor object

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union

from source.util import Assertor, Tracking

from .operation import Operation


class Factor(Operation):
    """
    Operation for producing a factor

    """

    def __init__(self, value: str, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        value       : str
                      data to factor
        desc        : str
                      description of operation

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([value, desc], [str, str])
        super().__init__(name=self.name, desc="id: {} \n factor: {}".format(desc, value))
        self.value = value

    @Tracking
    def run(self):
        """
        method for running the operation

        """
        return {"factor": self.value}
